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
  'Dear {#alphanumeric#}, The lien on your Mutual Fund units pledged against loan account {#alphanumeric#} has been removed successfully. Your units are now released from lien - Shriram Credit',
  'Dear AZHAGARSAMY, The lien on your Mutual Fund units pledged against loan account SCCLMF20261000102 has been removed successfully. Your units are now released from lien - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
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
  "When the OPS team rejects the Loan Account Opening or the Loan Lodgement in the backend LMS – one common SMS for either rejection – WITH payment link, when the customer has charges to pay (processing fee, lien marking and lien removal). Template drafted by Claude for approval; to be created and registered",
  "LMS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, We regret that your Loan Against Mutual Fund application could not be approved. Please pay the applicable charges (processing fee, lien marking and lien removal) of Rs. {#alphanumeric#} using this link: {#urg#} - Shriram Credit",
  "Dear AZHAGARSAMY, We regret that your Loan Against Mutual Fund application could not be approved. Please pay the applicable charges (processing fee, lien marking and lien removal) of Rs. 92,313 using this link: https://lamf.shriramcredit.in/ - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created"),
 ("Loan Account Opening / Loan Lodgement Rejection (without payment link)",
  "When the OPS team rejects the Loan Account Opening or the Loan Lodgement in the backend LMS – one common SMS for either rejection – WITHOUT payment link, when there are no charges for the customer to pay. Template drafted by Claude for approval; to be created and registered",
  "LMS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, We regret that your Loan Against Mutual Fund application could not be approved. For assistance, please contact our support team - Shriram Credit",
  "Dear AZHAGARSAMY, We regret that your Loan Against Mutual Fund application could not be approved. For assistance, please contact our support team - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created"),
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
  'Dear {#alphanumeric#}, Your withdrawal request of Rs. {#alphanumeric#} for loan account {#alphanumeric#} has been rejected. For assistance, please contact our support team - Shriram Credit',
  'Dear AZHAGARSAMY, Your withdrawal request of Rs. 10,000 for loan account SCCLMF20261000102 has been rejected. For assistance, please contact our support team - Shriram Credit',
  "-", "SGRCDT-T", "No – to be created"),
 ("Loan Disbursed (First Disbursement)",
  "When the loan is disbursed for the first time (first disbursement) – notifying the customer that the amount is credited to the bank account. Each subsequent withdrawal is the mail-only row below",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Congratulations! Your loan has been credited to your bank account. Thank you for choosing Shriram Credit - Shriram Credit",
  "Dear AZHAGARSAMY, Congratulations! Your loan has been credited to your bank account. Thank you for choosing Shriram Credit - Shriram Credit",
  "-", "SGRCDT-T", "Yes"), ("EMI Reminder (T-5)",
  "First EMI reminder: sent on the 1st of every month – T-5 / T-4 before the EMI presentation date – notifying the customer of the upcoming instalment (SMS and mail). The second reminder, T-1, is mail only (next row)",
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
  "Notifying the customer when the instalment presented on the 5th of the month bounces (rejected by the bank); the debit is retried on the 10th – SMS and mail",
  "LOS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your EMI of Rs. {#alphanumeric#} was rejected by your bank on {#alphanumeric#}. We will retry on {#alphanumeric#}. Please ensure sufficient balance - Shriram Credit",
  "Dear AZHAGARSAMY, Your EMI of Rs. 10,000 was rejected by your bank on 05-11-2026. We will retry on 10-11-2026. Please ensure sufficient balance - Shriram Credit",
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
  "When the customer forecloses (pre-closes) the loan before the end of the tenure and the foreclosure is completed. Template drafted by Claude for approval; to be created and registered",
  "LMS", "SMS", "SCCL",
  "Dear {#alphanumeric#}, Your Loan Against Mutual Fund account {#alphanumeric#} has been foreclosed successfully. Your MF units will be released from lien in 2-3 working days - Shriram Credit",
  "Dear AZHAGARSAMY, Your Loan Against Mutual Fund account SCCLMF20261000102 has been foreclosed successfully. Your MF units will be released from lien in 2-3 working days - Shriram Credit",
  "-", "SGRCDT-T", "No – to be created"),
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
                   "and you will not receive a response. Loan against Securities is for personal use only and cannot be used for speculative "
                   "activities, capital market-related purposes, or anti-social purposes.")
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
            self.parts.append(": ".join(self.row)); self.row = []
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
 # two rows share the stage “Withdrawal”, so this one is keyed by its scenario (DISC-209)
 "When the customer initiates a withdrawal from the loan account, an OTP is sent to confirm the withdrawal": ("06_Withdrawal_Verification.html",
    "{{OTP}} – Your Withdrawal Verification OTP for Shriram Credit LAMF", "123456 – Your Withdrawal Verification OTP for Shriram Credit LAMF",
    "", {"{{OTP}}": "123456", "{{WITHDRAWAL_AMOUNT}}": "10,000"}),
 "Loan Lodgement Approval": ("05_Withdrawal_Initiation.html",
    "Withdrawal Initiation: Successful LAMF Account Creation – {{CUSTOMER_FULL_NAME}}",
    "Withdrawal Initiation: Successful LAMF Account Creation – AZHAGARSAMY SUBBURAJ",
    "", {"{{LOAN_ID}}": "SCCLMF20261000102", "{{Link}}": "https://lamf.shriramcredit.in/"}),
 "EMI Reminder (T-5)": ("09_Upcoming_EMI_Due_Reminder_T-5.html",
    "Reminder: Your EMI of ₹{{EMI_AMOUNT}} is due on {{DUE_DATE}}", "Reminder: Your EMI of ₹10,000 is due on 05-11-2026",
    "Trigger: 1st of every month – T-5 / T-4 before the EMI presentation date\n\n",
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
def _sample_schedule(text):      # sample: 12 monthly rows from 05-Dec-2026 (interest only, principal with the last instalment)
    rows = [f"05-{m}-{y} | ₹{'10,088' if k == 11 else '88'}" for k, (m, y) in enumerate(
        [("Dec", 2026)] + [(x, 2027) for x in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]])]
    return text.replace("DD-MMM-YYYY | ₹XXXXXXX\n" * 12, "\n".join(rows) + "\n").replace(
        "(13th row only when required) DD-MMM-YYYY | ₹XXXXXXX\n", "(13th row only when required – not needed in this sample)\n")

def _with_mail(r):
    if r[0] in TEXT_MAILS and not r[10]:
        subj, subj_sample, body, subs = TEXT_MAILS[r[0]]
        sample = _sample_schedule(body).replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY")
        for k, v in subs.items():
            sample = sample.replace(k, v)
        return r[:3] + ("SMS, Mail",) + r[4:10] + (subj, subj_sample, body, sample, "Yes", "Required")
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

# Mail-only rows from HTML templates (no SMS): inserted after the given stage (DISC-216)
MAIL_ONLY = [
 ("EMI Reminder (T-5)", "EMI Presentation Reminder (T-1)",
  "Second EMI reminder: sent 1 day before the EMI presentation date (T-1) – mail only, no SMS. The first reminder, T-5, is the row above",
  "LOS", "10_EMI_Presentation_T-1.html", "EMI Presentation Alert – {{DATE}}", "EMI Presentation Alert – 05-11-2026",
  "Trigger: 1 day before the EMI presentation date (T-1)\n\n",
  {"{{EMI_AMOUNT}}": "10,000", "{{DATE}}": "05-11-2026", "{{BORROWED_AMOUNT}}": "1,00,000", "{{OUTSTANDING_AMOUNT}}": "1,00,000",
   "{{BANK_ACCOUNT_NUMBER}}": "XXXXXXXX8736", "{{LOAN_ID}}": "SCCLMF20261000102"}),
 ("Loan Disbursed (First Disbursement)", "Loan Disbursed (Subsequent Disbursement)",
  "On each subsequent withdrawal / disbursement after the first one – notifying the customer that the amount is credited to the bank account (mail only, no SMS). The first disbursement is the row above",
  "LOS", "08_Loan_Disbursal_Confirmation_Subsequent.html", "Loan disbursed to your account", "Loan disbursed to your account",
  "Trigger: each subsequent disbursement (Disbursement Type: Multiple); the repayment schedule shows the residual term only\n\n",
  {"{{LOAN_AMOUNT}}": "20,000", "{{CUSTOMER_ID}}": "SCCL1000102", "{{LOAN_ACCOUNT_ID}}": "SCCLMF20261000102", "{{DISBURSEMENT_NO}}": "2",
   "{{UTRN}}": "UTIBR52026110200002", "{{LOAN_TENURE}}": "12", "{{EMI_AMOUNT}}": "175", "{{FIRST_EMI_DATE}}": "05-Dec-2026",
   "{{BALANCE_AMOUNT}}": "1,55,06,100", "{{PURPOSE}}": "Home Renovation"}),
]
for after, stage, scen, app, fname, subj, subj_sample, head, subs in MAIL_ONLY:
    body = head + mail_text(fname)
    sample = body.replace("{{CUSTOMER_NAME}}", "AZHAGARSAMY").replace("{{CUSTOMER_FULL_NAME}}", "AZHAGARSAMY SUBBURAJ")
    for k, v in subs.items():
        sample = sample.replace(k, v)
    _i = [r[0] for r in COMMS].index(after) + 1
    COMMS.insert(_i, (stage, scen, app, "Mail", "SCCL", "-", "-", "-", "-", "-",
                      subj, subj_sample, body, sample, f"Yes [[view:mails/{fname}]]", "Required"))
assert all(len(r) == len(COMMS_COLS) - 1 for r in COMMS)

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

CONTACT = ('<p class="home-contact">Created by <b>Azhagarsamy Subburaj</b>. For any observation or clarification, '
           'please reach out to <a href="mailto:azhagarsamy.s@shriramcredit.in">azhagarsamy.s@shriramcredit.in</a></p>')

def comms_table(rows_data, cols, prefix):
    # “[[view:path]]” in a cell becomes a “View” link that opens the mail template (HTML) in a new tab (DISC-207)
    esc = lambda t: re.sub(r"\[\[view:([^\]]+)\]\]", r'<br><a class="mail-view" href="\1" target="_blank" rel="noopener">View</a>',
                           html.escape(t, quote=False).replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>").replace("\n", "<br>"))
    head = "".join(f"<th>{c}</th>" for c in cols)
    # a template that is not available yet (Available starts with “No”) is highlighted (DISC-190)
    avail = cols.index("SMS Available" if "SMS Available" in cols else "Available") - 1
    stat = cols.index("SMS Status") - 1 if "SMS Status" in cols else None
    cls = lambda r: " ".join(c for c, on in (("na", r[avail].startswith("No")), ("nr", stat is not None and r[stat] == "Not Required")) if on)
    slug = [re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-") for c in cols[1:]]     # each cell gets a class from its column (DISC-204)
    rows = "".join('<tr class="%s"><td class="c-s-no">%d</td>%s</tr>' % (cls(r), k, "".join(f'<td class="c-{c}">{esc(v)}</td>' for c, v in zip(slug, r)))
                   for k, r in enumerate(rows_data, 1))
    return f'<div class="comms-wrap"><table class="comms {prefix}"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'

def comms_body(home):
    return (LOGO.format(home=home) + '<h1>LAMF – Customer Communications</h1>'
            f'<p>SMS and mail sent to the customer during the LAMF journey ({len(COMMS)} SMS, {len(MAILS)} mails). '
            'Content Structure / Body (template) shows the approved template; Actual Content / Body (sample) shows a sample with the variables filled in.</p>'
            '<nav class="comms-jump"><a href="#comms-sms">SMS (' + str(len(COMMS)) + ')</a><a href="#comms-mail">Mail (' + str(len(MAILS)) + ')</a></nav>'
            f'<h2 id="comms-sms">SMS</h2>' + comms_table(COMMS, COMMS_COLS, 'sms') +
            f'<h2 id="comms-mail">Mail</h2><p>Mail Subject is filled; SMS Header does not apply.</p>' + comms_table(MAILS, MAIL_COLS, 'mail')
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
