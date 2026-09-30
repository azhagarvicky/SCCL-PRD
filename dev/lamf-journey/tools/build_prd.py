# Builds SCCL_LAMF_LOS_PRD.html in the format of the shared sample PRD
# (SL.No | Screenshot | Functionality | Description | Data Points Required | Status).
# Content lives in MODULES below — update it after every confirmed discussion, then run:
#   python3 tools/build_prd.py
import os, re, html, datetime

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
    return '<div class="spec">' + ''.join(rows) + '</div>'

def screen_content(items):
    """“Screen Content” block: every text shown on the screen, in one place (DISC-094)."""
    rows = ''.join(f'<li><b>{k}:</b> {v}</li>' for k, v in items)
    return f'<div class="spec"><p><b>Screen Content:</b></p><ul class="content-list">{rows}</ul></div>'

def data_points(html_):
    """Data Points Required: field name in bold, value in regular weight (DISC-087),
    e.g. <b>Mobile Number:</b> 10 digit numeric. Lines already starting in bold are kept."""
    out = []
    for seg in html_.split('<br>'):
        # a field name is followed by ": " (or ends the line); "HH:MM:SS" formats are left alone
        m = re.match(r'^([^:<]{1,60}):(?:\s+(.*))?$', seg, re.S)
        out.append(f'<b>{m.group(1)}:</b> {m.group(2) or ""}' if m else seg)
    return '<br>'.join(out)

def pend(*ids):
    """Amber badge that marks something as not yet decided and jumps to its
    Pending Clarifications row. Scrolls with JS (no hash change) because the
    cloud copy uses the URL hash for routing."""
    js = ("var t=document.getElementById('{p}');if(t){{t.scrollIntoView({{behavior:'smooth',block:'center'}});"
          "t.classList.remove('flash');void t.offsetWidth;t.classList.add('flash')}}return false")
    return ' '.join(f'<a class="pend-ref" href="#{p}" onclick="{js.format(p=p)}" title="Open pending clarification {p}">'
                    f'Pending · {p}</a>' for p in ids)

# ---- Pending Changes / Completed Changes (DISC-091, renamed DISC-094) ----------
# Items defined in this PRD that are not yet built in the live LOS journey.
# (ID, Module, Where in the PRD, What has to be implemented, Raised on)
def change(now, new):
    """Current behaviour in the live LOS journey vs what it has to change to (DISC-092)."""
    return f'<div class="chg"><div><b>Current:</b> {now}</div><div><b>To be changed as:</b> {new}</div></div>'

TO_IMPLEMENT = [
 ('CR-01', 'Module 1', 'Sl. No 2 – Mobile Number field (Continue CTA with no mobile number)',
  change('“*Required”', '“Please enter your MF linked mobile number.” – displayed when the user clicks the Continue CTA without entering the mobile number'), '30-09-2026'),
 ('CR-02', 'Module 1', 'Sl. No 2 – Mobile Number field (less than 10 digits)',
  change('“*Invalid mobile number”', '“Mobile number must be 10 digits.” – displayed when the user clicks the Continue CTA with less than 10 digits, and on exit from the field'), '30-09-2026'),
 ('CR-03', 'Module 1', 'Sl. No 2 – Mobile Number field (first digit 0 to 5)',
  change('“Error: Invalid phone number” – displayed only when the user clicks the Continue CTA',
         '“Mobile number cannot start with 0, 1, 2, 3, 4 or 5. Please enter a valid mobile number.” – displayed as soon as the customer attempts a first digit of 0 to 5'), '30-09-2026'),
 ('CR-04', 'Module 1', 'Sl. No 2 – Mobile Number field (non numeric character)',
  change('No validation – the character simply cannot be entered',
         'The character still cannot be entered, and “Only numbers are allowed. Letters, spaces and special characters cannot be entered.” is displayed when the customer attempts a non numeric character'), '30-09-2026'),
 ('CR-05', 'Module 2', 'Sl. No 3 – Enter OTP field (non numeric character)',
  change('No validation – the character simply cannot be entered',
         'The character still cannot be entered, and “Only numbers are allowed. Letters, spaces and special characters cannot be entered.” is displayed when the customer attempts a non numeric character'), '30-09-2026'),
 ('CR-06', 'Module 2', 'Sl. No 3 – Enter OTP field (wrong OTP, 1st and 2nd back to back attempt)',
  change('“Invalid OTP” on the 1st, 2nd and 3rd back to back wrong attempt',
         '“The OTP you entered is incorrect. Please try again. You have 2 attempts left.” (1st wrong attempt) / “The OTP you entered is incorrect. Please try again. You have 1 attempt left.” (2nd). The 3rd wrong attempt shows the CR-07 message instead'), '30-09-2026'),
 ('CR-07', 'Module 2', 'Sl. No 3 – Submit OTP (3 back to back wrong OTPs)',
  change('“Maximum OTP retry limit reached. Please retry again after 60 minute(s).” – shown on the next attempt after the 3rd wrong OTP',
         '“You have entered an incorrect OTP 3 times. Please try again after N minute(s).” – shown straight away on the 3rd back to back wrong OTP; N is the time left in the 60 minute block (e.g. a customer returning after 10 minutes sees 50)'), '30-09-2026'),
 ('CR-08', 'Module 2', 'Sl. No 3 – Resend OTP (click after the 3rd back to back resend)',
  change('“Error: Maximum OTP resend limit reached. Please retry again after 15 minute(s).”',
         '“You have used all 3 OTP resends. Please try again after N minute(s).” – N is the time left in the 15 minute block; no “Error:” prefix'), '30-09-2026'),
]
# Moved here only when the owner confirms the item is live in the LOS journey:
# (ID, Module, Where in the PRD, What was implemented, Implemented on)
IMPLEMENTED = [
]

def todo(*ids):
    """Blue tag “To be changed · CR-01” that jumps to its row in the Pending Changes list;
    once the item is in IMPLEMENTED it shows as a green “Changed · CR-01” tag (DISC-088, DISC-091, DISC-094)."""
    done = {i[0] for i in IMPLEMENTED}
    js = ("var t=document.getElementById('{p}');if(t){{var d=t.closest('details');if(d)d.open=true;"
          "t.scrollIntoView({{behavior:'smooth',block:'center'}});t.classList.remove('flash');void t.offsetWidth;t.classList.add('flash')}}return false")
    return ' '.join(f'<a class="{"done-ref" if t in done else "todo-ref"}" href="#{t}" onclick="{js.format(p=t)}" '
                    f'title="{"Changed in the live LOS journey" if t in done else "Defined in the PRD, not yet changed in the live LOS journey"} – open {t}">'
                    f'{"Changed" if t in done else "To be changed"} · {t}</a>' for t in ids)

def img(src, w=None):   # w kept for call-site readability; sizing is handled by the stylesheet
    return f'<img src="prd-assets/{src}" alt="">'

# Row status (DISC-086): YTS = yet to start, WIP = in progress, DONE = Completed.
# A row is moved to Completed only on the owner's explicit confirmation.
YTS = 'YTS'
WIP = 'WIP'
DONE = 'Completed'
OK = WIP   # field-level status inside a row (not displayed)
TAG = {YTS: 'yts', WIP: 'wip', DONE: 'ok'}

# ---- PRD content ----------------------------------------------------------
MODULES = [
 {
  'title': 'Module 1 – Mobile Number Verification',
  'screens': 'Screen 01) LAMF Landing Page · Screen 02) Enter MF linked Mobile Number',
  'rows': [
    {
      'sl': '1',
      'shot': img('screen-01.png'),
      'func': 'User clicking the “Check your eligibility in 2 minutes” CTA or the “Start Your Application” CTA in landing page to start the journey',
      'desc': ('<p>The customer shall access the SCCL LAMF journey through the LAMF URL '
               '(https://uatlamf.shriramcredit.in/). On successful access, the system shall load and display the '
               'SCCL LAMF Landing Page, which serves as the entry point for initiating the LAMF application journey.</p>'
               + spec(Field_Name='Check your eligibility in 2 minutes', Field_Type='CTA (Button)',
                      Action='On click, the system shall open the “Enter your MF linked Mobile Number” pop up over the landing page, which is the first step of the LAMF journey.')
               + spec(Field_Name='Start Your Application', Field_Type='CTA (Button)',
                      Action='Placed below the 8-step “How to Apply” section. On click, the system shall perform the same action as the “Check your eligibility in 2 minutes” CTA and open the mobile number pop up.')),
      'data': '<b>Clicked CTA:</b><ul><li>Check your eligibility in 2 minutes</li><li>Start Your Application</li></ul><br><b>Clicked Timestamp:</b><br>DD-MMM-YYYY; HH:MM:SS',
      'status': DONE,   # confirmed by the owner – do not change without the owner's instruction
    },
    {
      'sl': '2',
      'shot': img('screen-02.png'),
      'func': 'User entering the MF linked Mobile Number for the mobile number verification',
      'desc': ('<p>The system shall display the “Enter your MF linked Mobile Number” pop up over the landing page. '
               'While the pop up is open the background page shall remain frozen and shall not scroll; the pop up itself '
               'shall scroll only when its content does not fit the screen (for example when the customer has zoomed in).</p>'
               + screen_content([
                   ('Pop up title', '“Enter your MF linked Mobile Number”'),
                   ('Close icon', '(X) at the top right'),
                   ('Mobile Number field placeholder', '“9876543210”'),
                   ('Consent checkbox text', '“By proceeding, I agree to T&amp;C and Privacy Policy of Shriram Credit.” – T&amp;C and Privacy Policy are hyperlinks'),
                   ('CTA', '“Continue” – grey until the checkbox is ticked, then yellow'),
                   ('Validation messages', '<ul><li>“*Required” ' + todo('CR-01') + '</li><li>“*Invalid mobile number” ' + todo('CR-02') + '</li>'
                    '<li>“Error: Invalid phone number” ' + todo('CR-03') + '</li><li>No message for a non numeric character ' + todo('CR-04') + '</li></ul>'),
               ])),
      'data': '<b>Mobile Number:</b> 9597001623<br><br><b>Consent Accepted:</b><ul><li>Yes</li><li>No</li></ul><br><b>Submitted Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS',
      'status': DONE,   # confirmed by the owner – do not change without the owner's instruction
      'fields': [
        (img('f02-close.png', 160), spec(Field_Name='(X) Close Icon', Field_Type='Icon',
            Action='After clicking this, navigate user to landing page by closing this pop up'), OK),
        (img('f02-field.png', 360), spec(Field_Name='Mobile Number', Field_Type='Text Field',
            Minimum_Character='10 Char', Maximum_Character='10 Char', Value_Type='User inputs',
            Input_Value_format='Numeric only',
            Action='User has to enter the MF linked mobile number.',
            Condition='Only numbers can be entered. Alphabets, spaces and special characters cannot be entered, and no message is shown. ' + todo('CR-04'),
            # Current live LOS behaviour (DISC-095); the new wording is tracked only in Pending Changes
            Validation=[
              '“*Required” – displayed when user clicks Continue CTA without entering the mobile number ' + todo('CR-01'),
              '“*Invalid mobile number” – displayed when user clicks Continue CTA with less than 10 digits, and on exit from the field ' + todo('CR-02'),
              '“Error: Invalid phone number” – displayed when the mobile number starts with 0 to 5 and the user clicks Continue CTA ' + todo('CR-03'),
            ]), OK),
        (img('f02-consent.png', 360), spec(Field_Name='(Checkbox)', Field_Type='Check box',
            Action='User has to click the Checkbox. Once this checkbox is clicked then only the Continue CTA has to be enabled'), OK),
        (img('f02-tnc.png', 120), spec(Field_Name='T&amp;C', Field_Type='Hyperlink',
            Action='User has to click this hyperlink to view the Terms and Conditions. On click, the system shall redirect the user to https://www.shriramcredit.in/terms-and-conditions (opens in a new tab, so the details entered on this screen are kept).'), OK),
        (img('f02-privacy.png', 180), spec(Field_Name='Privacy Policy', Field_Type='Hyperlink',
            Action='User has to click this hyperlink to view the Privacy Policy. On click, the system shall redirect the user to https://www.shriramcredit.in/privacy-policy (opens in a new tab, so the details entered on this screen are kept).'), OK),
        (img('f02-cta.png', 360), spec(Field_Name='Continue', Field_Type='CTA (Button)',
            Action='On click, the system shall validate all conditions of this screen. If every condition is met, the system shall trigger the OTP to the entered mobile number and navigate the customer to the OTP verification screen. If any condition fails, the customer shall not be allowed to proceed and the respective validation shall be displayed.',
            Condition='CTA is disabled (grey) and cannot be clicked until the consent checkbox is ticked, so no validation is shown for the checkbox. Once enabled, validation order: mobile number entered → first digit 6 to 9 → 10 digits.'), OK),
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
               'in masked format (+91, first 2 digits, XXXX, last 4 digits).</p>'
               + screen_content([
                   ('Pop up title', '“Enter OTP”'),
                   ('Close icon', '(X) at the top right'),
                   ('Sent message', '“A 6-digit OTP has been sent by Shriram Credit to” followed by the masked mobile number and the “Edit” link'),
                   ('OTP boxes', '6 single digit boxes'),
                   ('Resend line', '“Didn’t Receive OTP?” with the countdown timer (0:30 to 0:01), then the “Resend OTP” link'),
                   ('Experian consent checkbox text', '“I hereby consent to appoint Shriram Credit as my authorised representative to receive my credit information from Experian for the purpose of providing/ evaluating loan offers.”'),
                   ('CTA', '“Submit OTP” – grey until all 6 digits are entered and the consent is ticked, then yellow'),
                   ('Validation messages', '<ul><li>“Invalid OTP” ' + todo('CR-06') + '</li>'
                    '<li>“Maximum OTP retry limit reached. Please retry again after 60 minute(s).” ' + todo('CR-07') + '</li>'
                    '<li>“Error: Maximum OTP resend limit reached. Please retry again after 15 minute(s).” ' + todo('CR-08') + '</li>'
                    '<li>No message for a non numeric character ' + todo('CR-05') + '</li></ul>'),
               ])),
      'data': ('<b>OTP Entered:</b> 6 digit numeric<br><br>'
               '<b>OTP Verified:</b><ul><li>Yes</li><li>No</li></ul><br>'
               '<b>OTP Verified Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Resend Count:</b> 0–3<br><br>'
               '<b>Wrong Attempt Count:</b> 0–3<br><br>'
               '<b>Blocked Start Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Blocked End Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Experian Consent:</b><ul><li>Yes</li><li>No</li></ul>'),
      'status': WIP,
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
            Action='User has to enter the 6 digit OTP received on the MF linked mobile number.',
            Condition='Only numbers can be entered, up to 6 digits. Alphabets, spaces and special characters cannot be entered, and no message is shown. ' + todo('CR-05'),
            # Current live LOS behaviour (DISC-096)
            Validation='“Invalid OTP” – displayed on each wrong OTP, for the 1st, 2nd and 3rd back to back wrong attempt. Wrong attempts are counted only while the pop up stays open: if the customer closes the pop up and then enters a wrong OTP again, it is counted as the 1st attempt ' + todo('CR-06')), OK),
        (img('f03-resend.png', 360), spec(Field_Name='Resend OTP', Field_Type='Timer with hyperlink CTA',
            Action='The timer shall start at 0:30 and run down to 0:01. At 0 the Resend OTP CTA shall be enabled. On click, the OTP shall be sent again and the timer shall restart.',
            Condition='The customer can click Resend OTP 3 times back to back (1st, 2nd and 3rd) in the same pop up. On the next click the customer is blocked from resending for 15 minutes.',
            Validation='“Error: Maximum OTP resend limit reached. Please retry again after 15 minute(s).” – displayed when the customer clicks Resend OTP after the 3rd back to back resend ' + todo('CR-08')), OK),
        (img('f03-consent.png', 360), spec(Field_Name='(Checkbox) Experian consent', Field_Type='Check box',
            Action='User has to tick this checkbox to appoint Shriram Credit as the authorised representative to receive the credit information from Experian for the purpose of providing / evaluating loan offers.',
            Condition='Submit OTP CTA shall be enabled only when this checkbox is ticked and all 6 OTP digits are entered, so no validation is shown for the checkbox.'), OK),
        (img('f03-cta.png', 360), spec(Field_Name='Submit OTP', Field_Type='CTA (Button)',
            Action='On click, the system shall validate the entered OTP. If the OTP is correct, the system shall trigger the Experian API with the mobile number to retrieve the credit score and navigate the customer to the PAN Verification screen. If the OTP is wrong, the customer shall not be allowed to proceed and the respective validation shall be displayed.',
            Condition='CTA is disabled (grey) and cannot be clicked until all 6 OTP digits are entered and the Experian consent checkbox is ticked, so no validation is shown for these. Once enabled, validation order: blocked for wrong attempts → OTP correct. After 3 back to back wrong OTP attempts in the same pop up the customer is blocked for 60 minutes.',
            Validation='“Maximum OTP retry limit reached. Please retry again after 60 minute(s).” – displayed on the next attempt after 3 back to back wrong OTPs ' + todo('CR-07')), OK),
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
               '<p><b>Field level requirements for this screen are yet to be confirmed</b> ' + pend('P-06') + '</p>'),
      'data': 'Mobile Number: carried from Module 1<br>Experian API Triggered: Yes/No<br>Experian Response: ' + pend('P-09'),
      'status': YTS,
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
    return (f'<span class="info" tabindex="0" aria-label="{title}" onclick="event.preventDefault()">i'
            f'<span class="info-pop" role="tooltip"><b>{title}</b><table>{body}</table></span></span>')

INTEGRATIONS = [
 ('INT-001', 'Experian', 'Retrieve credit information / credit score for evaluating loan offers',
  'On successful OTP verification (Module 2), after the customer gives the Experian consent',
  'Customer mobile number', 'Credit score / credit information ' + pend('P-09'),
  'Customer proceeds to PAN Verification without waiting for the response', pend('P-07')),
 ('INT-002', 'OTP Service Provider ' + pend('P-10'), 'Send and verify the 6 digit OTP for the MF linked mobile number',
  'Continue CTA on Module 1; Resend OTP CTA on Module 2', 'Mobile number', 'OTP sent / verification result',
  'Customer proceeds to PAN Verification', pend('P-02', 'P-10')),
]

# Column guide shown by the (i) next to the Pending Clarifications heading
PENDING_COLUMNS = [
 ('ID', 'Reference number. Anything not yet decided elsewhere in the PRD carries an amber “Pending · P-09” badge that jumps to its row here'),
 ('Module', 'Which part of the journey the question is about (“All” means the whole journey)'),
 ('Clarification Required', 'The question that must be answered before that requirement is final. Until then the related item stays TBD and must not be built on assumptions'),
 ('When answered', 'The answer is written into the PRD and the question moves to Completed Clarifications below'),
]

# Column guides for the Pending Changes / Completed Changes lists (DISC-091, DISC-094)
TODO_COLUMNS = [
 ('ID', 'Change reference (CR). Wherever the PRD above carries a blue “To be changed · CR-01” tag, it jumps to its row here'),
 ('Module', 'Which part of the journey the item belongs to'),
 ('Where in the PRD', 'The Sl. No and field that defines it'),
 ('What has to change', 'How the live LOS journey behaves today and what it has to change to, with the date it was raised'),
 ('When done', 'Once the owner confirms the change is live, it moves to Completed Changes below and its tags turn green'),
]
IMPLEMENTED_COLUMNS = [
 ('ID', 'Change reference (kept when it moves from Pending Changes)'),
 ('Module', 'Which part of the journey the item belongs to'),
 ('Where in the PRD', 'The Sl. No and field that defines it'),
 ('What was changed', 'What is now live in the LOS journey, and the date the owner confirmed it'),
]

# Column guide shown by the (i) next to the Completed Clarifications heading
COMPLETED_COLUMNS = [
 ('ID', 'Reference number of the question (kept when a pending item is answered)'),
 ('Module', 'Which part of the journey the question was about'),
 ('Clarification Required', 'The question that was asked'),
 ('Clarification Provided', 'The confirmed answer and the date it was given. The modules above already follow it'),
]

PENDING = [
 ('P-02', 'Module 1', 'Does the Continue CTA call an OTP send API at this point, and what is the failure behaviour?'),
 ('P-03', 'Module 1', 'Any backend check on the mobile number at this stage (existing customer, ongoing application, blacklist)?'),
 ('P-04', 'Module 2', 'OTP validity / expiry period.'),
 ('P-05', 'Module 2', 'Resend and wrong attempt blocks to be enforced server side against the mobile number (currently held in the prototype browser storage). Confirm reset conditions for the counters.'),
 ('P-06', 'Module 3', 'PAN Verification screen: field level rules, PAN format validation, name as per PAN matching logic and DOB / age rule.'),
 ('P-07', 'Module 2', 'Experian failure / timeout behaviour and the effect of the score on eligibility and offers.'),
 ('P-08', 'All', 'Where should the header Shriram Credit logo navigate in the live journey (shriramcredit.in, the LAMF landing page, or nowhere)? The prototype sends it to its own review home page.'),
 ('P-09', 'Module 2', 'Experian response (INT-001 Expected Output): what exactly comes back from Experian – only the credit score (e.g. 750), or the score plus the full credit report (existing loans, EMIs, missed payments, recent loan enquiries)? How should a “No record found” response be handled for a customer with no credit history? Depends on the Experian service Shriram Credit has signed up for.'),
 ('P-10', 'Module 1 & 2', 'OTP service provider (INT-002): which vendor sends and verifies the OTP, and what the customer sees if OTP verification fails or times out (a failure to send is covered in P-02).'),
]

# Answered clarifications: (ID, Module, Question, Answer, Answered on).
# P-11 – P-15 were answered on 23-09-2026, before this PRD was written (log PEND-006 – PEND-010).
COMPLETED = [
 ('P-11', 'Module 2', 'OTP length, resend timer duration and number of resends allowed.',
  '6 digit OTP; 30 second resend timer; 3 resends allowed, after which the number is blocked for 15 minutes. OTP validity is still open ' + pend('P-04'), '23-09-2026'),
 ('P-12', 'Module 2', 'Wrong OTP handling – message, maximum attempts and lockout.',
  'A validation message is shown for a wrong OTP; after 3 wrong attempts the number is blocked for 60 minutes.', '23-09-2026'),
 ('P-13', 'Module 2', 'Is the Experian consent checkbox mandatory to submit the OTP?',
  'Yes. Submit OTP is enabled only when the consent is ticked and all 6 digits are entered.', '23-09-2026'),
 ('P-14', 'Module 2', 'What does the “Edit” link on the OTP screen do?',
  'Returns to the mobile number screen (02) with the entered number prefilled.', '23-09-2026'),
 ('P-15', 'Module 2', 'Which screen opens after a successful OTP submission?',
  'Enter PAN Details (screen 04), after the Experian call is triggered.', '23-09-2026'),
 ('P-01', 'Module 1', 'Validation message wording: the shared sample PRD carries “*Required”, “*Invalid mobile number” and “Error: Invalid phone number”. The messages currently built follow the wording confirmed in discussion on 22-09-2026. Confirm which set is approved.',
  'Use the new validation wording given by the owner. The PRD row shows the current live messages; the new wording is tracked as ' + todo('CR-01', 'CR-02', 'CR-03', 'CR-04') + '.', '29-09-2026'),
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
                   '<th style="width:190px">Data Points Required</th><th style="width:165px">Status</th>'
                   '</tr></thead><tbody>')
        for r in m['rows']:
            fields = r.get('fields', [])
            span = f' rowspan="{len(fields) + 1}"' if fields else ''
            out.append(f'<tr><td{span} class="sl">{r["sl"]}</td><td class="shot">{r["shot"]}</td>'
                       f'<td{span}>{r["func"]}</td><td>{r["desc"]}</td>'
                       f'<td{span} class="dp">{data_points(r["data"])}</td><td{span}><span class="tag {TAG[r["status"]]}">{r["status"]}</span></td></tr>')
            for shot, desc, st in fields:
                out.append(f'<tr><td class="shot">{shot}</td><td>{desc}</td></tr>')
        out.append('</tbody></table>')

    out.append(f'<h2>Integration Requirements{info("How to read the columns", INT_COLUMNS)}</h2><table class="int"><thead><tr>'
               '<th>ID</th><th>Integration</th><th>Purpose</th><th>Trigger</th><th>Input</th>'
               '<th>Expected Output</th><th>Success Behaviour</th><th>Failure Behaviour</th></tr></thead><tbody>')
    for row in INTEGRATIONS:
        out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>')
    out.append('</tbody></table>')

    out.append(f'<h2>Pending Clarifications<span class="count wip">{len(PENDING)}</span>{info("How to read this list", PENDING_COLUMNS)}</h2><table class="int"><thead><tr>'
               '<th style="width:70px">ID</th><th style="width:110px">Module</th><th>Clarification Required</th>'
               '</tr></thead><tbody>')
    for pid, mod, q in PENDING:
        out.append(f'<tr id="{pid}"><td>{pid}</td><td>{mod}</td><td>{q}</td></tr>')
    out.append('</tbody></table>')

    # Collapsed by default so the PRD stays short; the chevron opens it
    out.append('<details class="done"><summary>'
               f'<span class="done-title">Completed Clarifications<span class="count ok">{len(COMPLETED)}</span></span>'
               f'{info("How to read this list", COMPLETED_COLUMNS)}'
               '<span class="chev" aria-hidden="true"></span></summary>'
               '<table class="int"><thead><tr>'
               '<th style="width:70px">ID</th><th style="width:110px">Module</th><th>Clarification Required</th><th>Clarification Provided</th>'
               '</tr></thead><tbody>')
    for cid, mod, q, a, on in COMPLETED:
        out.append(f'<tr id="{cid}"><td>{cid}</td><td>{mod}</td><td>{q}</td><td>{a}<span class="answered">Answered {on}</span></td></tr>')
    out.append('</tbody></table></details>')

    # Pending Changes / Completed Changes – same pattern as the clarification lists (DISC-091)
    out.append(f'<h2>Pending Changes<span class="count impl">{len(TO_IMPLEMENT)}</span>{info("How to read this list", TODO_COLUMNS)}</h2><table class="int"><thead><tr>'
               '<th style="width:70px">ID</th><th style="width:110px">Module</th><th style="width:220px">Where in the PRD</th><th>What has to change</th>'
               '</tr></thead><tbody>')
    for tid, mod, where, what, on in TO_IMPLEMENT:
        out.append(f'<tr id="{tid}"><td>{tid}</td><td>{mod}</td><td>{where}</td><td>{what}<span class="raised">Raised {on}</span></td></tr>')
    if not TO_IMPLEMENT:
        out.append('<tr><td colspan="4">Nothing pending.</td></tr>')
    out.append('</tbody></table>')
    out.append('<details class="done"><summary>'
               f'<span class="done-title">Completed Changes<span class="count ok">{len(IMPLEMENTED)}</span></span>'
               f'{info("How to read this list", IMPLEMENTED_COLUMNS)}'
               '<span class="chev" aria-hidden="true"></span></summary>'
               '<table class="int"><thead><tr>'
               '<th style="width:70px">ID</th><th style="width:110px">Module</th><th style="width:220px">Where in the PRD</th><th>What was changed</th>'
               '</tr></thead><tbody>')
    for tid, mod, where, what, on in IMPLEMENTED:
        out.append(f'<tr id="{tid}"><td>{tid}</td><td>{mod}</td><td>{where}</td><td>{what}<span class="answered">Changed {on}</span></td></tr>')
    if not IMPLEMENTED:
        out.append('<tr><td colspan="4">None yet.</td></tr>')
    out.append('</tbody></table></details>')
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
<p class="note">This document is generated from the confirmed discussion log. Status:
<span class="tag yts">YTS</span> yet to start ·
<span class="tag wip">WIP</span> in progress – not final ·
<span class="tag ok">Completed</span> confirmed as done by the product owner.</p>
{render()}
<p class="foot">Screenshots are taken from the clickable LAMF prototype hosted locally at <code>http://localhost:8080</code>.</p>
</main>
<script src="assets/review.js"></script>
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
<p class="note">This document is generated from the confirmed discussion log. Status:
<span class="tag yts">YTS</span> yet to start ·
<span class="tag wip">WIP</span> in progress – not final ·
<span class="tag ok">Completed</span> confirmed as done by the product owner.</p>
{render()}
</main>"""
with open(os.path.join(ROOT, 'assets', 'prd-body.js'), 'w') as f:
    f.write('window.PRD_HTML = ' + _json.dumps(BODY) + ';\n')
print('SCCL_LAMF_LOS_PRD.html + assets/prd-body.js written')
