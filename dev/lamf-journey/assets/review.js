/* Review comments (DISC-026).
   Select any text on a page → "Comment" → the comment is saved as a GitHub issue in the
   project repository, so it is visible on every device and to Claude. The Comments panel
   lists Open and Closed comments with their dates. Same on dev and production (DISC-027). */
(function () {
  const REPO = 'azhagarvicky/SCCL-PRD';
  const PREFIX = '[Dev comment]';
  const OWNER = 'azhagarvicky';   // only the project owner's comments count (the repository is public)
  if (window.LAMF_SPA) return;   // not in the single-page cloud copy

  /* ---------- helpers ---------- */
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (iso) => { if (!iso) return ''; const d = new Date(iso); return `${pad(d.getDate())}-${pad(d.getMonth() + 1)}-${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`; };
  const pageName = () => {
    const f = decodeURIComponent(location.pathname.split('/').pop() || '').replace(/\.html$/, '');
    if (!f || f === 'index') return 'Home';
    if (f === 'screens') return 'All screens';
    if (f === 'SCCL_LAMF_LOS_PRD') return 'PRD';
    return f;
  };
  const PAGE = pageName();
  const SITE = /\/dev\//.test(location.pathname) ? 'Development' : ['localhost', '127.0.0.1'].includes(location.hostname) ? 'Local' : 'Production';
  const ss = { get(k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } },
               set(k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };

  /* ---------- styles ---------- */
  const css = `
  #rv-root { font: 13px/1.45 system-ui, -apple-system, 'Segoe UI', sans-serif; color: #1d1d1f; }
  #rv-root * { box-sizing: border-box; }
  #rv-root button { font: inherit; cursor: pointer; }
  .rv-launch { position: fixed; left: 14px; bottom: 14px; z-index: 1001; background: #1d1d1f; color: #fff; border: 0; border-radius: 20px; padding: 8px 14px; box-shadow: 0 4px 14px rgba(0,0,0,.25); font-weight: 600; }
  .rv-launch b { background: #F79009; color: #1d1d1f; border-radius: 10px; padding: 0 7px; margin-left: 6px; }
  .rv-sel { position: fixed; z-index: 1003; background: #FFCB08; color: #1d1d1f; border: 0; border-radius: 16px; padding: 6px 12px; font-weight: 700; box-shadow: 0 4px 14px rgba(0,0,0,.25); display: none; }
  .rv-drawer { position: fixed; top: 0; right: 0; bottom: 0; width: min(420px, 100vw); z-index: 1002; background: #fff; box-shadow: -8px 0 30px rgba(0,0,0,.18); display: none; flex-direction: column; }
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
  .rv-dates { font-size: 11.5px; color: #555; margin-top: 4px; }
  .rv-item a { color: #175CD3; }
  .rv-res { margin-top: 6px; padding: 6px 8px; background: #F2F4F7; border-radius: 6px; white-space: pre-wrap; word-break: break-word; font-size: 12px; }
  .rv-lnk { border: 0; background: none; color: #175CD3; padding: 0; font-size: 12px; }
  .rv-empty, .rv-err { color: #777; padding: 8px 0; }
  .rv-err { color: #B42318; }
  .rv-modal { position: fixed; inset: 0; z-index: 1004; background: rgba(0,0,0,.4); display: none; align-items: center; justify-content: center; padding: 16px; }
  .rv-modal.show { display: flex; }
  .rv-card { background: #fff; border-radius: 12px; width: min(460px, 100%); padding: 18px; box-shadow: 0 10px 40px rgba(0,0,0,.3); }
  .rv-card h4 { margin: 0 0 4px; font-size: 16px; }
  .rv-card .pg { color: #666; font-size: 12px; margin-bottom: 8px; }
  .rv-card textarea { width: 100%; min-height: 110px; border: 1px solid #ccc; border-radius: 8px; padding: 8px; font: inherit; resize: vertical; }
  .rv-card .row { display: flex; justify-content: flex-end; gap: 8px; margin-top: 12px; }
  .rv-card .row button { border-radius: 8px; padding: 8px 14px; border: 1px solid #ddd; background: #fff; }
  .rv-card .row .go { background: #FFCB08; border-color: #FFCB08; font-weight: 700; }
  .rv-card .row .go:disabled { opacity: .5; cursor: default; }
  .rv-card .hint { font-size: 12px; color: #666; margin-top: 10px; }
  mark.rv-mark { background: #FFF1A8; border-bottom: 2px solid #F79009; color: inherit; cursor: pointer; padding: 0; }`;

  /* ---------- UI ---------- */
  const root = document.createElement('div');
  root.id = 'rv-root';
  root.innerHTML = `<style>${css}</style>
    <button class="rv-launch" title="Review comments (dev only)">💬 Comments <b class="rv-count">…</b></button>
    <button class="rv-sel">💬 Comment</button>
    <aside class="rv-drawer">
      <button class="rv-x" title="Close">×</button>
      <div class="rv-head"><h3>Review comments</h3><p>Stored as GitHub issues · visible on every device</p></div>
      <div class="rv-bar">
        <button data-scope="page" class="on">This page</button><button data-scope="all">All pages</button>
        <button class="rv-refresh" title="Reload from GitHub">↻</button>
        <button class="rv-new">+ New</button>
      </div>
      <div class="rv-list"></div>
    </aside>
    <div class="rv-modal"><div class="rv-card">
      <h4>Add a comment</h4><div class="pg"></div>
      <div class="rv-q" hidden></div>
      <textarea placeholder="What should be changed?"></textarea>
      <div class="row"><button class="cancel">Cancel</button><button class="go" disabled>Post on GitHub ↗</button></div>
      <div class="hint">GitHub opens in a new tab with the comment filled in — press <b>Create</b> there to save it. It then shows here as <b>Open</b>, and is marked <b>Closed</b> with the date once it has been done.</div>
    </div></div>`;
  const $ = (s) => root.querySelector(s);
  const attach = () => { if (!document.body.contains(root)) document.body.appendChild(root); };
  attach();

  let scope = 'page', items = [], pendingQuote = '';

  /* ---------- load comments from GitHub ---------- */
  function parse(i) {
    const m = (i.body || '').match(/<!-- rv:([^\s]+) -->/);
    let meta = {};
    if (m) { try { meta = JSON.parse(decodeURIComponent(m[1])); } catch (e) {} }
    const c = (i.body || '').split('**Comment:**')[1];
    const comment = c ? c.split('<!-- rv:')[0].trim() : (i.body || '').trim();
    return { num: i.number, url: i.html_url, open: i.state === 'open', reason: i.state_reason,
             page: meta.page || (i.title.replace(PREFIX, '').split(' — ')[0].trim()),
             quote: meta.quote || '', comment, created: i.created_at, closed: i.closed_at, comments_url: i.comments_url };
  }
  async function load(force) {
    const cached = !force && ss.get('rv-cache');
    if (cached && Date.now() - cached.t < 60000) { items = cached.items; return draw(); }
    $('.rv-list').innerHTML = '<div class="rv-empty">Loading…</div>';
    try {
      const r = await fetch(`https://api.github.com/repos/${REPO}/issues?state=all&per_page=100&sort=created&direction=desc`, { headers: { Accept: 'application/vnd.github+json' } });
      if (!r.ok) throw new Error(r.status === 403 ? 'GitHub rate limit reached — try again in a few minutes.' : 'GitHub returned ' + r.status);
      const data = await r.json();
      items = data.filter((i) => !i.pull_request && i.title.startsWith(PREFIX) && i.user && i.user.login === OWNER).map(parse);
      ss.set('rv-cache', { t: Date.now(), items });
      draw();
    } catch (e) {
      $('.rv-count').textContent = '!';
      $('.rv-list').innerHTML = `<div class="rv-err">Could not load comments: ${esc(e.message)}</div>`;
    }
  }

  function card(it) {
    const dates = `Opened ${fmt(it.created)}${it.closed ? ` · Closed ${fmt(it.closed)}` : ''}`;
    const status = it.open ? 'Open' : (it.reason === 'not_planned' ? 'Closed – not done' : 'Closed');
    return `<div class="rv-item ${it.open ? '' : 'closed'}" data-num="${it.num}">
      <div class="rv-meta"><span class="rv-tag ${it.open ? 'open' : 'closed'}">${status}</span><span>#${it.num}</span>${scope === 'all' ? `<span>· ${esc(it.page)}</span>` : ''}</div>
      ${it.quote ? `<div class="rv-q">“${esc(it.quote)}”</div>` : ''}
      <div class="rv-c">${esc(it.comment)}</div>
      <div class="rv-dates">${dates}</div>
      <div class="rv-meta" style="margin-top:4px">${it.open ? '' : `<button class="rv-lnk rv-show" data-num="${it.num}">What was done</button> ·`}<a href="${esc(it.url)}" target="_blank" rel="noopener">View on GitHub ↗</a></div>
      <div class="rv-res" hidden></div>
    </div>`;
  }
  function draw() {
    const mine = items.filter((it) => scope === 'all' || it.page === PAGE);
    const open = mine.filter((it) => it.open), closed = mine.filter((it) => !it.open);
    const openHere = items.filter((it) => it.open && it.page === PAGE).length;
    $('.rv-count').textContent = openHere + ' open';
    $('.rv-list').innerHTML =
      `<div class="rv-sec open">Open comments <span class="n">${open.length}</span></div>` +
      (open.length ? open.map(card).join('') : '<div class="rv-empty">No open comments. Select any text on the page to add one.</div>') +
      `<details class="rv-closed"><summary><div class="rv-sec closed">Closed comments <span class="n">${closed.length}</span></div></summary>` +
      (closed.length ? closed.map(card).join('') : '<div class="rv-empty">None yet.</div>') + '</details>';
    mark();
  }

  /* Closed item → show the last GitHub reply (what was changed) */
  $('.rv-list').addEventListener('click', async (e) => {
    const b = e.target.closest('.rv-show'); if (!b) return;
    const it = items.find((x) => x.num == b.dataset.num), box = b.closest('.rv-item').querySelector('.rv-res');
    box.hidden = false; box.textContent = 'Loading…';
    try {
      const r = await fetch(it.comments_url); const cs = await r.json();
      box.textContent = cs.length ? cs[cs.length - 1].body.replace(/\n---\n_Generated by[\s\S]*$/, '').trim() : 'No note was added.';
    } catch (err) { box.textContent = 'Could not load.'; }
  });

  /* ---------- highlight open comments on this page ---------- */
  function mark() {
    const want = items.filter((it) => it.open && it.page === PAGE && it.quote);
    want.forEach((it) => {
      if (document.querySelector(`mark.rv-mark[data-num="${it.num}"]`)) return;
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
        m.className = 'rv-mark'; m.dataset.num = it.num; m.title = 'Open comment #' + it.num;
        hit.parentNode.replaceChild(m, hit); m.appendChild(hit);
        break;
      }
    });
  }
  document.addEventListener('click', (e) => {
    const m = e.target.closest && e.target.closest('mark.rv-mark'); if (!m) return;
    e.preventDefault(); e.stopPropagation();
    openDrawer();
    const el = root.querySelector(`.rv-item[data-num="${m.dataset.num}"]`);
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
      pendingQuote = text.slice(0, 500);
      selBtn.style.display = 'block';
      selBtn.style.top = Math.min(window.innerHeight - 44, r.bottom + 8) + 'px';
      selBtn.style.left = Math.max(8, Math.min(window.innerWidth - 120, r.left)) + 'px';
    }, 200);
  });
  selBtn.addEventListener('mousedown', (e) => e.preventDefault());   // keep the selection
  selBtn.onclick = () => { selBtn.style.display = 'none'; compose(pendingQuote); };

  const modal = $('.rv-modal'), ta = modal.querySelector('textarea'), go = modal.querySelector('.go');
  function compose(quote) {
    pendingQuote = quote;
    modal.querySelector('.pg').textContent = 'Page: ' + PAGE;
    const qb = modal.querySelector('.rv-q');
    qb.hidden = !quote; qb.textContent = quote ? '“' + quote + '”' : '';
    ta.value = ''; go.disabled = true;
    modal.classList.add('show'); setTimeout(() => ta.focus(), 50);
  }
  ta.oninput = () => { go.disabled = !ta.value.trim(); };
  modal.querySelector('.cancel').onclick = () => modal.classList.remove('show');
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('show'); });
  go.onclick = () => {
    const comment = ta.value.trim();
    const short = comment.replace(/\s+/g, ' ').slice(0, 60) + (comment.length > 60 ? '…' : '');
    const quoteMd = pendingQuote ? pendingQuote.split('\n').map((l) => '> ' + l).join('\n') : '_(no text selected — general comment)_';
    const body = `**Page:** ${PAGE}\n**Site:** ${SITE}\n**Link:** ${location.href.split('#')[0]}\n\n**Selected text:**\n${quoteMd}\n\n**Comment:**\n${comment}\n\n` +
                 `<!-- rv:${encodeURIComponent(JSON.stringify({ page: PAGE, quote: pendingQuote }))} -->`;
    const url = `https://github.com/${REPO}/issues/new?title=${encodeURIComponent(`${PREFIX} ${PAGE} — ${short}`)}&body=${encodeURIComponent(body)}`;
    window.open(url, '_blank', 'noopener');
    modal.classList.remove('show');
    ss.set('rv-cache', null);   // reload on next open so the new comment appears
  };

  /* The prototype re-renders <body> when a screen changes; put the panel back and re-highlight. */
  let moTimer;
  new MutationObserver(() => { clearTimeout(moTimer); moTimer = setTimeout(() => { attach(); mark(); }, 150); })
    .observe(document.body, { childList: true });

  load();
})();
