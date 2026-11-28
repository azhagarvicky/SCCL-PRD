/* LMS prototype – Dashboard (DISC-497). All numbers are SAMPLE data (not the live LMS figures). Charts are plain SVG. Source file. */
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var C = { g: '#08994f', y: '#fdc34a', o: '#f58e0b', r: '#d7291f', line: '#7c6cf0', aum: '#0038cc' };
  var $ = function (id) { return document.getElementById(id); };
  var pad = function (n) { return ('0' + n).slice(-2); };
  var now = new Date();
  $('upd').textContent = pad(now.getDate()) + '-' + pad(now.getMonth() + 1) + '-' + now.getFullYear() + ' ' + pad(now.getHours()) + ':' +
    pad(now.getMinutes()) + ':' + pad(now.getSeconds());

  // utilisation legend (Risk Snapshot / Utilization)
  [].forEach.call(document.querySelectorAll('.lg-key'), function (el) {
    el.innerHTML = 'Utilisation Drawing Power <i style="--c:var(--g)"></i>&lt;= 80% <i style="--c:var(--y)"></i>80% - 90% ' +
      '<i style="--c:var(--o)"></i>90% - 100% <i style="--c:var(--r)"></i>&gt;= 100%';
  });

  function svg(w, h, cls) { var s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', '0 0 ' + w + ' ' + h); if (cls) s.setAttribute('class', cls); return s; }
  function el(tag, attrs, parent, text) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  // ---- hover pop-up (tooltip) as in the live LMS (DISC-504)
  var tip = document.createElement('div'); tip.className = 'tip'; tip.hidden = true; document.body.appendChild(tip);
  var BAND = { g: '&lt;= 80%', y: '80% - 90%', o: '90% - 100%', r: '100%+' };
  function inr(n, dec) {   // Indian grouping: 51,76,400
    var neg = n < 0, x = Math.abs(n), f = dec ? x.toFixed(dec) : String(Math.round(x)), p = f.split('.'), w = p[0];
    var last = w.slice(-3), rest = w.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    return (neg ? '-' : '') + (rest ? rest + ',' + last : last) + (p[1] ? '.' + p[1] : '');
  }
  function day(back) { var d = new Date(); d.setDate(d.getDate() - back); return pad(d.getDate()) + '-' + pad(d.getMonth() + 1) + '-' + d.getFullYear(); }
  function showTip(html, e) {
    tip.innerHTML = html; tip.hidden = false;
    var w = tip.offsetWidth, h = tip.offsetHeight, x = e.clientX + 14, y = e.clientY - h / 2;
    if (x + w > innerWidth - 8) x = e.clientX - w - 14;
    tip.style.left = Math.max(8, x) + 'px'; tip.style.top = Math.max(8, Math.min(y, innerHeight - h - 8)) + 'px';
  }
  function hideTip() { tip.hidden = true; }
  function row(c, label, val) { return '<div class="tr"><span>' + (c ? '<i style="background:' + C[c] + '"></i>' : '') + label + '</span><b>' + val + '</b></div>'; }
  function svgX(sv, e) { var r = sv.getBoundingClientRect(), vb = sv.viewBox.baseVal; return (e.clientX - r.left) * vb.width / r.width; }
  var gid = 0;
  function spark(data, flat, k) {   // lavender area sparkline as in the KPI cards
    var w = 132, h = 66, s = svg(w, h, 'sp'), mn = Math.min.apply(0, data), mx = Math.max.apply(0, data), r = mx - mn || 1;
    var pts = data.map(function (v, i) { return [i * w / (data.length - 1), flat ? h - 6 : 6 + (h - 12) * (1 - (v - mn) / r)]; });
    var d = 'M' + pts.map(function (p) { return p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' L');
    var id = 'sg' + (++gid), g = el('linearGradient', { id: id, x1: 0, y1: 0, x2: 0, y2: 1 }, el('defs', {}, s));
    el('stop', { offset: '0', 'stop-color': '#c9c0ff', 'stop-opacity': '.95' }, g); el('stop', { offset: '1', 'stop-color': '#ffffff', 'stop-opacity': '0' }, g);
    if (!flat) el('path', { d: d + ' L' + w + ' ' + h + ' L0 ' + h + ' Z', fill: 'url(#' + id + ')' }, s);
    el('path', { d: d, fill: 'none', stroke: C.line, 'stroke-width': 1.6 }, s);
    // hover: vertical line + dot + date / value (sample values scaled so the last point = the card value)
    var vl = el('line', { y1: 0, y2: h, stroke: '#c9ccd3', 'stroke-width': 1, visibility: 'hidden' }, s);
    var dot = el('circle', { r: 3.2, fill: C.line, stroke: '#fff', 'stroke-width': 1.2, visibility: 'hidden' }, s);
    var last = data[data.length - 1] || 1, mult = k && k.num ? k.num / last : 0, n = data.length;
    var hit = el('rect', { x: 0, y: 0, width: w, height: h, fill: 'transparent' }, s);
    hit.addEventListener('mousemove', function (e) {
      var i = Math.max(0, Math.min(n - 1, Math.round(svgX(s, e) / w * (n - 1)))), v = flat ? 0 : data[i] * mult;
      vl.setAttribute('x1', pts[i][0]); vl.setAttribute('x2', pts[i][0]); vl.setAttribute('visibility', 'visible');
      dot.setAttribute('cx', pts[i][0]); dot.setAttribute('cy', pts[i][1]); dot.setAttribute('visibility', 'visible');
      showTip('<div class="th">' + day((n - 1 - i) * 2) + '</div>' + row('', 'value', k && k.money ? '₹' + inr(v) : inr(v)), e);
    });
    hit.addEventListener('mouseleave', function () { vl.setAttribute('visibility', 'hidden'); dot.setAttribute('visibility', 'hidden'); hideTip(); });
    return s;
  }
  function delta(v) { var neg = /^-/.test(v); return '<b class="' + (neg ? 'dn-c' : 'up') + '">' + (neg ? v : '+' + v.replace(/^\+/, '')) + '</b>'; }
  function kpi(card, k) {
    card.innerHTML = '<span class="t">' + k.t + '</span><div class="vr"><span class="v">' + k.v + '</span><span class="dl">MTD' + delta(k.mtd) +
      '<br>MoM' + delta(k.mom) + '</span></div>';
    if (k.s) card.appendChild(spark(k.s, k.flat, k));
  }

  // ---- Top level KPIs (sample)
  var KPIS = [
    { t: 'Sanctioned Amount', v: '64.8L', num: 6480000, money: 1, mtd: '+5.2L', mom: '-41.7L', s: [8, 9, 30, 31, 24, 26, 27, 28, 31, 33, 34, 36, 37, 37, 36] },
    { t: 'Principal Outstanding', v: '6.9L', num: 690000, money: 1, mtd: '-15.4L', mom: '-22.1L', s: [60, 60, 60, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 2] },
    { t: 'No of Active Loans', v: '58', num: 58, mtd: '+29', mom: '+8', s: [4, 5, 6, 8, 9, 11, 12, 14, 16, 18, 20, 23, 25, 27, 28] },
    { t: 'Exposure at Risk', v: '47.3L', num: 4730000, money: 1, mtd: '+22.5L', mom: '+1.4L', s: [6, 7, 8, 9, 10, 11, 12, 14, 15, 15, 17, 20, 22, 27, 26] },
    { t: 'Defaulted Sanctioned Loans', v: '0', mtd: '+0', mom: '-15L', s: [1, 1, 1, 1, 1, 1, 1, 1], flat: true },
    { t: 'Margin Calls Pending', v: '4', num: 4, mtd: '-3', mom: '-7', s: [12, 9, 10, 6, 5, 2, 2, 2, 1, 1, 4, 5, 3, 6, 4] }];
  var kp = $('kpis');
  KPIS.forEach(function (k) { var c = document.createElement('section'); c.className = 'cd kp'; kpi(c, k); kp.appendChild(c); });

  // ---- Collections (sample)
  var COL = {
    po: { t: 'Principal Overdue', v: '0', mtd: '+0', mom: '+0', s: [1, 1, 1, 1, 1], flat: true },
    co: { t: 'Charges Overdue', v: '104', num: 104, mtd: '+0', mom: '+0', s: [9, 9, 9, 9, 9, 9] },
    pc: { t: 'Principal Collected', v: '15.6L', mtd: '+15.6L', mom: '+15.8L' },
    pd: { t: 'Principal due', v: '0', mtd: '+254.10', mom: '-31.25' },
    cc: { t: 'Charges Collected', v: '772.40', mtd: '+39814.20', mom: '-9520.75' },
    cdu: { t: 'Charges Due', v: '0', mtd: '+318', mom: '+318' } };
  [].forEach.call(document.querySelectorAll('.kp[data-k]'), function (c) { kpi(c, COL[c.getAttribute('data-k')]); });

  // ---- Donuts (sample)
  function donut(id, totalId, total, parts) {
    var box = $(id), s = svg(200, 200), R = 76, W = 40, L = 2 * Math.PI * R, sum = parts.reduce(function (a, p) { return a + p.v; }, 0), off = 0;
    $(totalId).textContent = total;
    // order around the ring as in the live screen: orange (top), red, green, yellow
    [['o', 0], ['r', 3], ['g', 2], ['y', 1]].forEach(function (o) {
      var p = parts[o[1]], len = L * p.v / sum;
      var seg = el('circle', { cx: 100, cy: 100, r: R, fill: 'none', stroke: C[o[0]], 'stroke-width': W, 'stroke-dasharray': len + ' ' + (L - len),
        'stroke-dashoffset': -off, transform: 'rotate(-180 100 100)', class: 'seg' }, s);
      seg.addEventListener('mousemove', function (e) { showTip(row(o[0], BAND[o[0]], p.tip || p.t), e); });
      seg.addEventListener('mouseleave', hideTip);
      off += len;
    });
    box.appendChild(s);
    var ul = document.createElement('ul');
    ul.innerHTML = parts.map(function (p) { return '<li><i style="--c:var(--' + p.c + ')"></i>' + p.t + '</li>'; }).join('');
    box.appendChild(ul);
  }
  donut('d1', 'd1t', '₹65,42,310', [{ c: 'o', v: 3285400, t: '₹32,85,400', tip: '₹32,85,400' }, { c: 'y', v: 1102750, t: '₹11,02,750' },
    { c: 'g', v: 1844160, t: '₹18,44,160' }, { c: 'r', v: 310000, t: '₹3,10,000' }]);
  donut('d2', 'd2t', '62', [{ c: 'o', v: 40, t: '40' }, { c: 'y', v: 8, t: '8' }, { c: 'g', v: 12, t: '12' }, { c: 'r', v: 2, t: '2' }]);

  // ---- Trends over 30 days (sample, in lakh)
  (function () {
    var W = 440, H = 270, x0 = 46, x1 = W - 10, y0 = 14, y1 = H - 34, s = svg(W, H, 'ch'), max = 60;
    var X = function (d) { return x0 + (x1 - x0) * (d - 1) / 29; }, Y = function (v) { return y1 - (y1 - y0) * v / max; };
    [0, 15, 30, 45, 60].forEach(function (v) {
      el('text', { x: x0 - 10, y: Y(v) + 4, 'text-anchor': 'end' }, s, '₹' + v + 'L');
      if (v) el('line', { x1: x0, x2: x1, y1: Y(v), y2: Y(v), stroke: '#f0f0f3', 'stroke-dasharray': '3 4' }, s);
    });
    el('line', { x1: x0, x2: x1, y1: y1, y2: y1, stroke: '#9aa0ab' }, s);
    for (var d = 1; d <= 30; d++) {
      el('line', { x1: X(d), x2: X(d), y1: y1, y2: y1 + 6, stroke: '#9aa0ab' }, s);
      if (d === 1 || d % 5 === 0) el('text', { x: X(d), y: y1 + 20, 'text-anchor': 'middle' }, s, d);
    }
    var S = {
      g: [33, 38, 38, 38, 40, 40, 40, 20, 19, 20, 21, 19, 20, 18, 21, 22, 23, 22, 23, 23, 21, 21, 26, 21, 19, 19, 18, 19, 19, 19],
      o: [6, 9, 9, 9, 9, 9, 10, 11, 13, 14, 15, 16, 16, 18, 19, 20, 20, 21, 22, 22, 24, 26, 28, 28, 31, 34, 33, 33, 33, 34],
      y: [4, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9],
      r: [3, 3, 3, 3, 2.5, 2.5, 2.5, 2.5, 2, 2, 2, 2, 2, 2, 1.5, 1.5, 1, 1, 1, 2, 2, 2, 1.5, 1.5, 1.5, 1.5, 4, 4, 3, 3] };
    ['g', 'o', 'y', 'r'].forEach(function (k) {
      el('path', { d: 'M' + S[k].map(function (v, i) { return X(i + 1).toFixed(1) + ' ' + Y(v).toFixed(1); }).join(' L'), fill: 'none', stroke: C[k], 'stroke-width': 1.5 }, s);
    });
    var dots = {}; ['g', 'y', 'o', 'r'].forEach(function (k) { dots[k] = el('circle', { r: 3.4, fill: C[k], stroke: '#fff', 'stroke-width': 1.2, visibility: 'hidden' }, s); });
    var hit = el('rect', { x: x0, y: y0, width: x1 - x0, height: y1 - y0, fill: 'transparent' }, s);
    hit.addEventListener('mousemove', function (e) {
      var d = Math.max(1, Math.min(30, Math.round((svgX(s, e) - x0) / (x1 - x0) * 29) + 1)), html = '<div class="th">' + day(30 - d) + '</div>';
      ['g', 'y', 'o', 'r'].forEach(function (k) {
        var v = S[k][d - 1];
        dots[k].setAttribute('cx', X(d)); dots[k].setAttribute('cy', Y(v)); dots[k].setAttribute('visibility', 'visible');
        html += row(k, BAND[k], '₹' + inr(v * 100000 + ((d * 7919 + k.charCodeAt(0) * 131) % 99000)));
      });
      showTip(html, e);
    });
    hit.addEventListener('mouseleave', function () { for (var k in dots) dots[k].setAttribute('visibility', 'hidden'); hideTip(); });
    $('tr').appendChild(s);
  })();

  // ---- Stacked / plain bar charts (sample)
  function bars(id, cats, data, max, ticks, rotate) {
    var W = 440, H = 390, x0 = 34, x1 = W - 8, y0 = 14, y1 = H - 62, s = svg(W, H, 'ch'), n = cats.length, bw = Math.min(24, (x1 - x0) / n * .38);
    var Y = function (v) { return y1 - (y1 - y0) * v / max; };
    ticks.forEach(function (v) {
      el('text', { x: x0 - 10, y: Y(v) + 4, 'text-anchor': 'end' }, s, v);
      el('line', { x1: x0, x2: x1, y1: Y(v), y2: Y(v), stroke: '#f0f0f3', 'stroke-dasharray': '3 4' }, s);
    });
    cats.forEach(function (c, i) {
      var cx = x0 + (x1 - x0) * (i + .5) / n, acc = 0, cw = (x1 - x0) / n;
      var band = el('rect', { x: cx - cw / 2, y: y0, width: cw, height: y1 - y0, fill: '#f3f3f4', opacity: 0 }, s);
      var hit = el('rect', { x: cx - cw / 2, y: y0, width: cw, height: y1 - y0, fill: 'transparent' }, null);
      var cnt = { r: 0, o: 0, y: 0, g: 0 }; (data[i] || []).forEach(function (seg) { cnt[seg[0]] += seg[1]; });
      hit.addEventListener('mousemove', function (e) {
        band.setAttribute('opacity', 1);
        showTip('<div class="th">' + c + '</div>' + ['r', 'o', 'y', 'g'].map(function (k) { return row(k, BAND[k], cnt[k]); }).join(''), e);
      });
      hit.addEventListener('mouseleave', function () { band.setAttribute('opacity', 0); hideTip(); });
      setTimeout(function () { s.appendChild(hit); });
      (data[i] || []).forEach(function (seg) {
        var h = (y1 - y0) * seg[1] / max;
        el('rect', { x: cx - bw / 2, y: Y(acc) - h, width: bw, height: h, fill: C[seg[0]] }, s);
        acc += seg[1];
      });
      var t = el('text', { x: cx, y: y1 + 18, 'text-anchor': 'end', transform: 'rotate(' + (rotate || -30) + ' ' + cx + ' ' + (y1 + 18) + ')' }, s, c);
      t.setAttribute('dx', '8');
    });
    $(id).appendChild(s);
  }
  var T = ['0-1L', '1L-5L', '5L-10L', '10L-25L', '25-50L', '50L+'];
  bars('b1', T, [[['o', 33], ['y', 8], ['g', 6]], [['r', 2], ['o', 8], ['y', 1], ['g', 4]], [['y', 1], ['g', 1]]], 50, [0, 15, 30, 45, 50]);
  bars('b2', T, [[['y', 27], ['g', 40]], [['r', 7], ['y', 8], ['g', 7]], [['y', 4]]], 80, [0, 20, 40, 60, 80]);
  bars('b3', ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100+'],
    [[['g', 5]], [], [], [['g', 2]], [], [], [['g', 3]], [['g', 2]], [['y', 8]], [['o', 41]], [['r', 2]]], 60, [0, 15, 30, 45, 60]);

  // ---- Top 10 Holdings – AUM by AMC (sample, in lakh)
  (function () {
    var amc = ['ICICI Prudential', 'HDFC', 'Aditya Birla Sun Life', 'Nippon India', 'UTI', 'DSP', 'Sundaram', 'Groww', 'Motilal Oswal', 'Axis'];
    var v = [20.4, 13.1, 12.5, 11.6, 9.4, 8.2, 8.0, 7.6, 6.1, 5.3];
    var W = 640, H = 420, x0 = 52, x1 = W - 10, y0 = 14, y1 = H - 78, s = svg(W, H, 'ch'), max = 22, n = v.length;
    var Y = function (x) { return y1 - (y1 - y0) * x / max; };
    [0, 5.5, 11, 16.5, 22].forEach(function (t) {
      el('text', { x: x0 - 10, y: Y(t) + 4, 'text-anchor': 'end' }, s, '₹' + t + 'L');
      el('line', { x1: x0, x2: x1, y1: Y(t), y2: Y(t), stroke: '#f0f0f3', 'stroke-dasharray': '3 4' }, s);
    });
    v.forEach(function (x, i) {
      var cx = x0 + (x1 - x0) * (i + .5) / n, cw = (x1 - x0) / n;
      var band = el('rect', { x: cx - cw / 2, y: y0, width: cw, height: y1 - y0, fill: '#f3f3f4', opacity: 0 }, s);
      el('rect', { x: cx - 13, y: Y(x), width: 26, height: y1 - Y(x), fill: C.aum }, s);
      var hit = el('rect', { x: cx - cw / 2, y: y0, width: cw, height: y1 - y0, fill: 'transparent' }, null);
      hit.addEventListener('mousemove', function (e) {
        band.setAttribute('opacity', 1);
        showTip('<div class="th">' + amc[i] + '</div>' + row('', 'AUM', '₹' + inr(x * 100000 + 2555.1079 + i * 913.37, 4)), e);
      });
      hit.addEventListener('mouseleave', function () { band.setAttribute('opacity', 0); hideTip(); });
      setTimeout(function () { s.appendChild(hit); });
      el('text', { x: cx + 6, y: y1 + 16, 'text-anchor': 'end', transform: 'rotate(-30 ' + (cx + 6) + ' ' + (y1 + 16) + ')' }, s, amc[i]);
    });
    $('aum').appendChild(s);
  })();

})();
