"""LMS PRD (DISC-535) – the requirements of the new LMS prototype (lms-app/*), written from the owner's UAT screenshots.
Source file: edit here, then run build_pages.py → writes LMS_PRD.html (generated, module "prd").
Status column: YTS / WIP / Completed – never set Completed without the owner's confirmation (same rule as the LOS PRD, DISC-086).
"""
import html

E = html.escape


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def content(items):   # "Screen Content" – every text shown on the screen
    return '<p class="lp-sc"><b>Screen Content:</b> ' + ' · '.join(f'“{E(t)}”' for t in items) + '</p>'


# (Sl. No, screen, prototype link, description (HTML), screen content list, status)
ROWS = [
    ('1', 'Login', 'lms-app/login.html',
     ul(['Only the LMS users can log in: opsmaker@shriramcredit.in (Maker), opschecker@shriramcredit.in (Checker), '
         'azhagarsamy.s@shriramcredit.in (Admin).',
         'Empty mail ID → “Please enter your email ID.”; not an @shriramcredit.in ID → “Please enter a valid Shriram Credit email ID '
         '(@shriramcredit.in).”; an SCCL ID that is not an LMS user → “This email ID does not have access to the LMS.” (wording to confirm).',
         'Send OTP sends a 6-digit OTP to the mail ID and opens the OTP step.']),
     ['Experience the simplicity of managing secured lending', 'Custom loan products with 30+ configurable parameters',
      'Real-time collateral tracking with automated risk alerts and thresholds',
      'Flexible digital, manual, and partner-assisted loan application workflows',
      'Role-based access with audit-ready security and governance controls', 'Login', 'Email ID', 'abc@shriramcredit.in', 'Send OTP'], 'WIP'),
    ('2', 'Login – OTP', 'lms-app/otp.html?mail=opsmaker%40shriramcredit.in',
     ul(['6 OTP boxes; typing moves to the next box, Backspace goes back, a pasted 6-digit OTP fills all boxes.',
         '30-second timer, then “Resend OTP” (to confirm with the UAT).',
         'Fewer than 6 digits → “Please enter the 6-digit OTP.”; wrong OTP → “Please enter the correct OTP.” and the boxes turn red.',
         'Correct OTP opens the Dashboard (prototype OTP: 000000).']),
     ['Login', '6-digit OTP has been sent to your Email Id', 'Resend OTP', 'Submit'], 'WIP'),
    ('3', 'OTP mail', 'lms-app/mail-otp.html?mail=opsmaker%40shriramcredit.in',
     ul(['Sent from noreply@shriramcredit.in to the entered mail ID with the subject “E-Mail Verification”, the OTP, a disclaimer and the footer.']),
     ['E-Mail Verification', 'OTP'], 'WIP'),
    ('4', 'Dashboard', 'lms-app/dashboard.html',
     ul(['Landing page after login. Left menu: Dashboard, Products, Loans (Active, Inactive, Draft, Submitted, Closed, Rejected), '
         'Collaterals, Clients, Approvals, Disbursement Management, Reports, Settings; the menu expands / collapses; profile pop-up with name, '
         'mail ID and Logout.',
         'Sections: Top level KPIs (MTD / MoM with sparklines), Risk Snapshot, Utilization, Collections, Top 10 Holdings, Top 10 LSPs; '
         'every chart shows a hover pop-up. A menu item not built yet opens the common Work in progress page.']),
     ['Last Updated', 'Top level KPIs', 'Risk Snapshot', 'Utilization', 'Collections', 'Coming Soon', 'Top 10 Holdings', 'Top 10 LSPs'], 'WIP'),
    ('5', 'Products – list', 'lms-app/products.html',
     ul(['Columns: Code, Loan Product (name entered; hover shows the full name), Status (Draft / In Review / Active / Inactive), '
         'Validity (dates chosen), Sanction Amount, Rate of Interest, Processing Fee (min – max from Terms; “-” until entered).',
         'A Draft opens Create a Product at its step; In Review / Active / Inactive open the product page. 10 rows per page.',
         '“+ Create a new product” (light blue-grey background on hover) opens Select security.']),
     ['Products', 'Create a new product', 'Code', 'Loan Product', 'Status', 'Validity', 'Sanction Amount', 'Rate of Interest',
      'Processing Fee', 'Showing 1 - 10 items', 'rows/page'], 'WIP'),
    ('6', 'Select security pop-up', 'lms-app/products.html',
     ul(['Loan Against Mutual Funds (default) / Loan Against Shares; Cancel / Confirm; ⊗ closes. Loan Against Mutual Funds → Create a Product.']),
     ['Select security', 'Loan Against Mutual Funds', 'Loan Against Shares', 'Cancel', 'Confirm'], 'WIP'),
    ('7', 'Create a Product – 1 Product Details', 'lms-app/create-product.html',
     ul(['Name of the Product and Description (letters, numbers and special characters allowed), Valid From (today), Valid Till (today + 10 years).',
         'Empty name + Next → “Product name is missing”. Next saves the product as a Draft with the next product code; the header shows '
         '“Draft Saved” (before the first save “Cannot Save Draft”).',
         '“Product Access Policy for LSPs – Update” opens Update Product Access Policy (Quicklend, Test, LARK, Liquify, SCCL LOS, Forward Wealth).',
         '← back keeps the edits of a saved draft. A finished step shows a blue tick; finished steps can be opened again.']),
     ['Create a Product', 'Draft Saved', 'Cannot Save Draft', 'Product Details', 'Disbursement Type', 'Terms', 'Charges', 'Collections', 'KYC',
      'Name of the Product', 'Description of the Product', 'Ex. Product Quicklend', 'Valid From', 'Valid Till',
      'Product Access Policy for LSPs', 'Update', 'Next'], 'WIP'),
    ('8', 'Create a Product – 2 Disbursement Type', 'lms-app/create-product.html',
     ul(['Revolving Overdraft (default) / Single Disbursement / Multiple Disbursement. The (i) opens a pop-up: Revolving Overdraft – '
         '“Withdrawal limit is restored when paid back”; Single – “Entire sanction amount is disbursed at once and withdrawal limit is not '
         'restored on repayment”; Multiple – “Sanction amount is disbursed multiple times and withdrawal limit is not restored on repayment”.']),
     ['Revolving Overdraft', 'Single Disbursement', 'Multiple Disbursement'], 'WIP'),
    ('9', 'Create a Product – 3 Terms', 'lms-app/create-product.html',
     ul(['Sanction Amount MIN / MAX (₹), Rate of Interest MIN / MAX (%), Tenure: Range (MIN / MAX months) or Discrete (type months + Enter '
         '→ chips such as 12, 24, 36), Processing Fee Min / Max (₹ or %).',
         'Empty → “Minimum sanction amount / rate of interest / tenure / processing fee is missing” (“Maximum … is missing” when only MIN is '
         'filled – to confirm); Discrete with no month → “Tenure is missing” (to confirm).']),
     ['Sanction Amount', 'Set minimum and maximum sanction amount', 'Rate of Interest', 'Set minimum and maximum rate of interest', 'Tenure',
      'Set minimum and maximum tenure (in months)', 'Discrete', 'Range', 'Type months and press Enter', 'Processing Fee',
      'Set the minimum and maximum PF', 'MIN', 'MAX', 'Type here'], 'WIP'),
    ('10', 'Create a Product – 4 Charges', 'lms-app/create-product.html',
     ul(['Renewal, Bounce, Bank Mandate Swap (in INR); Penal (% of defaulted amount), Liquidation (% of sale value), Prepayment (% of principal '
         'outstanding). All mandatory, 0 allowed. Empty → “Renewal charge is missing”, “Bounce charge is missing”, “Bank mandate swap is '
         'missing”, “Penal charge is missing”, “Liquidation charge is missing”, “Prepayment charge is missing”, and the header shows “Cannot Save Draft”.']),
     ['Renewal Charges', 'Bounce Charges', 'Bank Mandate Swap Charges', 'Penal Charges', 'Liquidation Charges', 'Prepayment Charges', 'in INR',
      '% of defaulted amount', '% of sale value', '% of principal outstanding'], 'WIP'),
    ('11', 'Create a Product – 5 Collections', 'lms-app/create-product.html',
     ul(['Maximum amount for mandate: Sanction Amount / Multiple of Loan Amount (Enter the Amount, Ex. 2X) / Absolute Value (₹, Ex. ₹2,00,000).',
         'Repayment Type: Fully Amortized and / or Balloon Type (shown as “Interest Only”); Frequency: Monthly + day of the month (Date); '
         'Processing Fee: 1st Disbursement (default) / 1st Collection.',
         'Errors: “Maximum Mandate Amount is missing”, Type “Required Field”, Frequency “Required field”.']),
     ['Maximum amount for mandate', 'Enter the Amount', 'Repayment', 'Type', 'Fully Amortized', 'Balloon Type', 'Frequency', 'Monthly', 'Date',
      'Processing Fee', '1st Disbursement', '1st Collection'], 'WIP'),
    ('12', 'Create a Product – 6 KYC and Submit', 'lms-app/create-product.html',
     ul(['PAN and Aadhaar ticked and locked; Liveness optional. Submit → “Product creation successful”, status In Review, a change request '
         '(Request ID) is raised for approval and the page returns to Products.']),
     ['PAN', 'Aadhaar', 'Liveness', 'Submit', 'Product creation successful'], 'WIP'),
    ('13', 'Product details page', 'lms-app/product-view.html?code=LAMF20261102',
     ul(['Name, status pill, Validity, description; tabs Product Details / Documents (“No preview documents available”); cards Product Details, '
         'KYC Requirements, Charges.',
         'Active: ≡ → Update Access Policy (LSP toggles save at once; LSPs with access listed first). Inactive / In Review: ≡ greyed.',
         'In Review: “Change: Product Creation”, Request ID, Initiated By / On; Reject / Approve bar only for In Review. The maker sees them '
         'greyed with “Maker cannot check”.']),
     ['Product Details', 'Documents', 'Update Access Policy', 'Update Product Access Policy', 'LSP Name', 'LSP Access', 'Cancel',
      'Change: Product Creation', 'Request ID', 'Initiated By', 'Initiated On', 'Reject', 'Approve', 'Maker cannot check'], 'WIP'),
    ('14', 'Approvals', 'lms-app/approvals.html',
     ul(['My Pending Approvals (requests of others, for Checker / Admin; empty: “No actions pending for your approval”) and All Approvals.',
         'Columns: Date of Change, Change Type (filter list of all change types, all ticked), Details (Product / ID), Permitted Roles '
         '(Ops_L2, Ops_L3, Admin, UpdateProductCreationTasks), Initiated By. “Product creation” opens the request.']),
     ['My Pending Approvals', 'All Approvals', 'Date of Change', 'Change Type', 'Details', 'Permitted Roles', 'Initiated By',
      'No actions pending for your approval'], 'WIP'),
    ('15', 'Checker approval', 'lms-app/approvals.html',
     ul(['Upload a file (optional; PDF, PNG or JPG, max 5 MB) and Add a note (mandatory – “Note is required”).',
         'Approve / Reject → “This action is irreversible. Are you sure you want to proceed?” No / Yes. Approve → Yes: “Approved successfully”, '
         'the product becomes Active and leaves the approval list. Reject result: to be shared.']),
     ['Upload a file', 'Drop files here or click', 'PDF, PNG or JPG. Max 5MB', 'Add a note', 'Note is required',
      'This action is irreversible. Are you sure you want to proceed?', 'No', 'Yes', 'Approved successfully'], 'WIP'),
]

RULES = [
    ('Product code', 'LAMF + year (4 digits) + month (2 digits) + running number of the product in that month (2 digits; 3 digits after 99). '
     'Example: LAMF20261104 = the 4th product created in November 2026.'),
    ('User roles', 'Maker creates products; Checker approves; Admin (ignored for now) may also approve. Nobody approves a request they raised.'),
    ('Status flow', 'Draft (until all 6 steps are submitted) → In Review (waiting for the checker) → Active (approved) / Inactive.'),
]

LOS = [
    'A product becomes visible on the LOS Curated offers page only when it is Active and “SCCL LOS” is switched on in its Update Product '
    'Access Policy; it is shown as its own offer card (Interest Rate = the product’s minimum rate, Tenure = its tenure).',
    'LOS Application summary for that product: Tenure (in months) lists every month from MIN to MAX for a Range product, or only the set months '
    'for a Discrete product; Repayment Type is a drop-down when both Interest Only and Fully Amortized are allowed; Revolving shows as “Line of Credit”.',
]

OPEN = [
    'Reject flow after Yes (message, status) – screenshot awaited.',
    'Login message for an SCCL ID that is not an LMS user; Resend OTP behaviour.',
    'Terms: “Maximum … is missing” and “Tenure is missing” wording; error when MIN is more than MAX.',
    'Collections: mandate default option; repayment check boxes default; days offered in the Date picker.',
    'Default tenure on the LOS Application summary (the prototype selects the maximum).',
    'Permitted Roles filter list on Approvals.',
]

CSS = """<style>
.lp { max-width: 1180px; margin: 0 auto; padding: 18px 16px 60px; }
.lp h1 { font-size: 28px; margin: 10px 0 4px; } .lp h2 { font-size: 20px; margin: 30px 0 10px; }
.lp-meta { color: #555; font-size: 14px; margin: 0 0 18px; }
.lp table { width: 100%; border-collapse: collapse; font-size: 14px; }
.lp th, .lp td { border: 1px solid #ddd; padding: 9px 10px; vertical-align: top; text-align: left; }
.lp th { background: #FFC20E; }
.lp ul { margin: 0; padding-left: 18px; list-style: disc; } .lp li { margin: 0 0 4px !important; padding: 0 !important; border: 0 !important; background: none !important; box-shadow: none !important; border-radius: 0 !important; display: list-item !important; }
.lp a { color: #1f5fbf; }
.lp-sc { margin: 8px 0 0; color: #333; font-size: 13px; }
.lp-st { display: inline-block; padding: 2px 8px; border-radius: 6px; background: #fff4e5; color: #8a5300; font-weight: 600; font-size: 12px; }
.lp-wrap { overflow-x: auto; }
@media (max-width: 700px) { .lp h1 { font-size: 22px; } }
</style>"""


def body(logo, updated):
    rows = ''.join(
        f'<tr id="lms-{n}"><td>{n}</td><td><b>{E(t)}</b><br><a href="{E(link)}">Open the screen →</a></td>'
        f'<td>{d}{content(sc)}</td><td><span class="lp-st">{st}</span></td></tr>'
        for n, t, link, d, sc, st in ROWS)
    rules = ''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>' for a, b in RULES)
    return (CSS + logo + '<main class="lp">'
            '<h1>LMS – Product Requirements (PRD)</h1>'
            f'<p class="lp-meta">Loan Management System · Loan Against Mutual Funds · Status: WIP · Last updated: {updated} · '
            'Written from the UAT screenshots; sample data only. <a href="lms-screens.html">LMS screens →</a></p>'
            '<h2>1. Screens</h2><div class="lp-wrap"><table><thead><tr><th style="width:52px">Sl. No</th><th style="width:210px">Screen</th>'
            f'<th>Description and rules</th><th style="width:90px">Status</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<h2>2. Rules</h2><div class="lp-wrap"><table><tbody>{rules}</tbody></table></div>'
            '<h2>3. Impact on the LOS journey</h2>' + ul([E(x) for x in LOS]) +
            '<h2>4. Open points</h2>' + ul([E(x) for x in OPEN]) +
            '</main>')
