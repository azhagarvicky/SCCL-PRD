# Apply for New Loan (Existing Customer) – separate prototype from lamf-journey/.
# Generates one HTML file per screen plus index.html. Content comes from assets/lamf.js
# templates in this folder. Re-run after adding a screen: python3 lamf-existing-customer/tools/build_pages.py
import os, html
from urllib.parse import quote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
 "01) LAMF Landing Page": "LAMF.render(LAMF.T.landing())",
 "02) Enter MF linked Mobile Number": "LAMF.render(LAMF.withModal(LAMF.T.landing(), LAMF.T.mobileModal()))",
 "03) Enter OTP for MF linked Mobile Number Verification": "LAMF.render(LAMF.withModal(LAMF.T.landing(), LAMF.T.otpModal()))",
 "04) Your Loans Page": "LAMF.render(LAMF.T.loans())",
 "04.1) Apply for New Loan Page": "LAMF.render(LAMF.T.applyNew())",
 "04.2) Apply for New Loan Existing PAN selected": "LAMF.render(LAMF.T.applyNew({mode:'existing', pan:'CBOPA8195B'}))",
 "04.3) Apply for New Loan New PAN verified": "LAMF.render(LAMF.T.applyNew({mode:'new'}))",
 "04.4) Your Loans Page Resume Loan Application": "LAMF.render(LAMF.T.loans())",
 "05) LOS to MF Central Redirection loading page": "LAMF.render(LAMF.withModal(LAMF.T.applyNew(), LAMF.T.mfcModal()))",
 "06) MF Central Mock Page": "LAMF.render(LAMF.T.mfMock())",
 "07) MF Central to LOS Redirecting Page": "LAMF.render(LAMF.T.redirecting())",
 "08) MF Central to LOS Fetching Mutual Fund Portfolio Page": "LAMF.render(LAMF.withModal(LAMF.T.applyNew(), LAMF.T.loader('Fetching your mutual fund portfolio..', 1)))",
 "09) MF Central to LOS Analysing Mutual Fund Portfolio Page": "LAMF.render(LAMF.withModal(LAMF.T.curated(), LAMF.T.loader('Analyzing your mutual fund portfolio..', 2)))",
 "10) MF Central to LOS Generating Loan Page": "LAMF.render(LAMF.withModal(LAMF.T.curated(), LAMF.T.loader('Generating best loan offers for you', 3)))",
 "11) Curated Offers Page": "LAMF.render(LAMF.T.curated())",
 "12) Mutual Fund Selection Page": "LAMF.render(LAMF.T.selection(LAMF.SEL_DEFAULT))",
 "12.1) Mutual Fund Selection page loan amount edit": "LAMF.render(LAMF.T.selection({editLoan:'9530700', sliderPct:47.6, mv:'1,27,07,600.09', count:1, selected:{icici:'95,30,700'}, ctaDisabled:true, cta:'95,30,700'}))",
 "12.2) Mutual Fund Selection page loan amount edit as fund wise": "LAMF.render(LAMF.T.selection({loan:'95,30,700', sliderPct:47.6, mv:'1,27,07,600.09', count:1, editing:{icici:'100000'}, cta:'95,30,700'}))",
 "13) Loan Application Summary": "LAMF.render(LAMF.T.summary())",
 "14) KYC Verification Page": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'done', bank:{name:'ICICI Bank', account:'001201548736', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'on'}))",
 "14.1) KYC Verification Page New PAN email verification": "LAMF.render(LAMF.T.kyc({email:'input'}))",
 "14.2) KYC Verification Page New PAN email OTP popup": "LAMF.render(LAMF.T.kyc({email:'input'}))",
 "15) DigiLocker Mock Page": "LAMF.render(LAMF.T.kycMock('aadhaar'))",
 "15.1) KYC Verification Page New PAN Aadhaar verification success": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'start', bank:{name:'ICICI Bank', account:'001201548736', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "15.2) KYC Verification Page New PAN Aadhaar verification failed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'start', aadErr:'Aadhaar verification failed. Please try again.', bank:{name:'ICICI Bank', account:'001201548736', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "16) Photo Verification Mock Page": "LAMF.render(LAMF.T.kycMock('photo'))",
 "16.1) KYC Verification Page New PAN Photo verification success": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'done', bank:{name:'ICICI Bank', account:'001201548736', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'on'}))",
 "16.2) KYC Verification Page New PAN Photo verification failed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'start', photoErr:'Photo verification failed. Please try again.', bank:{name:'ICICI Bank', account:'001201548736', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "16.3) KYC Verification Page New PAN bank details": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'done', bankForm:LAMF.T.bankForm(), cont:'off'}))",
 "17) Customer Details Page": "LAMF.render(LAMF.T.custDetails())",
 "18) Pledging of Mutual Fund Page": "LAMF.render(LAMF.T.pledge())",
 "18.1) Pledging of Mutual Fund OTP popup": "LAMF.render(LAMF.withModal(LAMF.T.pledge(), LAMF.T.pledgeOtpModal()))",
 "18.2) Pledging of Mutual Fund Successfully pledged": "LAMF.render(LAMF.withModal(LAMF.T.pledge(), LAMF.T.pledgedModal()))",
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
 "23) Loan Application Submitted Page": "LAMF.render(LAMF.T.submitted())",
 "24) Your Loans Page New Loan Submitted": "LAMF.render(LAMF.T.loanSubmitted())",
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
</body>
</html>
"""
for name, code in PAGES.items():
    with open(os.path.join(ROOT, name + ".html"), "w") as f:
        f.write(TPL.format(title=html.escape(name), code=code))

# Home page (index.html: Start the journey / View all pages) and screen list (screens.html).
# Same look as the lamf-journey home page; styles live in lamf.css (.page-home / .page-screens).
LOGO = '<a class="logo" href="index.html" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a>'
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="assets/lamf.css">
</head>
<body class="{cls}">{body}
</body>
</html>
"""
first = next(iter(PAGES))
home = (f'<header class="home-top">{LOGO}</header>'
        '<main class="home">'
        '<p class="home-kicker">Shriram Credit · Loan Against Mutual Funds</p>'
        '<h1>LAMF – Apply for New Loan (Existing Customer)</h1>'
        '<p class="home-sub">Clickable prototype of the new loan journey for existing customers.</p>'
        '<div class="home-ctas">'
        f'<a class="home-cta" href="{quote(first + ".html")}">Start the journey →</a>'
        '<a class="home-cta" href="screens.html">View all pages →</a>'
        '</div></main>')
items = "\n".join(f'<li><a href="{quote(n + ".html")}">{html.escape(n)}</a></li>' for n in PAGES)
screens = (LOGO + '<h1>LAMF – Apply for New Loan (Existing Customer) – Screens</h1>'
           f'<p>{len(PAGES)} screens, in screenshot order. Use the ☰ bar (bottom-right) or ← / → keys on any screen to move between them.</p>'
           f'<ol>{items}</ol>')
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – Apply for New Loan (Existing Customer)", cls="page-home", body=home))
with open(os.path.join(ROOT, "screens.html"), "w") as f:
    f.write(PAGE.format(title="LAMF – Apply for New Loan (Existing Customer) – Screens", cls="page-screens", body=screens))
print(len(PAGES), "pages + index.html (home) + screens.html written")
