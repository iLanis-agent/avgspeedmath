// Average Speed Math engine - round-trip average, time for a leg, and the speed a last leg needs.
// Mirrored by oracle.py; keep the op order identical.
// Distances are whole numbers from 1 to 100000, speeds whole numbers from 1 to 1000, in any one unit.
// Results are rounded half up. Each leg is taken at one steady speed.

function _int(x, label, max) {
  if (typeof x !== "number" || !isFinite(x) || Math.floor(x) !== x || x < 1 || x > max) {
    throw new Error(label + " must be a whole number from 1 to " + max);
  }
  return x;
}
function _d(x, label) { return _int(x, label, 100000); }
function _s(x, label) { return _int(x, label, 1000); }

function _div(n, d) {
  return Math.floor((2 * n + d) / (2 * d));
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

function _time(min) {
  if (min === 0) return "under 1 min";
  var h = Math.floor(min / 60), m = min % 60;
  if (h === 0) return m + " min";
  return h + " h " + m + " min";
}

function _took(min, exact) {
  return (exact || min === 0 ? "" : "about ") + _time(min);
}

// The trip truth: two legs, each at its own steady speed.
function tripTruth(d1, s1, d2, s2) {
  var a = _d(d1, "first distance"), x = _s(s1, "first speed");
  var b = _d(d2, "second distance"), y = _s(s2, "second speed");
  var den = a * y + b * x;
  var num = (a + b) * x * y;
  var avgExact = (num * 100) % den === 0;
  var timeExact = (60 * den) % (x * y) === 0;
  var avg = _fmt(_div(num * 100, den));
  var mean = _fmt((x + y) * 50);
  var tail = 2 * num === (x + y) * den
    ? "the same as the plain mean of the two speeds."
    : "not " + mean + ", the plain mean of the two speeds.";
  return "Covering " + a + " at " + x + " and " + b + " at " + y + " takes " + _took(_div(60 * den, x * y), timeExact) + " and averages " + (avgExact ? "" : "about ") + avg + ", " + tail;
}

// The time truth: one distance at one speed.
function timeTruth(distance, speed) {
  var d = _d(distance, "distance"), s = _s(speed, "speed");
  var exact = (60 * d) % s === 0;
  return "Covering " + d + " at " + s + " takes " + _took(_div(60 * d, s), exact) + ".";
}

// The need truth: the speed the last part needs to hit a target average over the whole distance.
function needTruth(total, done, speed, target) {
  var D = _d(total, "total distance"), d = _d(done, "distance covered");
  var s = _s(speed, "speed so far"), t = _s(target, "target average");
  if (d >= D) throw new Error("distance covered must be less than the total distance");
  var r = D - d;
  var den = D * s - d * t;
  if (den <= 0) {
    return "No speed on the last " + r + " reaches an average of " + t + " over " + D +
      ": the first " + d + " at " + s + " already uses all the time " + D + " allows at " + t + ".";
  }
  var top = r * t * s;
  var exact = (top * 100) % den === 0;
  return "To average " + t + " over " + D + ", the last " + r + " has to be covered at " +
    (exact ? "" : "about ") + _fmt(_div(top * 100, den)) + ", after the first " + d + " at " + s + ".";
}
