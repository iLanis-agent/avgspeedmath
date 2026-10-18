#!/usr/bin/env python3
# Average Speed Math oracle - mirrors engine.js.
import json, math

def _int(x, label, mx):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or math.floor(x) != x or x < 1 or x > mx:
        raise ValueError(f"{label} must be a whole number from 1 to {mx}")
    return int(x)

def _d(x, label): return _int(x, label, 100000)
def _s(x, label): return _int(x, label, 1000)

def _div(n, d):
    return (2 * n + d) // (2 * d)

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def _time(m):
    if m == 0:
        return "under 1 min"
    h, mm = divmod(m, 60)
    if h == 0:
        return f"{mm} min"
    return f"{h} h {mm} min"

def _took(m, exact):
    return ("" if exact or m == 0 else "about ") + _time(m)

def trip_truth(d1, s1, d2, s2):
    a = _d(d1, "first distance"); x = _s(s1, "first speed")
    b = _d(d2, "second distance"); y = _s(s2, "second speed")
    den = a * y + b * x
    num = (a + b) * x * y
    avg_exact = (num * 100) % den == 0
    time_exact = (60 * den) % (x * y) == 0
    avg = _fmt(_div(num * 100, den))
    mean = _fmt((x + y) * 50)
    tail = "the same as the plain mean of the two speeds." if 2 * num == (x + y) * den else f"not {mean}, the plain mean of the two speeds."
    return (f"Covering {a} at {x} and {b} at {y} takes {_took(_div(60 * den, x * y), time_exact)}"
            f" and averages {'' if avg_exact else 'about '}{avg}, {tail}")

def time_truth(distance, speed):
    d = _d(distance, "distance"); s = _s(speed, "speed")
    exact = (60 * d) % s == 0
    return f"Covering {d} at {s} takes {_took(_div(60 * d, s), exact)}."

def need_truth(total, done, speed, target):
    D = _d(total, "total distance"); d = _d(done, "distance covered")
    s = _s(speed, "speed so far"); t = _s(target, "target average")
    if d >= D:
        raise ValueError("distance covered must be less than the total distance")
    r = D - d
    den = D * s - d * t
    if den <= 0:
        return (f"No speed on the last {r} reaches an average of {t} over {D}: the first {d} at {s} already uses all the time {D} allows at {t}.")
    top = r * t * s
    exact = (top * 100) % den == 0
    return (f"To average {t} over {D}, the last {r} has to be covered at {'' if exact else 'about '}{_fmt(_div(top * 100, den))}, after the first {d} at {s}.")

FNS = {"tripTruth": trip_truth, "timeTruth": time_truth, "needTruth": need_truth}

CASES = [
    ("tripTruth", [60, 60, 60, 30]), ("tripTruth", [60, 60, 60, 60]), ("tripTruth", [100, 50, 100, 50]),
    ("tripTruth", [10, 60, 90, 30]), ("tripTruth", [90, 60, 10, 30]), ("tripTruth", [1, 1, 1, 1000]),
    ("tripTruth", [100000, 1000, 100000, 1]), ("tripTruth", [1, 1000, 1, 1000]), ("tripTruth", [30, 60, 60, 30]),
    ("tripTruth", [7, 3, 5, 11]), ("tripTruth", [120, 40, 60, 80]),
    ("tripTruth", [0, 60, 60, 30]), ("tripTruth", [60, 0, 60, 30]), ("tripTruth", [60, 60, 100001, 30]), ("tripTruth", [60, 60, 60, 1001]), ("tripTruth", [60.5, 60, 60, 30]),
    ("timeTruth", [100, 60]), ("timeTruth", [60, 60]), ("timeTruth", [1, 1000]), ("timeTruth", [1, 7]), ("timeTruth", [50, 100]),
    ("timeTruth", [100000, 1]), ("timeTruth", [90, 60]), ("timeTruth", [10, 60]), ("timeTruth", [5, 40]), ("timeTruth", [200, 3]),
    ("timeTruth", [0, 60]), ("timeTruth", [100, 0]), ("timeTruth", [100, 1001]), ("timeTruth", [100.5, 60]),
    ("needTruth", [120, 60, 40, 60]), ("needTruth", [120, 60, 60, 60]), ("needTruth", [120, 60, 120, 60]),
    ("needTruth", [100, 50, 30, 60]), ("needTruth", [100, 50, 30, 40]), ("needTruth", [100, 50, 30, 30]),
    ("needTruth", [100, 99, 50, 51]), ("needTruth", [100000, 1, 1, 1]), ("needTruth", [100, 1, 100, 100]), ("needTruth", [10, 1, 1000, 10]),
    ("needTruth", [100, 100, 50, 50]), ("needTruth", [100, 150, 50, 50]), ("needTruth", [0, 1, 50, 50]), ("needTruth", [100, 50, 0, 50]), ("needTruth", [100, 50, 30, 1001]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
