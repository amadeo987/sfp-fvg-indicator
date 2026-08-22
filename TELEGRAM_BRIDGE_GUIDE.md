# TradingView to Telegram bridge

This receiver accepts the indicators' SFP/FVG and S/R-touch JSON alerts, acknowledges TradingView quickly with HTTP 202, and delivers the message to Telegram from a background queue. It has no order or exchange API capability.

## Security first

The bot token shown in a screenshot or chat must be treated as exposed. Revoke it in BotFather and generate a new one before deployment. Never paste the replacement into Git, Pine, an alert message, or a public URL.

The receiver binds to `127.0.0.1` by default. Publish only its secret path through an existing HTTPS reverse proxy or tunnel. Keep the real environment file mode `600`.

## Server installation

```bash
install -d -m 700 ~/.config/tv-telegram-bridge ~/.local/lib/tv-telegram-bridge ~/.config/systemd/user
install -m 700 telegram_bridge/bridge.py ~/.local/lib/tv-telegram-bridge/bridge.py
install -m 644 telegram_bridge/tv-telegram-bridge.service ~/.config/systemd/user/tv-telegram-bridge.service
install -m 600 telegram_bridge/bridge.env.example ~/.config/tv-telegram-bridge/bridge.env
```

Edit the private environment file. Generate a path secret with `openssl rand -hex 32`. To obtain the chat ID, send `/start` to the bot, load the private environment into a protected shell, and run:

```bash
set -a
. ~/.config/tv-telegram-bridge/bridge.env
set +a
python3 ~/.local/lib/tv-telegram-bridge/bridge.py --show-updates
```

Then start the isolated user service:

```bash
systemctl --user daemon-reload
systemctl --user enable --now tv-telegram-bridge.service
curl --fail --silent http://127.0.0.1:8791/health
```

Expose `/hooks/<WEBHOOK_SECRET>` over HTTPS and reverse proxy it directly to the same localhost path. Do not redirect this endpoint and do not expose the environment file or localhost port.

## End-to-end check

From outside the server, POST a harmless supported event to the final HTTPS URL:

```bash
curl --fail-with-body \
  -H 'Content-Type: application/json' \
  --data '{"event":"sfp_confirmed","symbol":"TEST:TEST","timeframe":"60","direction":"long","price":1}' \
  'https://your-private-host.example/hooks/your-long-random-secret'
```

Success requires all three checks: HTTP 202, a new Telegram message, and a `delivered` log entry in `journalctl --user -u tv-telegram-bridge.service`.

## TradingView alert

1. Enable `Enable alert() events` in the indicator.
2. Create an alert using **Any alert() function call**.
3. Enable Webhook URL and enter the private HTTPS URL ending in `/hooks/<WEBHOOK_SECRET>`.
4. Create one alert for the main SFP/FVG indicator.

TradingView stores a snapshot of the script and inputs when an alert is created. Recreate it after changing code or settings. Delivery can occasionally fail, so inspect TradingView's webhook status and the server journal when a notification is missing.
