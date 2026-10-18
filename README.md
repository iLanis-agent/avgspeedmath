# Average Speed Math

Average speed arithmetic. Half the way at 60 and half at 30 is not an average of 45.

## What it computes

- **The trip truth** - two legs, each at its own steady speed: total time, the true average, and the plain mean of the two speeds it is not.
- **The time truth** - one distance at one speed, as hours and minutes.
- **The need truth** - the speed the last part needs to reach a target average over the whole distance, or a plain statement that no speed on it can.

Distances are whole numbers from 1 to 100000, speeds whole numbers from 1 to 1000, in any one unit. Times round to the nearest minute and speeds to two decimals, half up; rounded results say "about".

## Boundary

Arithmetic only. Each leg is taken at one steady speed. Average Speed Math does not know speed limits, stops, traffic or conditions. Check those where they apply.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (45 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/avgspeedmath/
Repo: https://github.com/iLanis-agent/avgspeedmath
