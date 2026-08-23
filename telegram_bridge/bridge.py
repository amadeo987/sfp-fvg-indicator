#!/usr/bin/env python3
"""Small, fail-closed TradingView webhook to Telegram bridge."""

from __future__ import annotations

import argparse
import hmac
import json
import logging
import os
import queue
import signal
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


LOG = logging.getLogger("tv-telegram-bridge")
MAX_BODY_BYTES = 64 * 1024
MAX_QUEUE_SIZE = 200
ALLOWED_EVENTS = {"sr_touch"}


def _safe_error(exc: BaseException) -> str:
    """Describe failures without ever rendering a URL that may contain a token."""
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}"
    return type(exc).__name__


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class Config:
    bot_token: str
    chat_id: str
    webhook_secret: str
    bind: str = "127.0.0.1"
    port: int = 8791
    topic_id: str = ""

    @classmethod
    def from_env(cls) -> "Config":
        secret = _required_env("WEBHOOK_SECRET")
        if len(secret) < 32:
            raise ValueError("WEBHOOK_SECRET must contain at least 32 characters")
        return cls(
            bot_token=_required_env("TELEGRAM_BOT_TOKEN"),
            chat_id=_required_env("TELEGRAM_CHAT_ID"),
            webhook_secret=secret,
            bind=os.environ.get("WEBHOOK_BIND", "127.0.0.1").strip(),
            port=int(os.environ.get("WEBHOOK_PORT", "8791")),
            topic_id=os.environ.get("TELEGRAM_TOPIC_ID", "").strip(),
        )


def _field(payload: dict[str, Any], name: str, fallback: str = "-") -> str:
    value = payload.get(name)
    if value is None:
        return fallback
    if not isinstance(value, (str, int, float, bool)):
        return fallback
    clean = str(value).replace("\n", " ").replace("\r", " ").strip()
    return clean[:160] or fallback


def validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")
    event = _field(payload, "event", "")
    if event not in ALLOWED_EVENTS:
        raise ValueError("Unsupported event")
    symbol = _field(payload, "symbol", "")
    if not symbol:
        raise ValueError("Missing symbol")
    return dict(payload)


def format_message(payload: dict[str, Any]) -> str:
    event_name = _field(payload, "event")
    if event_name != "sr_touch":
        raise ValueError("Unsupported notification event")
    market = _field(payload, "market", _field(payload, "symbol"))
    timeframe = _field(payload, "timeframe")
    short_timeframe = {"60": "1H", "240": "4H"}.get(timeframe, timeframe)
    return f"SFP DOTKNIĘTE — {market} {short_timeframe}"[:4096]


class TelegramClient:
    def __init__(self, config: Config) -> None:
        self._url = f"https://api.telegram.org/bot{config.bot_token}/sendMessage"
        self._chat_id = config.chat_id
        self._topic_id = config.topic_id

    def send(self, text: str) -> None:
        fields = {
            "chat_id": self._chat_id,
            "text": text,
            "disable_web_page_preview": "true",
        }
        if self._topic_id:
            fields["message_thread_id"] = self._topic_id
        request = urllib.request.Request(
            self._url,
            data=urllib.parse.urlencode(fields).encode("utf-8"),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=2.4) as response:
            result = json.loads(response.read().decode("utf-8"))
        if not result.get("ok"):
            raise RuntimeError("Telegram API rejected the message")


class DeliveryWorker(threading.Thread):
    def __init__(self, outbox: "queue.Queue[dict[str, Any]]", client: TelegramClient) -> None:
        super().__init__(name="telegram-delivery", daemon=True)
        self._outbox = outbox
        self._client = client
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                payload = self._outbox.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                message = format_message(payload)
                for attempt in range(3):
                    try:
                        self._client.send(message)
                        LOG.info(
                            "delivered event=%s symbol=%s",
                            _field(payload, "event"),
                            _field(payload, "symbol"),
                        )
                        break
                    except (OSError, RuntimeError, urllib.error.URLError) as exc:
                        if attempt == 2:
                            LOG.error("delivery failed: %s", _safe_error(exc))
                        else:
                            time.sleep(0.5 * (2**attempt))
            finally:
                self._outbox.task_done()


class BridgeServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], config: Config) -> None:
        super().__init__(address, BridgeHandler)
        self.config = config
        self.outbox: "queue.Queue[dict[str, Any]]" = queue.Queue(MAX_QUEUE_SIZE)


class BridgeHandler(BaseHTTPRequestHandler):
    server: BridgeServer
    server_version = "TVTelegramBridge/1.0"

    def _json_response(self, status: HTTPStatus, body: dict[str, Any]) -> None:
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if urllib.parse.urlsplit(self.path).path != "/health":
            self._json_response(HTTPStatus.NOT_FOUND, {"ok": False})
            return
        self._json_response(
            HTTPStatus.OK,
            {"ok": True, "queue_depth": self.server.outbox.qsize()},
        )

    def do_POST(self) -> None:  # noqa: N802
        path = urllib.parse.urlsplit(self.path).path
        expected = f"/hooks/{self.server.config.webhook_secret}"
        if not hmac.compare_digest(path, expected):
            self._json_response(HTTPStatus.NOT_FOUND, {"ok": False})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length < 1 or length > MAX_BODY_BYTES:
            self._json_response(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"ok": False})
            return
        try:
            raw = self.rfile.read(length)
            payload = validate_payload(json.loads(raw.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._json_response(HTTPStatus.BAD_REQUEST, {"ok": False})
            return
        try:
            self.server.outbox.put_nowait(payload)
        except queue.Full:
            self._json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"ok": False})
            return
        self._json_response(HTTPStatus.ACCEPTED, {"ok": True})

    def log_message(self, _format: str, *args: Any) -> None:
        return


def show_updates(token: str) -> int:
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        LOG.error("Cannot fetch Telegram updates: %s", _safe_error(exc))
        return 1
    chats: dict[str, str] = {}
    for update in result.get("result", []):
        message = update.get("message") or update.get("channel_post") or {}
        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        if chat_id is not None:
            name = chat.get("title") or chat.get("username") or chat.get("first_name") or "chat"
            chats[str(chat_id)] = str(name)
    if not chats:
        print("No chats found. Send /start to the bot and run this command again.")
        return 2
    for chat_id, name in chats.items():
        print(f"{chat_id}\t{name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-updates", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"), format="%(levelname)s %(message)s")
    if args.show_updates:
        return show_updates(_required_env("TELEGRAM_BOT_TOKEN"))
    try:
        config = Config.from_env()
    except (ValueError, TypeError) as exc:
        LOG.error("configuration error: %s", exc)
        return 2
    server = BridgeServer((config.bind, config.port), config)
    worker = DeliveryWorker(server.outbox, TelegramClient(config))
    worker.start()

    def shutdown(_signum: int, _frame: Any) -> None:
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    LOG.info("listening on %s:%s", config.bind, config.port)
    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        worker.stop()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
