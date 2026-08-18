import os
import sys
import json
import threading
import unittest
import urllib.error
from http.client import HTTPConnection

sys.path.insert(0, os.path.dirname(__file__))

from bridge import BridgeServer, Config, _safe_error, format_message, validate_payload  # noqa: E402


class PayloadTests(unittest.TestCase):
    def test_http_error_description_does_not_expose_url(self):
        error = urllib.error.HTTPError("https://api.telegram.org/botsecret/sendMessage", 401, "no", {}, None)
        text = _safe_error(error)
        self.assertEqual(text, "HTTP 401")
        self.assertNotIn("secret", text)

    def test_accepts_known_event(self):
        payload = validate_payload(
            {"event": "sfp_confirmed", "symbol": "OKX:BTCUSD", "timeframe": "60", "direction": "short"}
        )
        self.assertEqual(payload["event"], "sfp_confirmed")

    def test_rejects_unknown_event(self):
        with self.assertRaises(ValueError):
            validate_payload({"event": "place_order", "symbol": "OKX:BTCUSD"})

    def test_rejects_non_object(self):
        with self.assertRaises(ValueError):
            validate_payload(["sfp_confirmed"])

    def test_message_contains_only_selected_fields(self):
        text = format_message(
            {
                "event": "divergence_confirmed",
                "symbol": "OKX:BTCUSD",
                "timeframe": "240",
                "direction": "bullish",
                "kind": "regular",
                "secret": "must-not-be-forwarded",
            }
        )
        self.assertIn("DIVERGENCE CONFIRMED", text)
        self.assertIn("bullish", text)
        self.assertNotIn("must-not-be-forwarded", text)


class ReceiverTests(unittest.TestCase):
    def setUp(self):
        self.secret = "s" * 32
        config = Config("token", "123", self.secret, port=0)
        self.server = BridgeServer(("127.0.0.1", 0), config)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.connection = HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)

    def tearDown(self):
        self.connection.close()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_health(self):
        self.connection.request("GET", "/health")
        response = self.connection.getresponse()
        self.assertEqual(response.status, 200)
        self.assertTrue(json.loads(response.read())["ok"])

    def test_valid_secret_and_payload_are_queued(self):
        body = json.dumps({"event": "sfp_touch", "symbol": "OKX:BTCUSD", "timeframe": "60"})
        self.connection.request(
            "POST",
            f"/hooks/{self.secret}",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        response = self.connection.getresponse()
        self.assertEqual(response.status, 202)
        response.read()
        self.assertEqual(self.server.outbox.qsize(), 1)

    def test_wrong_secret_is_not_distinguishable_from_missing_path(self):
        body = json.dumps({"event": "sfp_touch", "symbol": "OKX:BTCUSD"})
        self.connection.request("POST", "/hooks/wrong", body=body)
        response = self.connection.getresponse()
        self.assertEqual(response.status, 404)
        response.read()


if __name__ == "__main__":
    unittest.main()
