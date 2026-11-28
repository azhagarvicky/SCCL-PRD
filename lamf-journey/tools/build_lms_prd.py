# Builds LMS_PRD.html – the LMS Product Requirements Document, in the same format as the LOS PRD (build_prd.py, DISC-536):
# Module → Sl. No (one row per screen) → field-by-field specification with screenshots, Screen Content, Data Points and Status.
# Written from the owner's UAT screenshots of the LMS; the screenshots are taken from the LMS prototype (sample data only) by
# tools/lms_prd_shots.js → prd-assets/lms/*.png. Run: python3 tools/build_lms_prd.py (build_pages.py also runs it).
# Status: YTS / WIP / Completed – a row becomes Completed only when the owner confirms it (DISC-086); a Completed row is frozen.
import os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')


# ---- helpers (same as the LOS PRD) ----------------------------------------------------------------------------------------
def spec(**kw):
    order = ['Field Name', 'Field Type', 'Minimum Character', 'Maximum Character', 'Value Type', 'Input Value format',
             'Prefilled Value', 'Action', 'Condition', 'Validation', 'Note']
    rows = []
    for label in order:
        key = label.replace(' ', '_')
        if kw.get(key):
            v = kw[key]
            if isinstance(v, list):
                v = '<ul>' + ''.join(f'<li>{x}</li>' for x in v) + '</ul>'
            rows.append(f'<p><b>{label}:</b> {v}</p>')
    return '<div class="spec">' + ''.join(rows) + '</div>'


def screen_content(items):
    rows = ''.join(f'<li><b>{k}:</b> {v}</li>' for k, v in items)
    return f'<div class="spec"><p><b>Screen Content:</b></p><ul class="content-list">{rows}</ul></div>'


def data_points(html_):
    out = []
    for seg in html_.split('<br>'):
        m = re.match(r'^([^:<]{1,60}):(?:\s+(.*))?$', seg, re.S)
        out.append(f'<b>{m.group(1)}:</b> {m.group(2) or ""}' if m else seg)
    return '<br>'.join(out)


def pend(*ids):
    js = ("var t=document.getElementById('{p}');if(t){{t.scrollIntoView({{behavior:'smooth',block:'center'}});"
          "t.classList.remove('flash');void t.offsetWidth;t.classList.add('flash')}}return false")
    return ' '.join(f'<a class="pend-ref" href="#{p}" onclick="{js.format(p=p)}" title="Open pending clarification {p}">Pending · {p}</a>' for p in ids)


def img(src):
    return f'<img src="prd-assets/lms/{src}.png" alt="">'


def states(*pairs):
    return ''.join(f'<figure class="state">{img(src)}<figcaption>{cap}</figcaption></figure>' for src, cap in pairs)


YTS, WIP, DONE = 'YTS', 'WIP', 'Completed'
OK = WIP
TAG = {YTS: 'yts', WIP: 'wip', DONE: 'ok'}
RED = ' When an error is shown for this field, its border turns red.'
TS = 'DD-MMM-YYYY; HH:MM:SS'

# ---- PRD content ------------------------------------------------------------------------------------------------------------
MODULES = [
 {
  'title': 'Module 1 – Login',
  'screens': 'Login · Login – OTP · OTP mail',
  'rows': [
    {
      'sl': '1', 'shot': img('l01-login'),
      'func': 'LMS user entering the SCCL mail ID to log in',
      'desc': ('<p>The LMS opens on the Login page: the left half shows the product message, four feature lines and a preview of the LMS; '
               'the right half shows the Login card. Only the LMS users can log in – Maker (opsmaker@shriramcredit.in), Checker '
               '(opschecker@shriramcredit.in) and Admin (azhagarsamy.s@shriramcredit.in).</p>'
               + screen_content([
                   ('Heading', '“Experience the simplicity of managing secured lending”'),
                   ('Feature lines', '“Custom loan products with 30+ configurable parameters” · “Real-time collateral tracking with automated risk alerts and thresholds” · “Flexible digital, manual, and partner-assisted loan application workflows” · “Role-based access with audit-ready security and governance controls”'),
                   ('Card title', '“Login”'), ('Field label', '“Email ID”'), ('Placeholder', '“abc@shriramcredit.in”'), ('CTA', '“Send OTP”'),
                   ('Validation messages', '“Please enter your email ID.” · “Please enter a valid Shriram Credit email ID (@shriramcredit.in).” · “This email ID does not have access to the LMS.” ' + pend('LP-01')),
               ])),
      'data': f'Email ID: opsmaker@shriramcredit.in<br><br>Send OTP clicked on:<br>{TS}',
      'status': WIP,
      'fields': [
        (img('l01-mail'), spec(Field_Name='Email ID', Field_Type='Text Field', Maximum_Character='120 Char', Value_Type='User inputs',
            Input_Value_format='Mail ID ending with @shriramcredit.in (not case sensitive)',
            Action='User enters the SCCL mail ID.',
            Validation=['“Please enter your email ID.” – Send OTP clicked with the field empty',
                        '“Please enter a valid Shriram Credit email ID (@shriramcredit.in).” – not a valid @shriramcredit.in mail ID',
                        '“This email ID does not have access to the LMS.” – an SCCL mail ID that is not an LMS user ' + pend('LP-01')]) + '<p>' + RED + '</p>', OK),
        (states(('l01-err-empty', 'Empty mail ID'), ('l01-err-bad', 'Not an SCCL mail ID'), ('l01-err-none', 'SCCL mail ID without LMS access')),
         spec(Field_Name='Validation message', Field_Type='Text (red, below the field)', Action='Shown on Send OTP; cleared as soon as the user types again.'), OK),
        (img('l01-send'), spec(Field_Name='Send OTP', Field_Type='CTA (Button)',
            Action='Validates the mail ID; when valid, sends a 6-digit OTP to that mail ID and opens the Login – OTP screen.'), OK),
      ],
    },
    {
      'sl': '2', 'shot': img('l02-otp'),
      'func': 'LMS user entering the 6-digit OTP received on the mail ID',
      'desc': ('<p>The Login card changes to the OTP step and shows the mail ID the OTP was sent to.</p>'
               + screen_content([
                   ('Back', '← (returns to Login)'), ('Title', '“Login”'), ('Sent message', '“6-digit OTP has been sent to your Email Id” followed by the mail ID in quotes'),
                   ('OTP boxes', '6 single-digit boxes'), ('Resend line', '“Didn’t receive OTP?” with a 30-second timer (0:29 … 0:01), then “Resend OTP” ' + pend('LP-02')),
                   ('CTA', '“Submit”'), ('Validation messages', '“Please enter the 6-digit OTP.” · “Please enter the correct OTP.”'),
               ])),
      'data': f'OTP entered: 6 digit numeric<br><br>OTP verified:<ul><li>Yes</li><li>No</li></ul><br>Logged in on:<br>{TS}',
      'status': WIP,
      'fields': [
        (img('l02-back'), spec(Field_Name='← Back', Field_Type='Icon', Action='Returns to the Login screen.'), OK),
        (img('l02-boxes'), spec(Field_Name='OTP', Field_Type='6 single-digit boxes', Minimum_Character='6', Maximum_Character='6', Value_Type='User inputs',
            Input_Value_format='Numeric only',
            Action='Typing a digit moves to the next box; Backspace moves back; a pasted 6-digit OTP fills all boxes.'), OK),
        (img('l02-timer'), spec(Field_Name='Resend OTP', Field_Type='Timer, then link',
            Action='A 30-second timer runs; then “Resend OTP” sends a new OTP and restarts the timer. ' + pend('LP-02')), OK),
        (states(('l02-err-short', 'Fewer than 6 digits'), ('l02-err-wrong', 'Wrong OTP – boxes and digits turn red')),
         spec(Field_Name='Submit', Field_Type='CTA (Button)',
            Action='Verifies the OTP. Correct OTP → the user lands on the Dashboard.',
            Validation=['“Please enter the 6-digit OTP.” – fewer than 6 digits', '“Please enter the correct OTP.” – wrong OTP; the boxes turn red'],
            Note='Prototype OTP: 000000.'), OK),
      ],
    },
    {
      'sl': '3', 'shot': img('l03-mail'),
      'func': 'OTP mail received by the LMS user',
      'desc': ('<p>The system sends the OTP mail to the entered mail ID.</p>'
               + screen_content([('From', 'noreply@shriramcredit.in'), ('Band', '“E-Mail Verification”'), ('Body', 'the 6-digit OTP, a disclaimer and the © footer')])),
      'data': f'Mail sent to: the entered mail ID<br><br>Sent on:<br>{TS}',
      'status': WIP,
    },
  ],
 },
 {
  'title': 'Module 2 – Dashboard',
  'screens': 'Dashboard · Left menu · Profile pop-up',
  'rows': [
    {
      'sl': '4', 'shot': img('l04-dashboard'),
      'func': 'LMS user viewing the portfolio dashboard after login',
      'desc': ('<p>Every LMS user lands on the Dashboard after login. All values in the prototype are sample values.</p>'
               + screen_content([
                   ('Top bar', '“Last Updated: DD-MM-YYYY HH:MM:SS” (stays on top while scrolling)'),
                   ('Sections', '“Top level KPIs” · “Risk Snapshot” · “Utilization” · “Collections” (with “Coming Soon” cards) · “Top 10 Holdings” · “Top 10 LSPs”'),
               ])),
      'data': 'Dashboard data as on: Last Updated date and time',
      'status': WIP,
      'fields': [
        (img('l04-kpis'), spec(Field_Name='Top level KPIs', Field_Type='Cards with sparklines',
            Action='Each card shows the value, MTD and MoM change; hovering the sparkline shows the date and value.'), OK),
        (states(('l04-menu', 'Collapsed (default)'), ('l04-menu-wide', 'Expanded')), spec(Field_Name='Left menu', Field_Type='Navigation',
            Action='Dashboard, Products, Loans (Active, Inactive, Draft, Submitted, Closed, Rejected), Collaterals, Clients, Approvals, Disbursement Management, Reports, Settings. The arrow expands / collapses the menu; the open page is highlighted. A page not built yet opens the common Work in progress page.'), OK),
        (img('l04-profile'), spec(Field_Name='Profile pop-up', Field_Type='Pop-up',
            Action='The profile icon opens the user’s name and mail ID and “Logout”; each row is greyed on hover; Logout returns to the Login page.'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 3 – Products',
  'screens': 'Products list · Select security · Product details (Active / Inactive / In Review) · Update Access Policy',
  'rows': [
    {
      'sl': '5', 'shot': img('l05-products'),
      'func': 'LMS user viewing the list of loan products',
      'desc': ('<p>Menu Products opens the list of every loan product, newest first.</p>'
               + screen_content([('Title', '“Products”'), ('CTA', '“+ Create a new product”'),
                   ('Columns', '“Code” · “Loan Product” · “Status” · “Validity” · “Sanction Amount” · “Rate of Interest” · “Processing Fee”'),
                   ('Status values', '“Draft” (grey) · “In Review” (orange) · “Active” (green) · “Inactive” (red)'),
                   ('Pager', '“Showing 1 - 10 items” · “10 rows/page” · ‹ ›')])),
      'data': 'Code: LAMF20261103<br>Loan Product: TEST Product SCCL<br>Status: Draft / In Review / Active / Inactive<br>Validity: DD/MM/YYYY - DD/MM/YYYY<br>Sanction Amount: ₹min - ₹max<br>Rate of Interest: min% - max%<br>Processing Fee: min - max (₹ or %)',
      'status': WIP,
      'fields': [
        (img('l05-head'), spec(Field_Name='Product list columns', Field_Type='Table',
            Action='Code = LAMF + year (4 digits) + month (2 digits) + running number of the product in that month (2 digits, 3 after 99); Loan Product = the name entered (hover shows the full name); Validity = the dates chosen; Sanction Amount, Rate of Interest, Processing Fee = the min – max set in Terms (“-” until set).',
            Condition='A Draft row opens Create a Product at its step; an In Review / Active / Inactive row opens the product details page.'), OK),
        (states(('l05-new', 'Default'), ('l05-new-hover', 'Hover – light blue-grey background')), spec(Field_Name='+ Create a new product', Field_Type='CTA (Link)',
            Action='Opens the Select security pop-up.'), OK),
        (img('l05-pager'), spec(Field_Name='Pager', Field_Type='Pagination', Action='10 rows per page; ‹ › move between pages (disabled when there is no other page).'), OK),
      ],
    },
    {
      'sl': '6', 'shot': img('l06-security'),
      'func': 'LMS user choosing the security type of the new product',
      'desc': ('<p>The Select security pop-up opens over the Products list.</p>'
               + screen_content([('Title', '“Select security”'), ('Options', '“Loan Against Mutual Funds” (selected by default) · “Loan Against Shares”'), ('CTAs', '“Cancel” · “Confirm”'), ('Close', '⊗')])),
      'data': 'Security type:<ul><li>Loan Against Mutual Funds</li><li>Loan Against Shares</li></ul>',
      'status': WIP,
      'fields': [
        (img('l06-modal'), spec(Field_Name='Security type', Field_Type='Radio buttons', Prefilled_Value='Loan Against Mutual Funds',
            Action='Confirm with Loan Against Mutual Funds opens Create a Product (Module 4). Cancel / ⊗ / a click outside / Esc closes the pop-up.',
            Note='Loan Against Shares is not built yet in the prototype.'), OK),
      ],
    },
    {
      'sl': '7', 'shot': img('l07-active'),
      'func': 'LMS user viewing an Active product',
      'desc': ('<p>The product details page of an Active product.</p>'
               + screen_content([('Header', 'Product name, status pill “Active”, “Validity: DD/MM/YYYY - DD/MM/YYYY”, description'),
                   ('Tabs', '“Product Details” · “Documents”'),
                   ('Product Details card', '“Disbursement Type” · “Sanction Amount” · “Rate of Interest” · “Tenure” · “Processing Fee” · “Maximum Mandate Amount” · “Repayment Type” · “Repayment Frequency” · “Collection of PF” · “Access Policy”'),
                   ('KYC Requirements card', '“Bank” · “Personal Details” · “Phone” · “Email” · “PAN” · “Aadhaar” · “Photo”'),
                   ('Charges card', '“Renewal Charges” · “Bounce Charges” · “Penal Charges” · “Liquidation Charges” · “Prepayment Charges” · “Bank Mandate Swap Charges”'),
                   ('Documents tab', '“No preview documents available”'), ('Menu', '≡ → “Update Access Policy”')])),
      'data': 'All values as set in Create a Product (Module 4)',
      'status': WIP,
      'fields': [
        (img('l07-tabs'), spec(Field_Name='Product Details / Documents', Field_Type='Tabs', Prefilled_Value='Product Details',
            Action='Switches between the product details and its documents (“No preview documents available” when there are none).'), OK),
        (img('l07-menu'), spec(Field_Name='≡ Menu', Field_Type='Icon (menu)', Action='Opens “Update Access Policy”.',
            Condition='Clickable only for an Active product; grey and not clickable for Inactive and In Review.'), OK),
        (states(('l16-policy-all', 'New product – every LSP off'), ('l16-policy-los', 'SCCL LOS switched on – listed first')),
         spec(Field_Name='Update Product Access Policy', Field_Type='Pop-up with toggles',
            Action='Lists the LSPs (Quicklend, Test, LARK, Liquify, SCCL LOS, Forward Wealth) with an access toggle each; a toggle saves at once; LSPs with access are listed first. Cancel / ⊗ closes.',
            Condition='SCCL LOS on → the product is offered on the LOS Curated offers page (INT-L01).'), OK),
      ],
    },
    {
      'sl': '7.1', 'shot': img('l07-inactive'),
      'func': 'LMS user viewing an Inactive product',
      'desc': '<p>Same page as Sl. No 7 with the red “Inactive” pill; the ≡ menu is grey and cannot be clicked; no Reject / Approve bar.</p>',
      'data': 'Status: Inactive', 'status': WIP,
    },
    {
      'sl': '7.2', 'shot': img('l07-inreview'),
      'func': 'LMS user viewing a product In Review',
      'desc': '<p>Same page as Sl. No 7 with the orange “In Review” pill and the Reject / Approve bar at the bottom (only for In Review). For a new product the change request block is shown on top (Sl. No 14).</p>',
      'data': 'Status: In Review', 'status': WIP,
      'fields': [
        (img('l07-inreview-foot'), spec(Field_Name='Reject / Approve', Field_Type='CTA (Buttons)', Condition='Shown only for In Review; greyed for the user who raised the request (Sl. No 14); active for a Checker / Admin (Sl. No 15).'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 4 – Create a Product',
  'screens': 'Step 1 Product Details · 2 Disbursement Type · 3 Terms · 4 Charges · 5 Collections · 6 KYC',
  'rows': [
    {
      'sl': '8', 'shot': img('l08-step1'),
      'func': 'Maker entering the product name, description and validity',
      'desc': ('<p>Create a Product opens on step 1. The six steps are listed on the left; a finished step shows a blue tick and can be opened again.</p>'
               + screen_content([('Header', '“← Create a Product” and the draft status “Cannot Save Draft” / “Draft Saved”'),
                   ('Steps', '“Product Details” · “Disbursement Type” · “Terms” · “Charges” · “Collections” · “KYC”'),
                   ('Fields', '“Name of the Product” · “Description of the Product” (placeholder “Ex. Product Quicklend”) · “Valid From” · “Valid Till”'),
                   ('Link', '“Product Access Policy for LSPs” “Update”'), ('CTA', '“Next”'), ('Validation message', '“Product name is missing”')])),
      'data': 'Name of the Product: TEST Product SCCL<br>Description of the Product: This is Testing Creation<br>Valid From: DD/MM/YYYY<br>Valid Till: DD/MM/YYYY<br><br>Draft saved on:<br>' + TS,
      'status': WIP,
      'fields': [
        (img('l08-steps'), spec(Field_Name='Steps', Field_Type='Step list',
            Action='The open step has a blue border; a finished step shows a blue tick; finished steps and the next one can be clicked.'), OK),
        (states(('l08-nodraft', 'Before the first save'), ('l08-draft', 'After Next on step 1')), spec(Field_Name='Draft status', Field_Type='Text with cloud icon',
            Action='“Cannot Save Draft” until the product is first saved (and when a step has errors); “Draft Saved” after each saved step.'), OK),
        (img('l08-err-name'), spec(Field_Name='Name of the Product', Field_Type='Text Field', Maximum_Character='80 Char', Value_Type='User inputs',
            Input_Value_format='Letters, numbers and special characters',
            Validation=['“Product name is missing” – Next clicked with the name empty (shown next to the label)']), OK),
        ('', spec(Field_Name='Description of the Product', Field_Type='Text Field', Maximum_Character='200 Char', Value_Type='User inputs',
            Input_Value_format='Letters, numbers and special characters', Note='Not mandatory. Shown under the validity on the product page.'), OK),
        (img('l08-dates'), spec(Field_Name='Valid From / Valid Till', Field_Type='Date pickers', Input_Value_format='DD/MM/YYYY',
            Prefilled_Value='Valid From = today; Valid Till = today + 10 years'), OK),
        (states(('l08-policy', 'Link'), ('l08-policy-pop', 'Pop-up')), spec(Field_Name='Product Access Policy for LSPs – Update', Field_Type='Link → pop-up',
            Action='Opens Update Product Access Policy with every LSP off (same pop-up as Sl. No 7).'), OK),
        ('', spec(Field_Name='Next', Field_Type='CTA (Button)',
            Action='Saves the product as a Draft – the first time it gets the next product code – and opens step 2.',
            Note='← Create a Product returns to Products and keeps what was typed in a saved draft.'), OK),
      ],
    },
    {
      'sl': '9', 'shot': img('l09-step2'),
      'func': 'Maker choosing the disbursement type',
      'desc': ('<p>Step 2 – one disbursement type per product.</p>'
               + screen_content([('Options', '“Revolving Overdraft” (default) · “Single Disbursement” · “Multiple Disbursement”, each with (i)'),
                   ('Info pop-ups', '“Withdrawal limit is restored when paid back” · “Entire sanction amount is disbursed at once and withdrawal limit is not restored on repayment” · “Sanction amount is disbursed multiple times and withdrawal limit is not restored on repayment”')])),
      'data': 'Disbursement Type:<ul><li>Revolving Overdraft</li><li>Single Disbursement</li><li>Multiple Disbursement</li></ul>',
      'status': WIP,
      'fields': [
        (img('l09-radios'), spec(Field_Name='Disbursement Type', Field_Type='Radio buttons', Prefilled_Value='Revolving Overdraft'), OK),
        (states(('l09-info-ro', 'Revolving Overdraft'), ('l09-info-single', 'Single Disbursement'), ('l09-info-multi', 'Multiple Disbursement')),
         spec(Field_Name='(i)', Field_Type='Icon → info pop-up', Action='Opens the explanation of that type; a click outside or Esc closes it; it does not change the selection.'), OK),
      ],
    },
    {
      'sl': '10', 'shot': img('l10-terms'),
      'func': 'Maker entering the sanction amount, rate of interest, tenure and processing fee ranges',
      'desc': ('<p>Step 3 – every value is entered as a minimum and a maximum.</p>'
               + screen_content([('Rows', '“Sanction Amount” “Set minimum and maximum sanction amount” · “Rate of Interest” “Set minimum and maximum rate of interest” · “Tenure” “Set minimum and maximum tenure (in months)” · “Processing Fee” “Set the minimum and maximum PF”'),
                   ('Placeholders', '“Ex. 1Cr” · “Ex. 2Cr” · “Ex. 9.49” · “Ex. 10.59” · “Ex. 3 months” · “Ex. 36 months” · “Type months and press Enter” · “Type here”'),
                   ('Validation messages', '“Minimum sanction amount is missing” · “Minimum rate of interest is missing” · “Minimum tenure is missing” · “Minimum processing fee is missing” (“Maximum … is missing” and “Tenure is missing” ' + pend('LP-03') + ')')])),
      'data': 'Sanction Amount: ₹10,000 - ₹2,00,00,000<br>Rate of Interest: 11% - 11%<br>Tenure type: Range / Discrete<br>Tenure: 12 - 36 months, or 12, 24, 36<br>Processing Fee: ₹1,499 - 1%',
      'status': WIP,
      'fields': [
        (img('l10-row1'), spec(Field_Name='Sanction Amount – MIN / MAX', Field_Type='Number fields (₹)', Value_Type='User inputs', Input_Value_format='Numeric',
            Validation=['“Minimum sanction amount is missing” / “Maximum sanction amount is missing”']), OK),
        (img('l10-row2'), spec(Field_Name='Rate of Interest – MIN / MAX', Field_Type='Number fields (%)', Value_Type='User inputs', Input_Value_format='Numeric with decimals',
            Validation=['“Minimum rate of interest is missing” / “Maximum rate of interest is missing”']), OK),
        (states(('l10-tenure-open', 'Tenure type list'), ('l10-row3', 'Range – MIN / MAX months'), ('l10-discrete', 'Discrete – months as chips')),
         spec(Field_Name='Tenure', Field_Type='Drop-down + fields', Prefilled_Value='Range',
            Action='Range: MIN and MAX months – the LOS offers every month in between. Discrete: type a month and press Enter to add it as a chip (⊗ or Backspace removes; numbers only, no duplicates) – the LOS offers only these months.',
            Validation=['“Minimum tenure is missing” / “Maximum tenure is missing” (Range)', '“Tenure is missing” (Discrete, no month added) ' + pend('LP-03')]), OK),
        (img('l10-row4'), spec(Field_Name='Processing Fee – Min / Max', Field_Type='Drop-down (₹ / %) + number field', Prefilled_Value='₹',
            Validation=['“Minimum processing fee is missing” / “Maximum processing fee is missing”']), OK),
        (img('l10-terms-err'), spec(Field_Name='Next', Field_Type='CTA (Button)',
            Action='Moves to step 4 only when every box is filled; empty boxes get a red border and the message under their row.'), OK),
      ],
    },
    {
      'sl': '11', 'shot': img('l11-charges'),
      'func': 'Maker entering the charges',
      'desc': ('<p>Step 4 – every charge is mandatory; 0 is accepted.</p>'
               + screen_content([('Fields', '“Renewal Charges” (in INR, “Ex. 1000”) · “Bounce Charges” (in INR, “Ex. 100”) · “Bank Mandate Swap Charges” (in INR, “Ex. 1000”) · “Penal Charges” (% of defaulted amount, “Ex. 2”) · “Liquidation Charges” (% of sale value, “Ex. 2”) · “Prepayment Charges” (% of principal outstanding, “Ex. 2”)'),
                   ('Validation messages', '“Renewal charge is missing” · “Bounce charge is missing” · “Bank mandate swap is missing” · “Penal charge is missing” · “Liquidation charge is missing” · “Prepayment charge is missing”')])),
      'data': 'Renewal Charges: ₹999<br>Bounce Charges: ₹100<br>Bank Mandate Swap Charges: ₹250<br>Penal Charges: 36%<br>Liquidation Charges: 0%<br>Prepayment Charges: 0%',
      'status': WIP,
      'fields': [
        (states(('l11-charges-err', 'Next with empty fields'), ('l11-cannot', 'Draft status with errors')), spec(Field_Name='Charge fields', Field_Type='Number fields',
            Value_Type='User inputs', Input_Value_format='Numeric (₹ for the INR charges, % for the others)',
            Validation=['The field’s “… is missing” message under its label; the header shows “Cannot Save Draft”']), OK),
      ],
    },
    {
      'sl': '12', 'shot': img('l12-collections'),
      'func': 'Maker setting the mandate, repayment and processing fee collection',
      'desc': ('<p>Step 5.</p>'
               + screen_content([('Sections', '“Maximum amount for mandate” · “Repayment” (“Type”, “Frequency”) · “Processing Fee”'),
                   ('Options', '“Sanction Amount” / “Multiple of Loan Amount” / “Absolute Value” · “Fully Amortized” · “Balloon Type” · “Monthly” + “Date” · “1st Disbursement” / “1st Collection”'),
                   ('Validation messages', '“Maximum Mandate Amount is missing” · “Required Field” (Type) · “Required field” (Frequency)')])),
      'data': 'Maximum amount for mandate: Sanction Amount / N time(s) of Sanction amount / ₹ amount<br>Repayment Type: Fully Amortized, Balloon Type<br>Repayment Frequency: 5th, Monthly<br>Collection of PF: 1st Disbursement / 1st Collection',
      'status': WIP,
      'fields': [
        (states(('l12-collections-err', 'Next with empty fields'), ('l12-absolute', 'Absolute Value')), spec(Field_Name='Maximum amount for mandate', Field_Type='Drop-down + amount field',
            Prefilled_Value='Sanction Amount ' + pend('LP-04'),
            Action='Multiple of Loan Amount → “Enter the Amount” (Ex. 2X); Absolute Value → ₹ amount (Ex. ₹2,00,000).',
            Validation=['“Maximum Mandate Amount is missing”']), OK),
        (img('l12-filled'), spec(Field_Name='Repayment – Type', Field_Type='Check boxes', Action='Fully Amortized and / or Balloon Type (shown as “Interest Only” on the product page and in the LOS).',
            Validation=['“Required Field” – none ticked']), OK),
        (img('l12-days-open'), spec(Field_Name='Repayment – Frequency', Field_Type='Check box + day picker', Input_Value_format='1st – 28th ' + pend('LP-04'),
            Validation=['“Required field” – Monthly not ticked or no date chosen']), OK),
        ('', spec(Field_Name='Processing Fee', Field_Type='Radio buttons', Prefilled_Value='1st Disbursement', Action='When the processing fee is collected: 1st Disbursement or 1st Collection.'), OK),
      ],
    },
    {
      'sl': '13', 'shot': img('l13-kyc'),
      'func': 'Maker choosing the KYC requirements and submitting the product',
      'desc': ('<p>Step 6 – the last step; the button reads Submit.</p>'
               + screen_content([('Options', '“PAN” · “Aadhaar” (ticked, cannot be changed) · “Liveness”'), ('CTA', '“Submit”'), ('Toast', '“Product creation successful”')])),
      'data': f'Liveness required:<ul><li>Yes</li><li>No</li></ul><br>Submitted on:<br>{TS}',
      'status': WIP,
      'fields': [
        (img('l13-kyc-list'), spec(Field_Name='KYC requirements', Field_Type='Check boxes', Prefilled_Value='PAN and Aadhaar ticked and locked'), OK),
        (states(('l13-toast', 'Toast'), ('l13-products-inreview', 'Products list after Submit')), spec(Field_Name='Submit', Field_Type='CTA (Button)',
            Action='Shows “Product creation successful”, sets the product In Review, raises a “Product creation” change request (Request ID) for approval and returns to Products.'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 5 – Approvals',
  'screens': 'Change request on the product page (maker) · Approvals list · Checker approval',
  'rows': [
    {
      'sl': '14', 'shot': img('l14-maker-view'),
      'func': 'Maker viewing the product sent for approval',
      'desc': ('<p>A submitted product shows its change request on top. The maker cannot approve their own request.</p>'
               + screen_content([('Change block', '“Change: Product Creation” · “Request ID: <10 letters>” · “Initiated By: <name>” · “Initiated On: DD/MM/YYYY”'),
                   ('Bar', '“Reject” · “Approve” (greyed) · “Maker cannot check”')])),
      'data': 'Request ID: tnBtVbQKpQvU<br>Initiated By: Ops Maker<br>Initiated On: DD/MM/YYYY',
      'status': WIP,
      'fields': [
        (img('l14-change'), spec(Field_Name='Change: Product Creation', Field_Type='Text block', Action='Request ID, who raised it and when.'), OK),
        (img('l14-maker-foot'), spec(Field_Name='Reject / Approve', Field_Type='CTA (Buttons)', Condition='Greyed for the user who raised the request, with the yellow bar “Maker cannot check”.'), OK),
      ],
    },
    {
      'sl': '15', 'shot': img('l15-all'),
      'func': 'Checker / Admin viewing the change requests waiting for approval',
      'desc': ('<p>Menu Approvals.</p>'
               + screen_content([('Tabs', '“My Pending Approvals” · “All Approvals”'), ('Empty', '“No actions pending for your approval”'),
                   ('Columns', '“Date of Change” · “Change Type” · “Details” (Product / ID chips) · “Permitted Roles” (Ops_L2, Ops_L3, Admin, UpdateProductCreationTasks) · “Initiated By”')])),
      'data': 'Date of Change: DD/MM/YYYY<br>Change Type: Product creation<br>Product: TEST Product SCCL<br>ID: LAMF20261103<br>Initiated By: Ops Maker',
      'status': WIP,
      'fields': [
        (states(('l15-pending-empty', 'Maker – nothing to approve'), ('l15-pending', 'Checker – request waiting')), spec(Field_Name='My Pending Approvals', Field_Type='Tab',
            Condition='Lists the requests the logged-in Checker / Admin can approve – never their own; a Maker sees “No actions pending for your approval”.'), OK),
        (img('l15-filter'), spec(Field_Name='Change Type filter', Field_Type='Filter list (check boxes)', Prefilled_Value='All ticked',
            Action='All, Product creation, Loan account opening, Loan lodgement, Disbursement, Foreclosure, Physical loan agreement, Physical mandate, Upsert asset ltv bulk, Upsert asset ltv, Pledging, Pledge release, Liquidation, Loan roi change, Loan email change, Loan mobile change, Update correspondence address, Loan transaction review, Collateral sale price confirmation. Unticking hides that type; All ticks / clears every type.',
            Note='Permitted Roles filter ' + pend('LP-05')), OK),
        ('', spec(Field_Name='Product creation', Field_Type='Link', Action='Opens the request – the product page with the change block (Sl. No 16).'), OK),
      ],
    },
    {
      'sl': '16', 'shot': img('l16-checker'),
      'func': 'Checker approving the new product',
      'desc': ('<p>The checker opens the request from Approvals (or the product page) and approves it.</p>'
               + screen_content([('Upload', '“Upload a file” · “Drop files here or click” · “PDF, PNG or JPG. Max 5MB”'), ('Note', '“Add a note”'),
                   ('CTAs', '“Reject” · “Approve”'), ('Validation message', '“Note is required”'),
                   ('Confirmation pop-up', '“This action is irreversible. Are you sure you want to proceed?” · “No” · “Yes”'), ('Toast', '“Approved successfully”')])),
      'data': f'Note: Test Approved<br>File: PDF / PNG / JPG (optional)<br>Approved by: Ops Checker<br>Approved on:<br>{TS}<br><br>Status after approval: Active',
      'status': WIP,
      'fields': [
        (img('l16-upload-note'), spec(Field_Name='Upload a file', Field_Type='File drop / click', Input_Value_format='PDF, PNG or JPG; max 5 MB', Note='Not mandatory.'), OK),
        (img('l16-note-err'), spec(Field_Name='Add a note', Field_Type='Text Field', Maximum_Character='500 Char', Value_Type='User inputs',
            Validation=['“Note is required” – Approve / Reject clicked with the note empty']), OK),
        (img('l16-confirm'), spec(Field_Name='Confirmation pop-up', Field_Type='Pop-up', Action='No / ⊗ / Esc closes it; Yes completes the action.'), OK),
        (states(('l16-buttons', 'Reject / Approve'), ('l16-approved', 'After Approve → Yes')), spec(Field_Name='Approve', Field_Type='CTA (Button)',
            Action='Yes → the product becomes Active, the request leaves Approvals and Approvals shows “Approved successfully”.'), OK),
        ('', spec(Field_Name='Reject', Field_Type='CTA (Button)', Action='Same note check and confirmation. Result after Yes ' + pend('LP-06')), OK),
      ],
    },
  ],
 },
]

INT_COLUMNS = [('ID', 'Reference number'), ('Integration', 'Which system is affected'), ('Purpose', 'Why'), ('Trigger', 'When it happens'),
               ('Input', 'Data used'), ('Expected Output', 'What the other system shows'), ('Success Behaviour', 'What the user sees'), ('Failure Behaviour', 'If it fails')]
INTEGRATIONS = [
 ('INT-L01', 'LOS – Curated offers', 'Offer an LMS product to LOS customers', 'Product Active and “SCCL LOS” switched on in Update Product Access Policy (Sl. No 7)',
  'Product terms (rate, tenure, PF)', 'An offer card for the product on the Curated offers page (Interest Rate = minimum rate, Tenure = its tenure)',
  'The customer can start an application on that product', pend('LP-07')),
 ('INT-L02', 'LOS – Application summary', 'Apply the product rules to the application', 'Customer starts the application from that offer',
  'Tenure (Range / Discrete), Repayment Type, Disbursement Type', 'Tenure drop-down with every month min–max (Range) or the set months (Discrete); Repayment Type drop-down when both types are allowed; Revolving shown as “Line of Credit”',
  'Customer picks tenure / repayment type', pend('LP-07')),
]

PENDING = [
 ('LP-01', 'Module 1', 'Sl. No 1 – exact message when an SCCL mail ID that is not an LMS user tries to log in (prototype: “This email ID does not have access to the LMS.”).'),
 ('LP-02', 'Module 1', 'Sl. No 2 – Resend OTP: timer length, number of resends, OTP validity and wrong-OTP limit.'),
 ('LP-03', 'Module 4', 'Sl. No 10 – wording of “Maximum … is missing” and “Tenure is missing”; message when MIN is more than MAX.'),
 ('LP-04', 'Module 4', 'Sl. No 12 – default of “Maximum amount for mandate”; days offered in the Date picker; are the Repayment check boxes empty for a new product?'),
 ('LP-05', 'Module 5', 'Sl. No 15 – Permitted Roles filter list; does an approved request stay in All Approvals (with a status)?'),
 ('LP-06', 'Module 5', 'Sl. No 16 – Reject: message after Yes and the product status after rejection.'),
 ('LP-07', 'LOS', 'INT-L01 / L02 – default tenure on the LOS Application summary (prototype: the maximum); Credit Limit and Processing Fee on the LMS product’s offer card.'),
]
COMPLETED = []
TO_IMPLEMENT = []
IMPLEMENTED = []


def info(title, rows):
    body = ''.join(f'<tr><th>{c}</th><td>{m}</td></tr>' for c, m in rows)
    return (f'<span class="info" tabindex="0" aria-label="{title}" onclick="event.preventDefault()">i'
            f'<span class="info-pop" role="tooltip"><b>{title}</b><table>{body}</table></span></span>')


def render():
    out = []
    for m in MODULES:
        out.append(f'<h2>{m["title"]}</h2><p class="screens">{m["screens"]}</p>')
        out.append('<table><thead><tr><th style="width:52px">SL.No</th><th style="width:330px">Screenshot</th>'
                   '<th style="width:190px">Functionality</th><th>Description</th><th style="width:190px">Data Points Required</th>'
                   '<th style="width:120px">Status</th></tr></thead><tbody>')
        for r in m['rows']:
            fields = r.get('fields', [])
            span = f' rowspan="{len(fields) + 1}"' if fields else ''
            out.append(f'<tr id="sl-{r["sl"]}"><td{span} class="sl">{r["sl"]}</td><td class="shot">{r["shot"]}</td>'
                       f'<td{span}>{r["func"]}</td><td>{r["desc"]}</td>'
                       f'<td{span} class="dp">{data_points(r["data"])}</td><td{span}><span class="tag {TAG[r["status"]]}">{r["status"]}</span></td></tr>')
            for shot, desc, st in fields:
                out.append(f'<tr><td class="shot">{shot}</td><td>{desc}</td></tr>')
        out.append('</tbody></table>')
    out.append(f'<h2>Integration Requirements{info("How to read the columns", INT_COLUMNS)}</h2><table class="int"><thead><tr>'
               '<th>ID</th><th>Integration</th><th>Purpose</th><th>Trigger</th><th>Input</th><th>Expected Output</th>'
               '<th>Success Behaviour</th><th>Failure Behaviour</th></tr></thead><tbody>')
    out += ['<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in INTEGRATIONS]
    out.append('</tbody></table>')
    out.append(f'<h2>Pending Clarifications<span class="count wip">{len(PENDING)}</span></h2><table class="int"><thead><tr>'
               '<th style="width:70px">ID</th><th style="width:110px">Module</th><th>Clarification Required</th></tr></thead><tbody>')
    out += [f'<tr id="{i}"><td>{i}</td><td>{mo}</td><td>{q}</td></tr>' for i, mo, q in PENDING]
    out.append('</tbody></table>')
    out.append('<details class="done"><summary><span class="done-title">Completed Clarifications'
               f'<span class="count ok">{len(COMPLETED)}</span></span><span class="chev" aria-hidden="true"></span></summary>'
               '<table class="int"><tbody>' + (''.join(f'<tr id="{c[0]}"><td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}<span class="answered">Answered {c[4]}</span></td></tr>' for c in COMPLETED)
                                           or '<tr><td>None yet.</td></tr>') + '</tbody></table></details>')
    out.append(f'<h2>Pending Changes<span class="count impl">{len(TO_IMPLEMENT)}</span></h2><table class="int"><tbody>'
               + (''.join(f'<tr id="{t[0]}"><td>{t[0]}</td><td>{t[1]}</td><td>{t[2]}</td><td>{t[3]}<span class="raised">Raised {t[4]}</span></td></tr>' for t in TO_IMPLEMENT)
                  or '<tr><td>Nothing pending.</td></tr>') + '</tbody></table>')
    return '\n'.join(out)


HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SCCL LAMF – LMS Product Requirements Document</title>
<link rel="stylesheet" href="assets/lamf.css">
<link rel="stylesheet" href="assets/prd.css">
</head>
<body class="prd">
<header class="prd-head">
  <a href="index.html" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a>
  <div>
    <h1>SCCL LAMF – LMS Product Requirements Document (PRD)</h1>
    <p>Loan Management System &nbsp;·&nbsp; Last updated: {UPDATED}</p>
  </div>
  <a class="prd-link" href="lms-screens.html">All screens →</a>
</header>
<main class="prd-body">
<p class="note">Written from the LMS UAT screenshots shared by the product owner; screenshots are taken from the LMS prototype (sample data only). Status:
<span class="tag yts">YTS</span> yet to start ·
<span class="tag wip">WIP</span> in progress – not final ·
<span class="tag ok">Completed</span> confirmed as done by the product owner.</p>
{render()}
</main>
<script src="assets/review.js"></script>
<script src="assets/colresize.js"></script>
</body>
</html>
"""

with open(os.path.join(ROOT, 'LMS_PRD.html'), 'w') as f:
    f.write(HTML)
print('LMS_PRD.html written')
