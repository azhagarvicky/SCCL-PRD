"""LMS page (DISC-327) – opened by the “LMS” CTA on the home page.

The modules follow the left menu of the LMS (uatlms.shriramcredit.in): Dashboard, Products, Loans (Active, Inactive, Draft,
Submitted, Closed, Rejected), Collaterals, Clients, Approvals, Disbursement Management, Reports, Settings.
Each module opens its own section (CSS :target, no script). Content for each module is added here as the owner shares it.
"""
import html as _h

LMS_MODULES = [   # (id, name, sub-modules, description)
    ("dashboard", "Dashboard", [], ""),
    ("products", "Products", [], ""),
    ("loans", "Loans", [("active", "Active"), ("inactive", "Inactive"), ("draft", "Draft"), ("submitted", "Submitted"),
                        ("closed", "Closed"), ("rejected", "Rejected")], ""),
    ("collaterals", "Collaterals", [], ""),
    ("clients", "Clients", [], ""),
    ("approvals", "Approvals", [], ""),
    ("disbursement", "Disbursement Management", [], ""),
    ("reports", "Reports", [], ""),
    ("settings", "Settings", [], ""),
]

TBA = '<p class="lms-tba">Screens and requirements for this module will be added here.</p>'

# ---- Loans list views (DISC-328) – columns, filters and status badges as in the live LMS (lms.shriramcredit.in/loans/<status>).
# Rows are SAMPLE data only (made-up names, PANs and LANs) – no real customer data.
BASE_COLS = ["LAN", "Product Id", "Client Name", "Status", "PAN", "Sanction Amount", "Rate of Interest", "Start Date", "End Date",
             "Generated", "Source"]
ACTIVE_COLS = BASE_COLS[:2] + ["Risk Level"] + BASE_COLS[2:]
REJECTED_COLS = ["LAN", "Product Id", "Client Name", "PAN", "Sanction Amount", "Rate of Interest", "Generated", "Source"]
_NAMES = ["Sample Customer A", "Sample Customer B", "Sample Customer C", "Sample Customer D", "Sample Customer E",
          "Sample Customer F", "Sample Customer G", "Sample Customer H", "Sample Customer I", "Sample Customer J"]
_SRC = ["SCCL LOS", "Quicklend", "Liquify", "SCCL LOS", "Quicklend", "Forward wealth", "SCCL LOS", "Liquify", "Quicklend", "SCCL LOS"]
_PROD = ["LAMF20261114", "LAMF20261113", "LAMF20261117", "LAMF20261114", "LAMF2026106", "LAMF20261113", "LAMF20261114",
         "LAMF20261117", "LAMF2026106", "LAMF20261113"]
_AMT = ["₹1,25,000", "₹59,300", "₹19,300", "₹1,06,000", "₹32,500", "₹10,600", "₹22,400", "₹19,000", "₹18,700", "₹18,200"]
_ROI = ["10.49%", "11%", "10.49%", "10.49%", "11%", "11%", "10.49%", "10.49%", "10.49%", "10.49%"]


START = {"active": 99, "inactive": 89, "draft": 79, "submitted": 69, "closed": 59, "rejected": 49}   # unique sample LANs per list


def _rows(view):
    n = {"active": 10, "inactive": 10, "draft": 10, "submitted": 5, "closed": 2, "rejected": 2}[view]
    status = {"active": "Active", "inactive": "Inactive", "draft": "Draft", "submitted": "Submitted", "closed": "Foreclosed"}.get(view)
    out = []
    for k in range(n):
        d = 17 - k // 2
        r = {"LAN": f"SCCLMF202611000{START[view] - k:02d}", "Product Id": _PROD[k], "Client Name": _NAMES[k], "Status": status,
             "PAN": f"ABCPX{1000 + k * 7}A", "Generated": f"{d:02d}/11/2026", "Source": _SRC[k],
             "Risk Level": ["No Risk", "No Risk", "No Risk", "L1", "L1", "L1", "L1", "L1", "No Risk", "No Risk"][k]}
        has_amt = view in ("active", "closed", "rejected") or k % 3 == 0
        r["Sanction Amount"] = _AMT[k] if has_amt else "-"
        r["Rate of Interest"] = _ROI[k] if (has_amt or k % 2 == 0) else "-"
        if view in ("active", "closed"):
            r["Start Date"] = f"{d - 1:02d}/11/2026"
            r["End Date"] = f"{d - 2:02d}/11/2029" if view == "active" else f"{d + 3:02d}/11/2026"
        else:
            r["Start Date"] = r["End Date"] = "-"
        out.append(r)
    return out


NUM = {"Sanction Amount", "Rate of Interest"}


def loan_view(view):
    cols = ACTIVE_COLS if view == "active" else REJECTED_COLS if view == "rejected" else BASE_COLS
    rows = _rows(view)
    def cell(c, r):
        v = r[c]
        if c == "Status":
            return f'<td><span class="lms-st st-{v.lower()}">{_h.escape(v)}</span></td>'
        if c == "LAN":
            return f'<td><a class="lms-lan" href="#lan-{view}-{v}">{_h.escape(v)}</a></td>'
        return f'<td class="{"num" if c in NUM else ""}">{_h.escape(v)}</td>'
    chips = ('<span class="lms-chip on">All</span><span class="lms-chip">Shortfall</span><span class="lms-chip">In Default</span>'
             if view == "active" else "")
    note = ('<p class="lms-note">Columns assumed to be the same as Draft – share a Submitted screenshot to confirm.</p>'
            if view == "submitted" else "")
    return (f'<div class="lms-filters"><span class="lms-select">Select a value <i>⌄</i></span>{chips}</div>{note}'
            '<div class="lms-tablewrap"><table class="lms-table"><thead><tr>'
            + "".join(f'<th class="{"num" if c in NUM else ""}">{c}</th>' for c in cols) + '</tr></thead><tbody>'
            + "".join("<tr>" + "".join(cell(c, r) for c in cols) + "</tr>" for r in rows) + '</tbody></table></div>'
            f'<div class="lms-pager"><span>Showing 1 - {len(rows)} items</span><span class="lms-pp"><span class="lms-select">10 <i>⌄</i></span>'
            ' rows/page <span class="lms-pg">‹</span><span class="lms-pg">›</span></span></div>'
            '<p class="lms-sample">Sample data for the prototype – not real customers.</p>')


# ---- LAN detail (DISC-329) – opened by clicking a LAN in any loan list; layout as in the LMS loan page (Overview tab).
TABS = ["Overview", "Approvals", "Disbursement &amp; Repayments", "Collateral", "Transactions &amp; Reports", "KYC", "Documents",
        "Audit", "Notes"]


def _num(v):
    return int(v.replace("₹", "").replace(",", "")) if v not in ("-", None) else None


def _rs(n, dec=False):
    if n is None:
        return "-"
    s = f"{n:,.2f}" if dec else f"{int(n):,}"
    whole, _, frac = s.partition(".")
    whole = whole.replace(",", "")
    head, tail = whole[:-3], whole[-3:]
    head = ",".join([head[max(0, i - 2):i] for i in range(len(head), 0, -2)][::-1]) if head else ""
    return "₹" + (head + "," if head else "") + tail + ("." + frac if frac else "")


# ---- Approvals tab for a DRAFT loan (DISC-337) – new, as per the Waiver BRD 3.1 / 3.2 (not in the live LMS yet).
# Charges depend on how far the customer went (Waiver BRD scenarios 2 – 4); amounts include 18% GST.
DRAFT_CHARGES = {2: [("Lien Marking Charges", 531), ("Lien Removal Charges", 118)],
                 3: [("Processing Fee", 1178.82), ("Lien Marking Charges", 531), ("Lien Removal Charges", 118)],
                 4: [("Processing Fee", 1178.82), ("Lien Marking Charges", 531), ("Lien Removal Charges", 118), ("Stamp Duty Charges", 236)]}


def _amt(v):
    return f"{v:,.2f}".rstrip("0").rstrip(".") if v % 1 else f"{int(v):,}"


def draft_approvals(r, tid):
    """Draft loan Approvals tab (DISC-338): waive-off table with its own Waive-off button, confirmation and success pop-ups;
    note, file upload and a Reject button only at the bottom, with the existing reconfirmation pop-up."""
    k = START["draft"] - int(r["LAN"][-2:])
    sc = 2 if k < 4 else 3 if k < 7 else 4
    rows = "".join(f'<tr data-name="{n}"><td><input type="checkbox" class="wv-chk" aria-label="Select {n}"></td><td>{n}</td><td class="num wv-chg">₹{_amt(a)}</td>'
                   f'<td><input class="wv-amt" type="number" min="0" step="0.01" value="0" data-max="{a}" disabled></td>'
                   f'<td class="num wv-pay">₹{_amt(a)}</td></tr>' for n, a in DRAFT_CHARGES[sc])
    total = sum(a for _, a in DRAFT_CHARGES[sc])
    pop = lambda cls, body: f'<div class="wv-pop {cls}" hidden><div class="wv-box"><button type="button" class="wv-x" aria-label="Close">×</button>{body}</div></div>'
    return (f'<div class="wv" data-tid="{tid}" data-orig="{total}"><p class="lms-new">New – as per the Waiver BRD (Waiver BRD scenario {sc}). '
            'Not in the live LMS yet.</p>'
            '<div class="wv-head"><h3>Waive-off charges</h3><button type="button" class="wv-waive" disabled>Waive-off</button></div>'
            '<table class="lms-table wv-table"><thead><tr><th><input type="checkbox" class="wv-all" aria-label="Select all"></th>'
            '<th>Charges Name</th><th class="num">Amount of Charges</th><th>Amount to be waived off</th><th class="num">Payable Charges</th></tr></thead>'
            f'<tbody>{rows}</tbody><tfoot><tr><td></td><td><b>Total</b></td><td class="num"><b class="wv-ctot">₹{_amt(total)}</b></td>'
            f'<td><b class="wv-wtot">₹0</b></td><td class="num"><b class="wv-ptot">₹{_amt(total)}</b></td></tr></tfoot></table>'
            '<p class="wv-allgone" hidden>All charges have been waived off – nothing is payable.</p>'
            '<p class="wv-type">Type of waive-off: <b>No waive-off</b></p>'
            '<label class="wv-lbl">Add a note <span>(rejection reason – recorded in the Audit)</span></label>'
            '<textarea class="wv-note" rows="2" placeholder="Add a note"></textarea><p class="wv-err"></p>'
            '<label class="wv-lbl">Upload a file</label><div class="wv-drop">Drop files here or <u>click</u></div>'
            '<p class="wv-hint">PDF, PNG or JPG. Max 5MB</p>'
            '<div class="wv-ctas"><button type="button" class="wv-reject">Reject</button></div><div class="wv-done" hidden></div>'
            + pop('wv-pw', '<h3>Are you sure you want to waive-off selected charges?</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No, don’t</button><button type="button" class="wv-yes-w">Yes, waive-off</button></div>')
            + pop('wv-ps', '<div class="wv-tick">✓</div><h3>Charges waived off successfully</h3><p class="wv-ps-txt"></p>'
                  '<div class="wv-pbtns one"><button type="button" class="wv-ok">OK</button></div>')
            + pop('wv-pr', '<h3>This action is irreversible. Are you sure you want to proceed?</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-r">Yes</button></div>')
            + '</div>')


DRAFT_AUDIT = ('<p class="lms-new">New – waive-off and rejection entries (Waiver BRD). Not in the live LMS yet.</p>'
               '<table class="lms-table wv-audit"><thead><tr><th>Date &amp; Time</th><th>Action</th><th>Charges Name</th>'
               '<th class="num">Amount waived</th><th class="num">Balance</th><th>Note</th><th>By</th></tr></thead>'
               '<tbody><tr class="wv-a-empty"><td colspan="7">No waive-off or rejection yet.</td></tr></tbody></table>')


WAIVER_JS = """<script>
/* Draft loan Approvals tab (DISC-339). Tick a charge → amount to waive (≤ balance) → Waive-off → confirm → success.
   After a waive-off only the balance stays: a fully waived charge leaves the table, a partly waived one shows its balance.
   Each waive-off and the rejection are written to the Audit tab. Reject needs the reason (note) and the reconfirmation. */
(function () {
  var r2 = function (v) { return Math.round(v * 100) / 100; };
  var f = function (v) { return '₹' + r2(v).toLocaleString('en-IN', { maximumFractionDigits: 2 }); };
  var now = function () { var d = new Date(), p = function (x) { return String(x).padStart(2, '0'); };
    return p(d.getDate()) + '-' + p(d.getMonth() + 1) + '-' + d.getFullYear() + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()); };
  function calc(w) {
    var tw = 0, bal = 0, pend = 0;
    w.querySelectorAll('tbody tr').forEach(function (tr) {
      var a = tr.querySelector('.wv-amt'), max = +a.dataset.max, v = +a.value || 0;
      if (v > max) { a.value = max; v = max; } if (v < 0) { a.value = 0; v = 0; }
      tw += v; bal += max; tr.querySelector('.wv-pay').textContent = f(max - v);
      if (tr.querySelector('.wv-chk').checked && v > 0) pend++;
    });
    var after = bal - tw, orig = +w.dataset.orig;
    w.querySelector('.wv-ctot').textContent = f(bal); w.querySelector('.wv-wtot').textContent = f(tw); w.querySelector('.wv-ptot').textContent = f(after);
    var t = after <= 0 ? 'Full waive-off' : after < orig ? 'Partial waive-off' : 'No waive-off';
    w.querySelector('.wv-type b').textContent = t;
    w.querySelector('.wv-waive').disabled = !pend || w.classList.contains('closed');
    w.querySelector('.wv-allgone').hidden = !!w.querySelector('tbody tr');
    w.querySelector('.wv-table').hidden = !w.querySelector('tbody tr');
    return { tw: tw, tp: after, type: t };
  }
  function audit(w, cells) {
    var tb = w.closest('.lms-lanpage').querySelector('.wv-audit tbody'); if (!tb) return;
    var e = tb.querySelector('.wv-a-empty'); if (e) e.remove();
    var tr = document.createElement('tr');
    tr.innerHTML = cells.map(function (c, i) { return '<td' + (i === 3 || i === 4 ? ' class="num"' : '') + '></td>'; }).join('');
    cells.forEach(function (c, i) { tr.children[i].textContent = c; }); tb.prepend(tr);
  }
  var show = function (w, c, on) { w.querySelector(c).hidden = !on; };
  document.addEventListener('change', function (e) {
    var w = e.target.closest('.wv'); if (!w) return;
    if (e.target.classList.contains('wv-all'))
      w.querySelectorAll('tbody .wv-chk').forEach(function (c) { c.checked = e.target.checked; c.dispatchEvent(new Event('change', { bubbles: true })); });
    if (e.target.classList.contains('wv-chk')) { var a = e.target.closest('tr').querySelector('.wv-amt'); a.disabled = !e.target.checked; if (!e.target.checked) a.value = 0; }
    calc(w);
  });
  document.addEventListener('input', function (e) { var w = e.target.closest('.wv'); if (w && e.target.classList.contains('wv-amt')) calc(w); });
  document.addEventListener('click', function (e) {
    var w = e.target.closest('.wv'), c = e.target.classList; if (!w) return;
    if (c.contains('wv-x') || c.contains('wv-no') || c.contains('wv-ok')) e.target.closest('.wv-pop').hidden = true;
    if (c.contains('wv-waive')) show(w, '.wv-pw', true);
    if (c.contains('wv-yes-w')) {
      show(w, '.wv-pw', false); var n = 0, tot = 0, when = now(), note = w.querySelector('.wv-note').value.trim();
      w.querySelectorAll('tbody tr').forEach(function (tr) {
        var a = tr.querySelector('.wv-amt'), chk = tr.querySelector('.wv-chk'), max = +a.dataset.max, v = Math.min(+a.value || 0, max);
        if (!chk.checked || v <= 0) return;
        var left = r2(max - v); n++; tot += v;
        audit(w, [when, left > 0 ? 'Partial waive-off' : 'Full waive-off', tr.dataset.name, f(v), f(left), note || '–', 'OPS user']);
        if (left <= 0) { tr.remove(); return; }                       // fully waived – not shown again
        a.dataset.max = left; a.value = 0; a.disabled = true; chk.checked = false;
        tr.querySelector('.wv-chg').textContent = f(left);            // partly waived – only the balance is shown
      });
      w.querySelector('.wv-all').checked = false;
      var r = calc(w);
      w.querySelector('.wv-ps-txt').textContent = n + ' charge(s) waived off – ' + f(tot) + '. Balance payable ' + f(r.tp) + '. Recorded in the Audit tab.';
      show(w, '.wv-ps', true);
    }
    if (c.contains('wv-reject')) {
      var err = w.querySelector('.wv-err');
      if (!w.querySelector('.wv-note').value.trim()) { err.textContent = 'Please add the rejection reason in the note.'; return; }
      err.textContent = ''; show(w, '.wv-pr', true);
    }
    if (c.contains('wv-yes-r')) {
      show(w, '.wv-pr', false);
      w.querySelectorAll('tbody tr').forEach(function (tr) { tr.querySelector('.wv-chk').checked = false; tr.querySelector('.wv-amt').value = 0; });
      var q = calc(w); w.classList.add('closed');
      w.querySelectorAll('input, textarea, .wv-reject, .wv-waive').forEach(function (x) { x.disabled = true; });
      audit(w, [now(), 'Rejected', '–', '–', f(q.tp), w.querySelector('.wv-note').value.trim(), 'OPS user']);
      var d = w.querySelector('.wv-done'); d.hidden = false;
      d.innerHTML = '<b>Application rejected.</b> LAN status: REJECTED. Type of waive-off: <b>' + q.type + '</b>. ' +
        (q.tp > 0 ? 'Payable charges ' + f(q.tp) + ' – rejection SMS and mail with the payment link sent to the customer; de-pledge after payment and Treasury confirmation.'
                  : 'Nothing payable – rejection SMS and mail sent without a payment link; the units can be de-pledged now.');
      var st = w.closest('.lms-lanpage').querySelector('.lms-lanhead .lms-st'); st.textContent = 'Rejected'; st.className = 'lms-st st-rejected';
    }
  });
})();
</script>"""


def lan_detail(view, r):
    amt = _num(r["Sanction Amount"])
    live = view in ("active", "closed")
    disb = round(amt * 0.48 / 100) * 100 if (amt and live) else None
    dp = amt * 1.0003 if amt else None
    fields = [
        ("LSP", r["Source"]), ("Sanctioned Amount", _rs(amt)), ("Drawing Power", _rs(dp, True) if dp else "-"),
        ("Disbursed Amount", _rs(disb) if live else "-"),
        ("Repaid Amount", "₹0" if live else "-"), ("Principal Outstanding", _rs(disb) if live else "-"),
        ("Available for Disbursement", _rs(amt - disb) if (live and amt) else "-"),
        ("Utilized Drawing Power", f'<span class="ok">{disb / dp * 100:.2f}% ▲</span>' if (live and amt) else "-"),
        ("Repayments", '<span class="ok">On time</span>' if view == "active" else "-"), ("Deduction Date", "5th, Monthly"),
        ("Repayment Type", "Interest Only"), ("Disbursement Type", "Revolving"),
        ("Rate of Interest", r["Rate of Interest"]), ("Processing Fee", _rs(amt * 0.0187, True) if amt else "-"),
        ("Tenure", "36 months"), ("Product Name", f'<span class="lnk">{r["Product Id"]}</span>'),
        ("Application Start Date", r["Generated"]), ("Application Submitted Date", r["Generated"] if view not in ("draft", "inactive") else "-"),
        ("Loan Start Date", r["Start Date"]), ("Loan End Date", r["End Date"]),
    ]
    if view == "draft":   # as in the LMS draft loan page (DISC-330): nothing sanctioned yet
        D = dict(fields)
        for k in ("Sanctioned Amount", "Drawing Power", "Disbursed Amount", "Repaid Amount", "Principal Outstanding",
                  "Available for Disbursement", "Utilized Drawing Power", "Repayments", "Processing Fee",
                  "Application Submitted Date", "Loan Start Date", "Loan End Date"):
            D[k] = "-"
        D["Disbursement Type"], D["Tenure"] = "Multiple", "12 months"
        fields = list(D.items())
    fields = [(k, v + ' <i class="lms-i" title="Breakup">ⓘ</i>' if k == "Processing Fee" else v) for k, v in fields]
    grid = "".join(f'<div><span>{k}</span><b>{v}</b></div>' for k, v in fields)
    coll = "".join(f'<div><span>{k}</span><b>Collected: {c}<br>Due: ₹0<br>Overdue: ₹0</b></div>'
                   for k, c in [("Interest", "₹0"), ("Principal", "₹0"), ("Charges", _rs(amt * 0.0187, True) if (live and amt) else "₹0")])
    status = r.get("Status") or "Rejected"
    risk = f'<span class="lms-risk">{r["Risk Level"]}</span>' if view == "active" else ""
    tid = f'{view}-{r["LAN"]}'
    tab_list = TABS   # Draft: Approvals tab after Overview, as per the Waiver BRD (DISC-337, replaces DISC-330)
    tabs = "".join(f'<input type="radio" name="t-{tid}" id="t-{tid}-{k}"{" checked" if k == 0 else ""}>'
                   f'<label for="t-{tid}-{k}">{t}</label>' for k, t in enumerate(tab_list))
    panes = ('<div class="lms-pane p0"><div class="lms-card2"><h3>Loan Details</h3><div class="lms-grid">' + grid + '</div></div>'
             '<div class="lms-card2"><h3>Collection Details</h3><div class="lms-grid g3">' + coll + '</div></div></div>'
             + "".join(f'<div class="lms-pane p{k}">{draft_approvals(r, tid) if (view == "draft" and k == 1) else DRAFT_AUDIT if (view == "draft" and tab_list[k] == "Audit") else TBA}</div>'
                       for k in range(1, len(tab_list))))
    return (f'<section id="lan-{tid}" class="lms-sec lms-lanpage"><div class="lms-lanhead"><a class="lms-back" href="#m-loans-{view}" '
            f'title="Back to the list">←</a><h2>LAN Number: {r["LAN"]}</h2><span class="lms-st st-{status.lower()}">{status}</span>{risk}'
            f'<span class="lms-vs">View status</span></div><div class="lms-tabs">{tabs}{panes}</div>'
            '<p class="lms-sample">Sample data for the prototype – not real customers.</p></section>')


def lms_body(logo, home):
    nav, secs = [], []
    for mid, name, subs, desc in LMS_MODULES:
        nav.append(f'<a class="lms-nav-m" href="#m-{mid}">{_h.escape(name)}</a>')
        nav += [f'<a class="lms-nav-s" href="#m-{mid}-{sid}">{_h.escape(s)}</a>' for sid, s in subs]
        subs_html = ("<ul class='lms-subs'>" + "".join(f'<li><a href="#m-{mid}-{sid}">{_h.escape(s)}</a></li>' for sid, s in subs)
                     + "</ul>") if subs else ""
        secs.append(f'<section id="m-{mid}" class="lms-sec"><h2>{_h.escape(name)}</h2>{desc or TBA}{subs_html}</section>')
        secs += [f'<section id="m-{mid}-{sid}" class="lms-sec lms-list"><p class="lms-crumb">{_h.escape(name)} › {_h.escape(s)}</p>'
                 + (loan_view(sid) if mid == "loans" else f'<h2>{_h.escape(name)} – {_h.escape(s)}</h2>{TBA}') + '</section>' for sid, s in subs]
    # one detail section per sample LAN in every list (DISC-329)
    for v in ("active", "inactive", "draft", "submitted", "closed", "rejected"):
        secs += [lan_detail(v, r) for r in _rows(v)]
    intro = ('<section class="lms-intro"><h2>LMS – Loan Management System</h2>'
             '<p>The modules of the LMS, as in the left menu of the LMS. Choose a module to open it.</p>'
             '<div class="lms-cards">' + "".join(f'<a class="lms-card" href="#m-{mid}"><b>{_h.escape(n)}</b>'
                                                 + (f'<small>{", ".join(s for _, s in subs)}</small>' if subs else '') + '</a>'
                                                 for mid, n, subs, _ in LMS_MODULES) + '</div></section>')
    return (f'<div class="lms"><aside class="lms-side"><div class="lms-logo">{logo}</div>'
            f'<a class="lms-home" href="{home}">← Home</a><nav>{"".join(nav)}</nav></aside>'
            f'<main class="lms-main">{intro}{"".join(secs)}</main></div>' + WAIVER_JS)
