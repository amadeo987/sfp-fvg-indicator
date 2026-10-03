# ad Current Day POC / VAH / VAL v1.0 guide

This separate overlay estimates the developing current-day volume profile and draws:

- `POC`: midpoint of the price row with the most allocated volume,
- `VAH`: upper edge of the selected value area,
- `VAL`: lower edge of the selected value area.

The value area expands outward from POC until it contains the configured percentage of the day's volume, selecting the larger adjacent row at each step.

## Default crypto setup

- Profile timezone: `Etc/UTC`
- Profile session: full day
- Value area: `70%`
- Price rows: `48`

For another market, select `exchange` or a listed timezone and adjust the session. The script is intended for intraday charts.

## Important approximation

The script distributes each chart bar's volume proportionally across every profile row overlapped by that bar's high-low range. Pine does not expose TradingView's internal tick-by-tick Volume Profile bins to another script, so these developing values can differ from the built-in Session Volume Profile. A lower chart timeframe usually provides a finer estimate but uses more stored bars.

POC, VAH, and VAL are recalculated as the current day develops. This movement is expected and is not historical repainting of a finished signal.
