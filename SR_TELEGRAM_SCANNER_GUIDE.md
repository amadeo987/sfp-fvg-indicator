# SK S/R Telegram Scanner v1.1

This Pine v6 scanner monitors the nearest confirmed pivot support and resistance for:

- BTC perpetual on OKX,
- ETH perpetual on OKX,
- HYPE perpetual on Hyperliquid,
- 1H and 4H for every enabled market.

The scanner uses closed source-timeframe candles for pivot confirmation. Touch detection is intrabar and uses a configurable percentage band around each confirmed level. The default band is 0.05%. It sends information only; it has no exchange API, order, or position-management capability.

## TradingView setup

1. Add the scanner to a standard-candle chart on 1H or lower. A 1H chart is the practical default.
2. Keep the three default perpetual symbols or replace them in the indicator settings.
3. Create one alert using **Any alert() function call**.
4. Enable Webhook URL and paste the private HTTPS bridge endpoint.

The dynamic JSON event includes event name, exchange-qualified symbol, source timeframe, support/resistance side, confirmed level, current price, distance percentage, and source-bar time.

The scanner intentionally draws no table or price objects on the chart. It runs only as an alert source, so it does not cover candles or interfere visually with the main SFP/FVG indicator.

TradingView alerts store a snapshot of code and inputs. Delete and recreate the scanner alert after changing the script, symbols, timeframes, or detection settings.

## Limits

- A pivot is confirmed only after the configured right-side delay.
- The scanner reports a structural level touch; it does not predict a bounce or breakout.
- Running the alert on a chart above 1H can skip 1H intrabar touches.
