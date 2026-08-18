# SK SFP + FVG / IFVG v5.5 guide

The main indicator is a compact liquidity and imbalance radar. Its visible hierarchy is `WATCH → RAW → CONF`.

## SFP hierarchy

- `SFP WATCH HIGH/LOW`: a confirmed quality swing and an active liquidity pool. It is context, not a signal.
- `WATCH — TOUCHED`: a consumed WATCH level retained briefly as reaction context.
- `SFP RAW SHORT/LONG`: a wick sweeps the level and the full candle body closes back behind it. RAW is confirmed on candle close and can be disabled independently.
- `SFP CONF SHORT/LONG`: within the next three candles, price closes beyond the opposite extreme of the RAW candle. This is the strongest state produced by the indicator, but it still requires trading context and risk management.

The default selective quality filter uses a 10/10 swing, a minimum 1.25 ATR reaction, and at most two current WATCH levels on each side of price. A used liquidity pool cannot produce another setup.

## FVG timeframe modes

Open **Settings → Inputs → FVG timeframes**.

- `Match chart`: default. The source follows the chart. An H4 chart shows confirmed H4 zones, H1 shows H1, M15 shows M15, M30 shows M30, and D1 shows D1.
- `Custom set`: enables up to three independent source books. Toggle each row and choose any supported TradingView timeframe. Duplicate timeframe selections are ignored.
- `Nearest zones per side and timeframe`: shows one to three nearest active zones above and below price for every enabled source.

Every source is calculated only from its last closed candle. A classic bullish FVG forms when the third candle's low is above the first candle's high; bearish is the reverse. A full wick fill removes the FVG. A source-timeframe close through the opposite edge converts it to an IFVG.

## Alerts

Enable `Enable alert() events`, then create one TradingView alert with the condition **Any alert() function call**. Dynamic JSON events include:

- `sfp_touch`
- `sfp_confirmed`
- `fvg_created`
- `ifvg_created`

The payload contains symbol, chart timeframe, event direction, price data, and source timeframe where relevant. It contains no credentials. Put the private HTTPS endpoint only in TradingView's Webhook URL field.

An alert uses a saved snapshot of the script and settings. Delete and recreate it after a code or input change.

## Limitations

WATCH is not a prediction, and CONF is not a complete strategy. The indicator never places orders. Historical testing of the SFP condition alone did not establish a standalone net-of-cost trading edge.
