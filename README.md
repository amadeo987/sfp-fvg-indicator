# SK TradingView Indicators

Open Pine Script v6 indicators for discretionary chart analysis. They do not place orders and do not require exchange API keys.

## Included scripts

### SK SFP + FVG / IFVG v5.7

[`SK_SFP_Najblizsze_Poziomy.pine`](./SK_SFP_Najblizsze_Poziomy.pine) combines:

- the `SFP WATCH → RAW → CONF` liquidity-sweep hierarchy,
- confirmed, non-repainting FVG and IFVG zone books,
- a default `Match chart` timeframe mode,
- a `Custom set` mode with any combination of three user-selected timeframes,
- nearest-zone selection above and below price,
- adaptive weekday/month markers and webhook-ready JSON alerts,
- an integrated, chart-clean 1H/4H scanner for BTC, ETH, SOL, XRP and LINK on OKX, HYPE on Hyperliquid, plus COMEX gold and silver continuous futures,
- automatic removal of consumed WATCH context after its second separate retest,
- a short `SKSFP 5.7` status-line name with no scanner table.

See [`SFP_WSKAZNIK_INSTRUKCJA.md`](./SFP_WSKAZNIK_INSTRUKCJA.md).

### SK Current Day POC / VAH / VAL v1.0

[`SK_Current_Day_POC_VAH_VAL.pine`](./SK_Current_Day_POC_VAH_VAL.pine) draws a developing current-day POC, VAH, and VAL on intraday charts. The default profile day is the full UTC day for 24/7 crypto markets.

The profile is an approximation based on chart-bar volume distributed across configurable price rows. It can differ from TradingView's built-in Volume Profile, which can use finer intrabar data. See [`CURRENT_DAY_PROFILE_GUIDE.md`](./CURRENT_DAY_PROFILE_GUIDE.md).

### SK MTF Nearest Support / Resistance v1.0

[`SK_MTF_Nearest_Support_Resistance.pine`](./SK_MTF_Nearest_Support_Resistance.pine) shows the nearest confirmed pivot support below price and resistance above price from up to three selected source timeframes. It is intentionally separate from the main SFP indicator. See [`SUPPORT_RESISTANCE_GUIDE.md`](./SUPPORT_RESISTANCE_GUIDE.md).

## Installation

1. Open a TradingView chart and select **Pine Editor**.
2. Copy the complete contents of one `.pine` file into a new Pine script.
3. Save the script and choose **Add to chart**.
4. Repeat for any additional indicator you want to use.

## Alerts and Telegram webhooks

The main SFP/FVG indicator emits structured JSON through `alert()`. Create an alert using **Any alert() function call** and paste your private HTTPS webhook URL into TradingView's Webhook URL field.

No bot token, chat ID, webhook secret, private hostname, or server address belongs in these public files. TradingView alerts are snapshots: recreate an alert after changing code or indicator inputs.

The repository also contains a dependency-free, queue-backed receiver for forwarding those events to a Telegram bot. It binds to localhost by default and keeps every credential in a server-only environment file. See [`TELEGRAM_BRIDGE_GUIDE.md`](./TELEGRAM_BRIDGE_GUIDE.md).

The scanner is integrated into the main SFP/FVG script, so one TradingView indicator slot and one **Any alert() function call** alert handle the chart logic and all 16 market/timeframe feeds. The former standalone scanner remains documented only as a legacy migration reference in [`SR_TELEGRAM_SCANNER_GUIDE.md`](./SR_TELEGRAM_SCANNER_GUIDE.md).

## Repainting policy

- SFP RAW and CONF signals require closed chart candles.
- FVG/IFVG sources use the previous closed source-timeframe candle with `lookahead_on`; zones do not change while the source candle is open.
- MTF support/resistance levels require confirmed pivots and therefore appear after the configured right-side pivot delay.
- The current-day profile is intentionally developing and may move as new volume arrives during the active day.

## Status

- Pine language: **v6**
- Main indicator: **v5.7**
- Current-day profile: **v1.0**
- MTF support/resistance: **v1.0**

## Important

These are analytical tools, not trading advice or autonomous strategies. They do not guarantee price reactions, profitability, or order execution.

## License

MIT. See [`LICENSE`](./LICENSE).
