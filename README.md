# ad TradingView Indicators

Open Pine Script v6 indicators for discretionary chart analysis. They do not place orders and do not require exchange API keys.

## Included scripts

### ad SFP + FVG / IFVG v5.17

[`SK_SFP_Najblizsze_Poziomy.pine`](./SK_SFP_Najblizsze_Poziomy.pine) combines:

- the compact `SFP? → SFP → RAW → CONF` liquidity-sweep hierarchy,
- confirmed, non-repainting FVG and IFVG zone books,
- a default `Match chart` timeframe mode,
- a `Custom set` mode with any combination of three user-selected timeframes,
- asymmetric nearest-zone selection: two active zones above and six below price per enabled timeframe by default,
- adaptive weekday/month markers,
- automatic removal of consumed WATCH context after its second separate retest,
- immediate removal of a touched radar level once its SFP setup is confirmed,
- three blue candidate levels on each side of price,
- no directional RAW/CONF signal lines on CRYPTOCAP market-cap indices such as TOTAL, while blue SFP context and FVG/IFVG zones remain visible,
- confirmed SFP events shown only as short-lived labels on the confirmation candle, with no horizontal CONF line that could look like a later retest entry,
- a chart-timeframe EMA 200 enabled by default, optional EMA 100 and EMA 50 overlays, and one configurable custom-length EMA,
- two band-free `hlc3` Auto VWAP overlays: a faster session/day context and a slower weekly context on intraday charts, with automatic longer anchors on higher chart timeframes, thin 1 px defaults, and no omitted reset candle,
- integrated PVP-style naked Daily/Weekly/Monthly POC levels based on selectable lower-timeframe OHLCV samples, extended right only while untouched,
- the configurable viewport watermark from `[ad] Watermark`, enabled by default with `ig: amadeusz.dyrek`,
- no `alert()` calls, Telegram scanner, webhook router, bot token or exchange API key,
- a short `adSFP 5.17` status-line name with no scanner table.

See [`SFP_WSKAZNIK_INSTRUKCJA.md`](./SFP_WSKAZNIK_INSTRUKCJA.md).

### ad Current Day POC / VAH / VAL v1.0

[`SK_Current_Day_POC_VAH_VAL.pine`](./SK_Current_Day_POC_VAH_VAL.pine) draws a developing current-day POC, VAH, and VAL on intraday charts. The default profile day is the full UTC day for 24/7 crypto markets.

The profile is an approximation based on chart-bar volume distributed across configurable price rows. It can differ from TradingView's built-in Volume Profile, which can use finer intrabar data. See [`CURRENT_DAY_PROFILE_GUIDE.md`](./CURRENT_DAY_PROFILE_GUIDE.md).

### ad MTF Nearest Support / Resistance v1.0

[`SK_MTF_Nearest_Support_Resistance.pine`](./SK_MTF_Nearest_Support_Resistance.pine) shows the nearest confirmed pivot support below price and resistance above price from up to three selected source timeframes. It is intentionally separate from the main SFP indicator. See [`SUPPORT_RESISTANCE_GUIDE.md`](./SUPPORT_RESISTANCE_GUIDE.md).

## Installation

1. Open a TradingView chart and select **Pine Editor**.
2. Copy the complete contents of one `.pine` file into a new Pine script.
3. Save the script and choose **Add to chart**.
4. Repeat for any additional indicator you want to use.

## TradingView publication

The canonical TradingView publication is the single private, protected entry **`[ad] SFP + FVG / IFVG`**. New releases must use **Pine Editor → Publish script → Update existing script** and select that stable entry. Do not publish a new version-numbered entry for routine updates; the saved source can keep its visible `adSFP x.y` version while the publication URL and access target stay unchanged.

## Alerts

The v5.17 main indicator is visual-only and contains no `alert()` or `alertcondition()` calls. Its former Telegram scanner and webhook bridge have been retired. Existing price/drawing alerts in the TradingView account are separate and are not changed by the script.

## Repainting policy

- SFP RAW and CONF signals require closed chart candles.
- FVG/IFVG sources use the previous closed source-timeframe candle with `lookahead_on`; zones do not change while the source candle is open.
- MTF support/resistance levels require confirmed pivots and therefore appear after the configured right-side pivot delay.
- The current-day profile is intentionally developing and may move as new volume arrives during the active day.

## Status

- Pine language: **v6**
- Main indicator: **v5.17**
- Current-day profile: **v1.0**
- MTF support/resistance: **v1.0**

## Important

These are analytical tools, not trading advice or autonomous strategies. They do not guarantee price reactions, profitability, or order execution.

## License

MIT. See [`LICENSE`](./LICENSE).
