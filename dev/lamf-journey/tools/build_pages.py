# Generates one HTML file per screenshot. Content comes from assets/lamf.js templates,
# so shared components stay in one place. Re-run after adding a screen: python3 tools/build_pages.py
import os, html, re
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
<script src="assets/colresize.js"></script>
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
 ('LAN Generated',
  'When the customer clicks Continue on the Loan Application Summary page and the Loan Account Number (LAN) is generated successfully',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Loan Against Mutual Fund application has been initiated successfully. Your Loan Account Number is {#alphanumeric#} - Shriram Credit',
  'Dear AZHAGARSAMY, Your Loan Against Mutual Fund application has been initiated successfully. Your Loan Account Number is SCCLMF20261000102 - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Pre-Pledge Application Expiry Reminder',
  'The application is still incomplete before pledging and reaches the configured expiry-reminder date (the application expires 30 days after LAN generation)',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Loan Against Mutual Fund application {#alphanumeric#} is incomplete and will expire on {#alphanumeric#}. Please complete it before this date to avoid cancellation {#urg#} - Shriram Credit',
  'Dear AZHAGARSAMY, Your Loan Against Mutual Fund application SCCLMF20261000102 is incomplete and will expire on 26-11-2026. Please complete it before this date to avoid cancellation https://lamf.shriramcredit.in/ - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Pre-Pledge Application Discarded',
  'On Day 31 the application has not been pledged or submitted, and the system discards it automatically',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Loan Against Mutual Fund application {#alphanumeric#} was closed as it was not completed within 30 days. We would be glad to help you - start a new application anytime {#urg#} - Shriram Credit',
  'Dear AZHAGARSAMY, Your Loan Against Mutual Fund application SCCLMF20261000102 was closed as it was not completed within 30 days. We would be glad to help you - start a new application anytime https://lamf.shriramcredit.in/ - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Customer-Initiated Discard',
  'The customer selects Discard before pledging and the application is cancelled. No backend approval – it is discarded at once',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Loan Against Mutual Fund application {#alphanumeric#} has been discarded as requested. You can start a new loan application anytime {#urg#} - Shriram Credit',
  'Dear AZHAGARSAMY, Your Loan Against Mutual Fund application SCCLMF20261000102 has been discarded as requested. You can start a new loan application anytime https://lamf.shriramcredit.in/ - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ("Pledging of Mutual Fund",
  "After the mutual fund units are successfully pledged on the “Pledging of Mutual Fund” page (Pledge Securities → MF Central OTP → “Successfully pledged!”)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Mutual Fund units have been successfully pledged against your loan with Shriram Credit. You may now proceed further - Shriram Credit",
  "Dear AZHAGARSAMY, Your Mutual Fund units have been successfully pledged against your loan with Shriram Credit. You may now proceed further - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Lien Marking Failed",
  "When the lien marking (pledge) of the mutual fund units fails on the “Pledging of Mutual Fund” page. Template drafted by Claude for approval; to be created and registered",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Lien marking of your Mutual Fund units could not be completed. Please log in and try pledging again to continue your loan application: {#urg#} - Shriram Credit",
  "Dear AZHAGARSAMY, Lien marking of your Mutual Fund units could not be completed. Please log in and try pledging again to continue your loan application: https://lamf.shriramcredit.in/ - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created"),
 ('Post-Pledge Journey Incomplete',
  'Lien marking is successful, then the customer is inactive for the configured period',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Mutual Fund units are pledged for loan account {#alphanumeric#}, but your loan application is not complete yet. Please resume and complete the remaining steps {#urg#} - Shriram Credit',
  'Dear AZHAGARSAMY, Your Mutual Fund units are pledged for loan account SCCLMF20261000102, but your loan application is not complete yet. Please resume and complete the remaining steps https://lamf.shriramcredit.in/ - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Post-Pledge Application Expiry Reminder',
  'The application approaches its 30-day expiry date, is still not submitted and the lien is active',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Loan Against Mutual Fund application {#alphanumeric#} will expire on {#alphanumeric#}. Your Mutual Fund units are lien-marked. Please complete the remaining steps before this date {#urg#} - Shriram Credit',
  'Dear AZHAGARSAMY, Your Loan Against Mutual Fund application SCCLMF20261000102 will expire on 26-11-2026. Your Mutual Fund units are lien-marked. Please complete the remaining steps before this date https://lamf.shriramcredit.in/ - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Application Expired – Lien Marked',
  'The application reaches Day 31 without submission and the lien is still marked',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Your Loan Against Mutual Fund application {#alphanumeric#} has expired as it was not submitted within 30 days. Your Mutual Fund units remain lien-marked. We will share the next steps for lien removal - Shriram Credit',
  'Dear AZHAGARSAMY, Your Loan Against Mutual Fund application SCCLMF20261000102 has expired as it was not submitted within 30 days. Your Mutual Fund units remain lien-marked. We will share the next steps for lien removal - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Lien Removal Request Received',
  'SCCL receives and records the customer’s lien removal request',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, We have received your lien removal request for loan account {#alphanumeric#}. It is under review and we will update you once the lien removal is initiated - Shriram Credit',
  'Dear AZHAGARSAMY, We have received your lien removal request for loan account SCCLMF20261000102. It is under review and we will update you once the lien removal is initiated - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Lien Removal Initiated',
  'SCCL initiates the lien removal through the applicable RTA / MF Central process',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Lien removal has been initiated for the Mutual Fund units pledged against loan account {#alphanumeric#}. We will update you once it is completed - Shriram Credit',
  'Dear AZHAGARSAMY, Lien removal has been initiated for the Mutual Fund units pledged against loan account SCCLMF20261000102. We will update you once it is completed - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ('Lien Removal Successful',
  'The lien removal confirmation is received from the RTA',
  "LOS", "SMS", "SCCL",
  'Dear {#alp#}, The lien on your Mutual Fund units has been successfully removed. Your MF units are now fully accessible to you - Shriram Credit',   # owner's SMS (DISC-336)
  'Dear AZHAGARSAMY, The lien on your Mutual Fund units has been successfully removed. Your MF units are now fully accessible to you - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created (Created)"),
 ('Lien Removal Failed',
  'The lien removal request fails or is rejected by the service provider',
  "LOS", "SMS", "SCCL",
  'Dear {#alphanumeric#}, Lien removal for loan account {#alphanumeric#} could not be completed due to a processing issue. Your Mutual Fund units remain lien-marked. We are reviewing it and will update you - Shriram Credit',
  'Dear AZHAGARSAMY, Lien removal for loan account SCCLMF20261000102 could not be completed due to a processing issue. Your Mutual Fund units remain lien-marked. We are reviewing it and will update you - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ("Sanction Letter",
  "After the Sanction Letter is generated successfully (customer clicks “Sign Agreement” on the “Agreement and E-Mandate” page and the Sanction Letter is generated)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Loan Against Mutual Fund has been sanctioned. Your Sanction Letter will be shared separately. Please proceed to sign the eAgreement to continue your loan journey - Shriram Credit",
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund has been sanctioned. Your Sanction Letter will be shared separately. Please proceed to sign the eAgreement to continue your loan journey - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Loan Agreement e-Sign",
  "After the customer signs the loan agreement successfully (e-Sign at Digio – Aadhaar / VID + OTP → “Signed Successfully”)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Loan Against Mutual Fund application has been successfully processed - Shriram Credit",
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund application has been successfully processed - Shriram Credit",
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
 ("Loan Account Opening / Loan Lodgement Rejection (with payment link)",
  "When the OPS team rejects the Loan Account Opening or the Loan Lodgement in the backend LMS with the option “Rejected with Charges” – the customer has to pay the charges (processing fee, lien marking and lien removal), so the communication carries the payment link. One common communication for either rejection.",
  "LMS", "SMS", "SCCL",
  "Dear {#alp#}, Your LAMF application has been rejected. To unpledge your MF units, please pay the charges of Rs. {#alp#} here: {#urg#} - Shriram Credit",   # owner's SMS (DISC-336)
  "Dear AZHAGARSAMY, Your LAMF application has been rejected. To unpledge your MF units, please pay the charges of Rs. 5000 here: https://lamf.shriramcredit.in/user/loans/ - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created (Created)"),
 ("Loan Account Opening / Loan Lodgement Rejection (without payment link)",
  "When the OPS team rejects the Loan Account Opening or the Loan Lodgement in the backend LMS with the option “Rejected without Charges” – the charges are waived for the customer (e.g. an internal employee who completed a testing scenario), so the communication has no payment link. One common communication for either rejection.",
  "LMS", "SMS", "SCCL",
  "Dear {#alp#}, Your Loan Against Mutual Fund application has been rejected.  We will initiate to unpledge your MF units shortly - Shriram Credit",   # owner's SMS (DISC-336)
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund application has been rejected.  We will initiate to unpledge your MF units shortly - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created (Created)"),
 ("Withdrawal",
  "When the customer initiates a withdrawal from the loan account, an OTP is sent to confirm the withdrawal",
  "LOS", "SMS", "SCCL",
  "{#numeric#} is your OTP to confirm the withdrawal of Rs. {#alphanumeric#} from your Loan Against Mutual Fund. Do not share this OTP with anyone - Shriram Credit",
  "<u>123456</u> is your OTP to confirm the withdrawal of Rs. 10,000 from your Loan Against Mutual Fund. Do not share this OTP with anyone - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("Withdrawal",
  "On the completion of each withdrawal by the customer (withdrawal request confirmed)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your withdrawal request is confirmed. Your loan amount will be disbursed to your bank account shortly - Shriram Credit",
  "Dear AZHAGARSAMY, Your withdrawal request is confirmed. Your loan amount will be disbursed to your bank account shortly - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ('Withdrawal Rejected',
  'The withdrawal status changes to Rejected after the Operations or Treasury team rejects it',
  "LMS", "SMS", "SCCL",
  'Dear {#alp#}, Your withdrawal request of Rs. {#alp#} has been rejected. For assistance, contact our support team - Shriram Credit',   # owner's SMS (DISC-333)
  'Dear AZHAGARSAMY, Your withdrawal request of Rs. 5000 has been rejected. For assistance, contact our support team - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created (Created)"),
 ("Loan Disbursed (First Disbursement)",
  "When the loan is disbursed for the first time (first disbursement) – notifying the customer that the amount is credited to the bank account. Each subsequent withdrawal is the row below (same SMS, different mail)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Congratulations! Your loan has been credited to your bank account. Thank you for choosing Shriram Credit - Shriram Credit",
  "Dear AZHAGARSAMY, Congratulations! Your loan has been credited to your bank account. Thank you for choosing Shriram Credit - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("EMI Presentation Reminder (T-4)",
  "This communication has to be triggered on the 1st of every month when the EMI is due on the 5th – first reminder of the upcoming instalment (SMS and mail). The second reminder, T-1, is mail only (next row)",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} is due on {#alphanumeric#}. Please ensure sufficient balance in your bank account for timely payment - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 is due on 05-11-2026. Please ensure sufficient balance in your bank account for timely payment - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("EMI Success",
  "Notifying the customer when the instalment is debited successfully",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was successfully debited on {#alphanumeric#}. Thank you for your timely payment - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was successfully debited on 05-11-2026. Thank you for your timely payment - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("EMI Failed",
  "When the EMI presentation fails on the 5th of the month, this communication has to be sent to the customer – SMS and mail",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was rejected by your bank on {#alphanumeric#}. We will retry on {#alphanumeric#}. Please ensure sufficient balance - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was rejected by your bank on 05-11-2026. We will retry on 10-11-2026. Please ensure sufficient balance - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("EMI Resubmission Reminder",
  "Notifying the customer before the bounced EMI is re-presented (resubmitted) to the bank – this communication has to be triggered 1 day before the re-presentation date (T-1), i.e. on the 9th when the EMI is re-presented on the 10th – SMS and mail",
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
  "-", "SGRCDT-T", "Yes"), ("LAMF Part Payment Confirmation",
  "When the customer makes a part payment towards the loan and it is processed successfully",
  "LOS", "SMS", "SCCL",
  "Dear {#alp#}, Part payment of Rs. {#alp#} towards your LAMF has been successfully processed. Revised outstanding: Rs. {#alp#}. - Shriram Credit",
  "Dear AZHAGARSAMY, Part payment of Rs. 5,000 towards your LAMF has been successfully processed. Revised outstanding: Rs. 5,000. - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("LTV Breach Trigger (Margin Call)",
  "When the loan-to-value (LTV) is breached because the value of the pledged portfolio has dropped – the customer is asked to pay or pledge more",
  "LOS", "SMS", "SCCL",
  "Dear {#alp#}, Your loan value has dropped. Please pay or pledge immediately to avoid liquidation of your portfolio. {#urg#} - Shriram Credit",
  "Dear AZHAGARSAMY, Your loan value has dropped. Please pay or pledge immediately to avoid liquidation of your portfolio. https://lamf.shriramcredit.in/user/loans/ - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("LAMF LTV Breach Liquidation",
  "When the LTV breach is not cured – liquidation of the pledged securities is initiated as per the loan terms to recover the shortfall",
  "LOS", "SMS", "SCCL",
  "Dear {#alp#}, Your LTV has breached. As per the loan terms, liquidation of your pledged securities will be initiated to recover the shortfall - Shriram Credit",
  "Dear AZHAGARSAMY, Your LTV has breached. As per the loan terms, liquidation of your pledged securities will be initiated to recover the shortfall - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("LAMF Principal Repayment Reminder",
  "The day after the loan end date (loan matured) when the outstanding principal is still not paid",
  "LOS", "SMS", "SCCL",
  "Dear {#alp#}, Your LAMF has matured and the outstanding principal remains unpaid. You are requested to make immediate payment to avoid liquidation of MF pledged units {#urg#} - Shriram Credit",
  "Dear AZHAGARSAMY, Your LAMF has matured and the outstanding principal remains unpaid. You are requested to make immediate payment to avoid liquidation of MF pledged units https://lamf.shriramcredit.in/user/loans/ - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("LAMF Liquidation for O/S",
  "On the day the liquidation is initiated for the outstanding principal that is still unpaid after maturity",
  "LOS", "SMS", "SCCL",
  "Dear {#alp#}, As the outstanding principal is still unpaid, we are initiating liquidation for recovery of outstanding dues - Shriram Credit",
  "Dear AZHAGARSAMY, As the outstanding principal is still unpaid, we are initiating liquidation for recovery of outstanding dues - Shriram Credit",
  "-", "SGRCDT-T", "Yes"),
 ("Foreclosure Completed",
  "When the customer forecloses (pre-closes) the loan before the end of the tenure and the foreclosure is completed.",
  "LMS", "SMS", "SCCL",
  # owner's created SMS template (DISC-331); status kept, “(Created)” added
  "Dear {#alp#}, Your Rs.{#alp#} payment towards LAMF foreclosure has been received successfully. Loan closure will be processed shortly - Shriram Credit",
  "Dear AZHAGARSAMY, Your Rs.10000 payment towards LAMF foreclosure has been received successfully. Loan closure will be processed shortly - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created (Created)"),
 ("Successful Loan Tenure Completion",
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
              "Actual Content", "Mail Subject", "SMS Header", "Available", "Status"]
# Status (DISC-201): SMS the owner marked “Not Required” stay in the table; every other SMS is “Required”.
SMS_NOT_REQUIRED = {"LAN Generated", "Pre-Pledge Application Expiry Reminder", "Pre-Pledge Application Discarded", "Customer-Initiated Discard",
                    "Lien Marking Failed", "Post-Pledge Journey Incomplete", "Post-Pledge Application Expiry Reminder", "Lien Removal Request Received"}
assert SMS_NOT_REQUIRED <= {r[0] for r in COMMS}
COMMS = [r + ("Not Required" if r[0] in SMS_NOT_REQUIRED else "Required",) for r in COMMS]
# Customer e-mails (owner's document "Email Notifications for Customer – Quicklend 0109 Revised", DISC-199).
# Same columns as COMMS; Communication Type “Mail”, Mail Subject filled, SMS Header “-”.
# Body text keeps the document wording; “\n” is a line break. Actual Content = the body with sample values.
MAIL_SIGN = "\n\nWarm regards,\nTeam Shriram Credit"
MAIL_DISCLAIMER = ("\n\nDisclaimer:\nThis is an automated reminder. Please do not reply to this message, as the mailbox is not monitored "
                   "and you will not receive a response. Loan against Securities is only for personal use. The loan amount cannot be used for "
                   "speculative activities, capital market-related purposes, or anti-social purposes.")
SUPPORT = "Should you have any questions, require clarification, or assistance, please feel free to reach out to our customer support at lassupport@shriramcredit.in. Our team will be happy to assist you."
THANKS = "Thank you for choosing Shriram Credit as your trusted financial partner. We look forward to supporting you throughout your loan journey."
CLOSED_BODY = ("We have received the final payment and are pleased to confirm that your loan account has been closed in our records. We appreciate your commitment to timely repayment and hope this facility served your financial needs effectively.\n\n"
               "Lien Removal Process:\nAs your loan is now fully repaid, we have initiated the process to release the lien on your pledged Mutual Fund units.\n"
               "• Timeline: The lien will be removed within 2 to 3 working days.\n"
               "• Confirmation: You will receive a separate notification from the Registrar and Transfer Agent (CAMS/KFintech) once your units are fully \"unlocked\" and fully accessible to you.\n\n"
               "Next Steps:\nNo Objection Certificate (NOC): Your formal No Objection Certificate is being generated and will be sent to you in a separate communication shortly.\n\n"
               "Important Information:\n• Please retain this email for your records as confirmation of loan closure until you receive your formal No Objection Certificate.\n"
               "• In case the lien is not removed within the stated timeline, please contact us for assistance.\n\n" + SUPPORT +
               "\n\nWe thank you for choosing Shriram Credit and look forward to serving you again.")
EMI_REMINDER = ("This is a reminder that your next EMI of Rs. 5,085 for your loan will be automatically deducted from your bank account on 10/07/2026. Kindly ensure that your account has sufficient funds to cover the payment.\n\n"
                "Here are the details of your loan:\n• Borrowed amount: ₹ 55,000\n• Outstanding amount: ₹ 55,000\n• Bank account number: XXXXXXXXXXX\n\n"
                "Please note that failure or bounce of the EMI payment may attract penal charges. We encourage you to make sure that your account balance is adequate to avoid any inconvenience.\n\nThank you for your cooperation.")
DISB = lambda first: ("We are happy to inform you that your loan amount of ₹[XXXX] has been credited to your bank account.\n\n"
                "Loan Details:\n• Customer ID: [XXXX]\n• Loan Account ID: [XXXX]\n• Disbursement Type: " + ("<<Single / Multiple>>" if first else "<<Multiple>>") +
                "\n• Disbursement No.: " + ("<<1>>" if first else "") + "\n• Disbursement UTRN: [XXXX]\n• Loan Tenure: [XX months]\n• " +
                ("EMI Amount: ₹[XXXX]" if first else "EMI Amount of this disbursement for 30-day cycle: ₹[XXXX]") +
                "\n• First EMI Due Date: [Date]\n• Balance amount available <<₹>> (If disbursement type is MULTIPLE.)\n\n" +
                ("Repayment Schedule – 12 rows, one per month of the 12-month tenure; a 13th row is shown only when required\nRepayment Date | Repayment Amount\n" +
                 "DD-MMM-YYYY | ₹XXXXXX\n" * 12 + "(13th row only when required) DD-MMM-YYYY | ₹XXXXXX\n\n" if first else
                 "Repayment Schedule (display only the residual term) – cumulative of all disbursements till date"
                 "\nRepayment Date | Repayment Amount\nDD-MMM-YYYY | ₹XXXXXX\nDD-MMM-YYYY | ₹XXXXXX\nDD-MMM-YYYY | ₹XXXXXX\n\n") +
                "Please note that the purpose of the loan, as confirmed by you, is <<Purpose>> and not for any speculative trading in securities, derivatives, commodities, or any unlawful purposes.\n\n" + THANKS)
_M = [
 ("Email Verification", "When the customer clicks Verify for the email on the KYC Verification page", "LOS",
  "XXXXXX – Your Email Verification OTP for Shriram Credit LAMF",
  "Dear Customer,\n\nXXXXXX is the OTP to verify your email and continue with your Shriram Credit’s Loan Against Mutual Fund application.\n\nPlease do not share the OTP with anyone.",
  [("XXXXXX", "123456")]),
 ("Mutual Fund Pledge Successful", "After the mutual fund units are successfully pledged", "LOS",
  "Your mutual fund pledge is successful",
  "Dear [Customer Name],\n\nCongratulations! Your mutual fund has been successfully pledged against your applied loan with Shriram Credit.\n\nYou are one step closer to receiving your funds. We’ll notify you once the loan is disbursed.", []),
 ("Loan Sanction Letter Mail", "After the Sanction Letter is generated. To: customer e-mail ID; CC: loandocuments@shriramcredit.in; Sanction Letter attached", "LOS",
  "SCCL Loan Sanction Letter – << Full Name of the customer >>",
  "Dear [Customer Name],\n\nWe are pleased to inform you that your loan application with Shriram Credit Company Limited (SCCL) has been approved.\n\nFor your reference, we have attached the Loan Sanction Letter, which contains the complete details of your approved loan, including the sanctioned amount, tenure, repayment schedule, interest rate, and applicable terms and conditions.\n\nWe encourage you to review this document thoroughly to ensure you are familiar with the loan structure and repayment obligations.\n\n" + SUPPORT + "\n\n" + THANKS, []),
 ("Loan Agreement Mail", "After the loan agreement is e-signed. To: customer e-mail ID; CC: loandocuments@shriramcredit.in; signed Loan Agreement attached", "LOS",
  "SCCL Loan Agreement – << Full Name of the customer >>",
  "Dear [Customer Name],\n\nWe are pleased to inform you that your loan application with Shriram Credit Company Limited (SCCL) has been approved, and your loan agreement is now ready for your review.\n\nYour Loan ID is XXXXXXXX\n\n📄 Attached to this email, you will find your digitally signed loan agreement. We request that you review the document carefully to ensure that all details, terms, and conditions are accurate and aligned with the Sanction Letter.\n\n✅ If everything is in order, no further action is required. Your loan will be processed strictly in accordance with the terms outlined in the agreement.\n\n" + SUPPORT + "\n\n" + THANKS,
  [("XXXXXXXX", "SCCLMF20261000102")]),
 ("Withdrawal Initiation", "After the loan is approved and the LAMF account is created – the customer can now initiate a withdrawal", "LMS",
  "Withdrawal Initiation: Successful LAMF Account Creation – << Full Name of the customer >>",
  "Dear [Customer Name],\n\nWe are pleased to inform you that your loan application with Shriram Credit Company Limited (SCCL) has been successfully approved, and your Loan ID is XXXXXXXX.\n\nYou can now initiate the withdrawal request for the approved amount at https://lamf.shriramcredit.in/.\n\n" + SUPPORT + "\n\n" + THANKS,
  [("XXXXXXXX", "SCCLMF20261000102")]),
 ("Loan Disbursal Confirmation (First Disbursement)", "When the first disbursement is credited to the customer’s bank account", "LMS",
  "Loan disbursed to your account", "Dear [Customer Name],\n\n" + DISB(True),
  [("₹[XXXX] has", "₹10,000 has"), ("Customer ID: [XXXX]", "Customer ID: SCCL1000102"), ("Loan Account ID: [XXXX]", "Loan Account ID: SCCLMF20261000102"), ("<<Single / Multiple>>", "Multiple"), ("<<1>>", "1"), ("UTRN: [XXXX]", "UTRN: UTIBR52026102700001"), ("[XX months]", "12 months"), ("EMI Amount: ₹[XXXX]", "EMI Amount: ₹88"), ("[Date]", "05-11-2026"), ("<<₹>>", "₹1,55,26,100"), ("<<Purpose>>", "Home Renovation")]),
 ("Loan Disbursal Confirmation (Subsequent Disbursement)", "When each later disbursement (disbursement type Multiple) is credited", "LMS",
  "Loan disbursed to your account", "Dear [Customer Name],\n\n" + DISB(False),
  [("₹[XXXX] has", "₹20,000 has"), ("Customer ID: [XXXX]", "Customer ID: SCCL1000102"), ("Loan Account ID: [XXXX]", "Loan Account ID: SCCLMF20261000102"), ("<<Multiple>>", "Multiple"), ("Disbursement No.: \n", "Disbursement No.: 2\n"), ("UTRN: [XXXX]", "UTRN: UTIBR52026110200002"), ("[XX months]", "12 months"), ("cycle: ₹[XXXX]", "cycle: ₹175"), ("[Date]", "05-12-2026"), ("<<₹>>", "₹1,55,06,100"), ("<<Purpose>>", "Home Renovation")]),
 ("Upcoming EMI Due Reminder", "Sent 5 days before the original presentation of the EMI (routine T-5)", "LMS",
  "Reminder: Your EMI of ₹[XXXX] is due on [Date]", "Dear [Customer Name],\n\n" + EMI_REMINDER, []),
 ("EMI Presentation Mail", "Sent one day before the EMI presentation date (routine T-1)", "LMS",
  "EMI Presentation Alert – <<Date of EMI>>", "Dear [Customer Name],\n\n" + EMI_REMINDER, []),
 ("Successful EMI Deduction Mail", "Routine EMI clearance – the EMI is debited successfully", "LMS",
  "Your EMI of ₹[XXXX] Has Been Successfully Deducted",
  "Dear [Customer Name],\n\nWe are writing to confirm that your EMI of ₹[XXXX] for the loan account [Loan ID] was successfully debited on [Date] from your registered bank account.\n\n📄 EMI Details:\n• Loan Account Number: [Loan ID]\n• EMI Amount: ₹[XXXX]\n• Deduction Date: [Date]\n• Next EMI Due Date: [Next Date]\n\nThank you for ensuring timely payment. Regular EMI payments help maintain a strong credit history and a smooth loan journey.\n\n" + SUPPORT,
  [("₹[XXXX]", "₹10,000"), ("[Loan ID]", "SCCLMF20261000102"), ("[Next Date]", "05-12-2026"), ("[Date]", "05-11-2026")]),
 ("Instalment Failure / EMI Bounce Notification (Bounce – 1A)", "When the EMI bounces (insufficient balance); re-presented on T+5 days", "LMS",
  "Alert: Your EMI payment failed",
  "Dear [Customer Name],\n\nWe could not process your EMI of ₹[XXXX] for the loan account [Loan ID] on [Date] due to insufficient balance.\n\nWe will re-present the EMI on <<T+5 days>>. Please ensure your account has a sufficient balance to avoid penalties.\n\nIn case the amount is not received on the re-presentation date, we shall initiate loan closure procedures.\n\n" + SUPPORT,
  [("₹[XXXX]", "₹10,000"), ("[Loan ID]", "SCCLMF20261000102"), ("[Date]", "05-11-2026"), ("<<T+5 days>>", "10-11-2026")]),
 ("Second EMI Representation Reminder (1B T-1)", "Sent one day before the EMI is re-presented", "LMS",
  "Final Reminder: EMI Re-presentation on [Date]",
  "Dear [Customer Name],\n\nThis is to inform you that your EMI of ₹[XXXX] will be re-presented on [Date].\n\nPlease ensure your account has a sufficient balance to avoid penalties and negative impact on your credit score.\n\nIn case the amount is not received on the re-presentation date, we shall initiate loan closure procedures.",
  [("₹[XXXX]", "₹10,000"), ("[Date]", "10-11-2026")]),
 ("Initiation of Loan Closure Procedures (2B Bounce)", "When the re-presented EMI bounces again – pledge liquidation is initiated", "LMS",
  "Urgent: Mutual Fund Liquidation Scheduled",
  "Dear [Customer Name],\n\nSince you defaulted on your repayment, we are initiating the pledge liquidation process to recover the total outstanding amount.\n\n" + SUPPORT, []),
 ("Part Payment", "When a part payment is processed successfully; the revised repayment schedule is attached", "LMS",
  "Payment Acknowledgment: Your Shriram Credit Loan Against Mutual Funds Part Payment Has Been Processed",
  "Dear [Customer Name],\n\nWe confirm that part payment towards your Loan Against Mutual Fund (LAMF) from Shriram Credit has been successfully processed.\n\nPayment Summary:\n• Transaction Status: Successful\n• Amount Received: [₹XXXX Mention Amount]\n• Revised Outstanding Balance: [₹XXXX Mention Amount]\n\nUpdated Repayment Schedule:\nAs a result of this payment, your Repayment Schedule has been revised. Please find the updated schedule attached to this email for your reference.\n\n" + SUPPORT + "\n\n" + THANKS,
  [("Amount Received: [₹XXXX Mention Amount]", "Amount Received: ₹5,000"), ("Balance: [₹XXXX Mention Amount]", "Balance: ₹5,000")]),
 ("Pre Closure", "When the customer pre-closes the loan (final payment received before the end of the tenure)", "LMS",
  "Loan Pre-Closure Confirmation: Your Shriram Credit Loan Against Mutual Funds Has Been Closed Successfully",
  "Dear [Customer Name],\n\nCongratulations on successfully pre-closing your Loan Against Mutual Fund (LAMF) with Shriram Credit.\n\n" + CLOSED_BODY, []),
 ("Margin Call / Mutual Fund Value Drop Mail", "When the market value of the pledged units drops and the LTV is above the limit", "LMS",
  "Action Required: Mutual Fund Margin Shortfall",
  "Dear [Customer Name],\n\nThe current market value of your Mutual Fund units pledged with us has declined and current LTV is at (YY.YY)%\n\nWe request you to make an immediate payment of ₹ (XXXX) (minimum amount) to reduce your total loan outstanding, or increase your collateral pledge (For Equity MF of (XXXX/0.65) or For Debt MF of (XXXX/0.75)) to bring your account within the prescribed limit.\n\nPlease visit our website and follow the easy steps to make the payment or increase your collateral pledge.\n\nFailure to maintain the required margin may result in loan adjustment actions as per the terms of Loan Agreement.\n\nShould you have any questions, require clarification, or need assistance, please feel free to reach out to our customer support team at lassupport@shriramcredit.in. Our team will be happy to assist you.\n\nThank you for your prompt attention to this matter.",
  [("(YY.YY)%", "82.50%"), ("₹ (XXXX) (minimum amount)", "₹ 10,000 (minimum amount)"), ("Equity MF of (XXXX/0.65)", "Equity MF of ₹15,385"), ("Debt MF of (XXXX/0.75)", "Debt MF of ₹13,333")]),
 ("Loan Tenure Completion (Closure Mail)", "EMI loan: when the last EMI is paid; balloon loan: when the principal outstanding is paid", "LMS",
  "Congratulations on completing your loan journey",
  "Dear [Customer Name],\n\nCongratulations on successfully closing your Loan Against Mutual Fund (LAMF) with Shriram Credit.\n\n" + CLOSED_BODY, []),
 ("NOC / Loan Closure Certificate", "Manual trigger after the loan is closed; the NOC is attached", "LMS",
  "Your Loan Account [Loan ID] is closed successfully",
  "Dear [Customer Name],\n\nWe are pleased to inform you that your loan account [Loan ID] has been closed successfully.\n\nThe No Objection Certificate (NOC) is attached for your records.\n\nYour Customer ID is active with us, and you may visit us for any future requirements.\n\nWe thank you for choosing Shriram Credit and look forward to serving you again.",
  [("[Loan ID]", "SCCLMF20261000102")]),
 ("LTV Breach beyond Policy Norms", "When the LTV keeps breaching after the margin call and reaches the liquidation threshold", "LMS",
  "Immediate Action: Liquidation of Pledged Mutual Fund Units due to LTV Breach",
  "Dear [Customer Name],\n\nDespite our previous communications, the Loan-to-Value (LTV) ratio of your Loan Against Mutual Funds has continued to breach the permissible limit and has now reached the liquidation threshold.\n\nAccordingly, Shriram Credit has initiated the liquidation of your pledged Mutual Fund units to recover the margin shortfall, in accordance with the terms and conditions of your Loan Agreement.\n\nAny surplus amount, after adjustment of all outstanding dues and applicable charges, shall be dealt with in accordance with the Loan Agreement.\n\nShould you require any clarification or assistance, please feel free to reach out to our customer support at lassupport@shriramcredit.in. Our team will be happy to assist you.\n\nThank you for your understanding.", []),
 ("Principal Repayment for Loan Closure", "When the loan reaches maturity and the outstanding principal is unpaid – 5 working days grace period", "LMS",
  "Action Required: Principal Repayment",
  "Dear [Customer Name],\n\nYour Loan Against Mutual Funds has reached its maturity date and the outstanding principal amount remains unpaid.\n\nAs a goodwill measure, Shriram Credit is providing a grace period of five (5) working days from the maturity date to enable you to repay the outstanding principal.\n\nPlease note that:\n• Interest at the applicable contractual rate shall continue to accrue during the grace period.\n• The outstanding amount must be repaid within the stipulated grace period.\n\nPlease use the below link to check the details and make payment.\n{LINK}\n\nFailure to repay the outstanding amount within the grace period shall result in liquidation of your pledged Mutual Fund units to recover the outstanding dues in accordance with the terms of your Loan Agreement.\n\nShould you require any clarification or assistance, please contact us at lassupport@shriramcredit.in.\n\nThank you for your prompt attention.",
  [("{LINK}", "https://lamf.shriramcredit.in/user/loans/")]),
 ("Liquidation for Outstanding Loan (after grace period)", "When the grace period for the matured loan has expired and the principal is still unpaid – liquidation is initiated. (Scenario name in the document was a pasted link – to be confirmed)", "LMS",
  "Immediate Action: Liquidation of Pledged Mutual Fund Units for Recovery of Outstanding Loan",
  "Dear [Customer Name],\n\nThe grace period provided for repayment of your matured Loan Against Mutual Funds has expired, and the outstanding principal amount remains unpaid.\n\nAccordingly, Shriram Credit has initiated the liquidation of your pledged Mutual Fund units to recover the outstanding loan amount, together with applicable interest, charges and other dues, in accordance with the terms of the Loan Agreement.\n\nAny balance amount remaining after adjustment of all outstanding dues shall be dealt with in accordance with the Loan Agreement.\n\nShould you require any clarification or assistance, please feel free to contact our customer support at lassupport@shriramcredit.in.\n\nThank you for your understanding.", []),
]
def _sample(text, subs):
    for a, b in subs:
        text = text.replace(a, b)
    return (text.replace("[Customer Name]", "AZHAGARSAMY").replace("<< Full Name of the customer >>", "AZHAGARSAMY SUBBURAJ")
                .replace("<<Date of EMI>>", "05-11-2026").replace("₹[XXXX]", "₹10,000").replace("[Date]", "05-11-2026"))
MAILS = [(stage, scen, app, "Mail", "SCCL", body + MAIL_SIGN + MAIL_DISCLAIMER, _sample(body + MAIL_SIGN + MAIL_DISCLAIMER, subs),
          subj, "-", "Provided") for stage, scen, app, subj, body, subs in _M]
MAIL_COLS = ["S.No", "Stage", "Scenarios", "Application", "Communication Type", "Sender", "Body (template)",
             "Body (sample)", "Mail Subject", "SMS Header", "Available"]

# SMS table layout (DISC-204): SMS columns first, then the mail columns. A row can be SMS only, mail only
# (Communication Type “Mail”, SMS columns “-”) or both. Mail values stay blank until the owner gives them.
COMMS_COLS = ["S.No", "Stage", "Scenarios", "Application", "Communication Type", "Sender",
              "SMS Content Structure", "Actual SMS Content", "SMS Header", "SMS Available", "SMS Status",
              "Mail Subject Structure", "Actual Mail Subject", "Mail Content Structure", "Actual Mail Content", "Mail Available", "Mail Status"]
SMS_MAIL = {}   # {"SMS stage": "Mail stage"} – cleared on the owner's request (DISC-203); filled again from the owner's list
_MAIL_BY_STAGE = {m[0]: m for m in MAILS}
assert set(SMS_MAIL) <= {r[0] for r in COMMS} and set(SMS_MAIL.values()) <= set(_MAIL_BY_STAGE)
def _sms_row(r):
    stage, scen, app, typ, sender, content, actual, _subject, header, available, status = r
    m = _MAIL_BY_STAGE.get(SMS_MAIL.get(stage))
    mail = (m[7], "", m[5], m[6], m[9], "Required") if m else ("", "", "", "", "", "")
    return (stage, scen, app, typ, sender, content, actual, header, available, status) + mail
COMMS = [_sms_row(r) for r in COMMS]

# Email verification OTP mail (owner's HTML template 01_Email_Verification.html, DISC-204) – mail only, no SMS
EMAIL_VERIFICATION_MAIL = (
 "Email Verification",
 "On the KYC Verification page (LOS step 9, after the Application Summary): the customer enters the email address and clicks Verify, and the OTP is sent to that email",
 "LOS", "Mail", "SCCL", "-", "-", "-", "-", "-",
 "XXXXXX – Your Email Verification OTP for Shriram Credit LAMF",
 "123456 – Your Email Verification OTP for Shriram Credit LAMF",
 "E-Mail Verification\n\nDear {{CUSTOMER_NAME}},\n\nOne-Time Password\n{{OTP}}\n\nPlease do not share the OTP with anyone.\n\n"
 "Use the OTP above to verify your email and continue with your Shriram Credit’s Loan Against Mutual Fund application.\n\n"
 "Warm regards,\nTeam Shriram Credit\n\nDisclaimer: This is an automated reminder. Please do not reply to this message, as the mailbox is not monitored "
 "and you will not receive a response. Loan against Securities is only for personal use. The loan amount cannot be used for speculative activities, "
 "capital market-related purposes, or anti-social purposes.\n\n© 2026 Shriram Credit Company Limited. All rights reserved.",
 "", "Yes [[view:mails/01_Email_Verification.html]]", "Required")
EMAIL_VERIFICATION_MAIL = EMAIL_VERIFICATION_MAIL[:13] + (EMAIL_VERIFICATION_MAIL[12].replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY").replace("{{OTP}}", "123456"),) + EMAIL_VERIFICATION_MAIL[14:]
_i = [r[0] for r in COMMS].index("LAN Generated") + 1     # email verification comes right after the Application Summary
COMMS = COMMS[:_i] + [EMAIL_VERIFICATION_MAIL] + COMMS[_i:]

# HTML mail templates sent together with an SMS (DISC-208). The mail text is read from the template itself,
# so the table and the “View” page always match. {stage: (file, subject structure, sample subject, header lines, samples)}
from html.parser import HTMLParser
class _MailText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts, self.cur, self.depth_p, self.hidden = [], "", 0, 0
    def handle_starttag(self, tag, attrs):
        if tag == "span" and "display:none" in (dict(attrs).get("style") or ""): self.hidden += 1
        if tag == "p": self.depth_p += 1; self.cur = ""
        if tag == "a" and not self.depth_p: self.btn = ""          # CTA button (link outside a paragraph)
        if tag == "tr": self.row = []                                # table rows (e.g. Loan Details) → “Label: Value”
        if tag == "td": self.td = ""
        if tag == "br" and self.depth_p: self.cur += "\n"
    def handle_endtag(self, tag):
        if tag == "span" and self.hidden: self.hidden -= 1
        if tag == "td" and getattr(self, "td", None) is not None:
            if self.td.strip(): self.row.append(" ".join(self.td.split()))
            self.td = None
        if tag == "tr" and getattr(self, "row", None):
            self.parts.append((" " if self.row[:1] == ["•"] else ": ").join(self.row)); self.row = []      # bullet rows: "• text"
        if tag == "a" and getattr(self, "btn", None) is not None:
            self.parts.append(f"[{self.btn.strip()}]"); self.btn = None
        if tag == "p" and self.depth_p:
            self.depth_p -= 1; self.parts.append(" ".join(self.cur.split(" ")).strip())
    def handle_data(self, d):
        if self.depth_p and not self.hidden: self.cur += d.replace("\xa0", " ")
        elif getattr(self, "btn", None) is not None: self.btn += d
        elif getattr(self, "td", None) is not None and not self.hidden: self.td += d.replace("\xa0", " ")
def mail_text(fname):
    t = _MailText(); t.feed(open(os.path.join(ROOT, "mails", fname), encoding="utf-8").read())
    return "\n\n".join(re.sub(r"[ \t]+", " ", x).replace(" \n", "\n").strip() for x in t.parts if x.strip())
MAIL_TEMPLATES = {
 "Pledging of Mutual Fund": ("02_Mutual_Fund_Pledge_Successful.html",
    "Your mutual fund pledge is successful", "Your mutual fund pledge is successful", "", {}),
 "Sanction Letter": ("03_Loan_Sanction_Letter.html",
    "SCCL Loan Sanction Letter – << Full Name of the customer >>", "SCCL Loan Sanction Letter – AZHAGARSAMY SUBBURAJ",
    "To: Customer Email ID\nCC: loandocuments@shriramcredit.in\nAttachment: Loan Sanction Letter PDF\n\n", {}),
 "Loan Agreement e-Sign": ("04_Loan_Agreement.html",
    "SCCL Loan Agreement – << Full Name of the customer >>", "SCCL Loan Agreement – AZHAGARSAMY SUBBURAJ",
    "To: Customer Email ID\nCC: loandocuments@shriramcredit.in\nAttachment: Digitally signed Loan Agreement PDF\n\n", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 # owner's HTML (DISC-321); Mail Available keeps “No – to be created” with the View link (see MAIL_STATUS_KEEP)
 "Loan Account Opening / Loan Lodgement Rejection (with payment link)": ("28_Application_Rejected_Pay_Charges.html",   # owner's HTML (DISC-322)
    "Action Required: Application Rejected – Pay Charges {{LOAN_ID}}", "Action Required: Application Rejected – Pay Charges SCCLMF20261000102", "",
    {"{{LOAN_ID}}": "SCCLMF20261000102", "{{PROCESSING_FEE}}": "1,499"}),
 "Loan Account Opening / Loan Lodgement Rejection (without payment link)": ("29_Application_Rejected.html",   # owner's HTML (DISC-323)
    "Update: Your Shriram Credit LAMF Application Is Rejected {{LOAN_ID}}", "Update: Your Shriram Credit LAMF Application Is Rejected SCCLMF20261000102", "",
    {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "Withdrawal Rejected": ("30_Withdrawal_Request_Rejected.html",   # owner's HTML (DISC-324)
    "Update: Your Withdrawal Request Was Rejected {{LOAN_ID}}", "Update: Your Withdrawal Request Was Rejected SCCLMF20261000102", "",
    {"{{LOAN_ID}}": "SCCLMF20261000102", "{{WITHDRAWAL_AMOUNT}}": "10,000"}),
 "Lien Removal Successful": ("27_Lien_Removal_Successful.html",
    "Lien Removed: Your Mutual Fund Units Are Unpledged", "Lien Removed: Your Mutual Fund Units Are Unpledged", "", {}),
 # two rows share the stage “Withdrawal”, so this one is keyed by its scenario (DISC-209)
 "When the customer initiates a withdrawal from the loan account, an OTP is sent to confirm the withdrawal": ("06_Withdrawal_Verification.html",
    "{{OTP}} – Your Withdrawal Verification OTP for Shriram Credit LAMF", "123456 – Your Withdrawal Verification OTP for Shriram Credit LAMF",
    "", {"{{OTP}}": "123456", "{{WITHDRAWAL_AMOUNT}}": "10,000"}),
 "Loan Lodgement Approval": ("05_Withdrawal_Initiation.html",
    "Withdrawal Initiation: Successful LAMF Account Creation – {{CUSTOMER_FULL_NAME}}",
    "Withdrawal Initiation: Successful LAMF Account Creation – AZHAGARSAMY SUBBURAJ",
    "", {"{{LOAN_ID}}": "SCCLMF20261000102", "{{Link}}": "https://lamf.shriramcredit.in/"}),
 "EMI Presentation Reminder (T-4)": ("09_Upcoming_EMI_Due_Reminder_T-5.html",
    "Reminder: Your EMI of ₹{{EMI_AMOUNT}} is due on {{DUE_DATE}}", "Reminder: Your EMI of ₹10,000 is due on 05-11-2026",
    "",
    {"{{EMI_AMOUNT}}": "10,000", "{{DUE_DATE}}": "05-11-2026", "{{BORROWED_AMOUNT}}": "1,00,000", "{{OUTSTANDING_AMOUNT}}": "1,00,000",
     "{{BANK_ACCOUNT_NUMBER}}": "XXXXXXXX8736", "{{LOAN_ID}}": "SCCLMF20261000102"}),
 "LAMF Part Payment Confirmation": ("20_Part_Payment.html",
    "Payment Acknowledgment: Your Shriram Credit LAMF Part Payment Has Been Processed",
    "Payment Acknowledgment: Your Shriram Credit LAMF Part Payment Has Been Processed",
    "Attachment: Updated Repayment Schedule PDF\n\n", {"{{AMOUNT_RECEIVED}}": "5,000", "{{REVISED_OUTSTANDING_BALANCE}}": "5,000"}),
 "Foreclosure Completed": ("21_Pre_Closure.html",
    "Loan Pre-Closure Confirmation: Your Shriram Credit LAMF Has Been Closed Successfully",
    "Loan Pre-Closure Confirmation: Your Shriram Credit LAMF Has Been Closed Successfully", "", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "Successful Loan Tenure Completion": ("23_Loan_Tenure_Completion.html",
    "Congratulations on completing your loan journey", "Congratulations on completing your loan journey",
    "Trigger: last EMI paid (EMI type) or principal outstanding paid (Balloon type)\n\n", {}),
 "LTV Breach Trigger (Margin Call)": ("22_Margin_Call_Mutual_Fund_Value_Drop_Mail.html",
    "Action Required: Mutual Fund Margin Shortfall <<Loan ID>>", "Action Required: Mutual Fund Margin Shortfall SCCLMF20261000102",
    "Trigger: LTV breach – notifying the customer of a margin shortfall\n\n",
    {"₹({{SHORTFALL_AMOUNT}}/0.65)": "₹15,385", "₹({{SHORTFALL_AMOUNT}}/0.75)": "₹13,333", "{{CURRENT_LTV}}": "82.50", "{{MINIMUM_AMOUNT}}": "10,000", "{{LOAN_ID}}": "SCCLMF20261000102"}),
 "LAMF LTV Breach Liquidation": ("24_LTV_Breach_Beyond_Policy_Norms.html",
    "Immediate Action: Liquidation of Pledged Mutual Fund Units due to LTV Breach {{LOAN_ID}}",
    "Immediate Action: Liquidation of Pledged Mutual Fund Units due to LTV Breach SCCLMF20261000102",
    "", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "Loan Account Closure": ("24_NOC_Loan_Closure_Certificate.html",
    "Your Loan Account {{LOAN_ID}} is closed successfully", "Your Loan Account SCCLMF20261000102 is closed successfully",
    "Trigger: manual trigger\nAttachment: NOC / Loan Closure Certificate PDF\n\n", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "LAMF Liquidation for O/S": ("26_Liquidation_for_Outstanding_Loan.html",
    "Immediate Action: Liquidation of Pledged Mutual Fund Units for Recovery of Outstanding Loan {{LOAN_ID}}",
    "Immediate Action: Liquidation of Pledged Mutual Fund Units for Recovery of Outstanding Loan SCCLMF20261000102",
    "", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "LAMF Principal Repayment Reminder": ("25_Principal_Repayment_for_Loan_Closure.html",
    "Action Required: Principal Repayment {{LOAN_ID}}", "Action Required: Principal Repayment SCCLMF20261000102",
    "", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "EMI Resubmission Reminder": ("12_Second_EMI_Representation_Reminder_1B_T-1.html",
    "Final Reminder: EMI Re-presentation on {{REPRESENTATION_DATE}} <<{{LOAN_ID}}>>",
    "Final Reminder: EMI Re-presentation on 10-11-2026 SCCLMF20261000102",
    "Trigger: 1 day prior to the EMI re-presentation (1B T-1)\n\n",
    {"{{EMI_AMOUNT}}": "10,000", "{{REPRESENTATION_DATE}}": "10-11-2026", "{{LOAN_ID}}": "SCCLMF20261000102"}),
 "EMI Resubmission Failed": ("18_Initiation_of_Loan_Closure_Procedures_2B_Bounce.html",
    "Urgent: Mutual Fund Liquidation Scheduled {{LOAN_ID}}", "Urgent: Mutual Fund Liquidation Scheduled SCCLMF20261000102",
    "", {"{{LOAN_ID}}": "SCCLMF20261000102"}),
 "EMI Success": ("11_Successful_EMI_Deduction.html",
    "Your EMI of ₹{{EMI_AMOUNT}} Has Been Successfully Deducted", "Your EMI of ₹10,000 Has Been Successfully Deducted",
    "", {"{{EMI_AMOUNT}}": "10,000", "{{LOAN_ID}}": "SCCLMF20261000102", "{{DEDUCTION_DATE}}": "05-11-2026", "{{NEXT_EMI_DATE}}": "05-12-2026"}),
 "EMI Failed": ("11_Instalment_Failure_EMI_Bounce_Notification_1A.html",
    "Alert: Your EMI payment failed {{LOAN_ID}}", "Alert: Your EMI payment failed SCCLMF20261000102",
    "Trigger: EMI presented on the 5th of the month bounces (Bounce - 1A); re-presented on the 10th\n\n",
    {"{{EMI_AMOUNT}}": "10,000", "{{LOAN_ID}}": "SCCLMF20261000102", "{{BOUNCE_DATE}}": "05-11-2026", "{{REPRESENTATION_DATE}}": "10-11-2026"}),
}
# Mails given as text / screenshots (no HTML template yet): {stage: (subject structure, sample subject, body, {placeholder: sample})} (DISC-214)
_SCHEDULE = "REPAYMENT SCHEDULE (12 rows – one per month of the 12-month tenure; a 13th row is shown only when required)\nRepayment Date | Repayment Amount\n"
TEXT_MAILS = {
 "Loan Disbursed (First Disbursement)": ("Loan disbursed to your account", "Loan disbursed to your account",
    "Loan Disbursed\n\nDear {{CUSTOMER_NAME}},\n\nWe are happy to inform you that your loan amount of ₹{{DISBURSED_AMOUNT}} has been credited to your bank account.\n\n"
    "LOAN DETAILS\nCustomer ID: {{CUSTOMER_ID}}\nLoan Account ID: {{LOAN_ACCOUNT_ID}}\nDisbursement Type: {{DISBURSEMENT_TYPE}}\nDisbursement No.: {{DISBURSEMENT_NO}}\n"
    "Disbursement UTRN: {{UTRN}}\nLoan Tenure: {{LOAN_TENURE}} months\nEMI Amount: ₹{{EMI_AMOUNT}}\nFirst EMI Due Date: {{FIRST_EMI_DATE}}\nBalance Amount Available: ₹{{BALANCE_AMOUNT}}\n\n"
    + _SCHEDULE + "DD-MMM-YYYY | ₹XXXXXXX\n" * 12 + "(13th row only when required) DD-MMM-YYYY | ₹XXXXXXX\n\n"
    "Please note that the purpose of the loan, as confirmed by you, is {{PURPOSE}} and not for any speculative trading in securities, derivatives, commodities, or any unlawful purposes.\n\n"
    + THANKS + MAIL_SIGN + MAIL_DISCLAIMER,
    {"{{DISBURSED_AMOUNT}}": "10,000", "{{CUSTOMER_ID}}": "SCCL1000102", "{{LOAN_ACCOUNT_ID}}": "SCCLMF20261000102", "{{DISBURSEMENT_TYPE}}": "Multiple",
     "{{DISBURSEMENT_NO}}": "1", "{{UTRN}}": "UTIBR52026102700001", "{{LOAN_TENURE}}": "12", "{{EMI_AMOUNT}}": "88", "{{FIRST_EMI_DATE}}": "05-Dec-2026",
     "{{BALANCE_AMOUNT}}": "1,55,26,100", "{{PURPOSE}}": "Home Renovation"}),
}
# HTML built by Claude from the text mail so that “View” works (DISC-253)
TEXT_MAIL_VIEW = {"Loan Disbursed (First Disbursement)": "07_Loan_Disbursal_Confirmation_First.html"}
def _sample_schedule(text):      # sample: 12 monthly rows from 05-Dec-2026 (interest only, principal with the last instalment)
    rows = [f"05-{m}-{y} | ₹{'10,088' if k == 11 else '88'}" for k, (m, y) in enumerate(
        [("Dec", 2026)] + [(x, 2027) for x in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]])]
    return text.replace("DD-MMM-YYYY | ₹XXXXXXX\n" * 12, "\n".join(rows) + "\n").replace(
        "(13th row only when required) DD-MMM-YYYY | ₹XXXXXXX\n", "(13th row only when required – not needed in this sample)\n")

# Mails not available yet – drafted by Claude for approval, to be created (DISC-247): {stage: (subject structure, sample subject, body[, {placeholder: sample}])}
_LIEN_DETAILS = ("LIEN REMOVAL DETAILS\nStatus: Lien removal initiated\nTimeline: 2–3 working days\n"
                 "Confirmation: You will receive a notification from CAMS/KFintech once your units are fully unlocked.\n\n")
DRAFT_MAILS = {
 "Application Expired – Lien Marked": ("Your LAMF application {{LOAN_ID}} has expired", "Your LAMF application SCCLMF20261000102 has expired",
    "Application Expired\n\nDear {{CUSTOMER_NAME}},\n\nYour Loan Against Mutual Fund (LAMF) application {{LOAN_ID}} has expired as it was not submitted within 30 days.\n\n"
    "Your Mutual Fund units pledged for this application remain lien-marked. We will initiate the lien removal and keep you informed of the next steps.\n\n"
    "You are welcome to start a new application at any time.\n\n" + SUPPORT + MAIL_SIGN + MAIL_DISCLAIMER),
 "Lien Removal Initiated": ("Lien removal initiated for your Mutual Fund units – {{LOAN_ID}}", "Lien removal initiated for your Mutual Fund units – SCCLMF20261000102",
    "Lien Removal Initiated\n\nDear {{CUSTOMER_NAME}},\n\nWe have initiated the removal of the lien on the Mutual Fund units pledged against loan account {{LOAN_ID}}.\n\n"
    + _LIEN_DETAILS + "We will update you once the lien removal is completed.\n\n" + SUPPORT + MAIL_SIGN + MAIL_DISCLAIMER),
 "LAMF Application Submit": ("Your LAMF application {{LOAN_ID}} has been submitted successfully",
    "Your LAMF application SCCLMF20261000102 has been submitted successfully",
    "Application Submitted\n\nDear {{CUSTOMER_NAME}},\n\nThank you for completing the E-Mandate. Your Loan Against Mutual Fund (LAMF) application {{LOAN_ID}} "
    "has been submitted successfully.\n\nOur team will now review your application, and you will be notified once your loan account is opened.\n\n"
    + SUPPORT + "\n\n" + THANKS + MAIL_SIGN + MAIL_DISCLAIMER),
 "EMI Resubmission Success": ("Your re-presented EMI of ₹{{EMI_AMOUNT}} has been successfully deducted",
    "Your re-presented EMI of ₹10,000 has been successfully deducted",
    "EMI Payment Confirmed\n\nDear {{CUSTOMER_NAME}},\n\nWe are writing to confirm that your EMI of ₹{{EMI_AMOUNT}} for the loan account {{LOAN_ID}}, "
    "which was re-presented after the earlier failed attempt, was successfully debited on {{DEDUCTION_DATE}} from your registered bank account.\n\n"
    "EMI DETAILS\nLoan Account Number: {{LOAN_ID}}\nEMI Amount: ₹{{EMI_AMOUNT}}\nDeduction Date: {{DEDUCTION_DATE}}\nNext EMI Due Date: {{NEXT_EMI_DATE}}\n\n"
    "Thank you for your payment. Regular EMI payments help maintain a strong credit history and a smooth loan journey.\n\n" + SUPPORT + MAIL_SIGN + MAIL_DISCLAIMER,
    {"{{EMI_AMOUNT}}": "10,000", "{{DEDUCTION_DATE}}": "10-11-2026", "{{NEXT_EMI_DATE}}": "05-12-2026"}),
 "On the completion of each withdrawal by the customer (withdrawal request confirmed)": ("Your withdrawal request for loan account {{LOAN_ID}} is confirmed",
    "Your withdrawal request for loan account SCCLMF20261000102 is confirmed",
    "Withdrawal Request Confirmed\n\nDear {{CUSTOMER_NAME}},\n\nYour withdrawal request of ₹{{WITHDRAWAL_AMOUNT}} for loan account {{LOAN_ID}} has been confirmed. "
    "The amount will be disbursed to your registered bank account shortly.\n\n"
    "WITHDRAWAL DETAILS\nLoan Account ID: {{LOAN_ID}}\nWithdrawal Amount: ₹{{WITHDRAWAL_AMOUNT}}\nRequest Date: {{REQUEST_DATE}}\n"
    "Bank Account Number: {{BANK_ACCOUNT_NUMBER}}\nStatus: Confirmed\n\n"
    "You will receive a separate confirmation once the amount is credited to your bank account.\n\n" + SUPPORT + MAIL_SIGN + MAIL_DISCLAIMER,
    {"{{WITHDRAWAL_AMOUNT}}": "10,000", "{{REQUEST_DATE}}": "02-11-2026", "{{BANK_ACCOUNT_NUMBER}}": "XXXXXXXX8736"}),
 "Lien Removal Failed": ("Lien removal could not be completed – {{LOAN_ID}}", "Lien removal could not be completed – SCCLMF20261000102",
    "Lien Removal Failed\n\nDear {{CUSTOMER_NAME}},\n\nThe removal of the lien on the Mutual Fund units pledged against loan account {{LOAN_ID}} could not be completed "
    "due to a processing issue. Your units remain lien-marked.\n\nOur team is reviewing it and will update you once the lien removal is completed.\n\n"
    + SUPPORT + MAIL_SIGN + MAIL_DISCLAIMER),
}
def _with_mail(r):
    if (r[0] in DRAFT_MAILS or r[1] in DRAFT_MAILS) and not r[10]:      # keyed by stage, or by scenario
        subj, subj_sample, body, *subs = DRAFT_MAILS.get(r[0]) or DRAFT_MAILS[r[1]]
        sample = body.replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY").replace("{{LOAN_ID}}", "SCCLMF20261000102")
        for k, v in (subs[0] if subs else {}).items():
            sample = sample.replace(k, v)
        return r[:3] + ("SMS, Mail",) + r[4:10] + (subj, subj_sample, body, sample, "No – to be created", "Required")
    if r[0] in TEXT_MAILS and not r[10]:
        subj, subj_sample, body, subs = TEXT_MAILS[r[0]]
        sample = _sample_schedule(body).replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY")
        for k, v in subs.items():
            sample = sample.replace(k, v)
        view = f" [[view:mails/{TEXT_MAIL_VIEW[r[0]]}]]" if r[0] in TEXT_MAIL_VIEW else ""
        return r[:3] + ("SMS, Mail",) + r[4:10] + (subj, subj_sample, body, sample, "Yes" + view, "Required")
    t = MAIL_TEMPLATES.get(r[0]) or MAIL_TEMPLATES.get(r[1])      # keyed by stage, or by scenario
    if not t or r[10]:                       # no template, or mail columns already filled
        return r
    fname, subj, subj_sample, head, subs = t
    body = head + mail_text(fname)
    sample = body.replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY").replace("{{CUSTOMER_FULL_NAME}}", "AZHAGARSAMY SUBBURAJ")
    for k, v in subs.items():
        sample = sample.replace(k, v)
    # Communication Type → “SMS, Mail”; SMS columns kept as they are
    return r[:3] + ("SMS, Mail",) + r[4:10] + (subj, subj_sample, body, sample, f"Yes [[view:mails/{fname}]]", "Required")
assert set(MAIL_TEMPLATES) <= {r[0] for r in COMMS} | {r[1] for r in COMMS}
COMMS = [_with_mail(r) for r in COMMS]
# Mail HTML attached but the mail is still to be created in the system: keep the status, add the View link below it (DISC-321)
# rows 8, 14, 15: owner’s HTML received – “(Created)” added (DISC-335)
MAIL_STATUS_KEEP = {"Lien Removal Successful": "No – to be created (Created)",
                    "Loan Account Opening / Loan Lodgement Rejection (with payment link)": "No – to be created (Created)",
                    "Loan Account Opening / Loan Lodgement Rejection (without payment link)": "No – to be created (Created)",
                    "Withdrawal Rejected": "No – to be created"}
COMMS = [r[:14] + (MAIL_STATUS_KEEP[r[0]] + r[14][3:],) + r[15:] if r[0] in MAIL_STATUS_KEEP and r[14].startswith("Yes") else r for r in COMMS]

# Mail-only rows from HTML templates (no SMS): inserted after the given stage (DISC-216)
MAIL_ONLY = [
 ("EMI Presentation Reminder (T-4)", "EMI Presentation Reminder (T-1)",
  "This communication has to be triggered 1 day before the EMI presentation date (T-1), i.e. on the 4th when the EMI is due on the 5th – SMS and mail. SMS template drafted by Claude for approval; to be created and registered",
  "LOS", "10_EMI_Presentation_T-1.html", "EMI Presentation Alert – {{DATE}}", "EMI Presentation Alert – 05-11-2026",
  "Trigger: 1 day before the EMI presentation date (T-1)\n\n",
  {"{{EMI_AMOUNT}}": "10,000", "{{DATE}}": "05-11-2026", "{{BORROWED_AMOUNT}}": "1,00,000", "{{OUTSTANDING_AMOUNT}}": "1,00,000",
   "{{BANK_ACCOUNT_NUMBER}}": "XXXXXXXX8736", "{{LOAN_ID}}": "SCCLMF20261000102"}),
 ("Loan Disbursed (First Disbursement)", "Loan Disbursed (Subsequent Disbursement)",
  "On each subsequent withdrawal / disbursement after the first one – notifying the customer that the amount is credited to the bank account. Same SMS as the first disbursement (row above); only the mail is different",
  "LOS", "08_Loan_Disbursal_Confirmation_Subsequent.html", "Loan disbursed to your account", "Loan disbursed to your account",
  "Trigger: each subsequent disbursement (Disbursement Type: Multiple); the repayment schedule shows the residual term only\n\n",
  {"{{LOAN_AMOUNT}}": "20,000", "{{CUSTOMER_ID}}": "SCCL1000102", "{{LOAN_ACCOUNT_ID}}": "SCCLMF20261000102", "{{DISBURSEMENT_NO}}": "2",
   "{{UTRN}}": "UTIBR52026110200002", "{{LOAN_TENURE}}": "12", "{{EMI_AMOUNT}}": "175", "{{FIRST_EMI_DATE}}": "05-Dec-2026",
   "{{BALANCE_AMOUNT}}": "1,55,06,100", "{{PURPOSE}}": "Home Renovation"}),
]
SAME_SMS_AS_ABOVE = {"Loan Disbursed (Subsequent Disbursement)"}
# SMS not available yet for a mail row – drafted by Claude for approval, to be created and registered (DISC-236)
NEW_SMS = {"EMI Presentation Reminder (T-1)": (
    "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} for loan account {#alphanumeric#} will be presented tomorrow, {#alphanumeric#}. Please maintain sufficient balance to avoid penal charges - Shriram Credit",
    "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 for loan account SCCLMF20261000102 will be presented tomorrow, 05-11-2026. Please maintain sufficient balance to avoid penal charges - Shriram Credit")}
for after, stage, scen, app, fname, subj, subj_sample, head, subs in MAIL_ONLY:
    body = head + mail_text(fname)
    sample = body.replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY").replace("{{CUSTOMER_FULL_NAME}}", "AZHAGARSAMY SUBBURAJ")
    for k, v in subs.items():
        sample = sample.replace(k, v)
    _i = [r[0] for r in COMMS].index(after) + 1
    sms = ("Mail", "SCCL", "-", "-", "-", "-", "-")
    if stage in SAME_SMS_AS_ABOVE:           # same SMS as the row it follows, only the mail differs (DISC-232)
        sms = ("SMS, Mail",) + COMMS[_i - 1][4:10]
    if stage in NEW_SMS:
        sms = ("SMS, Mail", "SCCL") + NEW_SMS[stage] + ("SGRCDT-T", "No – to be created", "Required")
    COMMS.insert(_i, (stage, scen, app) + sms + (subj, subj_sample, body, sample, f"Yes [[view:mails/{fname}]]", "Required"))
# DRAFT LAN rejection (Waiver BRD, DISC-350): same SMS as rows 14 / 15, new mails from tools/new_mails.py (new-mails/06, 07)
from new_mails import NEW_MAILS as _NM, mail_html as _nm_html
def _nm_text(fname):
    t = _MailText(); t.feed(_nm_html(next(m for m in _NM if m[0] == fname)))
    return "\n\n".join(re.sub(r"[ \t]+", " ", x).replace(" \n", "\n").strip() for x in t.parts if x.strip())
DRAFT_REJECTION_COMMS = [   # (copy SMS of row, stage, scenario, mail file, sample values)
 ("Loan Account Opening / Loan Lodgement Rejection (with payment link)", "DRAFT Application Rejection (with payment link)",
  "When OPS rejects a pledged DRAFT LAN in the backend LMS (Approvals tab) and the Payable Charges are not equal to zero (partial waive-off or no waive-off) – the communication carries the payment link and the customer pays the charges using that link. Waiver BRD.",
  "06_Draft_Application_Rejected_Pay_Charges",
  {"{{LOAN_ID}}": "SCCLMF20261100073", "{{CHARGE_NAME}}": "Processing Fee*", "{{CHARGE_AMOUNT}}": "1,768.82", "{{WAIVED_AMOUNT}}": "500",
   "{{PAYABLE_AMOUNT}}": "1,268.82", "{{TOTAL_CHARGES}}": "1,768.82", "{{TOTAL_WAIVED}}": "500", "{{TOTAL_PAYABLE}}": "1,268.82"}),
 ("Loan Account Opening / Loan Lodgement Rejection (without payment link)", "DRAFT Application Rejection (without payment link)",
  "When OPS rejects a pledged DRAFT LAN in the backend LMS (Approvals tab) and the Payable Charges are equal to zero (full waive-off) – the communication has no payment link; the units are de-pledged. Waiver BRD.",
  "07_Draft_Application_Rejected", {"{{LOAN_ID}}": "SCCLMF20261100073"}),
]
for _src, stage, scen, fname, subs in DRAFT_REJECTION_COMMS + [(None, "Charges Payment Received",
  "When the customer pays the charges in the LOS through the payment link after the DRAFT LAN is rejected (payment successful) – the receipt is generated, stored in the LMS Documents tab and attached to the mail. Waiver BRD.",
  "08_Charges_Payment_Received", {"{{LOAN_ID}}": "SCCLMF20261100073", "{{AMOUNT_PAID}}": "1,268.82", "{{TRANSACTION_ID}}": "pay_SCCL7Q2X9K4M1B",
                                  "{{PAYMENT_DATE}}": "23-11-2026 11:42 AM", "{{RECEIPT_NO}}": "RCPT/LAMF/2026/11/000149"})]:   # added at the end so the existing row numbers stay
    base = next(r for r in COMMS if r[0] == _src) if _src else (None, None, None, "SMS, Mail", "SCCL",
        # SMS drafted by Claude for approval – to be created and registered (DISC-351)
        "Dear {#alp#}, We have received your payment of Rs. {#alp#} for your LAMF application charges. The receipt is sent to your registered email. Your MF units lien removal will be initiated soon - Shriram Credit",
        "Dear AZHAGARSAMY, We have received your payment of Rs. 1,268.82 for your LAMF application charges. The receipt is sent to your registered email. Your MF units lien removal will be initiated soon - Shriram Credit",
        "SGRCDT-T", "No – to be created", "Required")
    m = next(x for x in _NM if x[0] == fname)
    body = _nm_text(fname)
    sample = body.replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY")
    for k, v in subs.items():
        sample = sample.replace(k, v)
    subj = m[2]
    COMMS.append((stage, scen, "LOS" if stage == "Charges Payment Received" else "LMS") + base[3:10] + (subj, subj.replace("{{LOAN_ID}}", subs["{{LOAN_ID}}"]), body, sample,
                                                       f"No – to be created [[view:new-mails/{fname}.html]]", "Required"))
assert all(len(r) == len(COMMS_COLS) - 1 for r in COMMS)
# SMS Status “Not Required” → Mail Status “Not Required” too (DISC-242)
assert COMMS_COLS[10] == "SMS Status" and COMMS_COLS[-1] == "Mail Status"
COMMS = [r[:-1] + ("Not Required",) if r[9] == "Not Required" else r for r in COMMS]

# Sender comes before Communication Type in both tables (DISC-205)
def _sender_first(cols, rows):
    i, j = cols.index("Communication Type"), cols.index("Sender")
    cols = cols[:i] + [cols[j], cols[i]] + cols[j + 1:]
    rows = [r[:i - 1] + (r[j - 1], r[i - 1]) + r[j:] for r in rows]
    return cols, rows
COMMS_COLS, COMMS = _sender_first(COMMS_COLS, COMMS)
MAIL_COLS, MAILS = _sender_first(MAIL_COLS, MAILS)

# Remarks – the owner's observations on the live behaviour, last column of the SMS table (DISC-211)
REMARKS = {
 "On the completion of each withdrawal by the customer (withdrawal request confirmed)":
   "This SMS has to come once the withdrawal OTP is verified successfully, but it currently comes only once the UTR is approved in the LMS.",
 "Loan Disbursed (First Disbursement)": "In the disbursement mail, Disbursement No. ({{DISBURSEMENT_NO}}) and Disbursement UTRN ({{UTRN}}) currently show a random format; the format of both has to be defined correctly.",
 "EMI Success": "In the mail, “Next EMI Due Date: {{NEXT_EMI_DATE}}” – what is shown for the last EMI (12th EMI), when there is no next EMI, has to be defined.",
 "EMI Failed": "In the mail, the title “Instalment Failure / EMI Bounce Notification (Bounce - 1A)” has to be changed to “EMI Payment Failed”.",
 "Pledging of Mutual Fund": "Both the SMS and Email communication are currently received once the loan lodgement is successful, but they are supposed to come right after the pledging is successful.",
}
assert set(REMARKS) <= {r[0] for r in COMMS} | {r[1] for r in COMMS}      # keyed by stage, or by scenario
COMMS_COLS = COMMS_COLS + ["Remarks"]
COMMS = [r + (REMARKS.get(r[0]) or REMARKS.get(r[1]) or "",) for r in COMMS]
# “Not Required” rows go to their own table below the main one, numbered separately (DISC-243)
COMMS_NR = [r for r in COMMS if r[COMMS_COLS.index("SMS Status") - 1] == "Not Required"]
COMMS = [r for r in COMMS if r not in COMMS_NR]
# SMS Status and Mail Status columns are not shown any more – the Not Required rows are in their own table (DISC-244)
_drop = {COMMS_COLS.index(c) - 1 for c in ("SMS Status", "Mail Status")}
COMMS, COMMS_NR = ([tuple(v for i, v in enumerate(r) if i not in _drop) for r in t] for t in (COMMS, COMMS_NR))
COMMS_COLS = [c for c in COMMS_COLS if c not in ("SMS Status", "Mail Status")]
# Column groups shown as a header row above the column names (DISC-245): General (S.No – Communication Type, and Remarks),
# SMS (SMS Content Structure – SMS Available), Mail (Mail Subject Structure – Mail Available)
def _group(c): return "General" if c in ("S.No", "Stage", "Scenarios", "Application", "Sender", "Communication Type", "Remarks") else "SMS" if "SMS" in c else "Mail"
COMMS_GROUPS = []                          # [(label, number of columns)] in column order
for _c in COMMS_COLS:
    if COMMS_GROUPS and COMMS_GROUPS[-1][0] == _group(_c):
        COMMS_GROUPS[-1] = (COMMS_GROUPS[-1][0], COMMS_GROUPS[-1][1] + 1)
    else:
        COMMS_GROUPS.append((_group(_c), 1))
assert COMMS_GROUPS == [("General", 6), ("SMS", 4), ("Mail", 5), ("General", 1)], COMMS_GROUPS
# SMS-only rows: the empty Mail columns show “-” (as the SMS columns of a mail-only row do) (DISC-246)
_mail_ix = [i - 1 for i, c in enumerate(COMMS_COLS) if _group(c) == "Mail"]
_type_ix = COMMS_COLS.index("Communication Type") - 1
COMMS, COMMS_NR = ([tuple("-" if r[_type_ix] == "SMS" and i in _mail_ix and not v else v for i, v in enumerate(r)) for r in t]
                   for t in (COMMS, COMMS_NR))

# Summary counts shown above the table and in the Excel notes (DISC-241)
def _col(name): return [r[COMMS_COLS.index(name) - 1] for r in COMMS]
_types, _sav = _col("Communication Type"), _col("SMS Available")
COMMS_SUMMARY = [
    ("Total scenarios", len(COMMS), ""),
    ("SMS", sum("SMS" in t for t in _types),
     f"{_sav.count('Yes')} available · {sum(a.startswith('No') for a in _sav)} to be created"),
    ("Mail", sum("Mail" in t for t in _types),
     f"{sum(a.startswith('Yes') for a in _col('Mail Available'))} available · {sum(a.startswith('No') for a in _col('Mail Available'))} to be created"),
    ("SMS and mail", _types.count("SMS, Mail"), ""),
    ("SMS only", _types.count("SMS"), ""),
    ("Mail only", _types.count("Mail"), ""),
    ("Not required", len(COMMS_NR), "separate table below"),
]

CONTACT = ('<p class="home-contact">Created by <b>Azhagarsamy Subburaj</b>. For any observation or clarification, '
           'please reach out to <a href="mailto:azhagarsamy.s@shriramcredit.in">azhagarsamy.s@shriramcredit.in</a></p>')

def comms_table(rows_data, cols, prefix):
    # “[[view:path]]” in a cell becomes a “View” link that opens the mail template (HTML) in a new tab (DISC-207)
    esc = lambda t: re.sub(r"\[\[view:([^\]]+)\]\]", r'<br><a class="mail-view" href="\1" target="_blank" rel="noopener">View</a>',
                           html.escape(t, quote=False).replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>").replace("\n", "<br>"))
    head = "".join(f'<th class="g-{_group(c).lower()}">{c}</th>' for c in cols)
    groups = "".join(f'<th class="grp g-{g.lower()}" colspan="{n}">{g}</th>' for g, n in COMMS_GROUPS) if cols == COMMS_COLS else ""
    # a template that is not available yet (Available starts with “No”) is highlighted (DISC-190)
    avail = cols.index("SMS Available" if "SMS Available" in cols else "Available") - 1
    stat = cols.index("SMS Status") - 1 if "SMS Status" in cols else None
    mavail = cols.index("Mail Available") - 1 if "Mail Available" in cols else avail      # a mail to be created is highlighted too (DISC-247)
    cls = lambda r: " ".join(c for c, on in (("na", r[avail].startswith("No") or r[mavail].startswith("No")), ("nr", stat is not None and r[stat] == "Not Required")) if on)
    slug = [re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-") for c in cols[1:]]     # each cell gets a class from its column (DISC-204)
    rows = "".join('<tr class="%s"><td class="c-s-no">%d</td>%s</tr>' % (cls(r), k, "".join(f'<td class="c-{c}">{esc(v)}</td>' for c, v in zip(slug, r)))
                   for k, r in enumerate(rows_data, 1))
    return f'<div class="comms-wrap"><table class="comms {prefix}"><thead>{f"<tr>{groups}</tr>" if groups else ""}<tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'

def comms_body(home):          # one table: SMS and mail together; the separate Mail table was removed (DISC-240)
    return (LOGO.format(home=home) + '<h1>LAMF – Customer Communications</h1>'
            '<p class="nm-cta-top"><a class="home-cta" href="new-mails.html">New Customer Mails (temporary) →</a></p>'   # DISC-304
            f'<p>SMS and mail sent to the customer during the LAMF journey ({len(COMMS)} communications; {len(COMMS_NR)} not required, in the table below). '
            'Content Structure shows the approved template; Actual Content shows a sample with the variables filled in.</p>'
            + '<div class="comms-summary">' + "".join(
                f'<div><b>{v}</b><span>{html.escape(k)}</span>' + (f'<small>{html.escape(d)}</small>' if d else '') + '</div>'
                for k, v, d in COMMS_SUMMARY) + '</div>'
            + comms_table(COMMS, COMMS_COLS, 'sms')
            + f'<h2 id="comms-nr">Not Required ({len(COMMS_NR)})</h2><p>SMS and mail marked “Not Required” – kept for reference only; they will not be sent.</p>'
            + comms_table(COMMS_NR, COMMS_COLS, 'sms') + CONTACT)

# Internal communications – LMS mail alerts to the OPS / Treasury teams (DISC-267); data in tools/internal_comms.py
from internal_comms import INTERNAL, NAMES, GREET_ONLY
IC_SAMPLE = {"{{LAN}}": "SCCLMF20261100017", "{{Customer Full Name}}": "Azhagarsamy Subburaj", "{{Customer Name}}": "Azhagarsamy Subburaj",
             "{{Sanction Amount}}": "1000000.00", "{{Disbursement Amount}}": "100000.00",
             # Charges Waived Off alert (DISC-343) – same sample as the LMS prototype (Processing Fee 1,768.82, 500 waived – DISC-354)
             "{{Waived Amount}}": "500.00", "{{Waive-off Type}}": "Partial waive-off", "{{OPS User Name}}": "OPS user",
             "{{Waive-off Date & Time}}": "23-11-2026 11:20 AM", "{{Balance Payable}}": "1,268.82",
             # DRAFT Application Rejected alert (DISC-348)
             "{{Rejection Reason}}": "Customer asked for lien removal", "{{Rejection Date & Time}}": "23-11-2026 11:25 AM",
             # Waive-off & Rejection approval alerts (DISC-361)
             "{{Submitted Date & Time}}": "23-11-2026 11:25 AM", "{{Approval Date & Time}}": "23-11-2026 12:05 PM",
             # Charges Payment Received alert (DISC-351)
             "{{Amount Paid}}": "1,268.82", "{{Transaction ID}}": "pay_SCCL7Q2X9K4M1B", "{{Payment Date & Time}}": "23-11-2026 11:42 AM", "{{Receipt No}}": "RCPT/LAMF/2026/11/000149",
             # Charges Received – Initiate De-pledge alert (DISC-359)
             "{{Treasury User Name}}": "Natarajan K", "{{Confirmation Date & Time}}": "23-11-2026 03:10 PM"}
IC_STATUS = r"\b(PENDING DISBURSEMENT|ACCOUNT OPENED|SUBMITTED|REJECTED|ACTIVE|CLOSED|REQUESTED|APPROVED)\b"
IC_FILE = lambda n: f"internal/IC-{n:02d}.html"

def ic_mail_body(text):     # mail view: “\n” starts a new paragraph, lines starting with “|” form a table (DISC-343)
    out, rows = [], []
    def flush():
        if rows:
            cell = lambda tag, c, i: f'<{tag} style="border:1px solid #ddd;padding:6px 10px;text-align:{"left" if i == 0 else "right"}">{c}</{tag}>'
            body = "".join("<tr>" + "".join(cell("th" if r == 0 or r == len(rows) - 1 and rows[r][0].strip() == "Total" else "td", c.strip(), i)
                                            for i, c in enumerate(row)) + "</tr>" for r, row in enumerate(rows))
            out.append(f'<table style="border-collapse:collapse;width:100%;margin:6px 0 14px;font-size:14px">{body}</table>'); rows.clear()
    for line in text.split("\n"):
        if line.startswith("|"):
            rows.append(ic_fill(line[1:]).split("|"))
        else:
            flush(); out.append(f"<p>{ic_fill(line)}</p>")
    flush()
    return "".join(out)

def ic_fill(text, bold=True):    # sample values in a structure; in the mail body the values and statuses are bold
    t = html.escape(text, quote=False)
    for k, v in IC_SAMPLE.items():
        t = t.replace(html.escape(k, quote=False), f"<b>{v}</b>" if bold else v)
    return re.sub(IC_STATUS, r"<b>\1</b>", t) if bold else t

def internal_body(home):
    esc = lambda t: html.escape(t, quote=False).replace("\n", "<br>")
    rows = []
    for n, (lan, disb, trig, subj, title, greet, body, scen) in enumerate(INTERNAL, 1):
        content = esc(f"{title}\n\nDear {greet},\n\n{body}\n\nRegards,\nTeam Shriram Credit\nThis is a system-generated email. Please do not reply.")
        for k, (sc, to, cc) in enumerate(scen):
            span = f' rowspan="{len(scen)}"' if len(scen) > 1 else ""
            first = (f'<td class="c"{span}>{n}</td><td{span}>{esc(lan)}</td><td{span}>{esc(disb)}</td><td class="trig"{span}>{esc(trig)}</td>'
                     f'<td{span}>{esc(subj)}</td><td class="body"{span}>{content}</td>') if k == 0 else ""
            view = f'<td class="c"{span}><a class="mail-view" href="{IC_FILE(n)}" target="_blank" rel="noopener">View</a></td>' if k == 0 else ""
            rows.append(f'<tr>{first}<td>{esc(sc)}</td><td class="em">{"<br>".join(to)}</td><td class="em">{"<br>".join(cc)}</td>{view}</tr>')
    n_sc = sum(len(e[7]) for e in INTERNAL)
    head = "".join(f"<th>{h}</th>" for h in ["#", "LAN Status", "Disbursement Status", "Trigger Event", "Subject Structure", "Email Content",
                                             "Scenario", "TO", "CC", "Mail"])
    return (LOGO.format(home=home) + '<h1>LAMF – Internal Communications</h1>'
            f'<p>Mail alerts sent from the LMS to the internal teams (OPS, Treasury) when the loan account or the disbursement status changes – '
            f'{len(INTERNAL)} alerts, {n_sc} recipient scenarios. “View” opens how the mail looks.</p>'
            f'<div class="comms-wrap"><table class="comms ic"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>' + CONTACT)

IC_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Internal mail</title>
<style>
body{{margin:0;background:#fff;font-family:"Segoe UI",Arial,Helvetica,sans-serif;color:#1a1a1a}}
.top{{padding:14px 28px 0}} .top a{{font-size:13px;color:#555;text-decoration:none}} .top a:hover{{text-decoration:underline}}
h1.subj{{font-size:24px;font-weight:400;margin:10px 28px 14px}}
.msg{{margin:0 22px 28px;border:1px solid #e3e3e3;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.mh{{display:flex;gap:14px;padding:18px 22px 14px}} .av{{flex:none;width:44px;height:44px;border-radius:50%;background:#f4c7cb;color:#a4262c;display:flex;align-items:center;justify-content:center;font-size:18px}}
.mi{{flex:1;min-width:0;font-size:14px;line-height:21px}} .mi .fr{{font-weight:600;font-size:16px}} .mi .lb{{color:#555}}
.dt{{flex:none;font-size:13px;color:#555;text-align:right}}
.sw{{display:flex;flex-wrap:wrap;gap:8px;padding:0 22px 12px 80px}} .sw button{{font:inherit;font-size:12.5px;border:1px solid #ccc;background:#fff;border-radius:14px;padding:4px 12px;cursor:pointer}}
.sw button.on{{background:#1a1a1a;color:#FFC20E;border-color:#1a1a1a}}
.wrap{{background:#efeeec;margin:0 22px 22px;padding:32px 12px 40px}}
.mail{{width:600px;max-width:100%;margin:0 auto;background:#fff;border-radius:8px;overflow:hidden}}
.logo{{text-align:center;padding:28px 40px 20px}} .logo img{{width:200px}} .rule{{height:5px;background:#FFC20E}}
.band{{background:#1a1a1a;color:#FFC20E;text-align:center;font-weight:bold;font-size:20px;line-height:26px;padding:22px 40px;font-family:Arial,Helvetica,sans-serif}}
.body{{padding:36px 48px 32px;font-size:15px;line-height:24px;color:#333;text-align:justify;font-family:Arial,Helvetica,sans-serif}}
.body .dear{{font-weight:bold;color:#1a1a1a;font-size:16px;margin:0 0 18px}} .body b{{color:#1a1a1a}} .body .reg{{margin-top:28px}}
.disc{{background:#FFC20E;padding:18px 48px;font-size:13px;font-family:Arial,Helvetica,sans-serif}}
.foot{{background:#1a1a1a;color:#ccc;text-align:center;font-size:12px;padding:14px 40px;font-family:Arial,Helvetica,sans-serif}}
@media (max-width:640px){{.mh{{flex-wrap:wrap}} .dt{{width:100%;text-align:left;padding-left:58px}} .sw{{padding-left:22px}} .wrap,.msg{{margin-left:8px;margin-right:8px}} .body,.disc{{padding-left:24px;padding-right:24px}}}}
</style></head><body>
<div class="top"><a href="../internal-communications.html">← Internal communications</a></div>
<h1 class="subj">{subject}</h1>
<div class="msg">
<div class="mh"><div class="av">S</div>
<div class="mi"><div class="fr">support.las@shriramcredit.in</div><div><span class="lb">To:</span> <span id="to">{to}</span></div><div><span class="lb">Cc:</span> <span id="cc">{cc}</span></div></div>
<div class="dt">Mon 16-11-2026 6:13 PM</div></div>{switch}
<div class="wrap"><div class="mail">
<div class="logo"><img src="../assets/img/shriram-logo.png" alt="Shriram Credit"></div><div class="rule"></div>
<div class="band">{title}</div>
<div class="body"><p class="dear">Dear <span id="dear">{greet}</span>,</p>{body}<p class="reg">Regards,<br><b>Team Shriram Credit</b></p></div>
<div class="disc">This is a system-generated email. Please do not reply.</div>
<div class="foot">© 2026 Shriram Credit Company Limited. All rights reserved.</div>
</div></div></div>{script}
</body></html>
"""

def write_internal_mails():
    import json as _json
    os.makedirs(os.path.join(ROOT, "internal"), exist_ok=True)
    name = lambda e: e if e in GREET_ONLY else NAMES.get(e, e)     # To / Cc as Outlook shows them: the name, else the address
    for n, (lan, disb, trig, subj, title, greet, body, scen) in enumerate(INTERNAL, 1):
        # Dear {{To User Name}} – the TO person's name (DISC-268); more than one TO keeps “All”
        rec = [{"to": "; ".join(name(e) for e in to), "cc": "; ".join(name(e) for e in cc),
                "dear": NAMES.get(to[0], to[0]) if greet == "{{To User Name}}" and len(to) == 1 else "All"} for _, to, cc in scen]
        switch = script = ""
        if len(scen) > 1:            # two recipient scenarios (< 5L / >= 5L): a switch changes To / Cc / Dear
            switch = '<div class="sw">' + "".join(f'<button type="button" data-i="{i}"{" class=on" if i == 0 else ""}>{html.escape(sc)}</button>'
                                                  for i, (sc, _, _) in enumerate(scen)) + "</div>"
            script = ("<script>var R=" + _json.dumps(rec) + ";document.querySelectorAll('.sw button').forEach(function(b){b.onclick=function(){"
                      "document.querySelectorAll('.sw button').forEach(function(x){x.classList.toggle('on',x===b)});var r=R[b.dataset.i];"
                      "document.getElementById('to').textContent=r.to;document.getElementById('cc').textContent=r.cc;"
                      "document.getElementById('dear').textContent=r.dear;};});</script>")
        with open(os.path.join(ROOT, IC_FILE(n)), "w") as f:
            f.write(IC_PAGE.format(title=html.escape(title), subject=ic_fill(subj, bold=False).strip(), switch=switch,
                                   to=html.escape(rec[0]["to"]), cc=html.escape(rec[0]["cc"]), greet=html.escape(rec[0]["dear"]),
                                   body=ic_mail_body(body), script=script))

def calc_body(home):          # calculator page, opened by the 4th CTA on the home page (DISC-256); logic in assets/calc.js (DISC-257, DISC-263)
    opt = lambda vals, sel=None: "".join(f'<option{" selected" if v == sel else ""}>{v}</option>' for v in vals)
    fld = lambda label, ctrl, cls="": f'<label class="calc-f {cls}"><span>{label}</span>{ctrl}</label>'
    sec = lambda n, title, body, cls="": f'<section class="calc-sec {cls}"><h2><i>{n}</i>{title}</h2>{body}</section>'
    rows = lambda cls, title, btn: (f'<div class="calc-list {cls}"><h3>{title}</h3><table><thead><tr><th>Date</th><th>Amount (₹)</th><th></th></tr></thead>'
                                    f'<tbody></tbody></table><button type="button" class="calc-add" data-add="{cls}">+ {btn}</button></div>')
    return (LOGO.format(home=home) + '<h1>LAMF – Calculator</h1>'
            '<p class="calc-intro">Enter the loan details and click Calculate Now to see the amount due on every due date, '
            'with the principal and interest split and the interest accrual period.</p>'
            '<form class="calc-form" novalidate>'
            + sec(1, "Loan details", '<div class="calc-grid">'
                  + fld("Product", f'<select name="product">{opt(["Line of Credit", "Single Disbursement", "Multiple Disbursement"], "Line of Credit")}</select>')
                  + fld("Repayment Type", f'<select name="type">{opt(["EMI", "Balloon / Interest Only"], "Balloon / Interest Only")}</select>')
                  + fld("Rate of Interest (% p.a.)", '<input name="rate" inputmode="decimal" value="11">')
                  + fld("Tenure in Months", f'<select name="tenure">{opt(["12", "24", "36", "48", "60", "72"], "12")}</select>')
                  + '<label class="calc-chk"><input type="checkbox" name="leap"><span>Leap year calculation – use 366 days for the days in a leap year '
                    '(when not ticked, 365 days are used in every year)</span></label></div>')
            + sec(2, "Loan period", '<div class="calc-grid">'
                  + fld("Lodgement Approval Date (Loan Start Date)", '<input type="date" name="start" value="2026-10-26">')
                  + fld("Loan End Date", '<input name="end" readonly tabindex="-1">', "ro")
                  + fld("Due Date of Every Month", '<input name="dueday" value="5th of every month" readonly tabindex="-1">', "ro")
                  + fld("As on Date", '<input type="date" name="ason" title="Date for the collected / pending summary">') + '</div>')
            + sec(3, "Withdrawals and repayments",
                  '<div class="tx-box"><div class="tx-new">'
                  '<div class="calc-f"><span>Type</span><div class="tx-seg"><button type="button" data-kind="w" class="on">↓ Withdrawal</button>'
                  '<button type="button" data-kind="r">↑ Repayment</button></div></div>'
                  + fld("Date", '<input type="date" name="txd">')
                  + fld("Amount", '<div class="amt-w"><i>₹</i><input name="txa" inputmode="decimal" placeholder="0"></div>')
                  + '<button type="button" class="tx-addbtn">+ Add</button></div><p class="tx-msg" role="alert"></p>'
                  '<ol class="tx-list"></ol><p class="tx-empty">No withdrawal or repayment added yet.</p>'
                  '<div class="tx-sum"><div><span>Total withdrawals</span><b class="sw"></b></div><div><span>Total repayments</span><b class="sr"></b></div>'
                  '<div class="hi"><span>Outstanding principal</span><b class="so"></b></div></div></div>')
            + '<div class="calc-actions"><button class="calc-go" type="submit">Calculate Now</button><p class="calc-err" role="alert"></p></div></form>'
            '<div class="calc-out"></div>' + CONTACT)

# BRD documents (DISC-269); data in tools/brds.py
from brds import BRDS
BRD_FILE = lambda b: f"brd-{b['slug']}.html"

def brd_list_body(home, link):
    cards = "".join(f'<a class="brd-card" href="{link(b)}"><span class="brd-st st-{b["status"].lower()}">{html.escape(b["status"])}</span>'
                    f'<b>{html.escape(b["title"])}</b><small>{html.escape(b["summary"])}</small>'
                    f'<i>Last updated {b["updated"]} →</i></a>' for b in BRDS)
    return (LOGO.format(home=home) + '<h1>LAMF – BRD Documents</h1>'
            f'<p>Business requirement documents ({len(BRDS)}). Click a BRD to open it.</p><div class="brd-grid">{cards}</div>' + CONTACT)

def brd_body(home, back, b):
    body = b["body"] or '<p class="brd-soon">The content of this BRD will be added here.</p>'
    return (LOGO.format(home=home) + f'<p class="brd-back"><a href="{back}">← All BRD documents</a></p>'
            f'<h1>BRD – {html.escape(b["title"])}</h1>'
            f'<p class="brd-meta"><span class="brd-st st-{b["status"].lower()}">{html.escape(b["status"])}</span>Last updated {b["updated"]} · {html.escape(b["summary"])}</p>'
            f'<div class="brd-body">{body}</div>' + CONTACT)

def home_body(home, prd, journey, comms, calc, internal, brd):
    # Communications opens a pop-up with Customer / Internal communications (DISC-269): a CSS :target pop-up, no script
    return (f'<header class="home-top">{LOGO.format(home=home)}</header>'
            '<main class="home">'
            '<p class="home-kicker">Shriram Credit · Loan Against Mutual Funds</p>'
            '<h1>LAMF – LOS Customer Online Journey</h1>'
            '<p class="home-sub">Product requirements and the clickable prototype of the online loan journey.</p>'
            '<div class="home-ctas">'
            f'<a class="home-cta" href="{prd}">Open the PRD document →</a>'
            f'<a class="home-cta" href="{brd}">Open BRD document →</a>'
            f'<a class="home-cta" href="{journey}">Start the LAMF journey →</a>'
            '<a class="home-cta" href="#comms-pop">Communications →</a>'
            f'<a class="home-cta" href="{calc}">Calculator →</a>'
            '<a class="home-cta" href="lms.html">LMS →</a>'   # LMS modules page (DISC-327)
            '</div>' + CONTACT + '</main>'
            '<div class="home-pop" id="comms-pop" role="dialog" aria-label="Communications"><a class="home-pop-bg" href="#" aria-label="Close"></a>'
            '<div class="home-pop-box"><a class="home-pop-x" href="#" aria-label="Close">×</a><h2>Communications</h2>'
            '<p>Choose the communications to open.</p><div class="home-pop-ctas">'
            f'<a class="home-cta" href="{comms}">Customer communications →</a>'
            f'<a class="home-cta" href="{internal}">Internal communications →</a></div></div></div>')

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
<script src="assets/colresize.js"></script>
</body>
</html>
"""
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(PAGE.format(title="LAMF Online Journey", cls="page-home",
                        body=home_body("index.html", "SCCL_LAMF_LOS_PRD.html", "screens.html", "communications.html", "calculator.html",
                                       "internal-communications.html", "brd.html")))
with open(os.path.join(ROOT, "brd.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – BRD Documents", cls="page-screens page-brd", body=brd_list_body("index.html", BRD_FILE)))
for _b in BRDS:
    with open(os.path.join(ROOT, BRD_FILE(_b)), "w") as f:
        f.write(PAGE.format(title=f"LAMF – BRD – {_b['title']}", cls="page-screens page-brd", body=brd_body("index.html", "brd.html", _b)))
with open(os.path.join(ROOT, "internal-communications.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – Internal Communications", cls="page-screens page-comms page-ic", body=internal_body("index.html")))
write_internal_mails()
with open(os.path.join(ROOT, "calculator.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – Calculator", cls="page-screens page-calc", body=calc_body("index.html") + '<script src="assets/calc.js"></script>'))
with open(os.path.join(ROOT, "communications.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – Customer Communications", cls="page-screens page-comms", body=comms_body("index.html")))
# LMS modules page, opened by the LMS CTA on the home page (DISC-327); data in tools/lms.py
from lms import lms_body
with open(os.path.join(ROOT, "lms.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – LMS", cls="page-lms", body=lms_body(LOGO.format(home="index.html"), "index.html")))
# LOS charges payment after a DRAFT rejection and the payment receipt (DISC-351); data in tools/charges_payment.py
import charges_payment as _cp
with open(os.path.join(ROOT, "charges-payment.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – LOS Charges Payment", cls="page-cp", body=_cp.body()))
with open(os.path.join(ROOT, "charges-receipt.html"), "w") as f:
    f.write(_cp.receipt())
# New customer mails from the additional scenarios sheet – separate list page + one HTML per mail (DISC-304)
from new_mails import NEW_MAILS, mail_html, list_body as new_mails_body
os.makedirs(os.path.join(ROOT, "new-mails"), exist_ok=True)
for _m in NEW_MAILS:
    with open(os.path.join(ROOT, "new-mails", _m[0] + ".html"), "w") as f:
        f.write(mail_html(_m))
with open(os.path.join(ROOT, "new-mails.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – New Customer Mails", cls="page-screens page-brd page-nm",
                        body=new_mails_body(LOGO.format(home="index.html"), "communications.html")))
with open(os.path.join(ROOT, "screens.html"), "w") as f:
    f.write(PAGE.format(title="LAMF Online Journey – Screens", cls="page-screens",
                        body=screens_body("index.html", lambda n: quote(n + ".html"))))
print(len(PAGES), "pages + index.html (home) + screens.html + communications.html + calculator.html written")

# ---- cloud copy: one page, hash routed (artifact sandboxes cannot navigate between files)
import json as _json
from urllib.parse import quote as _q

screens_js = ["/* Generated by tools/build_pages.py – one render function per screen. */",
              "window.SCREEN_RENDER = {"]
for name, code in PAGES.items():
    screens_js.append(f"  {_json.dumps(name)}: function () {{ {code}; }},")
screens_js.append("};")
screens_js.append("window.HOME_HTML = " + _json.dumps(home_body("#", "#PRD", "#SCREENS", "#COMMS", "#CALC", "#INTERNAL", "#BRD")) + ";")
screens_js.append("window.COMMS_HTML = " + _json.dumps(comms_body("#")) + ";")
screens_js.append("window.CALC_HTML = " + _json.dumps(calc_body("#")) + ";")
screens_js.append("window.INTERNAL_HTML = " + _json.dumps(internal_body("#")) + ";")
screens_js.append("window.BRD_HTML = " + _json.dumps({"": brd_list_body("#", lambda b: "#BRD/" + b["slug"]),
                                                      **{b["slug"]: brd_body("#", "#BRD", b) for b in BRDS}}) + ";")
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
<script>""" + _read("assets", "calc.js") + """</script>
<script>""" + _read("assets", "screens.js") + """</script>
<script>""" + _read("assets", "prd-body.js") + """</script>
<script>""" + _read("assets", "colresize.js") + """</script>
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
    if (name.split('/')[0] === 'BRD' && window.BRD_HTML[name.split('/')[1] || ''] !== undefined) {
      LAMF.render(window.BRD_HTML[name.split('/')[1] || ''], { bodyClass: 'page-screens' }); document.body.classList.add('page-brd'); return; }
    if (name === 'INTERNAL') { LAMF.render(window.INTERNAL_HTML, { bodyClass: 'page-screens' }); document.body.classList.add('page-comms', 'page-ic'); return; }
    if (name === 'CALC') { LAMF.render(window.CALC_HTML, { bodyClass: 'page-screens' }); document.body.classList.add('page-calc'); window.LAMFCalc.init(); return; }
    if (name === 'COMMS') { LAMF.render(window.COMMS_HTML, { bodyClass: 'page-screens' }); document.body.classList.add('page-comms'); return; }
    LAMF.render(window.HOME_HTML, { bodyClass: 'page-home' });
    if (name === 'comms-pop') document.getElementById('comms-pop').classList.add('open');   // Communications pop-up (DISC-269)
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
