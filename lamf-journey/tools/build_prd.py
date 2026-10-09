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

def drop_off(items):
    """“Drop off” block, below Screen Content: what happens when the customer leaves this page and comes back (DISC-122)."""
    rows = ''.join(f'<li><b>{k}:</b> {v}</li>' for k, v in items)
    return f'<div class="spec"><p><b>Drop off:</b></p><ul class="content-list">{rows}</ul></div>'

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
 ('CR-06', 'Module 2', 'Sl. No 3 – Enter OTP field (wrong OTP, 1st to 3rd back to back attempt)',
  change('“Invalid OTP” on the 1st, 2nd and 3rd back to back wrong attempt',
         '“The OTP you entered is incorrect. Please try again. You have 2 attempts left.” (1st wrong attempt) / “The OTP you entered is incorrect. Please try again. You have 1 attempt left.” (2nd) / “The OTP you entered is incorrect. You have no attempts left.” (3rd). The block message on the next attempt stays as it is today'), '30-09-2026'),
 ('CR-09', 'Module 2', 'Sl. No 3 – Enter OTP field (OTP submitted after 30 seconds)',
  change('“Invalid request id”',
         '“Your OTP has expired. Please click Resend OTP to get a new OTP.” – displayed when the customer submits the OTP more than 30 seconds after it was sent'), '30-09-2026'),
 ('CR-10', 'Module 3', 'Sl. No 4 – Name as per PAN, DOB and PAN Number (field left empty)',
  change('“*Required” for every empty field',
         'A message that names the field: “Please enter your name as per PAN.” / “Please enter your date of birth as per PAN.” / “Please enter your PAN Number.”'), '30-09-2026'),
 ('CR-11', 'Module 3', 'Sl. No 4 – PAN Number field (message for a character that does not fit its position)',
  change('Message shown next to the PAN Number label as the PAN is typed:<ul><li>“1st character must be a letter”</li><li>“2nd character must be a letter”</li><li>“3rd character must be a letter”</li><li>“4th character must be a letter”</li><li>“5th character must be a letter”</li><li>“6th character must be a number”</li><li>“7th character must be a number”</li><li>“8th character must be a number”</li><li>“9th character must be a letter”</li><li>“10th character must be a letter”</li></ul>',
         'Message for each position:<ul><li>“1st character must be a letter (A–Z).”</li><li>“2nd character must be a letter (A–Z).”</li><li>“3rd character must be a letter (A–Z).”</li><li>“The 4th character must be (P) – only individual PAN is allowed.” – see CR-18</li><li>“5th character must be a letter (A–Z).”</li><li>“6th character must be a number (0–9).”</li><li>“7th character must be a number (0–9).”</li><li>“8th character must be a number (0–9).”</li><li>“9th character must be a number (0–9).”</li><li>“10th character must be a letter (A–Z).”</li></ul>'), '01-10-2026'),
 ('CR-12', 'Module 3', 'Sl. No 4 – DOB field (typed date before 01-Jan-1920 or after today)',
  change('“*Invalid date” next to the DOB label',
         '“Please enter your date of birth exactly as on your PAN card.” (owner’s wording, DISC-134)'), '01-10-2026'),
 ('CR-13', 'Module 3', 'Sl. No 4 – Name as per PAN (name verification failure, name match below 60%)',
  change('One common message “PAN verification failed” for every verification failure – it does not say whether the name, DOB or PAN Number failed (DISC-126)',
         'Shown on this PAN Details page, next to the Name as per PAN label, only when the name check fails: “Please enter your name exactly as on your PAN card.” The match percentage (60%) is never shown to the customer (DISC-117, DISC-125)'), '01-10-2026'),
 ('CR-15', 'Module 3', 'Sl. No 4 – DOB (DOB does not match the PAN records)',
  change('One common message “PAN verification failed” for every verification failure – it does not say whether the name, DOB or PAN Number failed (DISC-126)',
         'Shown on this PAN Details page, next to the DOB label, only when the DOB check fails: “Please enter your date of birth exactly as on your PAN card.”'), '05-10-2026'),
 ('CR-16', 'Module 3', 'Sl. No 4 – PAN Number (fewer than 10 characters entered)',
  change('Live message not captured – the owner set the required wording (DISC-125)',
         'Message next to the PAN Number label when Continue is clicked: “Please enter your valid PAN Number.”'), '05-10-2026'),
 ('CR-17', 'Module 3', 'Sl. No 4 – PAN Number (PAN not available in the PAN records)',
  change('One common message “PAN verification failed” for every verification failure – it does not say whether the name, DOB or PAN Number failed (DISC-126)',
         'Shown on this PAN Details page, next to the PAN Number label, only when the PAN is not available: “Please enter your PAN Number exactly as on your PAN card.”'), '05-10-2026'),
 ('CR-18', 'Module 3', 'Sl. No 4 – PAN Number (4th character – individual PAN only)',
  change('Any letter is accepted in the 4th place (e.g. CBOCA8195B can be entered); a non-letter shows “4th character must be a letter”',
         'Only P is accepted in the 4th place (individual PAN only). Any other character is not entered and “The 4th character must be (P) – only individual PAN is allowed.” is shown at once next to the PAN Number label, so a non-individual PAN is stopped in the PAN Number field itself (DISC-137)'), '06-10-2026'),
]
# Moved here only when the owner confirms the item is live in the LOS journey:
# (ID, Module, Where in the PRD, What was implemented, Implemented on)
IMPLEMENTED = [
 ('CR-14', 'Module 3', 'Sl. No 4 – Name as per PAN (characters allowed)',
  'Alphabets (A–Z) and space only. Numbers and special characters cannot be entered; what is typed is captured in CAPITAL letters. Confirmed live by the owner (DISC-128)', '05-10-2026'),
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

def icon(src):   # small icons are shown at their own size, not stretched to the column width
    return f'<img class="icon" src="prd-assets/{src}" alt="">'

def states(*pairs):
    """Several screenshots of one element, each with a caption (e.g. before / after) (DISC-105)."""
    return ''.join(f'<figure class="state">{img(src)}<figcaption>{cap}</figcaption></figure>' for src, cap in pairs)

# Row status (DISC-086): YTS = yet to start, WIP = in progress, DONE = Completed.
# A row is moved to Completed only on the owner's explicit confirmation.
YTS = 'YTS'
WIP = 'WIP'
DONE = 'Completed'
OK = WIP   # field-level status inside a row (not displayed)
RED = ' When an error is shown for this field, its border turns red.'
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
        (states(('f02-consent.png', 'Before – unticked (default)'), ('f02-consent-ticked.png', 'After – ticked')), spec(Field_Name='(Checkbox)', Field_Type='Check box',
            Action='User has to click the Checkbox. Once this checkbox is clicked then only the Continue CTA has to be enabled'), OK),
        (img('f02-tnc.png', 120), spec(Field_Name='T&amp;C', Field_Type='Hyperlink',
            Action='User has to click this hyperlink to view the Terms and Conditions. On click, the system shall redirect the user to https://www.shriramcredit.in/terms-and-conditions (opens in a new tab, so the details entered on this screen are kept).'), OK),
        (img('f02-privacy.png', 180), spec(Field_Name='Privacy Policy', Field_Type='Hyperlink',
            Action='User has to click this hyperlink to view the Privacy Policy. On click, the system shall redirect the user to https://www.shriramcredit.in/privacy-policy (opens in a new tab, so the details entered on this screen are kept).'), OK),
        (states(('f02-cta.png', 'Before – disabled (grey) until the checkbox is ticked'), ('f02-cta-enabled.png', 'After – enabled once the checkbox is ticked')), spec(Field_Name='Continue', Field_Type='CTA (Button)',
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
                   ('Experian consent checkbox text (first OTP verification only)', '“I hereby consent to appoint Shriram Credit as my authorised representative to receive my credit information from Experian for the purpose of providing/ evaluating loan offers.”'),
                   ('CTA', '“Submit OTP” – grey until all 6 digits are entered and the consent is ticked (when the checkbox is displayed), then yellow'),
                   ('Validation messages', '<ul><li>“Invalid OTP” ' + todo('CR-06') + '</li>'
                    '<li>“Maximum OTP retry limit reached. Please retry again after N minute(s).” – N is the time left in the 60 minute block</li>'
                    '<li>“Error: Maximum OTP resend limit reached. Please retry again after N minute(s).” – N is the time left in the 15 minute block</li>'
                    '<li>“Invalid request id” – OTP submitted after 30 seconds ' + todo('CR-09') + '</li>'
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
      'status': DONE,   # confirmed by the owner – do not change without the owner's instruction
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
            # Current live LOS behaviour (DISC-096, DISC-103)
            Validation=[
              '“Invalid OTP” – displayed on each wrong OTP, for the 1st, 2nd and 3rd back to back wrong attempt. Wrong attempts are counted only while the pop up stays open: if the customer closes the pop up and then enters a wrong OTP again, it is counted as the 1st attempt ' + todo('CR-06'),
              '“Maximum OTP retry limit reached. Please retry again after N minute(s).” – after 3 back to back wrong OTP attempts in the same pop up the customer is blocked for 60 minutes; displayed on the next attempt. N is the time left in the 60 minute block (e.g. a customer returning after 10 minutes sees 50)',
              '“Invalid request id” – displayed when the customer submits the OTP more than 30 seconds after it was sent (the OTP is valid for 30 seconds) ' + todo('CR-09'),
            ]), OK),
        (states(('f03-resend.png', 'Before – timer running, Resend OTP disabled'), ('f03-resend-enabled.png', 'After – timer ends, Resend OTP enabled')), spec(Field_Name='Resend OTP', Field_Type='Timer with hyperlink CTA',
            Action='The timer shall start at 0:30 and run down to 0:01. At 0 the Resend OTP CTA shall be enabled. On click, the OTP shall be sent again and the timer shall restart.',
            Condition='The customer can click Resend OTP 3 times back to back (1st, 2nd and 3rd) in the same pop up. On the next click the customer is blocked from resending for 15 minutes.',
            Validation='“Error: Maximum OTP resend limit reached. Please retry again after N minute(s).” – displayed when the customer clicks Resend OTP after the 3rd back to back resend. N is the time left in the 15 minute block (e.g. a customer returning after 10 minutes sees 5)'), OK),
        (states(('f03-consent.png', 'Before – unticked (default)'), ('f03-consent-ticked.png', 'After – ticked')), spec(Field_Name='(Checkbox) Experian consent', Field_Type='Check box',
            Action='User has to tick this checkbox to appoint Shriram Credit as the authorised representative to receive the credit information from Experian for the purpose of providing / evaluating loan offers.',
            Condition='Displayed only when the customer verifies the OTP for the first time. For a customer who has already verified the OTP earlier, the checkbox is not displayed. When displayed, Submit OTP CTA shall be enabled only when this checkbox is ticked and all 6 OTP digits are entered, so no validation is shown for the checkbox.'), OK),
        (states(('f03-cta.png', 'Before – disabled (grey) until all 6 digits are entered'), ('f03-cta-enabled.png', 'After – enabled once all 6 digits are entered')), spec(Field_Name='Submit OTP', Field_Type='CTA (Button)',
            Action='On click, the system shall validate the entered OTP. If the OTP is correct, the system shall trigger the Experian API with the mobile number to retrieve the credit score and navigate the customer to the PAN Verification screen. If the OTP is wrong, the customer shall not be allowed to proceed and the respective validation shall be displayed.',
            Condition='CTA is disabled (grey) and cannot be clicked until all 6 OTP digits are entered and the Experian consent checkbox is ticked (for a customer who has already verified the OTP earlier, the checkbox is not displayed and only the 6 digits are needed), so no validation is shown for these. Once enabled, the wrong OTP and block validations are shown under the Enter OTP field.'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 3 – PAN Verification',
  'screens': 'Screen 04) Enter PAN Details',
  'rows': [
    {
      'sl': '4',
      'shot': img('screen-04.png'),
      'func': 'User entering the Name as per PAN, DOB and PAN Number to verify the PAN',
      'desc': ('<p>On successful OTP verification the system shall navigate the customer to the PAN Details page. '
               'The mobile number verified in Sl. No 2 and 3 is carried forward and displayed as a non editable field. '
               'The Experian credit information call is triggered in the background; the customer is not made to wait for the response.</p>'
               + screen_content([
                   ('Header', 'Shriram Credit logo (left) and the logout icon (right)'),
                   ('Page title', '“PAN Details”'),
                   ('Sub text', '“Please verify your PAN to get the best loan offers”'),
                   ('Field labels', '“Mobile Number”, “Name as per PAN”, “DOB”, “PAN Number”'),
                   ('Placeholders', 'DOB: “DD/MM/YYYY”; PAN Number: “ABCDE 1234 F”'),
                   ('CTA', '“Continue”'),
                   ('Validation messages', '<ul><li>“*Required” – any field left empty ' + todo('CR-10') + '</li>'
                    '<li>“*Invalid date” – DOB typed before 01-Jan-1920 or after today ' + todo('CR-12') + '</li>'
                    '<li>PAN Number with fewer than 10 characters ' + todo('CR-16') + '</li>'
                    '<li>PAN character that does not fit its position – “1st character must be a letter” … “10th character must be a letter” (one message per position) ' + todo('CR-11') + '</li>'
                    '<li>“PAN verification failed” – name match below 60%, DOB not matching the PAN records, or PAN Number not available ' + todo('CR-13', 'CR-15', 'CR-17') + '</li></ul>'),
               ])
               + drop_off([
                   ('When', 'The customer leaves the journey on this page before the PAN verification is completed (e.g. closes the browser or tab, or logs out)'),
                   ('On return', 'When the customer comes back and logs in again with the mobile number (Sl. No 2) and OTP (Sl. No 3), on OTP verification success the customer lands on this PAN Details page'),
               ])),
      'data': ('<b>Mobile Number:</b> 9597001623 (carried from Sl. No 2)<br><br>'
               '<b>Name as per PAN:</b> up to 150 characters<br><br>'
               '<b>DOB:</b><br>DD-MMM-YYYY<br><br>'
               '<b>PAN Number:</b> ABCDE1234F<br><br>'
               '<b>Submitted Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Experian API Triggered:</b><ul><li>Yes</li><li>No</li></ul><br>'
               '<b>Experian Response:</b> ' + pend('P-09')),
      'status': DONE,   # confirmed by the owner – do not change without the owner's instruction
      'fields': [
        (img('f04-logout.png'), spec(Field_Name='Logout', Field_Type='Icon (top navigation, right corner)',
            Action='On click, the customer is logged out and lands on the Landing page (Sl. No 1), as it is the exit page.'), OK),
        (img('f04-mobile.png'), spec(Field_Name='Mobile Number', Field_Type='Display field',
            Prefilled_Value='Mobile number verified in Sl. No 2 and 3', Action='Display only, not editable'), OK),
        (img('f04-name.png'), spec(Field_Name='Name as per PAN', Field_Type='Text Field',
            Minimum_Character='1 Char', Maximum_Character='150 Char', Value_Type='User inputs', Input_Value_format='Alphabets (A–Z) and space only ' + todo('CR-14'),
            Action='User has to enter the name exactly as printed on the PAN card.',
            Condition='Numbers and special characters cannot be entered. Whatever the user types is captured in CAPITAL letters (e.g. “azhagar samy” is captured as “AZHAGAR SAMY”).'+RED,
            Validation=['“*Required” – displayed when the user clicks Continue CTA without entering the name ' + todo('CR-10'),
                        'Name match with the PAN records below 60% – “PAN verification failed” is displayed when the user clicks Continue CTA ' + todo('CR-13')]), OK),
        (states(('f04-dob.png', 'Before – type the date, or click the calendar icon'), ('f04-dob-calendar.png', 'After – calendar opened from the icon (date selected)'), ('f04-dob-invalid.png', 'Typed date outside 01-Jan-1920 to today – “*Invalid date” next to the DOB label')),
         spec(Field_Name='DOB', Field_Type='Text Field with calendar icon',
            Minimum_Character='10 Char', Maximum_Character='10 Char', Value_Type='User inputs or selects', Input_Value_format='Numeric, DD/MM/YYYY',
            Action='User can type the date of birth, or click the calendar icon and select it from the calendar pop up.',
            Condition='The calendar allows dates from 01-Jan-1920 up to today only; a date outside this range cannot be selected. Any date can be typed; a typed date before 01-Jan-1920 or after today (e.g. 05/01/1900, year 1010 or 9090) is not accepted and the field border turns red. The age limit (18 to 70 years) is not checked on this page – it is validated on the Curated Offers page, so customers outside the limit are not blocked here and can be tracked (how many come in beyond the limit).'+RED,
            Validation=['“*Required” – displayed when the user clicks Continue CTA without entering the DOB ' + todo('CR-10'),
                        '“*Invalid date” – displayed next to the DOB label when the typed date is before 01-Jan-1920 or after today ' + todo('CR-12'),
                        'DOB not matching the DOB fetched from the PAN records – “PAN verification failed” is displayed when the user clicks Continue CTA ' + todo('CR-15')]), OK),
        (states(('f04-pan.png', 'Before – empty'), ('f04-pan-filled.png', 'After – PAN shown with spaces: ABCDE 1234 F'), ('f04-pan-error.png', 'Error – field border turns red')), spec(Field_Name='PAN Number', Field_Type='Text Field',
            Minimum_Character='10 Char', Maximum_Character='10 Char', Value_Type='User inputs',
            Input_Value_format='ABCDE1234F – characters 1 to 5 letters, 6 to 9 numbers, 10th a letter. Any letter is accepted in the 4th place ' + todo('CR-18'),
            Action='User has to enter the 10 character PAN.',
            Condition='The PAN is shown with spaces as ABCDE 1234 F (e.g. CBOPA 8195 B). A character that does not fit its position cannot be entered, and a message for that position is shown at once next to the PAN Number label:<ul><li>“1st character must be a letter”</li><li>“2nd character must be a letter”</li><li>“3rd character must be a letter”</li><li>“4th character must be a letter”</li><li>“5th character must be a letter”</li><li>“6th character must be a number”</li><li>“7th character must be a number”</li><li>“8th character must be a number”</li><li>“9th character must be a letter”</li><li>“10th character must be a letter”</li></ul>E.g. CBOPA8195B and CBOCA8195B can both be entered. ' + todo('CR-11', 'CR-18') + RED,
            Validation=['“*Required” – displayed when the user clicks Continue CTA without entering the PAN Number ' + todo('CR-10'),
                        'PAN Number with fewer than 10 characters – error displayed next to the PAN Number label when the user clicks Continue CTA ' + todo('CR-16'),
                        'PAN Number not available in the PAN records – “PAN verification failed” is displayed when the user clicks Continue CTA ' + todo('CR-17')]), OK),
        (img('f04-cta.png'), spec(Field_Name='Continue', Field_Type='CTA (Button)',
            Action='On click, the system shall validate all the fields on this page and then verify the PAN details in this order, each check running only when the previous one passes:<ol><li>PAN Number – must be available in the PAN records (100% match);</li><li>DOB – must match the DOB fetched from the PAN records (100% match);</li><li>Name as per PAN – must match the name in the PAN records by 60% or more.</li></ol>The customer’s age (18 to 70 years) is not checked here – see DOB. If everything passes, the customer is taken to the next page (LOS to MF Central consent). If any check fails, the customer is not allowed to proceed and “PAN verification failed” is displayed. ' + todo('CR-13', 'CR-15', 'CR-17'),
            Condition='Always enabled.'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 4 – Mutual Fund Portfolio Fetch (MF Central)',
  'screens': 'Screen 05) LOS to MF Central Redirection consent page · Screen 06) LOS to MF Central Redirection loading page',
  'rows': [
    {
      'sl': '5',
      'shot': img('screen-05.png'),
      'func': 'User giving consent to fetch the mutual fund portfolio from MF Central and clicking the “Check Credit Limit” CTA',
      'desc': ('<p>On successful PAN verification (Sl. No 4) the system shall navigate the customer to the Credit Limit Against Mutual Fund page. '
               'The PAN Number verified in Sl. No 4 is carried forward and displayed as a non editable field. '
               'The customer gives consent to fetch the mutual fund portfolio from MF Central and clicks Check Credit Limit; the customer is then redirected to MF Central, where the portfolio for the entered PAN and mobile number is fetched to determine the eligible credit limit and the loan offers. '
               'The left side of the page shows the loan highlights and the “How it works” steps (display only). '
               'The top navigation (Credit Score and Profile icons) is described in Sl. No 6.</p>'
               + screen_content([
                   ('Header', 'Top navigation – Shriram Credit logo (left); Credit Score icon and Profile icon (right) – see Sl. No 6'),
                   ('Left panel', '“Interest rates starting from 10.5% p.a.*”; “Get a Loan up to 75% of your eligible Mutual Fund portfolio”; “Interest-only EMI payments”; “Disbursal in 2 hours post application”'),
                   ('How it works', '“How it works” – “Apply for loan within mins.” with 9 steps:<ol>'
                    '<li>Check your eligibility, credit limit, and interest rates.</li>'
                    '<li>Select mutual fund units to pledge.</li>'
                    '<li>Complete your KYC verification.</li>'
                    '<li>Pledge your selected mutual fund units.</li>'
                    '<li>Your loan amount is approved, Sanction Letter with Key Fact Statement (KFS) is issued.</li>'
                    '<li>e-Sign the loan agreement.</li>'
                    '<li>Your loan account is ready to use.</li>'
                    '<li>Withdraw funds as needed.</li>'
                    '<li>Repay the loan at your convenience and regain complete control of your mutual fund holdings.</li></ol>'),
                   ('Card title', '“Credit Limit Against Mutual Fund”'),
                   ('Sub text', '“Mutual fund will be fetched from MF Central to determine the eligible credit limit and best loan offers”'),
                   ('Field label', '“PAN Number”'),
                   ('Consent checkbox text', '“I authorize Shriram Credit to fetch my mutual fund portfolio holdings from MF Central to assess my eligibility and credit limit for a Loan Against Mutual Funds.”'),
                   ('CTA', '“Check Credit Limit” – grey until the consent is ticked, then yellow'),
                   ('Validation messages', 'None on this page – the CTA stays grey until the consent is ticked'),
               ])
               + drop_off([
                   ('When', 'The customer leaves the journey on this page before clicking Check Credit Limit (e.g. closes the browser or tab)'),
                   ('On return', 'When the customer comes back and logs in again with the mobile number (Sl. No 2) and OTP (Sl. No 3), on OTP verification success the customer lands on this page, with the PAN Number prefilled'),
               ])),
      'data': ('<b>PAN Number:</b> ABCDE1234F (carried from Sl. No 4)<br><br>'
               '<b>MF Central Consent:</b><ul><li>Yes</li><li>No</li></ul><br>'
               '<b>Consent Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Check Credit Limit Clicked Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS'),
      'status': WIP,
      'fields': [
        (img('f05-pan.png'), spec(Field_Name='PAN Number', Field_Type='Display field',
            Prefilled_Value='PAN Number verified in Sl. No 4, shown with spaces as ABCDE 1234 F', Action='Display only, not editable'), OK),
        (states(('f05-consent.png', 'Before – unticked (default)'), ('f05-consent-ticked.png', 'After – ticked')),
         spec(Field_Name='(Checkbox) MF Central consent', Field_Type='Check box',
            Action='User has to tick this checkbox to authorize Shriram Credit to fetch the mutual fund portfolio holdings from MF Central to assess the eligibility and credit limit for a Loan Against Mutual Funds.',
            Condition='Unticked by default. Check Credit Limit CTA is enabled only when this checkbox is ticked, so no validation is shown for the checkbox.'), OK),
        (states(('f05-cta.png', 'Before – disabled (grey) until the consent is ticked'), ('f05-cta-enabled.png', 'After – enabled once the consent is ticked')),
         spec(Field_Name='Check Credit Limit', Field_Type='CTA (Button)',
            Action='On click, the system shall record the MF Central consent and open the MF Central redirection pop up (Sl. No 7); after the 5 second countdown the customer is redirected to MF Central to fetch the mutual fund portfolio for the entered PAN Number and mobile number.',
            Condition='CTA is disabled (grey) and cannot be clicked until the consent checkbox is ticked, so no validation is shown.'), OK),
      ],
    },
    {
      'sl': '7',
      'shot': img('f07-redirect.png'),
      'func': 'MF Central redirection pop up after clicking “Check Credit Limit” – countdown, then redirect to MF Central',
      'desc': ('<p>On clicking Check Credit Limit (Sl. No 5) the system shall open the MF Central redirection pop up over the page. '
               'The pop up counts down from 5 seconds to 1 second (“Redirecting to MF Central in 5 seconds” … “1 seconds”) while the progress bar fills; '
               'when the countdown ends, MF Central checks the PAN and mobile number combination: if data is available the customer is redirected to the MF Central page (Sl. No 8), otherwise the “isn’t linked to the PAN” page is shown (Sl. No 9). '
               'If the customer clicks the close icon, a confirmation pop up asks whether to cancel the portfolio fetch.</p>'
               + screen_content([
                   ('Logo', 'MF Central logo'),
                   ('Countdown', '“Redirecting to MF Central in N seconds” – N counts down 5, 4, 3, 2, 1; a yellow progress bar fills as it counts'),
                   ('Heading', '“Here’s what you need to do”'),
                   ('Steps', '<ol><li>Enter the 6-digit OTP received from MF Central on your mobile number.</li><li>Select all the AMCs and continue</li></ol>'),
                   ('Note', '“Note You’ll return to the process automatically after completing this step.”'),
                   ('Close icon', '(X) at the top right'),
                   ('Cancel confirmation pop up', '“Are you sure you want to cancel your mutual fund portfolio fetch?” with “No, don’t” and “Yes, cancel”'),
               ])),
      'data': ('<b>Redirection Pop up Shown Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Cancel Clicked:</b><ul><li>Yes, cancel</li><li>No, don’t</li></ul><br>'
               '<b>Cancel Clicked Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Redirected to MF Central Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS'),
      'status': WIP,
      'fields': [
        (img('f07-countdown.png'), spec(Field_Name='Redirection countdown', Field_Type='Timer with progress bar',
            Action='Starts at 5 seconds and counts down to 1 second; when it ends the customer is redirected to the MF Central page automatically.',
            Condition='The countdown stops while the cancel confirmation pop up is open.'), OK),
        (icon('f07-close.png'), spec(Field_Name='(X) Close icon', Field_Type='Icon',
            Action='On click, the system shall open the cancel confirmation pop up.'), OK),
        (img('f07-cancel.png'), spec(Field_Name='Cancel confirmation pop up', Field_Type='Pop up',
            Action='Shows “Are you sure you want to cancel your mutual fund portfolio fetch?” with two CTAs: “No, don’t” and “Yes, cancel”.'), OK),
        (img('f07-no.png'), spec(Field_Name='No, don’t', Field_Type='CTA (text button)',
            Action='On click, the confirmation pop up closes and the redirection pop up continues, with the countdown starting again from 5 seconds.'), OK),
        (img('f07-yes.png'), spec(Field_Name='Yes, cancel', Field_Type='CTA (Button)',
            Action='On click, both pop ups close, the portfolio fetch is cancelled and the customer is back on the LOS to MF Central consent page (Sl. No 5).'), OK),
      ],
    },
  ],
 },
 {
  'title': 'Module 5 – Mutual Fund Portfolio Fetching',
  'screens': 'Screen 07) MF Central Mock Page · Screen 06.1) PAN and Mobile Number not linked page',
  'rows': [
    {
      'sl': '8',
      'shot': img('screen-08.png'),
      'func': 'User entering the OTP received from MF Central to fetch the mutual fund portfolio (PAN and mobile number linked)',
      'desc': ('<p>After the redirection countdown (Sl. No 7), when MF Central has data for the PAN and mobile number combination, the customer is taken to the MF Central page. '
               'MF Central sends a 6-digit OTP to the mobile number; the customer enters it and clicks Submit to allow the mutual fund portfolio to be fetched. '
               'In UAT this page is a mock MF Central page.</p>'
               + screen_content([
                   ('Header', 'Top navigation – see Sl. No 6'),
                   ('Title', '“Mock MFCentral Page” (UAT)'),
                   ('Sub title', '“Enter Otp”'),
                   ('OTP boxes', '6 single digit boxes'),
                   ('CTA', '“Submit” – grey until all 6 digits are entered, then yellow'),
               ])),
      'data': ('<b>MF Central OTP Submitted Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>MF Central OTP Status:</b><ul><li>Success</li><li>Failure</li></ul>'),
      'status': WIP,
      'fields': [
        (img('f08-otp.png'), spec(Field_Name='Enter Otp', Field_Type='OTP field (6 boxes)',
            Minimum_Character='6 Char', Maximum_Character='6 Char', Input_Value_format='Numeric',
            Action='User has to enter the 6-digit OTP received from MF Central on the mobile number.',
            Validation='Wrong OTP message and attempt limit on the MF Central page to be confirmed ' + pend('P-21')), OK),
        (img('f08-submit.png'), spec(Field_Name='Submit', Field_Type='CTA (Button)',
            Action='On click with the correct OTP, MF Central shares the mutual fund portfolio and the customer is returned to the LOS (MF Central to LOS redirecting page).',
            Condition='Disabled (grey) until all 6 digits are entered.'), OK),
      ],
    },
    {
      'sl': '9',
      'shot': img('screen-09.png'),
      'func': 'PAN and mobile number not linked – MF Central has no data for the combination',
      'desc': ('<p>After the redirection countdown (Sl. No 7), when MF Central has no data for the PAN and mobile number combination, the customer is not taken to MF Central; '
               'a separate page is shown saying the mobile number is not linked to the PAN entered.</p>'
               + screen_content([
                   ('Header', 'Top navigation – see Sl. No 6'),
                   ('Illustration', 'Three cards with question marks'),
                   ('Message', '“The identifier below isn’t linked to the PAN you entered”'),
                   ('Mobile number', 'Phone icon with the masked mobile number (e.g. +919XXXX1623)'),
                   ('CTA', '“Refresh” with the refresh icon'),
               ])),
      'data': ('<b>Not Linked Page Shown Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS<br><br>'
               '<b>Refresh Clicked:</b><ul><li>Yes</li><li>No</li></ul><br>'
               '<b>Refresh Clicked Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS'),
      'status': WIP,
      'fields': [
        (img('f09-message.png'), spec(Field_Name='Not linked message', Field_Type='Display text',
            Action='“The identifier below isn’t linked to the PAN you entered” – display only.'), OK),
        (img('f09-mobile.png'), spec(Field_Name='Mobile number', Field_Type='Display field',
            Prefilled_Value='Mobile number verified in Sl. No 2 and 3, masked as +91 + first digit + XXXX + last 4 digits',
            Action='Display only, not editable'), OK),
        (icon('f09-refresh.png'), spec(Field_Name='Refresh', Field_Type='CTA',
            Action='On click, the MF Central fetch is tried again ' + pend('P-21')), OK),
      ],
    },
  ],
 },
 {
  'title': 'Top Navigation',
  'screens': 'Screen 04) Enter PAN Details – logo and Logout only (Sl. No 6.3) · every page from Screen 05) LOS to MF Central Redirection consent page onwards – logo, Credit Score and Profile (Sl. No 6, 6.1, 6.2)',
  'rows': [
    {
      'sl': '6',
      'shot': img('f06-topnav.png'),
      'func': 'Top navigation shown on every page after PAN verification',
      'desc': ('<p>The top navigation is shown at the top of every page from Sl. No 5 onwards and stays fixed when the page is scrolled (the PAN Details page has its own top navigation – see Sl. No 6.3). '
               'It gives the customer access to the credit score fetched from Experian and to the profile (with Logout) from any page.</p>'
               + screen_content([
                   ('Left', 'Shriram Credit logo'),
                   ('Right', 'Credit Score icon (Sl. No 6.1) and Profile icon (Sl. No 6.2)'),
               ])),
      'data': 'Captured in Sl. No 6.1 and 6.2',
      'status': WIP,
      'fields': [
        (icon('f06-logo.png'), spec(Field_Name='Shriram Credit logo', Field_Type='Image (top navigation, left corner)',
            Action='Display only.'), OK),
        (icon('f05-credit-icon.png'), spec(Field_Name='Credit Score icon', Field_Type='Icon (top navigation, right corner)',
            Action='On click, opens the credit score pop up – see Sl. No 6.1.'), OK),
        (icon('f05-profile-icon.png'), spec(Field_Name='Profile icon', Field_Type='Icon (top navigation, right corner)',
            Action='On click, opens the Profiles pop up – see Sl. No 6.2.'), OK),
      ],
    },
    {
      'sl': '6.1',
      'shot': img('f05-credit-report.png'),
      'func': 'User clicking the Credit Score icon in the top navigation to view the credit score',
      'desc': ('<p>The Credit Score icon is part of the top navigation (Sl. No 6). '
               'On click, the system shall open the credit score pop up over the current page, showing the credit score fetched from Experian (Sl. No 3). '
               'The customer stays on the same page; closing the pop up returns to it. What the pop up shows when Experian returns no score (no credit history / no record found / Experian call failed) is to be confirmed ' + pend('P-20') + '</p>'
               + screen_content([
                   ('Title', '“Your credit score as of DD MMM YYYY” – the date the score was fetched (e.g. 07 Oct 2026)'),
                   ('Score meter', 'The score on a 300 – 900 meter (e.g. 790), with its category below it (e.g. “Very Good”); “300” and “900” at the ends'),
                   ('Category table', '<table class="mini"><tr><th>Category</th><th>Score Range</th></tr><tr><td><i style="background:#1E8E3E"></i>Excellent</td><td><b>826 - 900</b></td></tr><tr><td><i style="background:#34C759"></i>Very Good</td><td><b>776 - 825</b></td></tr><tr><td><i style="background:#FFC107"></i>Good</td><td><b>701 - 775</b></td></tr><tr><td><i style="background:#FF8C1A"></i>Average</td><td><b>601 - 700</b></td></tr><tr><td><i style="background:#E02424"></i>Needs Help</td><td><b>300 - 600</b></td></tr></table>'),
                   ('Issue line', '“Issue with your Credit Score? Raise an issue”'),
                   ('Footer', '“Powered by experian”'),
                   ('Close icon', '(X) at the top right'),
               ])),
      'data': ('<b>Credit Score Viewed:</b><ul><li>Yes</li><li>No</li></ul><br>'
               '<b>Credit Score Viewed Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS'),
      'status': WIP,
      'fields': [
        (icon('f05-credit-icon.png'), spec(Field_Name='Credit Score icon', Field_Type='Icon (top navigation, right corner)',
            Action='On click, the system shall open the credit score pop up.'), OK),
        (img('f06-raise-issue.png'), spec(Field_Name='Raise an issue', Field_Type='Hyperlink',
            Action='Shown as “Issue with your Credit Score? Raise an issue”. On click, the system shall open https://www.experian.com/help/dispute-credit/ in a new tab; the pop up stays open.'), OK),
        (icon('f06-close-credit.png'), spec(Field_Name='(X) Close icon', Field_Type='Icon',
            Action='On click, the credit score pop up is closed and the customer stays on the same page.'), OK),
      ],
    },
    {
      'sl': '6.2',
      'shot': img('f05-profile.png'),
      'func': 'User clicking the Profile icon in the top navigation to view the profile or log out',
      'desc': ('<p>The Profile icon is part of the top navigation (Sl. No 6). '
               'On click, the system shall open the Profiles pop up over the current page, showing the name fetched from the PAN records and the PAN Number, with the Logout CTA.</p>'
               + screen_content([
                   ('Title', '“Profiles”'),
                   ('Profile card', 'Initial letter of the name, the name as per PAN (e.g. AZHAGARSAMY SUBBURAJ) and the PAN Number (e.g. CBOPA8195B), with a tick'),
                   ('CTA', '“Logout” with the logout icon'),
                   ('Close icon', '(X) at the top right'),
               ])),
      'data': ('<b>Profile Viewed:</b><ul><li>Yes</li><li>No</li></ul><br>'
               '<b>Profile Viewed Date &amp; Time:</b><br>DD-MMM-YYYY; HH:MM:SS'),
      'status': WIP,
      'fields': [
        (icon('f05-profile-icon.png'), spec(Field_Name='Profile icon', Field_Type='Icon (top navigation, right corner)',
            Action='On click, the system shall open the Profiles pop up.'), OK),
        (icon('f06-logout-cta.png'), spec(Field_Name='Logout', Field_Type='CTA',
            Action='On click, the customer is logged out and lands on the Landing page (Sl. No 1).'), OK),
        (icon('f06-close-profile.png'), spec(Field_Name='(X) Close icon', Field_Type='Icon',
            Action='On click, the profile pop up is closed and the customer stays on the same page.'), OK),
      ],
    },
    {
      'sl': '6.3',
      'shot': img('f06-topnav-pan.png'),
      'func': 'Top navigation on the PAN Details page – logo and Logout',
      'desc': ('<p>On the PAN Details page (Sl. No 4) only, the top navigation shows the Shriram Credit logo and the Logout icon. '
               'The Logout icon is shown directly in the top navigation (not inside the Profiles pop up). '
               'The Credit Score and Profile icons are not shown on this page; from Sl. No 5 onwards Logout is available inside the Profiles pop up (Sl. No 6.2).</p>'
               + screen_content([
                   ('Left', 'Shriram Credit logo'),
                   ('Right', 'Logout icon'),
               ])),
      'data': 'No data captured from this navigation',
      'status': WIP,
      'fields': [
        (icon('f06-logo.png'), spec(Field_Name='Shriram Credit logo', Field_Type='Image (top navigation, left corner)',
            Action='Display only.'), OK),
        (icon('f06-logout-icon.png'), spec(Field_Name='Logout', Field_Type='Icon (top navigation, right corner)',
            Action='On click, the customer is logged out and lands on the Landing page (Sl. No 1).',
            Condition='Shown only on the PAN Details page (Sl. No 4).'), OK),
      ],
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
 ('P-21', 'Module 5', 'Mutual Fund Portfolio Fetching: (a) Sl. No 9 – what exactly happens on Refresh (MF Central checked again and the redirection pop up shown again, or something else), and can the customer change the mobile number or PAN from here; (b) Sl. No 8 – the wrong OTP message and the number of attempts allowed on the MF Central page.'),
 ('P-20', 'Top Navigation', 'Sl. No 6.1 – credit score pop up when there is no valid score. Experian scores run from 300 to 900, so a score below 300 is not returned; instead the response can carry no score for (a) a customer with no or too little credit history (new to credit), (b) no record found for the mobile number / PAN, or (c) the Experian call failing or timing out. Please check on UAT (e.g. with a new-to-credit customer) or with the tech team what the live journey does in each case: is the Credit Score icon still shown, what does the pop up show (e.g. “Score not available”, a blank meter, or an error), and does the journey continue as normal?'),
 ('P-18', 'Module 4', 'Curated Offers page: the 18 to 70 years age limit (from the DOB entered on the PAN Details page) is validated on this page, not on PAN Details, so customers outside the limit are not blocked at PAN verification and can be tracked. Message confirmed by the owner: “Applicant must be between 18 to 70 years of age.” (DISC-139). Still to confirm: where exactly on the Curated Offers page it is shown, and whether Start Application is blocked.'),
 ('P-02', 'Module 1', 'Does the Continue CTA call an OTP send API at this point, and what is the failure behaviour?'),
 ('P-03', 'Module 1', 'Any backend check on the mobile number at this stage (existing customer, ongoing application, blacklist)?'),
 ('P-05', 'Module 2', 'Resend and wrong attempt blocks to be enforced server side against the mobile number (currently held in the prototype browser storage). Confirm reset conditions for the counters.'),
 ('P-07', 'Module 2', 'Experian failure / timeout behaviour and the effect of the score on eligibility and offers.'),
 ('P-08', 'All', 'Where should the header Shriram Credit logo navigate in the live journey (shriramcredit.in, the LAMF landing page, or nowhere)? The prototype sends it to its own review home page.'),
 ('P-09', 'Module 2', 'Experian response (INT-001 Expected Output): what exactly comes back from Experian – only the credit score (e.g. 750), or the score plus the full credit report (existing loans, EMIs, missed payments, recent loan enquiries)? How should a “No record found” response be handled for a customer with no credit history? Depends on the Experian service Shriram Credit has signed up for.'),
 ('P-10', 'Module 1 & 2', 'OTP service provider (INT-002): which vendor sends and verifies the OTP, and what the customer sees if OTP verification fails or times out (a failure to send is covered in P-02).'),
]

# Answered clarifications: (ID, Module, Question, Answer, Answered on).
# P-11 – P-15 were answered on 23-09-2026, before this PRD was written (log PEND-006 – PEND-010).
COMPLETED = [
 ('P-19', 'Module 4', 'Sl. No 5 – LOS to MF Central consent page: the row is written from the prototype screen. Please share the UAT screenshots so the screenshot and field crops can be replaced, and confirm what the Dashboard and Profile icons (top right) do on this page.',
  'UAT screenshots shared (DISC-142). Credit Score icon opens the credit score pop up (score from Experian, fetched date, category, Raise an issue link to Experian, close); Profile icon opens the Profiles pop up (name as per PAN, PAN Number, Logout to the Landing page, close).', '07-10-2026'),
 ('P-16', 'Module 2', 'Experian consent checkbox: the UAT screenshots shared on 30-09-2026 (uatlamf.shriramcredit.in) show the Enter OTP pop up without the Experian consent checkbox, and Submit OTP turns yellow as soon as 6 digits are entered. Sl. No 3 describes the checkbox as mandatory. Confirm whether the checkbox is part of the live journey.',
  'The checkbox is displayed only when the customer verifies the OTP for the first time. A customer who has already verified the OTP earlier sees the Enter OTP pop up without the checkbox, and Submit OTP is enabled once all 6 digits are entered (DISC-129).', '05-10-2026'),
 ('P-17', 'Module 3', 'PAN Details page: the exact live text for (a) a PAN Number not in the ABCDE1234F format, and (b) the PAN verification failures – name match below 60%, DOB not matching the PAN records, PAN not available. Also: where does the customer land after Logout?',
  'Live: one common message “PAN verification failed” for every verification failure (DISC-126). The owner set the required messages (DISC-125): empty fields – CR-10; PAN with fewer than 10 characters – “Please enter your valid PAN Number.” (CR-16); name match below 60% – “Please enter your name exactly as on your PAN card.” (CR-13); DOB not matching – “Please enter your date of birth exactly as on your PAN card.” (CR-15); PAN not available – “Please enter your PAN Number exactly as on your PAN card.” (CR-17). Logout lands on the Landing page (exit page).', '05-10-2026'),
 ('P-11', 'Module 2', 'OTP length, resend timer duration and number of resends allowed.',
  '6 digit OTP; 30 second resend timer; 3 resends allowed, after which the number is blocked for 15 minutes. OTP validity: 30 seconds (see P-04).', '23-09-2026'),
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
 ('P-04', 'Module 2', 'OTP validity / expiry period.',
  'The OTP is valid for 30 seconds. An OTP submitted later shows “Invalid request id” today; the new wording is tracked as ' + todo('CR-09') + '.', '30-09-2026'),
 ('P-06', 'Module 3', 'PAN Verification screen: field level rules, PAN format validation, name as per PAN matching logic and DOB / age rule.',
  'Name as per PAN: alphanumeric, up to 150 characters. DOB: typed (DD/MM/YYYY) or picked from the calendar, 01-Jan-1920 to today, age 18 to 70 years. PAN: ABCDE1234F format. Continue validates every field; an empty field shows “*Required”. Name match threshold: 60% (answered later). Exact error texts are still open ' + pend('P-17') + '.', '30-09-2026'),
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
            out.append(f'<tr id="sl-{r["sl"]}"><td{span} class="sl">{r["sl"]}</td><td class="shot">{r["shot"]}</td>'
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
<script>
  // Opened from the journey's "Go to PRD" button (#sl-5 etc.): bring that row into view and highlight it (DISC-153)
  (function () {{
    var t = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!t) return;
    setTimeout(function () {{ t.scrollIntoView({{ block: 'start' }}); t.classList.remove('flash'); void t.offsetWidth; t.classList.add('flash'); }}, 60);
  }})();
</script>
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
