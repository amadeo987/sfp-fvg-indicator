# SK WaveTrend Divergence v1.0 guide

This separate lower-pane indicator compares confirmed price pivots with confirmed pivots in an independently calculated WaveTrend-style oscillator.

## Signals

- Regular bullish: price makes a lower low while the oscillator makes a higher low.
- Hidden bullish: price makes a higher low while the oscillator makes a lower low.
- Regular bearish: price makes a higher high while the oscillator makes a lower high.
- Hidden bearish: price makes a lower high while the oscillator makes a higher high.

The script draws the comparison line in the oscillator pane and labels it `REG BULL`, `HID BULL`, `REG BEAR`, or `HID BEAR`.

## Timeframes and confirmation

The indicator follows the active chart timeframe. Switch the chart timeframe to inspect divergence on another timeframe. A pivot appears only after `Pivot right bars` have closed, so the signal is delayed by design but does not later move to another candle.

## Independence from Cipher B

Pine scripts cannot access the private internal series of another indicator. This implementation does not copy VuManChu Cipher B code and does not claim to reproduce its proprietary signals. It provides a transparent oscillator and divergence layer that can be used alongside another study.

## Alerts

Enable `Enable alert() events` and create an alert using **Any alert() function call**. The JSON event is `divergence_confirmed` and includes symbol, timeframe, direction, divergence kind, pivot price, oscillator value, and pivot time.
