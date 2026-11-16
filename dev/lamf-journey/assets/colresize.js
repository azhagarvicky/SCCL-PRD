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

  // grips go on every header cell (all rows of <thead>, so grouped headings work too), or on the first row without a <thead>
  function gripCells(t) {
    var h = t.tHead, cells = [];
    if (h && h.rows.length) Array.prototype.forEach.call(h.rows, function (r) { cells = cells.concat(Array.prototype.slice.call(r.cells)); });
    else if (ownRows(t)[0]) cells = Array.prototype.slice.call(ownRows(t)[0].cells);
    return cells;
  }

  function setup(t) {
    if (t.__cr || t.classList.contains('no-resize') || t.closest('.info-pop')) return;
    var cells = gripCells(t);
    if (cells.length < 2) return;
    t.__cr = true;
    var right = t.getBoundingClientRect().right;
    cells.forEach(function (c) {
      if (!t.tHead && Math.abs(c.getBoundingClientRect().right - right) < 2) return;   // nothing to the right of the last cell
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
    // lay the cells on a grid (rowspan / colspan aware) and measure each column from a cell that spans only that column
    var rows = ownRows(t), grid = [], widths = [], edges = [], n = 0;
    rows.forEach(function (r, ri) {
      grid[ri] = grid[ri] || [];
      var ci = 0;
      Array.prototype.forEach.call(r.cells, function (c) {
        while (grid[ri][ci]) ci++;
        for (var a = 0; a < c.rowSpan; a++) {
          grid[ri + a] = grid[ri + a] || [];
          for (var b = 0; b < c.colSpan; b++) grid[ri + a][ci + b] = true;
        }
        if (c.colSpan === 1 && widths[ci] === undefined) {
          var bx = c.getBoundingClientRect();
          widths[ci] = bx.width; edges[ci] = bx.right;
        }
        ci += c.colSpan;
        if (ci > n) n = ci;
      });
    });
    var tb = t.getBoundingClientRect(), tw = tb.width, known = 0, missing = 0;
    for (var i = 0; i < n; i++) { if (widths[i] === undefined) missing++; else known += widths[i]; }
    var x = tb.left;
    for (i = 0; i < n; i++) {
      if (widths[i] === undefined) widths[i] = Math.max(40, (tw - known) / missing);
      x += widths[i];
      if (edges[i] === undefined) edges[i] = x;
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
    var x = t.getBoundingClientRect().left;                      // edges from the current widths (earlier drags move them)
    f.cols.forEach(function (col, i) { x += parseFloat(col.style.width); var d = Math.abs(x - right); if (d < best) { best = d; k = i; } });
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
