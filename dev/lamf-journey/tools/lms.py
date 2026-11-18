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


def _rows(view):
    n = {"active": 10, "inactive": 10, "draft": 10, "submitted": 5, "closed": 2, "rejected": 2}[view]
    status = {"active": "Active", "inactive": "Inactive", "draft": "Draft", "submitted": "Submitted", "closed": "Foreclosed"}.get(view)
    out = []
    for k in range(n):
        d = 17 - k // 2
        r = {"LAN": f"SCCLMF202611000{60 - k:02d}", "Product Id": _PROD[k], "Client Name": _NAMES[k], "Status": status,
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
    intro = ('<section class="lms-intro"><h2>LMS – Loan Management System</h2>'
             '<p>The modules of the LMS, as in the left menu of the LMS. Choose a module to open it.</p>'
             '<div class="lms-cards">' + "".join(f'<a class="lms-card" href="#m-{mid}"><b>{_h.escape(n)}</b>'
                                                 + (f'<small>{", ".join(s for _, s in subs)}</small>' if subs else '') + '</a>'
                                                 for mid, n, subs, _ in LMS_MODULES) + '</div></section>')
    return (f'<div class="lms"><aside class="lms-side"><div class="lms-logo">{logo}</div>'
            f'<a class="lms-home" href="{home}">← Home</a><nav>{"".join(nav)}</nav></aside>'
            f'<main class="lms-main">{intro}{"".join(secs)}</main></div>')
