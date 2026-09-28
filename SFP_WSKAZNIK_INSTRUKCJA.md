# SK SFP + FVG / IFVG v5.17 guide

The main indicator is a compact liquidity and imbalance radar. Its visible hierarchy is `SFP? → SFP → RAW → CONF`.

## SFP hierarchy

- `SFP?`: a confirmed quality swing and an active liquidity pool that price has not used yet. Up to three nearest candidates on either side of price are drawn in blue. It is context, not a signal.
- `SFP`: a candidate that price has touched or swept. It is retained briefly as reaction context and disappears immediately after a second separate retest; one continuous overlap is not counted twice. The short label does not by itself mean RAW or CONF confirmation.
- `SFP RAW SHORT/LONG`: a wick sweeps the level and the full candle body closes back behind it. RAW is confirmed on candle close and can be disabled independently.
- `SFP CONF SHORT/LONG`: within the next three candles, price closes beyond the opposite extreme of the RAW candle. It is a historical confirmation of that setup, not a new entry signal when price returns later. CONF is shown only on its confirmation candle, without a horizontal line. The consumed pool is blocked from returning to the active or touched radar; a nearby level can become valid again only from a genuinely newer pivot.

The default selective quality filter uses a 10/10 swing, a minimum 1.25 ATR reaction, and at most three current `SFP?` levels on each side of price. A used liquidity pool cannot produce another setup.

On CRYPTOCAP market-cap indices such as `TOTAL`, `TOTAL2` and `TOTAL3`, the indicator keeps blue `SFP?`/`SFP` context and FVG/IFVG zones but suppresses directional red/green RAW and CONF lines. These indices are observational aggregates rather than directly tradable instruments, so signal-style lines would be misleading there. Normal crypto pairs and other instruments keep the full hierarchy.

## FVG timeframe modes

Open **Settings → Inputs → FVG timeframes**.

- `Match chart`: default. The source follows the chart. An H4 chart shows confirmed H4 zones, H1 shows H1, M15 shows M15, M30 shows M30, and D1 shows D1.
- `Custom set`: enables up to three independent source books. Toggle each row and choose any supported TradingView timeframe. Duplicate timeframe selections are ignored.
- `Nearest zones above per timeframe`: shows two active zones above price by default.
- `Nearest zones below per timeframe`: shows six active zones below price by default, so deeper unfilled imbalances remain visible. Both limits can be set from one to eight independently for every enabled source timeframe.

Every source is calculated only from its last closed candle. A classic bullish FVG forms when the third candle's low is above the first candle's high; bearish is the reverse. A full wick fill removes the FVG. A source-timeframe close through the opposite edge converts it to an IFVG.

## Adaptive calendar markers

With `Day / month separators` enabled, intraday charts keep Warsaw weekday labels and day separators. Daily, weekly, and monthly charts switch to abbreviated month labels. Monthly charts omit the repeated vertical separator so the bottom of the chart does not become a continuous white strip.

## Moving averages

Open **Settings → Inputs → Moving averages**. EMA 200 is enabled by default. EMA 100, EMA 50 and one custom-length EMA are available in the same indicator but disabled by default. All averages use `close` from the current chart timeframe, so no separate timeframe request or higher-timeframe delay is involved. Each EMA has its own color setting, and the shared line width can be set from one to four.

## Dual Auto VWAP

Open **Settings → Inputs → Dual Auto VWAP**. Both lines are enabled by default, use `hlc3 = (high + low + close) / 3`, have no deviation bands, and default to a thin 1 px width. On intraday charts the fast VWAP resets each session/day and the slow VWAP resets each week. The first candle of every new anchor is plotted immediately instead of being hidden, so the reset does not create an extra one-candle hole. On higher chart timeframes their anchors advance automatically: `1D → month / quarter`, `2D-10D → quarter / year`, `11D-60D → year / decade`, and longer charts use decade / century anchors. Each line has its own color and both share a configurable line width.

The VWAPs are visual context only. They do not emit alerts. A crossover is not a standalone entry signal; use price acceptance, rejection or reclaim together with the existing SFP context.

## PVP naked POC

Open **Settings → Inputs → PVP naked POC**. The module creates POC levels from completed Daily, Weekly and Monthly profiles. It distributes every lower-timeframe bar's volume proportionally across the price rows crossed by that bar, selects the highest-volume row, and extends its midpoint to the right. The sampling timeframe and row count are configurable; lower sampling is more detailed but heavier and provides less history.

Only still-untouched levels remain visible. The first later sample whose high-low range crosses a level removes it immediately. Daily, Weekly and Monthly visibility, nearest-level limits, colors and labels can be configured independently. Lines are 1 px and white by default.

This is a deterministic OHLCV approximation. Pine Script cannot read TradingView's internal tick-by-price PVP engine, so exact POC values can differ from the built-in Periodic Volume Profile, especially when the selected sampling timeframe is coarse.

## Watermark

The `[SK] Watermark v1.2` controls are integrated under the three Watermark groups. The default text is `ig: amadeusz.dyrek` in the upper-right corner. It supports a second line, multiple font styles, bold/italic formatting, underline/strikethrough, colors, size, position and edge offset. Disable `Show watermark` when a clean chart is needed.

## Alerts

SKSFP v5.17 is visual-only. It contains no `alert()` or `alertcondition()` calls and has no Telegram/webhook dependency. Removing its obsolete indicator alert does not affect separate price or drawing alerts.

## Limitations

WATCH is not a prediction, and CONF is not a complete strategy. PVP nPOC levels are context, not automatic entries. The indicator never places orders. Historical testing of the SFP condition alone did not establish a standalone net-of-cost trading edge.
