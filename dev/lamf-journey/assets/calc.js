/* LAMF – Calculator (DISC-257): repayment schedule from the loan inputs.
   Interest (DISC-258, DISC-259): step 1 daily rate = ROI / 365 or 366 (366 for days in a leap year, only when the
   “Leap year calculation” option is ticked – otherwise 365 in every year, DISC-260); step 2 round it to 6 decimals
   (10.5% / 365 = 0.000287671… → 0.000288); step 3 Interest = daily rate × Principal × Days, where Principal is the
   outstanding withdrawal balance of each day and Days the interest accrual days (row total shown to 2 decimals).
   First due date (DISC-261): first withdrawal on the 1st – 20th of a month → the due day of the next month
   (19-Jan → 05-Feb); after the 20th → the due day of the month after next (21-Jan → 05-Mar).
   Accrual (DISC-261): interest accrues by calendar month – the due on the 5th collects the interest of the whole
   previous month (1st – last day; the first due from the withdrawal date). The days from the 1st to the end of the
   current month are collected next month. The last row is the loan end date (start date + tenure − 1 day, DISC-265): interest from
   the 1st of that month up to and including the end date, with the principal balance.
   A withdrawal, a repayment or the principal paid on a due date changes the principal from that date.
   EMI      – equated instalment on the outstanding principal over the remaining due dates (re-worked every due);
              the last row clears the balance.
   Balloon / Interest Only – interest every month, the principal on the loan end date (DISC-264).
   Products (DISC-264): Line of Credit, Single Disbursement (one withdrawal only), Multiple Disbursement.
   Due date fixed on the 5th of every month (DISC-264).
   Interest split rows (DISC-262, DISC-264) are shown only for a due whose interest has a withdrawal, a repayment or a
   365 / 366 change inside it, and can be expanded or collapsed. */
(function () {
  const DAY = 86400000;
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const toDay = (s) => { if (!s) return null; const [y, m, d] = s.split('-').map(Number); return Date.UTC(y, m - 1, d) / DAY; };
  const toISO = (n) => new Date(n * DAY).toISOString().slice(0, 10);
  const fmtD = (n) => { const d = new Date(n * DAY); return `${String(d.getUTCDate()).padStart(2, '0')}-${MON[d.getUTCMonth()]}-${d.getUTCFullYear()}`; };
  const money = (v) => '₹' + (Math.round(v * 100) / 100).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const num = (s) => parseFloat(String(s || '').replace(/,/g, '')) || 0;
  const addMonths = (n, k, day) => {           // same day k months later (or the given day of that month)
    const d = new Date(n * DAY), y = d.getUTCFullYear(), m = d.getUTCMonth() + k;
    const want = day || d.getUTCDate(), last = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    return Date.UTC(y, m, Math.min(want, last)) / DAY;
  };

  // Loan End Date = start date + tenure − 1 day: 12-Nov-2026 + 12 months → 11-Nov-2027 (DISC-265)
  const loanEnd = (s, months) => addMonths(s, months) - 1;

  function schedule(inp) {
    const { start, tenure, rate, type, dueDay, leap } = inp;
    const end = loanEnd(start, tenure);
    const firstW = Math.min(...inp.withdrawals.map((w) => w.d));
    const firstDue = addMonths(firstW, new Date(firstW * DAY).getUTCDate() <= 20 ? 1 : 2, dueDay);   // DISC-261
    const dues = [];
    for (let k = 0, d = firstDue; d < end; d = addMonths(firstDue, ++k, dueDay)) dues.push(d);
    if (!dues.length || dues[dues.length - 1] !== end) dues.push(end);
    const monthEnd = (D) => { const d = new Date(D * DAY); return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 0) / DAY; };  // last day of the previous month

    const yearDays = (t) => { if (!leap) return 365;   // 366 only when the leap-year option is ticked (DISC-260)
      const y = new Date(t * DAY).getUTCFullYear(); return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0 ? 366 : 365; };
    const round2 = (v) => Math.round(v * 100) / 100, round6 = (v) => Math.round(v * 1e6) / 1e6, r = rate / 1200;
    const events = [...inp.withdrawals.map((w) => ({ d: w.d, a: w.a, k: 'w' })), ...inp.repayments.map((x) => ({ d: x.d, a: -x.a, k: 'r' }))];
    const P = (t) => Math.max(0, events.reduce((s, e) => s + (e.d <= t ? e.a : 0), 0));   // principal on day t (after that day's events)
    let from = firstW;
    const rows = [];
    dues.forEach((D, i) => {
      const last = i === dues.length - 1, to = last ? D : monthEnd(D);   // last row: up to and including the loan end date
      // Interest split (DISC-262): one part for every run of days with the same principal and the same daily rate;
      // each part = principal × daily rate (6 decimals) × days, rounded to 2 decimals; the row interest is their sum.
      const segs = [];
      for (let t = from; t <= to; t++) {
        const p = P(t), dr = round6(rate / 100 / yearDays(t)), sg = segs[segs.length - 1];
        if (sg && sg.p === p && sg.dr === dr) { sg.to = t; sg.days++; continue; }
        const why = [], kinds = [];
        if (sg) {
          events.filter((e) => e.d === t).forEach((e) => kinds.push(e.k));
          if (dr !== sg.dr) kinds.push('year');
          events.filter((e) => e.d === t).forEach((e) => why.push(e.k === 'w' ? `Withdrawal ${money(e.a)} on ${fmtD(t)}`
            : e.k === 'r' ? `Repayment ${money(-e.a)} on ${fmtD(t)}` : `Principal ${money(-e.a)} paid on ${fmtD(t)}`));
          if (dr !== sg.dr) why.push(`Year ${new Date(t * DAY).getUTCFullYear()} – ${yearDays(t)} days`);
        }
        segs.push({ from: t, to: t, days: 1, p, dr, kinds, why: why.join(' · ') || (segs.length ? '' : 'From ' + fmtD(t)) });
      }
      segs.forEach((sg) => { sg.interest = round2(sg.p * sg.dr * sg.days); });
      const interest = round2(segs.reduce((v, sg) => v + sg.interest, 0)), out = P(D), left = dues.length - i;
      let principal = 0, intDue = interest;
      if (last) principal = out;
      else if (type === 'EMI') {
        const emi = r ? out * r * Math.pow(1 + r, left) / (Math.pow(1 + r, left) - 1) : out / left;
        principal = Math.min(out, Math.max(0, round2(emi - interest)));
      }
      if (principal) events.push({ d: D, a: -principal, k: 'due' });     // the principal paid on the due date reduces it from that date
      const split = segs.some((sg) => sg.kinds.some((k) => k !== 'due'));    // withdrawal, repayment or 365 / 366 change in this due
      rows.push({ no: i + 1, due: D, out, principal, interest: intDue, accrued: interest, from, to, days: to - from + 1, segs, split });
      from = to + 1;
    });
    return { end, rows };
  }

  function read(f) {
    const g = (n) => f.querySelector(`[name="${n}"]`).value;
    const list = (k) => (f._tx || []).filter((x) => x.k === k).map((x) => ({ d: x.d, a: x.a }));
    return { start: toDay(g('start')), tenure: +g('tenure'), rate: num(g('rate')), type: g('type'), dueDay: 5,
             product: g('product'), ason: toDay(g('ason')), leap: f.querySelector('[name="leap"]').checked, withdrawals: list('w'), repayments: list('r') };
  }

  function check(inp) {
    if (inp.start === null) return 'Enter the Lodgement Approval Date (Loan Start Date).';
    if (!inp.withdrawals.length) return 'Enter at least one withdrawal (date and amount).';
    if (inp.product === 'Single Disbursement' && inp.withdrawals.length > 1) return 'Single Disbursement allows one withdrawal only.';
    if (!(inp.rate > 0)) return 'Enter the Rate of Interest.';
    const end = loanEnd(inp.start, inp.tenure);
    if (inp.withdrawals.some((w) => w.d < inp.start || w.d > end)) return 'Each withdrawal date has to be between the Loan Start Date and the Loan End Date.';
    if (inp.repayments.some((p) => p.d < inp.start || p.d > end)) return 'Each repayment date has to be between the Loan Start Date and the Loan End Date.';
    return '';
  }

  function render(f) {
    const out = f.parentNode.querySelector('.calc-out'), err = f.querySelector('.calc-err');
    const inp = read(f), msg = check(inp);
    err.textContent = msg; if (msg) { out.innerHTML = ''; return; }
    const { end, rows } = schedule(inp);
    const sum = (k) => rows.reduce((s, x) => s + x[k], 0);
    const wTot = inp.withdrawals.reduce((s, w) => s + w.a, 0), rTot = inp.repayments.reduce((s, w) => s + w.a, 0);
    // Summary (DISC-263): dues on or before the As on Date are taken as collected on their due date
    const asOn = inp.ason === null ? Math.floor(Date.now() / DAY) : inp.ason;
    const done = rows.filter((x) => x.due <= asOn), todo = rows.filter((x) => x.due > asOn), next = todo[0];
    const amt = (l) => l.reduce((v, x) => v + x.principal + x.interest, 0);
    const pOut = Math.max(0, inp.withdrawals.reduce((v, w) => v + (w.d <= asOn ? w.a : 0), 0) - inp.repayments.reduce((v, w) => v + (w.d <= asOn ? w.a : 0), 0)
                 - done.reduce((v, x) => v + x.principal, 0));
    const tile = (cls, label, v, sub) => `<div class="kpi ${cls}"><span>${label}</span><b>${v}</b><small>${sub}</small></div>`;
    const totDue = sum('principal') + sum('interest'), pct = totDue ? Math.round(amt(done) / totDue * 100) : 0;
    const seg = (x, sg) => `<tr class="seg" data-of="${x.no}" hidden><td></td><td colspan="2">↳ ${money(sg.p)} × ${sg.dr.toFixed(6)} × ${sg.days} day${sg.days > 1 ? 's' : ''}${sg.why ? `<small>${sg.why}</small>` : ''}</td>
      <td></td><td></td><td class="n">${money(sg.interest)}</td><td>${fmtD(sg.from)}</td><td>${fmtD(sg.to)}</td><td class="c">${sg.days}</td><td></td></tr>`;
    const stat = (x) => x.due <= asOn ? '<span class="st ok">Collected</span>' : x === next ? '<span class="st nx">Next due</span>' : '<span class="st">Upcoming</span>';
    const nSplit = rows.filter((x) => x.split).length;
    const tr = rows.map((x) => `<tr class="main${x.split ? ' has-split' : ''}"><td class="c">${x.no}</td><td>${fmtD(x.due)}</td><td class="n">${money(x.out)}</td>
      <td class="n b">${money(x.principal + x.interest)}</td><td class="n">${money(x.principal)}</td>
      <td class="n">${money(x.interest)}${x.split ? `<button type="button" class="calc-tg" data-row="${x.no}" aria-expanded="false" title="Show / hide the interest split">Split ▸</button>` : ''}</td>
      <td>${fmtD(x.from)}</td><td>${fmtD(x.to)}</td><td class="c">${x.days}</td><td class="c">${stat(x)}</td></tr>`
      + (x.split ? x.segs.map((sg) => seg(x, sg)).join('') : '')).join('');
    out.innerHTML = `
      <div class="calc-res">
        <div class="calc-chips"><span>${inp.product}</span><span>${inp.type}</span><span>${inp.rate}% p.a.${inp.leap ? ' · leap year 366' : ''}</span>
          <span>${inp.tenure} months</span><span>${fmtD(inp.start)} → ${fmtD(end)}</span><span>${rows.length} dues · 5th of every month</span></div>
        <div class="calc-kpis">
          ${tile('tot', 'Total due', money(totDue), `Principal ${money(sum('principal'))} · Interest ${money(sum('interest'))}`)}
          ${tile('ok', 'Due collected', money(amt(done)), `${done.length} of ${rows.length} dues · as on ${fmtD(asOn)}`)}
          ${tile('due', 'Due pending', money(amt(todo)), `${todo.length} due${todo.length === 1 ? '' : 's'} remaining`)}
          ${tile('nx', 'Next due', next ? money(next.principal + next.interest) : '–', next ? 'on ' + fmtD(next.due) : 'All dues collected')}
          ${tile('', 'Principal outstanding', money(pOut), 'as on ' + fmtD(asOn))}
        </div>
        <div class="calc-bar"><i style="width:${pct}%"></i></div>
        <p class="calc-barl"><b>${pct}%</b> of the total due collected as on ${fmtD(asOn)} · Total withdrawals ${money(wTot)} · Total repayments ${money(rTot)} · Interest collected ${money(done.reduce((v, x) => v + x.interest, 0))}</p>
      </div>
      ${nSplit ? `<div class="calc-tools"><span>${nSplit} due${nSplit === 1 ? ' has' : 's have'} an interest split (withdrawal, repayment or 365 / 366 change)</span>
        <button type="button" data-all="1">Expand all</button><button type="button" data-all="0">Collapse all</button></div>` : ''}
      <div class="comms-wrap"><table class="calc-table">
        <thead><tr><th rowspan="2">Sl. No</th><th rowspan="2">Due Date</th><th rowspan="2">Outstanding Principal</th><th rowspan="2">Due Amount</th>
          <th colspan="2">Due Amount Bifurcation</th><th colspan="3">Interest Accrual</th><th rowspan="2">Status</th></tr>
          <tr><th>Principal</th><th>Interest</th><th>Start Date</th><th>End Date</th><th>No. of Days</th></tr></thead>
        <tbody>${tr}</tbody>
        <tfoot><tr><td></td><td>Total</td><td></td><td class="n b">${money(totDue)}</td><td class="n">${money(sum('principal'))}</td>
          <td class="n">${money(sum('interest'))}</td><td></td><td></td><td class="c">${sum('days')}</td><td></td></tr></tfoot>
      </table></div>
      <p class="calc-note">Interest = ROUND(ROI / ${inp.leap ? '365 or 366' : '365'}, 6) × Principal × Days – daily rate ${(Math.round(inp.rate / 100 / 365 * 1e6) / 1e6).toFixed(6)}${inp.leap ? ` (366 days in a leap year: ${(Math.round(inp.rate / 100 / 366 * 1e6) / 1e6).toFixed(6)})` : ' (leap-year calculation off: 365 days in every year)'}; Principal is the outstanding withdrawal balance.
      Outstanding Principal is the principal on the due date, before that due is paid. “Split ▸” opens the interest of a due part by part (principal × daily rate × days) when a withdrawal, a repayment or a 365 / 366 change falls inside it.
      Due collected assumes every due on or before the As on Date was paid on its due date.${inp.type !== 'EMI' ? ' Balloon / Interest Only: interest every month, the principal on the loan end date.' : ''}</p>`;
    const toggle = (no, open) => { out.querySelectorAll(`tr.seg[data-of="${no}"]`).forEach((r) => { r.hidden = !open; });
      const b = out.querySelector(`.calc-tg[data-row="${no}"]`); if (b) { b.setAttribute('aria-expanded', open); b.textContent = open ? 'Split ▾' : 'Split ▸'; } };
    out.onclick = (e) => {
      const b = e.target.closest('.calc-tg'); if (b) toggle(b.dataset.row, b.getAttribute('aria-expanded') !== 'true');
      const a = e.target.closest('[data-all]'); if (a) rows.filter((x) => x.split).forEach((x) => toggle(x.no, a.dataset.all === '1'));
    };
  }

  // Withdrawals and repayments (DISC-266): pick the type, the date and the amount and click Add; the entries are listed
  // by date as a timeline with the outstanding principal after each one, and can be removed.
  const inr = (v) => (Math.round(v * 100) / 100).toLocaleString('en-IN', { maximumFractionDigits: 2 });

  function init() {
    const f = document.querySelector('.calc-form'); if (!f || f.dataset.ready) return; f.dataset.ready = '1';
    f._tx = [{ k: 'w', d: toDay('2026-11-02'), a: 100000 }];
    const endEl = f.querySelector('[name="end"]'), list = f.querySelector('.tx-list'), msg = f.querySelector('.tx-msg');
    const dIn = f.querySelector('[name="txd"]'), aIn = f.querySelector('[name="txa"]');
    let kind = 'w';
    const single = () => f.querySelector('[name="product"]').value === 'Single Disbursement';
    const setKind = (k) => { kind = k; f.querySelectorAll('.tx-seg button').forEach((b) => b.classList.toggle('on', b.dataset.kind === k)); };
    const syncEnd = () => { const s = toDay(f.querySelector('[name="start"]').value);
      endEl.value = s === null ? '' : fmtD(loanEnd(s, +f.querySelector('[name="tenure"]').value)); };
    const syncTx = () => {
      f._tx.sort((x, y) => x.d - y.d || (x.k === 'w' ? -1 : 1));
      let bal = 0;
      list.innerHTML = f._tx.map((x, i) => { bal = Math.max(0, bal + (x.k === 'w' ? x.a : -x.a));
        return `<li class="${x.k}"><span class="ic">${x.k === 'w' ? '↓' : '↑'}</span>
          <div class="tx-main"><b>${x.k === 'w' ? 'Withdrawal' : 'Repayment'}</b><small>${fmtD(x.d)}</small></div>
          <div class="tx-amt"><b>${x.k === 'w' ? '+' : '−'} ${money(x.a)}</b><small>Outstanding after ${money(bal)}</small></div>
          <button type="button" class="tx-x" data-i="${i}" title="Remove" aria-label="Remove">✕</button></li>`; }).join('');
      const w = f._tx.filter((x) => x.k === 'w').reduce((v, x) => v + x.a, 0), r = f._tx.filter((x) => x.k === 'r').reduce((v, x) => v + x.a, 0);
      f.querySelector('.tx-sum .sw').textContent = money(w); f.querySelector('.tx-sum .sr').textContent = money(r);
      f.querySelector('.tx-sum .so').textContent = money(Math.max(0, w - r));
      f.querySelector('.tx-box').classList.toggle('empty', !f._tx.length);
      const lock = single() && f._tx.some((x) => x.k === 'w');            // Single Disbursement: one withdrawal only
      const wb = f.querySelector('.tx-seg [data-kind="w"]'); wb.disabled = lock; if (lock && kind === 'w') setKind('r');
    };
    const add = () => {
      const d = toDay(dIn.value), a = num(aIn.value);
      if (d === null || !(a > 0)) { msg.textContent = 'Enter the date and the amount.'; return; }
      if (kind === 'w' && single() && f._tx.some((x) => x.k === 'w')) { msg.textContent = 'Single Disbursement allows one withdrawal only.'; return; }
      msg.textContent = ''; f._tx.push({ k: kind, d, a }); aIn.value = ''; syncTx(); aIn.focus();
    };
    const ason = f.querySelector('[name="ason"]'); if (!ason.value) ason.value = toISO(Math.floor(Date.now() / DAY));
    aIn.addEventListener('blur', () => { const a = num(aIn.value); aIn.value = a ? inr(a) : ''; });
    aIn.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); add(); } });
    f.addEventListener('input', (e) => { if (!e.target.closest('.tx-new')) syncEnd(); });
    f.addEventListener('change', (e) => { if (!e.target.closest('.tx-new')) { syncEnd(); syncTx(); } });
    f.addEventListener('click', (e) => {
      const k = e.target.closest('.tx-seg button'); if (k && !k.disabled) setKind(k.dataset.kind);
      if (e.target.closest('.tx-addbtn')) add();
      const x = e.target.closest('.tx-x'); if (x) { f._tx.splice(+x.dataset.i, 1); syncTx(); }
    });
    f.addEventListener('submit', (e) => { e.preventDefault(); render(f); });
    syncEnd(); syncTx();
  }

  window.LAMFCalc = { init, schedule, toDay, toISO };
  if (document.readyState !== 'loading') init(); else document.addEventListener('DOMContentLoaded', init);
})();
