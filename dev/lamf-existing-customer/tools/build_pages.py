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
