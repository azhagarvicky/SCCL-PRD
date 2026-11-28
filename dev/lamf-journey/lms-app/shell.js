/* LMS prototype – app shell shared by every screen after login (DISC-499, DISC-503): profile pop-up, expand / collapse menu,
   and links to screens not built yet → wip.html (Work in progress). Source file. */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  // every menu item / link not built yet opens the common Work in progress page, with the item highlighted
  [].forEach.call(document.querySelectorAll('[data-todo]'), function (a) {
    a.setAttribute('href', 'wip.html?p=' + encodeURIComponent(a.getAttribute('data-todo')));
  });
  var cur = new URLSearchParams(location.search).get('p');
  if (cur) [].forEach.call(document.querySelectorAll('.sb-i, .sb-s'), function (a) {
    a.classList.toggle('on', a.getAttribute('data-todo') === cur);
  });
  // ---- profile pop-up and expand / collapse menu (DISC-499)
  var app = document.body, sb = $('sb'), av = $('sb-av'), pf = $('pf'), sx = $('sb-x');
  try { var who = sessionStorage.getItem('lms-user'); if (who) $('pf-m').textContent = who; } catch (e) {}
  function openPf(on) { pf.hidden = !on; av.setAttribute('aria-expanded', on ? 'true' : 'false'); }
  av.addEventListener('click', function (e) { e.stopPropagation(); openPf(pf.hidden); });
  document.addEventListener('click', function (e) { if (!pf.hidden && !pf.contains(e.target)) openPf(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') openPf(false); });
  $('pf-out').addEventListener('click', function () {   // logout → back to the LMS login page (the LMS lock stays)
    try { sessionStorage.removeItem('lms-user'); } catch (e) {}
    location.href = 'login.html';
  });
  var longs = [].slice.call(document.querySelectorAll('[data-long]'));
  function wide(on) {
    sb.classList.toggle('wide', on); app.classList.toggle('wide', on);
    sx.setAttribute('aria-label', on ? 'Collapse menu' : 'Expand menu');
    longs.forEach(function (x) { if (!x.dataset.short) x.dataset.short = x.textContent; x.textContent = on ? x.dataset.long : x.dataset.short; });
    try { sessionStorage.setItem('lms-menu-wide', on ? '1' : ''); } catch (e) {}
  }
  sx.addEventListener('click', function () { wide(!sb.classList.contains('wide')); });
  try { if (sessionStorage.getItem('lms-menu-wide')) wide(true); } catch (e) {}

})();
