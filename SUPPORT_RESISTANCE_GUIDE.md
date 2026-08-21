# SK MTF Nearest Support / Resistance v1.0

This standalone Pine v6 indicator shows the nearest confirmed pivot resistance above price and pivot support below price from up to three selected timeframes.

## Defaults

- Timeframe 1: 1H
- Timeframe 2: 4H
- Timeframe 3: 1D
- Pivot confirmation: 5 bars left and 5 bars right
- Six recent confirmed pivots checked on each side

Duplicate timeframes are ignored. Red lines are resistance; teal lines are support. Labels include the source timeframe, side, and exact price.

## Confirmation and repainting

The source calculation uses only closed source-timeframe candles. Pivot levels appear after the configured right-side confirmation delay and do not use future data. A level can disappear from the visible nearest set when price crosses it or when a closer confirmed level becomes available.

This tool marks structural reference levels. It does not predict a reaction, place orders, or provide a complete trading strategy.
