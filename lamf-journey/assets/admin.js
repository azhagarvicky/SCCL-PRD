/* LAMF site access – admin portal (DISC-477). Needs assets/gate.js (login) and the Apps Script in tools/access-apps-script.gs. */
(function () {
  var G = window.LAMF_GATE, M = document.getElementById('adm-main'), users = [], filter = 'Pending', token = '', q = '';
  if (!G) return;
  document.getElementById('adm-out').onclick = function () { G.logout(); };
  G.onAdmin = function (t, me) { token = t; document.getElementById('adm-who').textContent = me.mail; load(); };
  function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function load() {
    M.innerHTML = '<p class="msg">Loading users…</p>';
    G.call({ action: 'list', token: token }).then(function (r) {
      if (!r.ok) { M.innerHTML = '<p class="msg">' + esc(r.error) + '</p>'; return; }
      users = r.users; draw();
    }).catch(function () { M.innerHTML = '<p class="msg">Could not load the users. <a href="">Try again</a></p>'; });
  }
  function draw() {
    var st = ['Pending', 'Approved', 'Rejected', 'Removed', 'All'];
    var cnt = function (s) { return s === 'All' ? users.length : users.filter(function (u) { return u.status === s; }).length; };
    var rows = users.filter(function (u) {
      return (filter === 'All' || u.status === filter) && (!q || (u.mail + ' ' + u.name).toLowerCase().indexOf(q) >= 0);
    });
    M.innerHTML = '<div class="cards">' + st.map(function (s) {
      return '<div class="card' + (s === filter ? ' on' : '') + '" data-f="' + s + '"><b>' + cnt(s) + '</b><span>' + s + '</span></div>';
    }).join('') + '</div><input class="q" placeholder="Search name or mail ID" value="' + esc(q) + '">' +
      '<div class="wrap"><table><thead><tr><th>Name</th><th>Mail ID</th><th>Requested on</th><th>Status</th><th>Approved / changed by</th>' +
      '<th>On</th><th>Last login</th><th>Action</th></tr></thead><tbody>' +
      (rows.length ? rows.map(function (u) {
        var a = u.name === 'Admin' && u.by === 'Setup' ? '' :
          (u.status !== 'Approved' ? '<button type="button" class="ap" data-s="Approved">Approve</button>' : '') +
          (u.status === 'Pending' ? '<button type="button" class="rj" data-s="Rejected">Reject</button>' : '') +
          (u.status === 'Approved' ? '<button type="button" class="rj" data-s="Removed">Remove</button>' : '');
        return '<tr data-m="' + esc(u.mail) + '"><td>' + esc(u.name) + '</td><td>' + esc(u.mail) + '</td><td>' + esc(u.requested) + '</td>' +
          '<td><span class="st st-' + esc(u.status) + '">' + esc(u.status) + '</span></td><td>' + esc(u.by) + '</td><td>' + esc(u.on) +
          '</td><td>' + esc(u.last) + '</td><td class="act">' + a + '</td></tr>';
      }).join('') : '<tr><td colspan="8">No users here.</td></tr>') + '</tbody></table></div>' +
      '<p class="msg">Approve and Reject send a mail to the user. Remove takes the access back at once (the user can ask again).</p>';
    M.querySelectorAll('.card').forEach(function (c) { c.onclick = function () { filter = c.dataset.f; draw(); }; });
    var qi = M.querySelector('.q'); qi.oninput = function () { q = qi.value.trim().toLowerCase(); draw(); var n = M.querySelector('.q'); n.focus(); n.setSelectionRange(n.value.length, n.value.length); };
    M.querySelectorAll('td button').forEach(function (b) {
      b.onclick = function () {
        var m = b.closest('tr').dataset.m, s = b.dataset.s;
        var verb = { Approved: 'approve', Rejected: 'reject', Removed: 'remove the access of' }[s];
        if (!confirm('Are you sure you want to ' + verb + ' ' + m + '?')) return;
        b.disabled = true;
        G.call({ action: 'set', token: token, mail: m, status: s }).then(function (r) {
          if (!r.ok) { alert(r.error); b.disabled = false; return; }
          load();
        }).catch(function () { alert('Could not save. Please try again.'); b.disabled = false; });
      };
    });
  }
})();
