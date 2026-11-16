/* LAMF – Calculator (DISC-257): repayment schedule from the loan inputs.
   Interest (DISC-258, DISC-259): step 1 daily rate = ROI / 365 or 366 (366 for days in a leap year, only when the
   “Leap year calculation” option is ticked – otherwise 365 in every year, DISC-260); step 2 round it to 6 decimals
   (10.5% / 365 = 0.000287671… → 0.000288); step 3 Interest = daily rate × Principal × Days, where Principal is the
   outstanding withdrawal balance of each day and Days the interest accrual days (row total shown to 2 decimals).
   First due date (DISC-261): first withdrawal on the 1st – 20th of a month → the due day of the next month
   (19-Jan → 05-Feb); after the 20th → the due day of the month after next (21-Jan → 05-Mar).
   Accrual (DISC-261): interest accrues by calendar month – the due on the 5th collects the interest of the whole
   previous month (1st – last day; the first due from the withdrawal date). The days from the 1st to the end of the
   current month are collected next month. The last row is the loan end date (start date + tenure): interest from the
   1st of that month to the day before, with the principal balance.
   A withdrawal, a repayment or the principal paid on a due date changes the principal from that date.
   EMI      – equated instalment on the outstanding principal over the remaining due dates (re-worked every due);
              the last row clears the balance.
   Interest Only – interest every month, the principal on the loan end date.
   Balloon  – nothing is due monthly; the principal and all the interest accrued are due on the loan end date. */
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

  function schedule(inp) {
    const { start, tenure, rate, type, dueDay, leap } = inp;
    const end = addMonths(start, tenure);
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
    let from = firstW, carry = 0;   // carry: interest not yet due (Balloon)
    const rows = [];
    dues.forEach((D, i) => {
      const last = i === dues.length - 1, to = last ? D - 1 : monthEnd(D);
      // Interest split (DISC-262): one part for every run of days with the same principal and the same daily rate;
      // each part = principal × daily rate (6 decimals) × days, rounded to 2 decimals; the row interest is their sum.
      const segs = [];
      for (let t = from; t <= to; t++) {
        const p = P(t), dr = round6(rate / 100 / yearDays(t)), sg = segs[segs.length - 1];
        if (sg && sg.p === p && sg.dr === dr) { sg.to = t; sg.days++; continue; }
        const why = [];
        if (sg) {
          events.filter((e) => e.d === t).forEach((e) => why.push(e.k === 'w' ? `Withdrawal ${money(e.a)} on ${fmtD(t)}`
            : e.k === 'r' ? `Repayment ${money(-e.a)} on ${fmtD(t)}` : `Principal ${money(-e.a)} paid on ${fmtD(t)}`));
          if (dr !== sg.dr) why.push(`Year ${new Date(t * DAY).getUTCFullYear()} – ${yearDays(t)} days`);
        }
        segs.push({ from: t, to: t, days: 1, p, dr, why: why.join(' · ') || (segs.length ? '' : 'From ' + fmtD(t)) });
      }
      segs.forEach((sg) => { sg.interest = round2(sg.p * sg.dr * sg.days); });
      const interest = round2(segs.reduce((v, sg) => v + sg.interest, 0)), out = P(D), left = dues.length - i;
      let principal = 0, intDue = interest;
      if (last) { principal = out; intDue = interest + carry; carry = 0; }
      else if (type === 'EMI') {
        const emi = r ? out * r * Math.pow(1 + r, left) / (Math.pow(1 + r, left) - 1) : out / left;
        principal = Math.min(out, Math.max(0, round2(emi - interest)));
      } else if (type === 'Balloon') { carry += interest; intDue = 0; }
      if (principal) events.push({ d: D, a: -principal, k: 'due' });     // the principal paid on the due date reduces it from that date
      rows.push({ no: i + 1, due: D, out, principal, interest: intDue, accrued: interest, from, to, days: to - from + 1, segs });
      from = to + 1;
    });
    return { end, rows };
  }

  function read(f) {
    const g = (n) => f.querySelector(`[name="${n}"]`).value;
    const list = (cls) => [...f.querySelectorAll(`.${cls} tbody tr`)]
      .map((tr) => ({ d: toDay(tr.querySelector('input[type=date]').value), a: num(tr.querySelector('input.amt').value) }))
      .filter((x) => x.d !== null && x.a > 0);
    return { start: toDay(g('start')), tenure: +g('tenure'), rate: num(g('rate')), type: g('type'), dueDay: +g('dueday') || 5,
             product: g('product'), leap: f.querySelector('[name="leap"]').checked, withdrawals: list('calc-w'), repayments: list('calc-r') };
  }

  function check(inp) {
    if (inp.start === null) return 'Enter the Lodgement Approval Date (Loan Start Date).';
    if (!inp.withdrawals.length) return 'Enter at least one withdrawal (date and amount).';
    if (!(inp.rate > 0)) return 'Enter the Rate of Interest.';
    const end = addMonths(inp.start, inp.tenure);
    if (inp.withdrawals.some((w) => w.d < inp.start || w.d >= end)) return 'Each withdrawal date has to be on or after the Loan Start Date and before the Loan End Date.';
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
    const seg = (x, sg) => `<tr class="seg"><td></td><td colspan="2">↳ ${money(sg.p)} × ${sg.dr.toFixed(6)} × ${sg.days} day${sg.days > 1 ? 's' : ''}${sg.why ? `<small>${sg.why}</small>` : ''}</td>
      <td></td><td></td><td class="n">${money(sg.interest)}${x.interest !== x.accrued ? '<small>accrued</small>' : ''}</td><td>${fmtD(sg.from)}</td><td>${fmtD(sg.to)}</td><td class="c">${sg.days}</td></tr>`;
    const tr = rows.map((x) => `<tr class="main"><td class="c">${x.no}</td><td>${fmtD(x.due)}</td><td class="n">${money(x.out)}</td>
      <td class="n b">${money(x.principal + x.interest)}</td><td class="n">${money(x.principal)}</td><td class="n">${money(x.interest)}</td>
      <td>${fmtD(x.from)}</td><td>${fmtD(x.to)}</td><td class="c">${x.days}</td></tr>`
      + (x.segs.length > 1 ? x.segs.map((sg) => seg(x, sg)).join('') : '')).join('');
    out.innerHTML = `
      <div class="comms-summary calc-sum">
        <div><b>${fmtD(end)}</b><span>Loan End Date</span></div>
        <div><b>${money(wTot)}</b><span>Total withdrawals</span></div>
        <div><b>${money(rTot)}</b><span>Total repayments</span></div>
        <div><b>${money(sum('interest'))}</b><span>Total interest</span></div>
        <div><b>${money(sum('principal') + sum('interest'))}</b><span>Total due</span></div>
        <div><b>${rows.length}</b><span>Due dates</span></div>
      </div>
      <div class="comms-wrap"><table class="calc-table">
        <thead><tr><th rowspan="2">Sl. No</th><th rowspan="2">Due Date</th><th rowspan="2">Outstanding Principal</th><th rowspan="2">Due Amount</th>
          <th colspan="2">Due Amount Bifurcation</th><th colspan="3">Interest Accrual</th></tr>
          <tr><th>Principal</th><th>Interest</th><th>Start Date</th><th>End Date</th><th>No. of Days</th></tr></thead>
        <tbody>${tr}</tbody>
        <tfoot><tr><td></td><td>Total</td><td></td><td class="n b">${money(sum('principal') + sum('interest'))}</td><td class="n">${money(sum('principal'))}</td>
          <td class="n">${money(sum('interest'))}</td><td></td><td></td><td class="c">${sum('days')}</td></tr></tfoot>
      </table></div>
      <p class="calc-note">${inp.product} · ${inp.type} · ${inp.rate}% p.a. · ${inp.tenure} months. Interest = ROUND(ROI / ${inp.leap ? '365 or 366' : '365'}, 6) × Principal × Days – daily rate ${(Math.round(inp.rate / 100 / 365 * 1e6) / 1e6).toFixed(6)}${inp.leap ? ` (366 days in a leap year: ${(Math.round(inp.rate / 100 / 366 * 1e6) / 1e6).toFixed(6)})` : ' (leap-year calculation off: 365 days in every year)'}; Principal is the outstanding withdrawal balance.
      Outstanding Principal is the principal on the due date, before that due is paid. When the principal or the daily rate changes within a period, the rows marked ↳ show each part of the interest (principal × daily rate × days).${inp.type === 'Balloon' ? ' Balloon: the interest of every month is accrued and is due with the principal on the loan end date.' : ''}</p>`;
  }

  function addRow(tbody, d, a) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td><input type="date" value="${d || ''}"></td><td><input class="amt" inputmode="decimal" placeholder="Amount (₹)" value="${a || ''}"></td>
      <td><button type="button" class="calc-del" title="Remove">✕</button></td>`;
    tbody.appendChild(tr);
  }

  function init() {
    const f = document.querySelector('.calc-form'); if (!f || f.dataset.ready) return; f.dataset.ready = '1';
    const endEl = f.querySelector('[name="end"]');
    const syncEnd = () => { const s = toDay(f.querySelector('[name="start"]').value);
      endEl.value = s === null ? '' : fmtD(addMonths(s, +f.querySelector('[name="tenure"]').value)); };
    const syncOut = () => { const i = read(f);
      f.querySelector('[name="outstanding"]').value = money(i.withdrawals.reduce((s, w) => s + w.a, 0) - i.repayments.reduce((s, w) => s + w.a, 0)); };
    addRow(f.querySelector('.calc-w tbody'), '2026-11-02', '1,00,000');
    f.addEventListener('input', () => { syncEnd(); syncOut(); });
    f.addEventListener('change', () => { syncEnd(); syncOut(); });
    f.addEventListener('click', (e) => {
      const add = e.target.closest('[data-add]'); if (add) addRow(f.querySelector(`.${add.dataset.add} tbody`));
      const del = e.target.closest('.calc-del'); if (del) { del.closest('tr').remove(); syncOut(); }
    });
    f.addEventListener('submit', (e) => { e.preventDefault(); render(f); });
    syncEnd(); syncOut();
  }

  window.LAMFCalc = { init, schedule, toDay, toISO };
  if (document.readyState !== 'loading') init(); else document.addEventListener('DOMContentLoaded', init);
})();
