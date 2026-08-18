# SK TradingView Indicators

Three independent, open Pine Script v6 indicators for discretionary chart analysis. They do not place orders and do not require exchange API keys.

## Included scripts

### SK SFP + FVG / IFVG v5.5

[`SK_SFP_Najblizsze_Poziomy.pine`](./SK_SFP_Najblizsze_Poziomy.pine) combines:

- the `SFP WATCH → RAW → CONF` liquidity-sweep hierarchy,
- confirmed, non-repainting FVG and IFVG zone books,
- a default `Match chart` timeframe mode,
- a `Custom set` mode with any combination of three user-selected timeframes,
- nearest-zone selection above and below price,
- day separators and webhook-ready JSON alerts.

See [`SFP_WSKAZNIK_INSTRUKCJA.md`](./SFP_WSKAZNIK_INSTRUKCJA.md).

### SK WaveTrend Divergence v1.0

[`SK_WaveTrend_Divergence.pine`](./SK_WaveTrend_Divergence.pine) is a separate lower-pane oscillator. It detects confirmed regular and hidden bullish/bearish divergence and draws the comparison lines directly in its own pane.

This is an independent WaveTrend-style implementation. It does not copy or read the internal values of VuManChu Cipher B or any other protected script. See [`DIVERGENCE_INDICATOR_GUIDE.md`](./DIVERGENCE_INDICATOR_GUIDE.md).

### SK Current Day POC / VAH / VAL v1.0

[`SK_Current_Day_POC_VAH_VAL.pine`](./SK_Current_Day_POC_VAH_VAL.pine) draws a developing current-day POC, VAH, and VAL on intraday charts. The default profile day is the full UTC day for 24/7 crypto markets.

The profile is an approximation based on chart-bar volume distributed across configurable price rows. It can differ from TradingView's built-in Volume Profile, which can use finer intrabar data. See [`CURRENT_DAY_PROFILE_GUIDE.md`](./CURRENT_DAY_PROFILE_GUIDE.md).

## Installation

1. Open a TradingView chart and select **Pine Editor**.
2. Copy the complete contents of one `.pine` file into a new Pine script.
3. Save the script and choose **Add to chart**.
4. Repeat for any additional indicator you want to use.

## Alerts and Telegram webhooks

The main SFP/FVG indicator and the divergence indicator emit structured JSON through `alert()`. Create an alert using **Any alert() function call** and paste your private HTTPS webhook URL into TradingView's Webhook URL field.

No bot token, chat ID, webhook secret, private hostname, or server address belongs in these public files. TradingView alerts are snapshots: recreate an alert after changing code or indicator inputs.

The repository also contains a dependency-free, queue-backed receiver for forwarding those events to a Telegram bot. It binds to localhost by default and keeps every credential in a server-only environment file. See [`TELEGRAM_BRIDGE_GUIDE.md`](./TELEGRAM_BRIDGE_GUIDE.md).

## Repainting policy

- SFP RAW and CONF signals require closed chart candles.
- FVG/IFVG sources use the previous closed source-timeframe candle with `lookahead_on`; zones do not change while the source candle is open.
- Divergences require confirmed pivots and therefore appear after the configured right-side pivot delay.
- The current-day profile is intentionally developing and may move as new volume arrives during the active day.

## Status

- Pine language: **v6**
- Main indicator: **v5.5**
- Divergence indicator: **v1.0**
- Current-day profile: **v1.0**

## Important

These are analytical tools, not trading advice or autonomous strategies. They do not guarantee price reactions, profitability, or order execution.

## License

MIT. See [`LICENSE`](./LICENSE).
