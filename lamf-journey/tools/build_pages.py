# Generates one HTML file per screenshot. Content comes from assets/lamf.js templates,
# so shared components stay in one place. Re-run after adding a screen: python3 tools/build_pages.py
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR = "LAMF.T.curated()"
CUR75 = "LAMF.T.curated({banner:'Avail a loan of up to 75% of your eligible Mutual Fund portfolio'})"
SEL = "LAMF.T.selection(LAMF.SEL_DEFAULT)"
PAGES = {
 "01) LAMF Landing Page": "LAMF.render(LAMF.T.landing())",
 "02) Enter MF linked Mobile Number": "LAMF.render(LAMF.withModal(LAMF.T.landing(), LAMF.T.mobileModal()))",
 "03) Enter OTP for MF linked Mobile Number Verification": "LAMF.render(LAMF.withModal(LAMF.T.landing(), LAMF.T.otpModal()))",
 "04) Enter PAN Details": "LAMF.render(LAMF.T.pan())",
 "05) LOS to MF Central Redirection consent page": "LAMF.render(LAMF.T.consent())",
 "06) LOS to MF Central Redirection loading page": "LAMF.render(LAMF.withModal(LAMF.T.consent(), LAMF.T.mfcModal()))",
 "07) MF Central Mock Page": "LAMF.render(LAMF.T.mfMock())",
 "08) MF Central to LOS Redirecting Page": "LAMF.render(LAMF.T.redirecting())",
 "09) MF Central to LOS Fetching Mutual Fund Portfolio Page": "LAMF.render(LAMF.withModal(LAMF.T.consent(), LAMF.loader('Fetching your mutual fund portfolio..', 1)))",
 "10) MF Central to LOS Analysing Mutual Fund Portfolio Page": f"LAMF.render(LAMF.withModal({CUR}, LAMF.loader('Analyzing your mutual fund portfolio..', 2)))",
 "11) MF Central to LOS Generating Loan Page": f"LAMF.render(LAMF.withModal({CUR}, LAMF.loader('Generating best loan offers for you', 3)))",
 "12) Curated Offers Page": f"LAMF.render({CUR})",
 "12.1.1) How is it calculated_All Portfolio": "LAMF.render(LAMF.T.calc('all'))",
 "12.1.2) How is it calculated_Eligible Portfolio": "LAMF.render(LAMF.T.calc('eligible'))",
 "12.1.3) How is it calculated_Non Eligible Portfolio": "LAMF.render(LAMF.T.calc('ne'))",
 "12.2) Curated offers page for dorpoff view": "LAMF.render(LAMF.T.curated({dropoff:true, banner:'Avail a loan of up to 75% of your eligible Mutual Fund portfolio'}))",
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
from urllib.parse import quote
links = "\n".join(f'<li><a href="{quote(n + ".html")}">{html.escape(n)}</a></li>' for n in PAGES)
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>LAMF Online Journey</title>
<link rel="stylesheet" href="assets/lamf.css">
<style>body{{padding:40px 76px}} h1{{font-size:28px;margin:24px 0 6px}} p{{color:#555;margin-bottom:20px}} ol{{list-style:none;columns:2;column-gap:40px}} li{{break-inside:avoid;border:1px solid var(--line);border-radius:8px;margin-bottom:10px}} li a{{display:block;padding:12px 16px;font-weight:500}} li a:hover{{background:var(--yellow-soft)}}</style>
</head><body><img src="assets/img/shriram-logo.png" style="height:40px"><h1>LAMF Online Journey – Screens</h1>
<p><a href="SCCL_LAMF_LOS_PRD.html" style="display:inline-block;background:var(--yellow);padding:8px 14px;border-radius:6px;font-weight:700;margin-bottom:14px">Open the PRD document →</a></p>
<p>{len(PAGES)} screens, in screenshot order. Use the ☰ bar (bottom-right) or ← / → keys on any screen to move between them.</p>
<ol>{links}</ol></body></html>""")
print(len(PAGES), "pages written")

# ---- cloud copy: one page, hash routed (artifact sandboxes cannot navigate between files)
import json as _json
from urllib.parse import quote as _q

screens_js = ["/* Generated by tools/build_pages.py – one render function per screen. */",
              "window.SCREEN_RENDER = {"]
for name, code in PAGES.items():
    screens_js.append(f"  {_json.dumps(name)}: function () {{ {code}; }},")
screens_js.append("};")
index_links = "".join(f'<li><a href="#{_q(n)}">{html.escape(n)}</a></li>' for n in PAGES)
screens_js.append(
    "window.INDEX_HTML = " + _json.dumps(
        f'<img src="assets/img/shriram-logo.png" style="height:40px"><h1>LAMF Online Journey – Screens</h1>'
        f'<p><a class="prd-open" href="#PRD">Open the PRD document →</a></p>'
        f'<p>{len(PAGES)} screens, in screenshot order. Use the ☰ bar (bottom-right) or ← / → keys on any screen to move between them.</p>'
        f'<ol>{index_links}</ol>') + ";")
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
  body.screen-index { padding: 40px 60px; }
  body.screen-index h1 { font-size: 28px; margin: 22px 0 8px; }
  body.screen-index p { color: #555; margin-bottom: 18px; }
  body.screen-index ol { list-style: none; columns: 2; column-gap: 40px; }
  body.screen-index li { break-inside: avoid; border: 1px solid var(--line); border-radius: 8px; margin-bottom: 10px; }
  body.screen-index li a { display: block; padding: 12px 16px; font-weight: 500; }
  body.screen-index li a:hover { background: var(--yellow-soft); }
  .prd-open { display: inline-block; background: var(--yellow); padding: 8px 14px; border-radius: 6px; font-weight: 700; }
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
    if (name === 'PRD' && window.PRD_HTML) { LAMF.renderPRD(window.PRD_HTML); return; }
    var fn = window.SCREEN_RENDER[name];
    if (fn) { fn(); return; }
    LAMF.render(window.INDEX_HTML, { bodyClass: 'screen-index' });
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
