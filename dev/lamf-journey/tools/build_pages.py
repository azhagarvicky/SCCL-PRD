# Generates one HTML file per screenshot. Content comes from assets/lamf.js templates,
# so shared components stay in one place. Re-run after adding a screen: python3 tools/build_pages.py
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR = "LAMF.T.curated()"
CUR75 = "LAMF.T.curated()"
SEL = "LAMF.T.selection(LAMF.SEL_DEFAULT)"
PAGES = {
 "01) LAMF Landing Page": "LAMF.render(LAMF.T.landing())",
 "02) Enter MF linked Mobile Number": "LAMF.render(LAMF.withModal(LAMF.T.landing(), LAMF.T.mobileModal()))",
 "03) Enter OTP for MF linked Mobile Number Verification": "LAMF.render(LAMF.withModal(LAMF.T.landing(), LAMF.T.otpModal()))",
 "04) Enter PAN Details": "LAMF.render(LAMF.T.pan())",
 "05) LOS to MF Central Redirection consent page": "LAMF.render(LAMF.T.consent())",
 "06) LOS to MF Central Redirection loading page": "LAMF.render(LAMF.withModal(LAMF.T.consent(), LAMF.T.mfcModal()))",
 "07) MF Central Data Check Mock": "LAMF.render(LAMF.withModal(LAMF.T.consent(), LAMF.T.dataMockModal()))",
 "07.1) PAN and Mobile Number Combination No Data Available": "LAMF.render(LAMF.T.notLinked())",
 "07.2) MF Central OTP Page": "LAMF.render(LAMF.T.mfMock())",
 "07.3) MF Central Select AMCs Page": "LAMF.render(LAMF.T.mfcAmc())",
 "07.4) MF Central Portfolio Fetching Page": "LAMF.render(LAMF.T.mfcFetching())",
 "07.5) MF Central Portfolio Discovery Complete Page": "LAMF.render(LAMF.T.mfcDone())",
 "08) MF Central to LOS Redirecting Page": "LAMF.render(LAMF.T.redirecting())",
 "09) MF Central to LOS Fetching Mutual Fund Portfolio Page": "LAMF.render(LAMF.withModal(LAMF.T.consent(), LAMF.loader('Fetching your mutual fund portfolio..', 1)))",
 "10) MF Central to LOS Analysing Mutual Fund Portfolio Page": f"LAMF.render(LAMF.withModal({CUR}, LAMF.loader('Analyzing your mutual fund portfolio..', 2)))",
 "11) MF Central to LOS Generating Loan Page": f"LAMF.render(LAMF.withModal({CUR}, LAMF.loader('Generating best loan offers for you', 3)))",
 "12) Curated Offers Page": f"LAMF.render({CUR})",
 "12.1.1) How is it calculated_All Portfolio": "LAMF.render(LAMF.T.calc('all'))",
 "12.1.2) How is it calculated_Eligible Portfolio": "LAMF.render(LAMF.T.calc('eligible'))",
 "12.1.3) How is it calculated_Non Eligible Portfolio": "LAMF.render(LAMF.T.calc('ne'))",
 "12.2) Curated offers page for dorpoff view": "LAMF.render(LAMF.T.curated({dropoff:true}))",
 "12.2) Refresh portfolio": f"LAMF.render(LAMF.withModal({CUR75}, LAMF.T.refreshModal()))",
 "13.1) Mutual Fund Selection Location access": f"LAMF.render({SEL} + LAMF.T.locationPopup(), {{bodyClass:'scrolled-bottom'}})",
 "13.2) Mutual Fund Selection Page": f"LAMF.render({SEL})",
 "13.3) Mutual Fund Selection page if location disabled": "LAMF.render(LAMF.T.selection(Object.assign({ctaDisabled:true}, LAMF.SEL_DEFAULT)) + '<div class=\"overlay\" style=\"background:rgba(40,40,40,.4)\"></div>' + LAMF.T.locationToast(), {bodyClass:'scrolled-bottom'})",
 "13.4) Mutual Fund Selection page if location disabled & proceed": f"LAMF.render(LAMF.withModal({SEL}, LAMF.T.ongoingModal(), true) + LAMF.T.locationPopup(), {{bodyClass:'scrolled-bottom'}})",
 "13.5) Mutual Fund Selection page loan amount edit": "LAMF.render(LAMF.T.selection({editLoan:'9530700', sliderPct:47.6, mv:'1,27,07,600.09', count:1, selected:{icici:'95,30,700'}, ctaDisabled:true, cta:'95,30,700'}))",
 "13.6) Mutual Fund Selection page loan amount edit as fund wise": "LAMF.render(LAMF.T.selection({loan:'95,30,700', sliderPct:47.6, mv:'1,27,07,600.09', count:1, editing:{icici:'100000'}, cta:'95,30,700'}), {bodyClass:'scrolled-sel'})",
 "14) Loan Application Summary": "LAMF.render(LAMF.T.summary())",
 "16.1) KYC Verification Page": "LAMF.render(LAMF.T.kyc({email:'input'}))",
 "16.2) KYC Verification Page view details popup": "LAMF.render(LAMF.withModal(LAMF.T.kyc({email:'input'}), LAMF.T.loanDetailsModal()))",
 "16.3) KYC Verification Page Email verification popup": "LAMF.render(LAMF.withModal(LAMF.T.kyc({email:'filled'}), LAMF.T.emailOtpModal()))",
 "16.4) KYC Verification Page email verification completed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'start'}))",
 "16.5.1) KYC Verification Page Aadhar verification": "LAMF.render(LAMF.T.digio(false))",
 "16.5.2) KYC Verification Page Aadhar verification Enter aadhar": "LAMF.render(LAMF.T.digilocker('aadhaar'))",
 "16.5.3) KYC Verification Page Aadhar verification Enter aadhar OTP": "LAMF.render(LAMF.T.digilocker('otp'))",
 "16.5.4) KYC Verification Page Aadhar verification Enter PIN": "LAMF.render(LAMF.T.digilocker('pin'))",
 "16.5.5) KYC Verification Page Aadhar verification Fetching": "LAMF.render(LAMF.T.digio(true))",
 "16.5.6) KYC Verification Page Aadhar verification process done in digilocker yet to redirect to los": "LAMF.render(LAMF.T.digioExit())",
 "16.5.7) KYC Verification Page Aadhar verification process done in digilocker  to los auto redirection": "LAMF.render(LAMF.T.kycRedirect())",
 "16.5.8) KYC Verification Page Aadhar verification process done in digilocker  redirected to los but status getting updated": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'status'}), {bodyClass:'scrolled-kyc'})",
 "16.5.9) KYC Verification Page Aadhar verification completed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'start'}))",
 "16.6) KYC Verification Page Photo verification Mock": "LAMF.render(LAMF.T.kycMock())",
 "16.6.1) KYC Verification Page Photo verification failed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'start', photoErr:'Photo verification failed. Please try again.'}))",
 "16.7) KYC Verification Page Bank details": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'done', bankForm:LAMF.T.bankForm('AZHAGARSAMY SUBBURAJ'), cont:'off'}))",
 "16.8) KYC Verification Page KYC completed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'done', bank:LAMF.BANK_DEMO, cont:'on'}))",
 "17) Customer Details Page": "LAMF.render(LAMF.T.custDetails())",
 "18) Pledging of Mutual Fund Page": "LAMF.render(LAMF.T.pledge())",
 "18.1) Pledging of Mutual Fund OTP popup": "LAMF.render(LAMF.withModal(LAMF.T.pledge(), LAMF.T.pledgeOtpModal()))",
 "18.2) Pledging of Mutual Fund Successfully pledged": "LAMF.render(LAMF.withModal(LAMF.T.pledge({status:'pledged'}), LAMF.T.pledgedModal()))",
 "19) Agreement and E-Mandate Page": "LAMF.render(LAMF.T.agreement())",
 "20) Sanction Letter Page": "LAMF.render(LAMF.T.sanction())",
 "21) Loan Agreement e-Sign Page": "LAMF.render(LAMF.T.esign())",
 "21.1) Loan Agreement e-Sign OTP popup": "LAMF.render(LAMF.T.esign() + LAMF.T.esignOtpModal())",
 "21.2) Loan Agreement e-Sign Signed Successfully": "LAMF.render(LAMF.T.esignDone())",
 "21.3) Loan Agreement Signed Successfully": "LAMF.render(LAMF.T.agreementSigned())",
 "19.1) Agreement and E-Mandate Page Loan Agreement signed": "LAMF.render(LAMF.T.agreement(true))",
 "22) E-Mandate Page": "LAMF.render(LAMF.T.emandate())",
 "22.1) E-Mandate NPCI Simulation Page": "LAMF.render(LAMF.T.npci())",
 "22.2) E-Mandate Authenticated Successfully": "LAMF.render(LAMF.T.emandateDone())",
 "19.2) Agreement and E-Mandate Page E-Mandate failed": "LAMF.render(LAMF.T.agreement(true, 'failed'))",
 "23) Loan Application Submitted Page": "LAMF.render(LAMF.T.submitted())",
 "24) Your Loans Page": "LAMF.render(LAMF.T.loanSubmitted())",
}
TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="assets/lamf.css">
</head>
<body>
<script src="assets/lamf.js"></script>
<script>{code}</script>
<script src="assets/review.js"></script>
</body>
</html>
"""
for name, code in PAGES.items():
    with open(os.path.join(ROOT, name + ".html"), "w") as f:
        f.write(TPL.format(title=html.escape(name), code=code))
from urllib.parse import quote

# Home page (index.html) and screen list (screens.html). Same markup for the local
# files and the cloud copy; only the link targets differ. Styles live in lamf.css.
LOGO = '<a class="logo" href="{home}" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a>'

# Customer communications (SMS / mail) sent by the LOS – shown on communications.html (DISC-176).
# Columns follow the owner's sheet "Oct_2026": S.No, Stage, Scenarios, Application, Communication Type,
# Sender, Content Structure, Actual Content, Mail Subject, SMS Header, Available. Add new rows here.
COMMS = [
 ("Enter Mobile Number Page",
  "After entered the mobile number and user clicking the “Continue” CTA on “Enter your MF linked Mobile Number” page",
  "LOS", "SMS", "SCCL",
  "{#numeric#} is your OTP to sign in to Shriram Credit Loan Against Mutual Fund. Do not share this OTP with anyone - Shriram Credit",
  "<u>123456</u> is your OTP to sign in to Shriram Credit Loan Against Mutual Fund. Do not share this OTP with anyone - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Mutual Fund Portfolio fetching in MF Central",
  "After clicked the “Check Credit Limit” CTA in “LOS to MF Central Redirection consent page” then in MF central, there is no data available the combination of “mobile number” and “PAN Number”",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, No Mutual Fund investments were found for the details you provided. Please verify your credentials and try again - Shriram Credit",
  "Dear AZHAGARSAMY, No Mutual Fund investments were found for the details you provided. Please verify your credentials and try again - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Applying SCCL’s Eligibility Business Rule Engine (BRE)",
  "After fetched mutual fund portfolio from MF central then applying SCCL’s eligibility BRE, as per BRE users not eligible",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, We regret that your loan request could not be approved per our policy. For assistance, contact our support team - Shriram Credit",
  "Dear AZHAGARSAMY, We regret that your loan request could not be approved per our policy. For assistance, contact our support team - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Pledging of Mutual Fund",
  "After the mutual fund units are successfully pledged on the “Pledging of Mutual Fund” page (Pledge Securities → MF Central OTP → “Successfully pledged!”)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Mutual Fund units have been successfully pledged against your loan with Shriram Credit. You may now proceed further - Shriram Credit",
  "Dear AZHAGARSAMY, Your Mutual Fund units have been successfully pledged against your loan with Shriram Credit. You may now proceed further - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Sanction Letter",
  "After the Sanction Letter is generated successfully (customer clicks “Sign Agreement” on the “Agreement and E-Mandate” page and the Sanction Letter is generated)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Loan Against Mutual Fund has been sanctioned. Your Sanction Letter will be shared separately. Please proceed to sign the eAgreement to continue your loan journey - Shriram Credit",
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund has been sanctioned. Your Sanction Letter will be shared separately. Please proceed to sign the eAgreement to continue your loan journey - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Loan Agreement e-Sign",
  "After the customer signs the loan agreement successfully (e-Sign at Digio – Aadhaar / VID + OTP → “Signed Successfully”)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Loan Against Mutual Fund application has been successfully processed - Shriram Credit.",
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund application has been successfully processed - Shriram Credit.",
  "-", "SGRCDT-T", "Yes"), ("LAMF Application Submit",
  "Once the E-Mandate is completed successfully – the loan application is then considered submitted",
  "LOS", "SMS", "SCCL",
  "Dear {#alp#}, Your Loan Against Mutual Fund application has been successfully submitted - Shriram Credit",
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund application has been successfully submitted - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Loan Lodgement Approval",
  "After the application is submitted, the OPS team approves in the backend LMS, back to back: first the Loan Account Opening approval, then the Loan Lodgement approval. This SMS is triggered when the Loan Lodgement is approved",
  "LMS", "SMS", "SCCL",
  "Dear {#alp#}, Your Shriram Credit - Loan Against Mutual Fund is approved and active. Withdraw your funds now:- {#urg#} - Shriram Credit",
  "Dear AZHAGARSAMY, Your Shriram Credit - Loan Against Mutual Fund is approved and active. Withdraw your funds now:- https://lamf.shriramcredit.in/ - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Loan Account Opening / Loan Lodgement Rejection",
  "When the OPS team rejects the Loan Account Opening or the Loan Lodgement in the backend LMS – one common SMS for either rejection, with a payment link for the charges the customer has to pay (processing fee, lien marking and lien removal). Template drafted by Claude for approval; to be created and registered",
  "LMS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, We regret that your Loan Against Mutual Fund application could not be approved. Please pay the applicable charges (processing fee, lien marking and lien removal) of Rs. {#alphanumeric#} using this link: {#urg#} - Shriram Credit",
  "Dear AZHAGARSAMY, We regret that your Loan Against Mutual Fund application could not be approved. Please pay the applicable charges (processing fee, lien marking and lien removal) of Rs. 92,313 using this link: https://lamf.shriramcredit.in/ - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created"),
 ("Withdrawal",
  "When the customer initiates a withdrawal from the loan account, an OTP is sent to confirm the withdrawal",
  "LOS", "SMS", "SCCL",
  "{#numeric#} is your OTP to confirm the withdrawal of Rs. {#alphanumeric#} from your Loan Against Mutual Fund. Do not share this OTP with anyone - Shriram Credit",
  "<u>123456</u> is your OTP to confirm the withdrawal of Rs. 10,000 from your Loan Against Mutual Fund. Do not share this OTP with anyone - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Withdrawal",
  "On the completion of each withdrawal by the customer (withdrawal request confirmed)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your withdrawal request is confirmed. Your loan amount will be disbursed to your bank account shortly - Shriram Credit.",
  "Dear AZHAGARSAMY, Your withdrawal request is confirmed. Your loan amount will be disbursed to your bank account shortly - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Loan Disbursed",
  "When the loan is disbursed – notifying the customer that the amount is credited to the bank account",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Congratulations! Your loan has been credited to your bank account. Thank you for choosing Shriram Credit - Shriram Credit.",
  "Dear AZHAGARSAMY, Congratulations! Your loan has been credited to your bank account. Thank you for choosing Shriram Credit - Shriram Credit.",
  "-", "SGRCDT-T", "Yes"), ("EMI Reminder",
  "Notifying the customer of an upcoming instalment before its due date",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} is due on {#alphanumeric#}. Please ensure sufficient balance in your bank account for timely payment - Shriram Credit.",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 is due on 05-11-2026. Please ensure sufficient balance in your bank account for timely payment - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("EMI Success",
  "Notifying the customer when the instalment is debited successfully",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was successfully debited on {#alphanumeric#}. Thank you for your timely payment - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was successfully debited on 05-11-2026. Thank you for your timely payment - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("EMI Failed",
  "Notifying the customer when the instalment bounces (rejected by the bank); the debit is retried on the 10th",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was rejected by your bank on {#alphanumeric#}. We will retry on {#alphanumeric#}. Please ensure sufficient balance - Shriram Credit.",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was rejected by your bank on 05-11-2026. We will retry on 10-11-2026. Please ensure sufficient balance - Shriram Credit.",
  "-", "SGRCDT-T", "Yes"), ("EMI Resubmission Reminder",
  "Notifying the customer before the bounced EMI is re-presented (resubmitted) to the bank",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} will be re-presented on {#alphanumeric#}. Please ensure sufficient balance to avoid any disruption - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 will be re-presented on 10-11-2026. Please ensure sufficient balance to avoid any disruption - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("EMI Resubmission Success",
  "Notifying the customer when the EMI resubmission is successful",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was successfully debited on {#alphanumeric#}. Thank you for your payment - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was successfully debited on 10-11-2026. Thank you for your payment - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("EMI Resubmission Failed",
  "Notifying the customer when the EMI resubmission fails (rejected again by the bank)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was rejected again by your bank on {#alphanumeric#}. Please check your registered email for further details - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was rejected again by your bank on 10-11-2026. Please check your registered email for further details - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Successful Loan Tenure Completion",
  "When the customer completes all the EMI instalments (loan fully repaid)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Loan fully repaid! Your MF units will be released in 2-3 working days and your loan account will be closed - Shriram Credit",
  "Dear AZHAGARSAMY, Loan fully repaid! Your MF units will be released in 2-3 working days and your loan account will be closed - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Loan Account Closure",
  "When the loan account is closed (closed on = loan end date)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your loan account {#alphanumeric#} has been successfully closed on {#alphanumeric#}. Thank you for your association with Shriram Credit - Shriram Credit",
  "Dear AZHAGARSAMY, Your loan account SCCLMF20261000102 has been successfully closed on 26-10-2027. Thank you for your association with Shriram Credit - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
]
COMMS_COLS = ["S.No", "Stage", "Scenarios", "Application", "Communication Type", "Sender", "Content Structure",
              "Actual Content", "Mail Subject", "SMS Header", "Available"]
CONTACT = ('<p class="home-contact">Created by <b>Azhagarsamy Subburaj</b>. For any observation or clarification, '
           'please reach out to <a href="mailto:azhagarsamy.s@shriramcredit.in">azhagarsamy.s@shriramcredit.in</a></p>')

def comms_body(home):
    esc = lambda t: html.escape(t, quote=False).replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")
    head = "".join(f"<th>{c}</th>" for c in COMMS_COLS)
    # a template that is not available yet (Available starts with “No”) is highlighted (DISC-190)
    rows = "".join('<tr%s><td>%d</td>%s</tr>' % (' class="na"' if r[-1].startswith("No") else "", k, "".join(f"<td>{esc(v)}</td>" for v in r))
                   for k, r in enumerate(COMMS, 1))
    return (LOGO.format(home=home) + '<h1>LAMF – Customer Communications</h1>'
            f'<p>SMS and mail sent to the customer during the LOS journey ({len(COMMS)} communications). '
            'Content Structure shows the approved template; Actual Content shows a sample with the variable filled in.</p>'
            f'<div class="comms-wrap"><table class="comms"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            + CONTACT)

def home_body(home, prd, journey, comms):
    return (f'<header class="home-top">{LOGO.format(home=home)}</header>'
            '<main class="home">'
            '<p class="home-kicker">Shriram Credit · Loan Against Mutual Funds</p>'
            '<h1>LAMF – LOS Customer Online Journey</h1>'
            '<p class="home-sub">Product requirements and the clickable prototype of the online loan journey.</p>'
            '<div class="home-ctas">'
            f'<a class="home-cta" href="{prd}">Open the PRD document →</a>'
            f'<a class="home-cta" href="{journey}">Start the LAMF journey →</a>'
            f'<a class="home-cta" href="{comms}">Customer communications →</a>'
            '</div>' + CONTACT + '</main>')

def screens_body(home, link):
    items = "\n".join(f'<li><a href="{link(n)}">{html.escape(n)}</a></li>' for n in PAGES)
    return (LOGO.format(home=home) + '<h1>LAMF Online Journey – Screens</h1>'
            f'<p>{len(PAGES)} screens, in screenshot order. Use the ☰ bar (bottom-right) or ← / → keys on any screen to move between them.</p>'
            f'<ol>{items}</ol>')

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="assets/lamf.css">
</head>
<body class="{cls}">{body}
<script src="assets/review.js"></script>
</body>
</html>
"""
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(PAGE.format(title="LAMF Online Journey", cls="page-home",
                        body=home_body("index.html", "SCCL_LAMF_LOS_PRD.html", "screens.html", "communications.html")))
with open(os.path.join(ROOT, "communications.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – Customer Communications", cls="page-screens page-comms", body=comms_body("index.html")))
with open(os.path.join(ROOT, "screens.html"), "w") as f:
    f.write(PAGE.format(title="LAMF Online Journey – Screens", cls="page-screens",
                        body=screens_body("index.html", lambda n: quote(n + ".html"))))
print(len(PAGES), "pages + index.html (home) + screens.html + communications.html written")

# ---- cloud copy: one page, hash routed (artifact sandboxes cannot navigate between files)
import json as _json
from urllib.parse import quote as _q

screens_js = ["/* Generated by tools/build_pages.py – one render function per screen. */",
              "window.SCREEN_RENDER = {"]
for name, code in PAGES.items():
    screens_js.append(f"  {_json.dumps(name)}: function () {{ {code}; }},")
screens_js.append("};")
screens_js.append("window.HOME_HTML = " + _json.dumps(home_body("#", "#PRD", "#SCREENS", "#COMMS")) + ";")
screens_js.append("window.COMMS_HTML = " + _json.dumps(comms_body("#")) + ";")
screens_js.append("window.SCREENS_HTML = " + _json.dumps(screens_body("#", lambda n: "#" + _q(n))) + ";")
with open(os.path.join(ROOT, "assets", "screens.js"), "w") as f:
    f.write("\n".join(screens_js) + "\n")

def _read(*parts):
    with open(os.path.join(ROOT, *parts)) as fh:
        text = fh.read().replace("</script", "<\\/script")
    # The artifact viewer's CSP allows Google Fonts only, so the Fontshare import
    # is dropped for the cloud copy and Plus Jakarta Sans is loaded instead.
    return "\n".join(l for l in text.split("\n") if "api.fontshare.com" not in l)

# The artifact sandbox does not apply linked stylesheets, so the cloud copy
# carries its CSS and JS inline. Images are still served as published files.
CLOUD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LAMF Online Journey</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
""" + _read("assets", "lamf.css") + "\n" + _read("assets", "prd.css") + """
</style>
</head>
<body>
<script>
  window.LAMF_SPA = true;
  // The artifact viewer nests this document inside its own <body>, so our <style>
  // and font <link> land in the body and would be wiped by the first render.
  // Move them into <head> first.
  document.querySelectorAll('body style, body link[rel="stylesheet"], body link[rel="preconnect"]')
    .forEach(function (el) { document.head.appendChild(el); });
</script>
<script>""" + _read("assets", "lamf.js") + """</script>
<script>""" + _read("assets", "screens.js") + """</script>
<script>""" + _read("assets", "prd-body.js") + """</script>
<script>
  function route() {
    var name = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (name.split('/')[0] === 'PRD' && window.PRD_HTML) {
      LAMF.renderPRD(window.PRD_HTML);
      var row = name.split('/')[1], t = row && document.getElementById(row);   // #PRD/sl-5 opens that row (DISC-153)
      if (t) setTimeout(function () { t.scrollIntoView({ block: 'start' }); t.classList.add('flash'); }, 60);
      return;
    }
    var fn = window.SCREEN_RENDER[name];
    if (fn) { fn(); return; }
    if (name === 'SCREENS') { LAMF.render(window.SCREENS_HTML, { bodyClass: 'page-screens' }); return; }
    if (name === 'COMMS') { LAMF.render(window.COMMS_HTML, { bodyClass: 'page-screens' }); document.body.classList.add('page-comms'); return; }
    LAMF.render(window.HOME_HTML, { bodyClass: 'page-home' });
  }
  window.addEventListener('hashchange', route);
  route();
</script>
</body>
</html>
"""
with open(os.path.join(ROOT, "cloud.html"), "w") as f:
    f.write(CLOUD)
print("cloud.html + assets/screens.js written")
