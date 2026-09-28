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
 "14) KYC Verification Page": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'start', bank:{name:'ICICI Bank', account:'123405670006', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "14.1) KYC Verification Page New PAN email verification": "LAMF.render(LAMF.T.kyc({email:'input'}))",
 "15) DigiLocker Mock Page": "LAMF.render(LAMF.T.kycMock('aadhaar'))",
 "15.1) KYC Verification Page Aadhaar verification success": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'start', bank:{name:'ICICI Bank', account:'123405670006', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "15.2) KYC Verification Page Aadhaar verification failed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'start', aadErr:'Aadhaar verification failed. Please try again.', bank:{name:'ICICI Bank', account:'123405670006', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "16) Photo Verification Mock Page": "LAMF.render(LAMF.T.kycMock('photo'))",
 "16.1) KYC Verification Page Photo verification success": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'done', bank:{name:'ICICI Bank', account:'123405670006', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'on'}))",
 "16.2) KYC Verification Page Photo verification failed": "LAMF.render(LAMF.T.kyc({email:'done', aadhaar:'done', photo:'start', photoErr:'Photo verification failed. Please try again.', bank:{name:'ICICI Bank', account:'123405670006', ifsc:'ICIC0002692', logo:'funds/icici.png'}, cont:'off'}))",
 "17) Customer Details Page": "LAMF.render(LAMF.T.custDetails())",
 "18) Pledging of Mutual Fund Page": "LAMF.render(LAMF.T.pledge())",
 "18.1) Pledging of Mutual Fund OTP popup": "LAMF.render(LAMF.withModal(LAMF.T.pledge(), LAMF.T.pledgeOtpModal()))",
 "18.2) Pledging of Mutual Fund Successfully pledged": "LAMF.render(LAMF.withModal(LAMF.T.pledge(), LAMF.T.pledgedModal()))",
 "19) Agreement and E-Mandate Page": "LAMF.render(LAMF.T.agreement())",
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

items = "\n".join(f'<li><a href="{quote(n + ".html")}">{html.escape(n)}</a></li>' for n in PAGES)
INDEX = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LAMF – Apply for New Loan (Existing Customer)</title>
<link rel="stylesheet" href="assets/lamf.css">
</head>
<body class="page-screens"><a class="logo" href="index.html" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a><h1>LAMF – Apply for New Loan (Existing Customer) – Screens</h1><p>{len(PAGES)} screens, in screenshot order. Use the ☰ bar (bottom-right) or ← / → keys on any screen to move between them.</p><ol>{items}</ol>
</body>
</html>
"""
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(INDEX)
print(len(PAGES), "pages + index.html written")
