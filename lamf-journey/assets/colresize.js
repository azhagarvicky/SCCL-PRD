/* Column width drag for every table (DISC-293).
   Hover a header's right edge, drag to make the column wider or narrower; double-click the edge to reset the table.
   Works on mouse and touch, on every page and in cloud.html (tables added later are picked up automatically).
   Skips tables inside tooltips (.info-pop) and tables with class "no-resize". */
(function () {
  if (window.__colResize) return;
  window.__colResize = true;

  var css = '.col-grip{position:absolute;top:0;right:-4px;width:9px;height:100%;cursor:col-resize;z-index:4;touch-action:none}'
    + '.col-grip::after{content:"";position:absolute;top:15%;bottom:15%;left:4px;width:1px;background:transparent}'
    + 'th:hover>.col-grip::after,td:hover>.col-grip::after{background:rgba(37,99,235,.35)}'
    + '.col-grip:hover::after,.col-grip.on::after{background:#2563EB;width:3px;left:3px;top:0;bottom:0}'
    + 'table.col-fixed{table-layout:fixed}'
    + 'table.col-fixed th,table.col-fixed td{overflow-wrap:anywhere}'
    + '.col-wrap{overflow-x:auto;max-width:100%}'
    + 'body.col-dragging,body.col-dragging *{cursor:col-resize!important;user-select:none!important}';

  function addCss() {
    if (document.getElementById('col-resize-css')) return;
    var s = document.createElement('style');
    s.id = 'col-resize-css';
    s.textContent = css;
    (document.head || document.documentElement).appendChild(s);
  }

  function ownRows(t) {
    return Array.prototype.filter.call(t.rows, function (r) { return r.closest('table') === t; });
  }

  function gripRow(t) {
    var h = t.tHead;
    if (h && h.rows.length) return h.rows[h.rows.length - 1];
    return ownRows(t)[0];
  }

  function setup(t) {
    if (t.__cr || t.classList.contains('no-resize') || t.closest('.info-pop')) return;
    var r = gripRow(t);
    if (!r || r.cells.length < 2) return;
    t.__cr = true;
    Array.prototype.forEach.call(r.cells, function (c, i) {
      if (i === r.cells.length - 1 && !t.tHead) return;          // nothing to the right of the last cell
      var g = document.createElement('span');
      g.className = 'col-grip';
      g.title = 'Drag to change the column width (double-click to reset)';
      if (getComputedStyle(c).position === 'static') c.style.position = 'relative';
      c.appendChild(g);
    });
  }

  function scan(root) {
    addCss();
    (root || document).querySelectorAll('table').forEach(setup);
  }

  // Fix every column to its current width (colgroup + fixed layout), so one column can change without moving the others.
  function freeze(t) {
    if (t.__cols) return t.__cols;
    var rows = ownRows(t), n = 0, base = null;
    rows.forEach(function (r) {
      var s = 0;
      Array.prototype.forEach.call(r.cells, function (c) { s += c.colSpan; });
      if (s > n) n = s;
    });
    rows.some(function (r) {
      var plain = Array.prototype.every.call(r.cells, function (c) { return c.colSpan === 1 && c.rowSpan === 1; });
      if (plain && r.cells.length === n) { base = r; return true; }
      return false;
    });
    var tw = t.getBoundingClientRect().width, widths = [], edges = [];
    if (base) {
      Array.prototype.forEach.call(base.cells, function (c) {
        var b = c.getBoundingClientRect();
        widths.push(b.width); edges.push(b.right);
      });
    } else {
      var left = t.getBoundingClientRect().left;
      for (var i = 0; i < n; i++) { widths.push(tw / n); edges.push(left + tw / n * (i + 1)); }
    }
    Array.prototype.forEach.call(t.querySelectorAll(':scope > colgroup'), function (cg) { cg.remove(); });
    var cg = document.createElement('colgroup'), cols = [];
    widths.forEach(function (w) {
      var col = document.createElement('col');
      col.style.width = w + 'px';
      cg.appendChild(col); cols.push(col);
    });
    t.insertBefore(cg, t.firstChild);
    t.style.width = tw + 'px';
    t.style.minWidth = '0';
    t.style.maxWidth = 'none';
    t.classList.add('col-fixed');
    if (!scrolls(t.parentElement)) {                             // let a widened table scroll sideways instead of the page
      var w = document.createElement('div');
      w.className = 'col-wrap';
      t.parentNode.insertBefore(w, t);
      w.appendChild(t);
    }
    t.__cols = { cols: cols, widths: widths, edges: edges };
    return t.__cols;
  }

  function scrolls(el) {
    for (var e = el; e && e !== document.body; e = e.parentElement) {
      var o = getComputedStyle(e).overflowX;
      if (o === 'auto' || o === 'scroll') return true;
    }
    return false;
  }

  function reset(t) {
    Array.prototype.forEach.call(t.querySelectorAll(':scope > colgroup'), function (cg) { cg.remove(); });
    t.style.width = t.style.minWidth = t.style.maxWidth = '';
    t.classList.remove('col-fixed');
    t.__cols = null;
  }

  document.addEventListener('pointerdown', function (e) {
    var g = e.target.closest && e.target.closest('.col-grip');
    if (!g) return;
    e.preventDefault(); e.stopPropagation();
    var cell = g.parentElement, t = cell.closest('table');
    var right = cell.getBoundingClientRect().right;
    var f = freeze(t), k = 0, best = Infinity;
    f.edges.forEach(function (x, i) { var d = Math.abs(x - right); if (d < best) { best = d; k = i; } });
    var startX = e.clientX, startW = parseFloat(f.cols[k].style.width), startT = parseFloat(t.style.width);
    g.classList.add('on');
    document.body.classList.add('col-dragging');
    try { g.setPointerCapture(e.pointerId); } catch (err) { /* older browsers */ }
    function move(ev) {
      var w = Math.max(40, startW + ev.clientX - startX);
      f.cols[k].style.width = w + 'px';
      t.style.width = (startT + w - startW) + 'px';
    }
    function up() {
      g.classList.remove('on');
      document.body.classList.remove('col-dragging');
      g.removeEventListener('pointermove', move);
      g.removeEventListener('pointerup', up);
      g.removeEventListener('pointercancel', up);
    }
    g.addEventListener('pointermove', move);
    g.addEventListener('pointerup', up);
    g.addEventListener('pointercancel', up);
  }, true);

  // a drag must not also open a <details>, sort a column or follow a link in the header
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.col-grip')) { e.preventDefault(); e.stopPropagation(); }
  }, true);

  document.addEventListener('dblclick', function (e) {
    var g = e.target.closest && e.target.closest('.col-grip');
    if (!g) return;
    e.preventDefault(); e.stopPropagation();
    reset(g.closest('table'));
  }, true);

  var queued = false;
  function later() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; scan(); });
  }

  function start() {
    scan();
    new MutationObserver(later).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
