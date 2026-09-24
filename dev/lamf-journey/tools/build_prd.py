# Builds SCCL_LAMF_LOS_PRD.html in the format of the shared sample PRD
# (SL.No | Screenshot | Functionality | Description | Data Points Required | Status).
# Content lives in MODULES below — update it after every confirmed discussion, then run:
#   python3 tools/build_prd.py
import os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')

# ---- helpers used inside Description cells -------------------------------
def spec(**kw):
    """One field specification block, in the sample PRD's label: value style."""
    order = ['Field Name', 'Field Type', 'Minimum Character', 'Maximum Character',
             'Value Type', 'Input Value format', 'Prefilled Value', 'Action', 'Condition', 'Validation', 'Note']
    rows = []
    for label in order:
        key = label.replace(' ', '_')
        if key in kw and kw[key]:
            v = kw[key]
            if isinstance(v, list):
                v = '<ul>' + ''.join(f'<li>{x}</li>' for x in v) + '</ul>'
            rows.append(f'<p><b>{label}:</b> {v}</p>')
    return ''.join(rows)

def img(src, w=None):   # w kept for call-site readability; sizing is handled by the stylesheet
    return f'<img src="prd-assets/{src}" alt="">'

OK = 'Confirmed'
WIP = 'Pending Confirmation'

# ---- PRD content ----------------------------------------------------------
MODULES = [
 {
  'title': 'Module 1 – Mobile Number Verification',
  'screens': 'Screen 01) LAMF Landing Page · Screen 02) Enter MF linked Mobile Number',
  'rows': [
    {
      'sl': '1',
      'shot': img('screen-01.png'),
      'func': 'User clicking the “Check your eligibility in 2 minutes” CTA in landing page to start the journey',
      'desc': ('<p>The customer shall access the SCCL LAMF journey through the LAMF URL '
               '(https://uatlamf.shriramcredit.in/). On successful access, the system shall load and display the '
               'SCCL LAMF Landing Page, which serves as the entry point for initiating the LAMF application journey.</p>'
               + spec(Field_Name='Check your eligibility in 2 minutes', Field_Type='CTA (Button)',
                      Action='On click, the system shall open the “Enter your MF linked Mobile Number” pop up over the landing page, which is the first step of the LAMF journey.')
               + spec(Field_Name='Start Your Application', Field_Type='CTA (Button)',
                      Action='Placed below the 8-step “How to Apply” section. On click, the system shall perform the same action as the “Check your eligibility in 2 minutes” CTA and open the mobile number pop up.')),
      'data': 'Landing Page Accessed: Yes/No<br>Page Access Date &amp; Time: Timestamp<br>CTA Clicked: Check your eligibility / Start Your Application',
      'status': OK,
    },
    {
      'sl': '2',
      'shot': img('screen-02.png'),
      'func': 'User entering the MF linked Mobile Number for the mobile number verification',
      'desc': ('<p>The system shall display the “Enter your MF linked Mobile Number” pop up over the landing page. '
               'While the pop up is open the background page shall remain frozen and shall not scroll; the pop up itself '
               'shall scroll only when its content does not fit the screen (for example when the customer has zoomed in).</p>'),
      'data': 'Mobile Number: 10 digit numeric<br>Consent Accepted: Yes/No<br>Consent Date &amp; Time: Timestamp',
      'status': OK,
      'fields': [
        (img('f02-close.png', 160), spec(Field_Name='(X) Close Icon', Field_Type='Icon',
            Action='After clicking this, navigate user to landing page by closing this pop up'), OK),
        (img('f02-field.png', 360), spec(Field_Name='Mobile Number', Field_Type='Text Field',
            Minimum_Character='10 Char', Maximum_Character='10 Char', Value_Type='User inputs',
            Input_Value_format='Numeric only',
            Action='User has to enter the MF linked mobile number. Alphabets, spaces and special characters shall not be enterable. A first digit of 0 to 5 shall not be accepted.',
            Validation=[
              '“Please enter your MF linked mobile number.” – displayed when user clicks Continue CTA without entering the mobile number',
              '“Mobile number must be 10 digits.” – displayed when user clicks Continue CTA with less than 10 digits, and on exit from the field',
              '“Mobile number cannot start with 0, 1, 2, 3, 4 or 5. Please enter a valid mobile number.” – displayed when the customer attempts a first digit of 0 to 5',
              '“Only numbers are allowed. Letters, spaces and special characters cannot be entered.” – displayed when the customer attempts a non numeric character',
            ],
            Note='Wording to be aligned with the approved copy (refer Pending Clarification P-01).'), OK),
        (img('f02-consent.png', 360), spec(Field_Name='(Checkbox)', Field_Type='Check box',
            Action='User has to click the Checkbox. Once this checkbox is clicked then only the Continue CTA has to be enabled',
            Validation='“Please accept the T&amp;C and Privacy Policy to continue.” – displayed when the customer clicks Continue CTA without ticking the checkbox'), OK),
        (img('f02-tnc.png', 120), spec(Field_Name='T&amp;C', Field_Type='Hyperlink',
            Action='User has to click this hyperlink to view the Terms and Conditions. On click, the system shall display the Terms and Conditions pop up containing a Close (X) icon and an Accept CTA. Content source: https://www.shriramcredit.in/terms-and-conditions',
            Condition='Accept CTA shall close the pop up and tick the consent checkbox. Close (X) icon shall close the pop up without changing the consent.'), OK),
        (img('f02-privacy.png', 180), spec(Field_Name='Privacy Policy', Field_Type='Hyperlink',
            Action='User has to click this hyperlink to view the Privacy Policy. On click, the system shall display the Privacy Policy pop up containing a Close (X) icon and an Accept CTA. Content source: https://www.shriramcredit.in/privacy-policy',
            Condition='Same Accept / Close behaviour as the T&amp;C pop up.'), OK),
        (img('f02-cta.png', 360), spec(Field_Name='Continue', Field_Type='CTA (Button)',
            Action='On click, the system shall validate all conditions of this screen. If every condition is met, the system shall trigger the OTP to the entered mobile number and navigate the customer to the OTP verification screen. If any condition fails, the customer shall not be allowed to proceed and the respective validation shall be displayed.',
            Condition='CTA is disabled (grey) until the consent checkbox is ticked. Validation order: consent → mobile number entered → first digit 6 to 9 → 10 digits.'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 2 – OTP Verification (MF linked Mobile Number)',
  'screens': 'Screen 03) Enter OTP for MF linked Mobile Number Verification',
  'rows': [
    {
      'sl': '3',
      'shot': img('screen-03.png'),
      'func': 'User entering the OTP received on the MF linked mobile number to complete the mobile number verification',
      'desc': ('<p>On successful submission of the mobile number, the system shall send a 6 digit OTP to the MF linked '
               'mobile number and display the “Enter OTP” pop up over the landing page. The mobile number shall be displayed '
               'in masked format (+91, first 2 digits, XXXX, last 4 digits).</p>'),
      'data': ('OTP Entered: 6 digit numeric<br>OTP Verified: Yes/No<br>OTP Verified Date &amp; Time: Timestamp<br>'
               'Resend Count: 0–3<br>Wrong Attempt Count: 0–3<br>Blocked Until: Timestamp<br>'
               'Experian Consent: Yes/No<br>Experian Consent Date &amp; Time: Timestamp'),
      'status': OK,
      'fields': [
        (img('f03-close.png', 160), spec(Field_Name='(X) Close Icon', Field_Type='Icon',
            Action='After clicking this, close the pop up and navigate the user to the landing page'), OK),
        (img('f03-sent.png', 360), spec(Field_Name='Masked Mobile Number', Field_Type='Display text',
            Prefilled_Value='Mobile number entered on the previous screen, masked as +91 + first 2 digits + XXXX + last 4 digits',
            Action='Display only, not editable'), OK),
        (img('f03-edit.png', 120), spec(Field_Name='Edit', Field_Type='Icon with hyperlink',
            Action='On click, navigate the user to the previous screen (Enter your MF linked Mobile Number). The mobile number entered by the user shall be prefilled in the field.'), OK),
        (img('f03-otp.png', 360), spec(Field_Name='Enter OTP', Field_Type='6 single character boxes',
            Minimum_Character='6 Char', Maximum_Character='6 Char', Value_Type='User inputs',
            Input_Value_format='Numeric only',
            Action='User has to enter the 6 digit OTP received on the MF linked mobile number. Alphabets, spaces and special characters shall not be enterable and the customer shall not be able to enter more than 6 characters.',
            Validation=[
              '“Only numbers are allowed. Letters, spaces and special characters cannot be entered.” – displayed when the customer attempts a non numeric character',
              '“Please enter the 6-digit OTP.” – displayed when the customer clicks Submit OTP with fewer than 6 digits',
              '“The OTP you entered is incorrect. Please try again. N attempt(s) remaining.” – displayed on a wrong OTP (1st and 2nd attempt)',
            ]), OK),
        (img('f03-resend.png', 360), spec(Field_Name='Resend OTP', Field_Type='Timer with hyperlink CTA',
            Action='The timer shall start at 0:30 and run down to 0:01. At 0 the Resend OTP CTA shall be enabled. On click, the OTP shall be sent again and the timer shall restart.',
            Condition='The customer may resend back to back 3 times. On the 3rd resend the customer shall be blocked and shall not be able to proceed for 15 minutes. The waiting time displayed shall be calculated from the blocked date and time, so a customer returning after 10 minutes shall see the balance 5 minutes.',
            Validation='“You have used all 3 OTP resend attempts. Please try again after N minutes.”'), OK),
        (img('f03-consent.png', 360), spec(Field_Name='(Checkbox) Experian consent', Field_Type='Check box',
            Action='User has to tick this checkbox to appoint Shriram Credit as the authorised representative to receive the credit information from Experian for the purpose of providing / evaluating loan offers.',
            Condition='Submit OTP CTA shall be enabled only when this checkbox is ticked and all 6 OTP digits are entered.',
            Validation='“Please provide the consent to proceed.”'), OK),
        (img('f03-cta.png', 360), spec(Field_Name='Submit OTP', Field_Type='CTA (Button)',
            Action='On click, the system shall check all the conditions of this screen. If every condition is met, the system shall verify the OTP, trigger the Experian API with the mobile number to retrieve the credit score, and navigate the customer to the PAN Verification screen. If any condition fails, the respective validation shall be displayed and the customer shall not be allowed to proceed.',
            Condition='3 consecutive wrong OTP attempts shall block the customer for 60 minutes, with the remaining time calculated from the blocked date and time. While blocked, the OTP boxes, consent checkbox, Submit OTP and Resend OTP shall be disabled.',
            Validation='“You have entered an incorrect OTP 3 times. Please try again after N minutes.”'), OK),
      ],
    },
    {
      'sl': '4',
      'shot': img('screen-04.png'),
      'func': 'On successful mobile number verification the customer lands on the PAN Verification screen',
      'desc': ('<p>On successful OTP verification the system shall navigate the customer to the PAN Verification screen. '
               'The mobile number entered by the customer shall be carried forward and displayed as a non editable field. '
               'The Experian credit information call shall be triggered in the background; the customer shall not be made to '
               'wait for the response.</p>'
               '<p><b>Field level requirements for this screen are yet to be confirmed (refer Pending Clarification P-06).</b></p>'),
      'data': 'Mobile Number: carried from Module 1<br>Experian API Triggered: Yes/No<br>Experian Response: TBD',
      'status': WIP,
    },
  ],
 },
]

# Column guide shown by the (i) next to the Integration Requirements heading
INT_COLUMNS = [
 ('ID', 'Reference number, so other parts of the PRD can point to it (e.g. “Submit OTP triggers INT-001”)'),
 ('Integration', 'Which external system is called'),
 ('Purpose', 'Why the journey needs it'),
 ('Trigger', 'The exact moment or button that makes the call happen'),
 ('Input', 'Data the LOS sends to that system'),
 ('Expected Output', 'Data the LOS gets back'),
 ('Success Behaviour', 'What the customer experiences when the call works'),
 ('Failure Behaviour', 'What happens if the call fails, times out or returns an error'),
]

def info(title, rows):
    """(i) icon that shows a small guide table on hover, keyboard focus or tap."""
    body = ''.join(f'<tr><th>{c}</th><td>{m}</td></tr>' for c, m in rows)
    return (f'<span class="info" tabindex="0" aria-label="{title}">i'
            f'<span class="info-pop" role="tooltip"><b>{title}</b><table>{body}</table></span></span>')

INTEGRATIONS = [
 ('INT-001', 'Experian', 'Retrieve credit information / credit score for evaluating loan offers',
  'On successful OTP verification (Module 2), after the customer gives the Experian consent',
  'Customer mobile number', 'Credit score / credit information – TBD',
  'Customer proceeds to PAN Verification without waiting for the response', 'TBD – Confirmation Required'),
 ('INT-002', 'OTP Service Provider – TBD', 'Send and verify the 6 digit OTP for the MF linked mobile number',
  'Continue CTA on Module 1; Resend OTP CTA on Module 2', 'Mobile number', 'OTP sent / verification result',
  'Customer proceeds to PAN Verification', 'TBD – Confirmation Required'),
]

PENDING = [
 ('P-01', 'Module 1', 'Validation message wording: the shared sample PRD carries “*Required”, “*Invalid mobile number” and “Error: Invalid phone number”. The messages currently built follow the wording confirmed in discussion on 22-09-2026. Confirm which set is approved.'),
 ('P-02', 'Module 1', 'Does the Continue CTA call an OTP send API at this point, and what is the failure behaviour?'),
 ('P-03', 'Module 1', 'Any backend check on the mobile number at this stage (existing customer, ongoing application, blacklist)?'),
 ('P-04', 'Module 2', 'OTP validity / expiry period.'),
 ('P-05', 'Module 2', 'Resend and wrong attempt blocks to be enforced server side against the mobile number (currently held in the prototype browser storage). Confirm reset conditions for the counters.'),
 ('P-06', 'Module 3', 'PAN Verification screen: field level rules, PAN format validation, name as per PAN matching logic and DOB / age rule.'),
 ('P-07', 'Module 2', 'Experian failure / timeout behaviour and the effect of the score on eligibility and offers.'),
 ('P-08', 'All', 'Where should the header Shriram Credit logo navigate in the live journey (shriramcredit.in, the LAMF landing page, or nowhere)? The prototype sends it to its own review home page.'),
]

# ---- render ---------------------------------------------------------------
def render():
    out = []
    for m in MODULES:
        out.append(f'<h2>{m["title"]}</h2>')
        out.append(f'<p class="screens">{m["screens"]}</p>')
        out.append('<table><thead><tr>'
                   '<th style="width:52px">SL.No</th><th style="width:330px">Screenshot</th>'
                   '<th style="width:190px">Functionality</th><th>Description</th>'
                   '<th style="width:190px">Data Points Required</th><th style="width:110px">Status</th>'
                   '</tr></thead><tbody>')
        for r in m['rows']:
            fields = r.get('fields', [])
            span = f' rowspan="{len(fields) + 1}"' if fields else ''
            out.append(f'<tr><td{span} class="sl">{r["sl"]}</td><td class="shot">{r["shot"]}</td>'
                       f'<td{span}>{r["func"]}</td><td>{r["desc"]}</td>'
                       f'<td{span} class="dp">{r["data"]}</td><td{span}><span class="tag {"ok" if r["status"]==OK else "wip"}">{r["status"]}</span></td></tr>')
            for shot, desc, st in fields:
                out.append(f'<tr><td class="shot">{shot}</td><td>{desc}</td></tr>')
        out.append('</tbody></table>')

    out.append(f'<h2>Integration Requirements{info("How to read the columns", INT_COLUMNS)}</h2><table class="int"><thead><tr>'
               '<th>ID</th><th>Integration</th><th>Purpose</th><th>Trigger</th><th>Input</th>'
               '<th>Expected Output</th><th>Success Behaviour</th><th>Failure Behaviour</th></tr></thead><tbody>')
    for row in INTEGRATIONS:
        out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>')
    out.append('</tbody></table>')

    out.append('<h2>Pending Clarifications</h2><table class="int"><thead><tr>'
               '<th style="width:70px">ID</th><th style="width:110px">Module</th><th>Clarification Required</th>'
               '</tr></thead><tbody>')
    for pid, mod, q in PENDING:
        out.append(f'<tr><td>{pid}</td><td>{mod}</td><td>{q}</td></tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SCCL LAMF – LOS Product Requirements Document</title>
<link rel="stylesheet" href="assets/lamf.css">
<link rel="stylesheet" href="assets/prd.css">
</head>
<body class="prd">
<header class="prd-head">
  <a href="index.html" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a>
  <div>
    <h1>SCCL LAMF – LOS Product Requirements Document (PRD)</h1>
    <p>Customer Online Journey &nbsp;·&nbsp; Last updated: {UPDATED}</p>
  </div>
  <a class="prd-link" href="screens.html">All screens →</a>
</header>
<main class="prd-body">
<p class="note">This document is generated from the confirmed discussion log. Sections marked
<span class="tag wip">Pending Confirmation</span> are not yet confirmed and must not be treated as final requirements.</p>
{render()}
<p class="foot">Screenshots are taken from the clickable LAMF prototype hosted locally at <code>http://localhost:8080</code>.</p>
</main>
</body>
</html>
"""

with open(os.path.join(ROOT, 'SCCL_LAMF_LOS_PRD.html'), 'w') as f:
    f.write(HTML)

# cloud copy: the same PRD body as a hash route inside cloud.html
import json as _json
BODY = f"""<header class="prd-head">
  <a href="#" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a>
  <div><h1>SCCL LAMF – LOS Product Requirements Document (PRD)</h1>
  <p>Customer Online Journey &nbsp;·&nbsp; Last updated: {UPDATED}</p></div>
  <a class="prd-link" href="#SCREENS">All screens →</a>
</header>
<main class="prd-body">
<p class="note">This document is generated from the confirmed discussion log. Sections marked
<span class="tag wip">Pending Confirmation</span> are not yet confirmed and must not be treated as final requirements.</p>
{render()}
</main>"""
with open(os.path.join(ROOT, 'assets', 'prd-body.js'), 'w') as f:
    f.write('window.PRD_HTML = ' + _json.dumps(BODY) + ';\n')
print('SCCL_LAMF_LOS_PRD.html + assets/prd-body.js written')
