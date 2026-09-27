/* Review comments (DISC-026, DISC-028).
   Anyone reviewing the prototype or the PRD can select text → "Comment" → enter their name and
   comment → Save. General comments (not about a piece of text) are added from the Comments
   button, for this page or for all pages. Comments are stored in the project Google Sheet
   through a Google Apps Script web app (tools/comments-apps-script.gs); no sign-in is needed.
   Open / Closed status comes from comment-status.json, maintained by Claude. */
(function () {
  const ENDPOINT = '';   // Google Apps Script web app URL (…/exec). Empty = not connected yet.
  if (window.LAMF_SPA) return;   // not in the single-page cloud copy

  /* ---------- helpers ---------- */
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const pageName = () => {
    const f = decodeURIComponent(location.pathname.split('/').pop() || '').replace(/\.html$/, '');
    if (!f || f === 'index') return 'Home';
    if (f === 'screens') return 'All screens';
    if (f === 'SCCL_LAMF_LOS_PRD') return 'PRD';
    return f;
  };
  const PAGE = pageName(), ALL = 'All pages';
  const SITE = /\/dev\//.test(location.pathname) ? 'Development'
    : ['localhost', '127.0.0.1'].includes(location.hostname) ? 'Local' : 'Production';
  const store = (s) => ({ get(k) { try { return JSON.parse(s.getItem(k)); } catch (e) { return null; } },
                          set(k, v) { try { s.setItem(k, JSON.stringify(v)); } catch (e) {} } });
  const ss = store(window.sessionStorage), ls = store(window.localStorage);

  /* ---------- styles ---------- */
  const css = `
  #rv-root { font: 13px/1.45 system-ui, -apple-system, 'Segoe UI', sans-serif; color: #1d1d1f; }
  #rv-root * { box-sizing: border-box; }
  #rv-root button { font: inherit; cursor: pointer; }
  .rv-launch { position: fixed; left: 14px; bottom: 14px; z-index: 1001; background: #1d1d1f; color: #fff; border: 0; border-radius: 20px; padding: 8px 14px; box-shadow: 0 4px 14px rgba(0,0,0,.25); font-weight: 600; }
  .rv-launch b { background: #F79009; color: #1d1d1f; border-radius: 10px; padding: 0 7px; margin-left: 6px; }
  .rv-sel { position: fixed; z-index: 1003; background: #FFCB08; color: #1d1d1f; border: 0; border-radius: 16px; padding: 6px 12px; font-weight: 700; box-shadow: 0 4px 14px rgba(0,0,0,.25); display: none; }
  .rv-drawer { position: fixed; top: 0; right: 0; bottom: 0; width: min(430px, 100vw); z-index: 1002; background: #fff; box-shadow: -8px 0 30px rgba(0,0,0,.18); display: none; flex-direction: column; }
  .rv-open .rv-drawer { display: flex; }
  .rv-head { padding: 14px 16px 10px; border-bottom: 1px solid #eee; }
  .rv-head h3 { margin: 0 0 2px; font-size: 16px; }
  .rv-head p { margin: 0; color: #666; font-size: 12px; }
  .rv-bar { display: flex; gap: 6px; padding: 10px 16px; border-bottom: 1px solid #eee; flex-wrap: wrap; align-items: center; }
  .rv-bar button { border: 1px solid #ddd; background: #fff; border-radius: 14px; padding: 4px 10px; }
  .rv-bar button.on { background: #1d1d1f; color: #fff; border-color: #1d1d1f; }
  .rv-bar .rv-new { margin-left: auto; background: #FFCB08; border-color: #FFCB08; font-weight: 700; }
  .rv-x { position: absolute; top: 10px; right: 12px; border: 0; background: none; font-size: 22px; line-height: 1; color: #666; }
  .rv-list { overflow: auto; padding: 10px 16px 30px; flex: 1; }
  .rv-sec { margin: 8px 0 6px; font-weight: 700; font-size: 13px; display: flex; align-items: center; gap: 8px; }
  .rv-sec .n { border-radius: 10px; padding: 0 8px; font-size: 12px; }
  .rv-sec.open .n { background: #FEF0C7; color: #B54708; }
  .rv-sec.closed .n { background: #D1FADF; color: #027A48; }
  details.rv-closed > summary { cursor: pointer; list-style: none; }
  details.rv-closed > summary::-webkit-details-marker { display: none; }
  details.rv-closed > summary .rv-sec::after { content: '▸'; color: #888; }
  details.rv-closed[open] > summary .rv-sec::after { content: '▾'; }
  .rv-item { border: 1px solid #eee; border-left: 4px solid #F79009; border-radius: 8px; padding: 10px 12px; margin-bottom: 10px; }
  .rv-item.closed { border-left-color: #12B76A; background: #FAFAFA; }
  .rv-item.flash { box-shadow: 0 0 0 3px #FFCB08; }
  .rv-meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; font-size: 11.5px; color: #666; }
  .rv-tag { border-radius: 10px; padding: 1px 8px; font-weight: 700; font-size: 11px; }
  .rv-tag.open { background: #FEF0C7; color: #B54708; }
  .rv-tag.closed { background: #D1FADF; color: #027A48; }
  .rv-q { margin: 6px 0; padding: 4px 8px; border-left: 3px solid #FFCB08; background: #FFFBEA; font-style: italic; white-space: pre-wrap; word-break: break-word; }
  .rv-c { white-space: pre-wrap; word-break: break-word; margin: 4px 0; }
  .rv-by { font-size: 11.5px; color: #555; margin-top: 4px; }
  .rv-res { margin-top: 6px; padding: 6px 8px; background: #ECFDF3; border-radius: 6px; white-space: pre-wrap; word-break: break-word; font-size: 12px; }
  .rv-empty, .rv-err { color: #777; padding: 8px 0; }
  .rv-err { color: #B42318; }
  .rv-modal { position: fixed; inset: 0; z-index: 1004; background: rgba(0,0,0,.4); display: none; align-items: center; justify-content: center; padding: 16px; }
  .rv-modal.show { display: flex; }
  .rv-card { background: #fff; border-radius: 12px; width: min(460px, 100%); padding: 18px; box-shadow: 0 10px 40px rgba(0,0,0,.3); }
  .rv-card h4 { margin: 0 0 10px; font-size: 16px; }
  .rv-card label { display: block; font-size: 12px; font-weight: 600; margin: 10px 0 4px; }
  .rv-card input[type=text], .rv-card textarea { width: 100%; border: 1px solid #ccc; border-radius: 8px; padding: 8px; font: inherit; }
  .rv-card textarea { min-height: 100px; resize: vertical; }
  .rv-card .scope { display: flex; gap: 16px; font-size: 13px; }
  .rv-card .scope label { display: inline-flex; gap: 6px; align-items: center; font-weight: 400; margin: 0; }
  .rv-card .row { display: flex; justify-content: flex-end; gap: 8px; margin-top: 14px; }
  .rv-card .row button { border-radius: 8px; padding: 8px 16px; border: 1px solid #ddd; background: #fff; }
  .rv-card .row .go { background: #FFCB08; border-color: #FFCB08; font-weight: 700; }
  .rv-card .row .go:disabled { opacity: .5; cursor: default; }
  .rv-card .msg { font-size: 12px; margin-top: 8px; color: #B42318; min-height: 1em; }
  .rv-hp { position: absolute; left: -9999px; }
  mark.rv-mark { background: #FFF1A8; border-bottom: 2px solid #F79009; color: inherit; cursor: pointer; padding: 0; }
  .rv-toast { position: fixed; left: 50%; bottom: 64px; transform: translateX(-50%); z-index: 1005; background: #1d1d1f; color: #fff; padding: 8px 16px; border-radius: 18px; display: none; }`;

  /* ---------- UI ---------- */
  const root = document.createElement('div');
  root.id = 'rv-root';
  root.innerHTML = `<style>${css}</style>
    <button class="rv-launch" title="Review comments">💬 Comments <b class="rv-count">…</b></button>
    <button class="rv-sel">💬 Comment</button>
    <div class="rv-toast"></div>
    <aside class="rv-drawer">
      <button class="rv-x" title="Close">×</button>
      <div class="rv-head"><h3>Review comments</h3><p>Select any text on the page to comment on it, or use “+ New comment”.</p></div>
      <div class="rv-bar">
        <button data-scope="page" class="on">This page</button><button data-scope="all">All pages</button>
        <button class="rv-refresh" title="Reload">↻</button>
        <button class="rv-xls" title="Download all comments as an Excel file">⬇ Excel</button>
        <button class="rv-new">+ New comment</button>
      </div>
      <div class="rv-list"></div>
    </aside>
    <div class="rv-modal"><form class="rv-card" autocomplete="off">
      <h4>Add a comment</h4>
      <div class="rv-q" hidden></div>
      <div class="scope-wrap"><label>Applies to</label><div class="scope">
        <label><input type="radio" name="rv-scope" value="page" checked> This page</label>
        <label><input type="radio" name="rv-scope" value="all"> All pages</label></div></div>
      <label for="rv-name">Your name</label><input type="text" id="rv-name" maxlength="80" required>
      <label for="rv-text">Comment</label><textarea id="rv-text" maxlength="3000" placeholder="What should be changed?" required></textarea>
      <input type="text" class="rv-hp" name="website" tabindex="-1" aria-hidden="true">
      <div class="msg"></div>
      <div class="row"><button type="button" class="cancel">Cancel</button><button type="submit" class="go" disabled>Save</button></div>
    </form></div>`;
  const $ = (s) => root.querySelector(s);
  const attach = () => { if (!document.body.contains(root)) document.body.appendChild(root); };
  attach();

  let scope = 'page', items = [], pendingQuote = '';
  const onPage = (it) => it.page === PAGE || it.page === ALL;
  const isOpen = (it) => !/^closed/i.test(it.status);
  function toast(t) { const el = $('.rv-toast'); el.textContent = t; el.style.display = 'block'; setTimeout(() => { el.style.display = 'none'; }, 2600); }

  /* ---------- load ---------- */
  async function load(force) {
    if (!ENDPOINT) { $('.rv-count').textContent = 'off'; $('.rv-list').innerHTML = '<div class="rv-err">Comments are not connected yet.</div>'; return; }
    const cached = !force && ss.get('rv-cache');
    if (cached && Date.now() - cached.t < 30000) { items = cached.items; return draw(); }
    if (root.classList.contains('rv-open')) $('.rv-list').innerHTML = '<div class="rv-empty">Loading…</div>';
    try {
      const r = await fetch(ENDPOINT);
      const data = await r.json();
      if (!data.ok) throw new Error(data.error || 'error');
      items = data.rows.reverse();                       // newest first
      ss.set('rv-cache', { t: Date.now(), items });
      draw();
    } catch (e) {
      $('.rv-count').textContent = '!';
      $('.rv-list').innerHTML = `<div class="rv-err">Could not load comments. Check the connection and press ↻.</div>`;
    }
  }

  function card(it) {
    const open = isOpen(it);
    return `<div class="rv-item ${open ? '' : 'closed'}" data-id="${esc(it.id)}">
      <div class="rv-meta"><span class="rv-tag ${open ? 'open' : 'closed'}">${open ? 'Open' : esc(it.status)}</span><span>${esc(it.id)}</span>
        ${scope === 'all' || it.page === ALL ? `<span>· ${esc(it.page)}</span>` : ''}</div>
      ${it.quote ? `<div class="rv-q">“${esc(it.quote)}”</div>` : ''}
      <div class="rv-c">${esc(it.comment)}</div>
      <div class="rv-by">— ${esc(it.name)} · ${esc(it.created)}${it.closed ? ` · Closed ${esc(it.closed)}` : ''}</div>
      ${!open && it.note ? `<div class="rv-res"><b>What was done:</b> ${esc(it.note)}</div>` : ''}
    </div>`;
  }
  function draw() {
    const mine = items.filter((it) => scope === 'all' || onPage(it));
    const open = mine.filter(isOpen), closed = mine.filter((it) => !isOpen(it));
    $('.rv-count').textContent = items.filter((it) => isOpen(it) && onPage(it)).length + ' open';
    $('.rv-list').innerHTML =
      `<div class="rv-sec open">Open comments <span class="n">${open.length}</span></div>` +
      (open.length ? open.map(card).join('') : '<div class="rv-empty">No open comments.</div>') +
      `<details class="rv-closed"><summary><div class="rv-sec closed">Closed comments <span class="n">${closed.length}</span></div></summary>` +
      (closed.length ? closed.map(card).join('') : '<div class="rv-empty">None yet.</div>') + '</details>';
    mark();
  }

  /* ---------- highlight commented text on this page ---------- */
  function mark() {
    items.filter((it) => isOpen(it) && it.page === PAGE && it.quote).forEach((it) => {
      if (document.querySelector(`mark.rv-mark[data-id="${CSS.escape(it.id)}"]`)) return;
      const q = it.quote.split('\n')[0].trim().slice(0, 120);
      if (q.length < 2) return;
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
        acceptNode: (n) => (n.parentElement.closest('#rv-root, script, style, textarea, mark.rv-mark') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) });
      let n;
      while ((n = w.nextNode())) {
        const k = n.nodeValue.indexOf(q);
        if (k < 0) continue;
        const hit = n.splitText(k); hit.splitText(q.length);
        const m = document.createElement('mark');
        m.className = 'rv-mark'; m.dataset.id = it.id; m.title = 'Open comment ' + it.id;
        hit.parentNode.replaceChild(m, hit); m.appendChild(hit);
        break;
      }
    });
  }
  document.addEventListener('click', (e) => {
    const m = e.target.closest && e.target.closest('mark.rv-mark'); if (!m) return;
    e.preventDefault(); e.stopPropagation();
    scope = 'page'; root.querySelectorAll('[data-scope]').forEach((x) => x.classList.toggle('on', x.dataset.scope === 'page'));
    openDrawer(); draw();
    const el = root.querySelector(`.rv-item[data-id="${CSS.escape(m.dataset.id)}"]`);
    if (el) { el.scrollIntoView({ block: 'center' }); el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1500); }
  }, true);

  /* ---------- drawer ---------- */
  function openDrawer() { root.classList.add('rv-open'); if (!items.length) load(); }
  $('.rv-launch').onclick = () => root.classList.contains('rv-open') ? root.classList.remove('rv-open') : openDrawer();
  $('.rv-x').onclick = () => root.classList.remove('rv-open');
  $('.rv-refresh').onclick = () => load(true);
  root.querySelectorAll('[data-scope]').forEach((b) => b.onclick = () => {
    scope = b.dataset.scope;
    root.querySelectorAll('[data-scope]').forEach((x) => x.classList.toggle('on', x === b));
    draw();
  });
  $('.rv-new').onclick = () => compose('');

  /* ---------- Excel download (all comments, Open and Closed sheets) ---------- */
  $('.rv-xls').onclick = async () => {
    if (!items.length) { toast('No comments to download yet'); return; }
    try {
      if (!window.XLSX) await new Promise((ok, bad) => {
        const s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
        s.onload = ok; s.onerror = bad; document.head.appendChild(s);
      });
      const rows = (list) => list.map((it) => ({ ID: it.id, 'Created on': it.created, Site: it.site, Page: it.page, 'Selected text': it.quote,
        Comment: it.comment, Name: it.name, Status: isOpen(it) ? 'Open' : it.status, 'Closed on': it.closed, 'What was done': it.note }));
      const wb = XLSX.utils.book_new();
      const add = (name, list) => { const ws = XLSX.utils.json_to_sheet(rows(list)); ws['!cols'] = [8, 16, 12, 28, 40, 60, 18, 10, 16, 50].map((w) => ({ wch: w })); XLSX.utils.book_append_sheet(wb, ws, name); };
      add('Open', items.filter(isOpen)); add('Closed', items.filter((it) => !isOpen(it))); add('All', items);
      const d = new Date(), p = (n) => String(n).padStart(2, '0');
      XLSX.writeFile(wb, `LAMF review comments ${p(d.getDate())}-${p(d.getMonth() + 1)}-${d.getFullYear()}.xlsx`);
    } catch (e) { toast('Excel download failed – check the connection'); }
  };

  /* ---------- select text → comment ---------- */
  const selBtn = $('.rv-sel');
  let selTimer;
  document.addEventListener('selectionchange', () => {
    clearTimeout(selTimer);
    selTimer = setTimeout(() => {
      const s = window.getSelection();
      const text = s && s.rangeCount ? s.toString().trim() : '';
      if (!text || root.contains(s.anchorNode)) { selBtn.style.display = 'none'; return; }
      const r = s.getRangeAt(0).getBoundingClientRect();
      pendingQuote = text.slice(0, 1000);
      selBtn.style.display = 'block';
      selBtn.style.top = Math.min(window.innerHeight - 44, r.bottom + 8) + 'px';
      selBtn.style.left = Math.max(8, Math.min(window.innerWidth - 120, r.left)) + 'px';
    }, 200);
  });
  selBtn.addEventListener('mousedown', (e) => e.preventDefault());   // keep the selection
  selBtn.onclick = () => { selBtn.style.display = 'none'; compose(pendingQuote); };

  const modal = $('.rv-modal'), form = modal.querySelector('form'), nameIn = $('#rv-name'), ta = $('#rv-text'), go = modal.querySelector('.go'), msg = modal.querySelector('.msg');
  const ready = () => { go.disabled = !(nameIn.value.trim() && ta.value.trim()); };
  function compose(quote) {
    pendingQuote = quote;
    const qb = modal.querySelector('.rv-q');
    qb.hidden = !quote; qb.textContent = quote ? '“' + quote + '”' : '';
    modal.querySelector('.scope-wrap').hidden = !!quote;          // text comments always belong to this page
    form.querySelector('input[value="page"]').checked = true;
    nameIn.value = ls.get('rv-name') || ''; ta.value = ''; msg.textContent = ''; ready();
    modal.classList.add('show'); setTimeout(() => (nameIn.value ? ta : nameIn).focus(), 50);
  }
  nameIn.oninput = ready; ta.oninput = ready;
  const close = () => modal.classList.remove('show');
  modal.querySelector('.cancel').onclick = close;
  modal.addEventListener('click', (e) => { if (e.target === modal) close(); });
  form.onsubmit = async (e) => {
    e.preventDefault();
    if (!ENDPOINT) { msg.textContent = 'Comments are not connected yet.'; return; }
    const name = nameIn.value.trim(), comment = ta.value.trim();
    const page = form.querySelector('input[name="rv-scope"]:checked').value === 'all' && !pendingQuote ? ALL : PAGE;
    ls.set('rv-name', name);
    go.disabled = true; go.textContent = 'Saving…'; msg.textContent = '';
    try {
      // text/plain keeps this a "simple" request, which Apps Script web apps accept from any site
      const r = await fetch(ENDPOINT, { method: 'POST', body: JSON.stringify({ name, comment, page, quote: pendingQuote, site: SITE,
        link: location.href.split('#')[0], website: form.website.value }) });
      const d = await r.json();
      if (!d.ok) throw new Error(d.error || 'error');
      close(); toast('Comment saved' + (d.id ? ' · ' + d.id : ''));
      await load(true); openDrawer();
    } catch (err) {
      msg.textContent = 'Could not save – please try again.';
    } finally { go.textContent = 'Save'; ready(); }
  };

  /* The prototype re-renders <body> when a screen changes; put the panel back and re-highlight. */
  let moTimer;
  new MutationObserver(() => { clearTimeout(moTimer); moTimer = setTimeout(() => { attach(); mark(); }, 150); })
    .observe(document.body, { childList: true });

  load();
})();
