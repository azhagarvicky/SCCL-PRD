"""New customer mail templates (DISC-304) from the owner's LAMF_Customer_Communications_Additional_Scenarios_1_1.xlsx.

Kept apart from the Customer Communications table on purpose: build_pages.py writes one HTML mail per entry into
new-mails/NN_<name>.html and a list page new-mails.html (opened from a temporary CTA on communications.html), so the
owner can view and download them. The reviewer's struck-out text in the sheet is left out and the red notes are applied.
Placeholders follow the existing mails/*.html: {{CUSTOMER_NAME}}, {{LOAN_ID}} …
"""
import html as _h

FONT = "font-family:Arial,Helvetica,sans-serif;"

# Block helpers – each returns one <tr> of the 600px mail card (same look as mails/*.html)
def para(text, pad="16px 48px 0 48px", align="justify", color="#333333"):
    return (f'<tr><td class="px" style="padding:{pad};"><p style="margin:0;{FONT}font-size:15px;line-height:24px;color:{color};'
            f'text-align:{align};">{text}</p></td></tr>')

def badge(text, kind):
    bg, border, color = {"ok": ("#F0FFF6", "#2d9652", "#1a6633"), "warn": ("#FFF5F5", "#c0392b", "#8c1d18")}[kind]
    icon = "&#10003;" if kind == "ok" else "&#9888;"
    return (f'<tr><td class="px" align="center" style="padding:22px 48px 0 48px;"><table role="presentation" cellpadding="0" cellspacing="0" '
            f'border="0" width="100%" style="background-color:{bg};border:1px solid {border};border-radius:8px;"><tr><td align="center" '
            f'style="padding:18px 24px;"><p style="margin:0;{FONT}font-size:16px;line-height:24px;color:{color};font-weight:bold;">'
            f'{icon}&nbsp; {text}</p></td></tr></table></td></tr>')

def details(title, rows, right=""):   # right: optional heading over the value column, e.g. "Amount" (DISC-316)
    body = "".join(f'<tr><td style="padding:9px 16px;{FONT}font-size:14px;line-height:20px;color:#555555;border-top:1px solid #ececec;'
                   f'width:45%;">{k}</td><td style="padding:9px 16px;{FONT}font-size:14px;line-height:20px;color:#1a1a1a;font-weight:bold;'
                   f'border-top:1px solid #ececec;">{v}</td></tr>' for k, v in rows)
    return (f'<tr><td class="px" style="padding:22px 48px 0 48px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" '
            f'width="100%" style="background-color:#FAFAF8;border:1px solid #e2e2e2;border-radius:8px;"><tr><td colspan="{1 if right else 2}" '
            f'style="padding:12px 16px;{FONT}font-size:13px;line-height:18px;font-weight:bold;letter-spacing:.5px;color:#1a1a1a;'
            f'text-transform:uppercase;">{title}</td>'
            + (f'<td style="padding:12px 16px;{FONT}font-size:13px;line-height:18px;font-weight:bold;letter-spacing:.5px;color:#1a1a1a;'
               f'text-transform:uppercase;">{right}</td>' if right else '')
            + f'</tr>{body}</table></td></tr>')

def bullets(title, items):
    li = "".join(f'<tr><td valign="top" style="padding:4px 10px 4px 0;{FONT}font-size:15px;line-height:24px;color:#333333;">&bull;</td>'
                 f'<td style="padding:4px 0;{FONT}font-size:15px;line-height:24px;color:#333333;text-align:justify;">{t}</td></tr>' for t in items)
    return (f'<tr><td class="px" style="padding:22px 48px 0 48px;"><p style="margin:0 0 6px 0;{FONT}font-size:15px;line-height:24px;'
            f'color:#1a1a1a;font-weight:bold;">{title}</p><table role="presentation" cellpadding="0" cellspacing="0" border="0">{li}</table></td></tr>')

def button(label, link):
    return (f'<tr><td class="px" align="center" style="padding:24px 48px 8px 48px;"><table role="presentation" cellpadding="0" cellspacing="0" '
            f'border="0"><tr><td align="center" bgcolor="#1a1a1a" style="border-radius:6px;"><a href="{link}" target="_blank" '
            f'style="display:inline-block;{FONT}font-size:15px;line-height:20px;font-weight:bold;color:#FFC20E;text-decoration:none;'
            f'padding:14px 34px;border-radius:6px;">{label}</a></td></tr></table></td></tr>')

def link(url):
    return f'<a href="{url}" style="color:#0b5ed7;text-decoration:underline;">{url}</a>'

def charges_table(title):   # DRAFT rejection mails (DISC-350): one row per charge incurred, then the total
    th = lambda t, al="right": (f'<td style="padding:10px 12px;{FONT}font-size:12px;line-height:16px;font-weight:bold;color:#1a1a1a;'
                                f'text-align:{al};text-transform:uppercase;">{t}</td>')
    td = lambda t, al="right", b=False: (f'<td style="padding:9px 12px;{FONT}font-size:14px;line-height:20px;color:{"#1a1a1a" if b else "#555555"};'
                                         f'{"font-weight:bold;" if b else ""}text-align:{al};border-top:1px solid #ececec;{"" if al == "left" else "white-space:nowrap;"}">{t}</td>')
    row = lambda c, b=False: "<tr>" + td(c[0], "left", b) + "".join(td(x, b=b) for x in c[1:]) + "</tr>"
    return (f'<tr><td class="px" style="padding:22px 48px 0 48px;"><p style="margin:0 0 8px 0;{FONT}font-size:13px;line-height:18px;'
            f'font-weight:bold;letter-spacing:.5px;color:#1a1a1a;text-transform:uppercase;">{title}</p>'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#FAFAF8;'
            'border:1px solid #e2e2e2;border-radius:8px;"><tr>' + th("Charges", "left") + th("Amount") + th("Waived off") + th("Payable") + "</tr>"
            + "<!-- one row per charge incurred -->"
            + row(["{{CHARGE_NAME}}", "&#8377;{{CHARGE_AMOUNT}}", "&#8377;{{WAIVED_AMOUNT}}", "&#8377;{{PAYABLE_AMOUNT}}"])
            + row(["Total", "&#8377;{{TOTAL_CHARGES}}", "&#8377;{{TOTAL_WAIVED}}", "&#8377;{{TOTAL_PAYABLE}}"], True)
            + "</table></td></tr>")

SUPPORT = para('Should you have any questions, require clarification, or assistance, please feel free to reach out to our customer support at '
               '<a href="mailto:lassupport@shriramcredit.in" style="color:#0b5ed7;text-decoration:underline;">lassupport@shriramcredit.in</a>. '
               'Our team will be happy to assist you.', pad="22px 48px 0 48px")
LIEN_PROCESS = details("Lien Removal Process", [
    ("Status", "{STATUS}"), ("Timeline", "2&ndash;3 working days"),
    ("Confirmation", "You will receive a separate notification from CAMS/KFintech once your units are fully unlocked.")])

NEW_MAILS = [   # (file name, title band, subject, preheader, placeholders, blocks, owner note)
    ("01_Lien_Removal_Initiated", "Lien Removal Initiated",
     "Lien Removal Initiated for Your Mutual Fund Units",
     "We have initiated the removal of the lien on your Mutual Fund units.",
     ["{{CUSTOMER_NAME}}"],
     [badge("Lien Removal Initiated", "ok"),
      para("We have initiated the removal of the lien on your Mutual Fund units pledged with Shriram Credit Company Limited (SCCL).", pad="22px 48px 0 48px"),
      LIEN_PROCESS.replace("{STATUS}", "Lien removal initiated"),
      bullets("Important Information", ["Until the lien is removed, your units cannot be redeemed or transferred.",
                                        "If the lien is not removed within the stated timeline, please contact us for assistance."]),
      SUPPORT],
     "Reviewer note in the sheet: this stage is not required – it will go as a loan closure communication."),
    ("02_Lien_Removal_Successful", "Lien Removal Successful",
     "Lien Removed: Your Mutual Fund Units Are Unpledged",
     "The lien on your Mutual Fund units has been successfully removed.",
     ["{{CUSTOMER_NAME}}"],
     [para("Thank you for being a valued customer.", pad="18px 48px 0 48px"),
      para("We are pleased to confirm that the lien on your Mutual Fund units pledged with Shriram Credit Company Limited (SCCL) has been successfully removed."),
      badge("Lien Successfully Removed", "ok"),
      para("Your units are now fully accessible to you.", pad="22px 48px 0 48px"),
      para("Need funds in the future? You can apply for a Loan Against Mutual Fund again anytime at: " + link("https://lamf.shriramcredit.in/")),
      SUPPORT,
      para("Thank you for choosing Shriram Credit. We look forward to serving you again.")],
     ""),
    ("03_Application_Rejected_Pay_Charges", "Application Rejected &ndash; Payment of Charges",     # processing fee only; the all-charges version removed (DISC-319)
     "Action Required: Application Rejected – Pay Charges {{LOAN_ID}}",
     "Your Loan Against Mutual Fund application could not be approved. Please pay the applicable charges.",
     ["{{CUSTOMER_NAME}}", "{{LOAN_ID}}", "{{PROCESSING_FEE}}", "{{PAYMENT_LINK}}"],
     [badge("Your Loan Against Mutual Fund application could not be approved", "warn"),
      para("After review, we regret to inform you that your Loan Against Mutual Fund application (<b>{{LOAN_ID}}</b>) with Shriram Credit "
           "Company Limited (SCCL) could not be taken forward.", pad="22px 48px 0 48px"),
      para("As per the applicable terms, the following charges are payable:"),
      details("Charges Payable", [("Processing Fee*", "&#8377;{{PROCESSING_FEE}} + GST")], right="Amount"),   # no total row (DISC-316); fee is all-inclusive (DISC-317)
      f'<tr><td class="px" style="padding:8px 48px 0 48px;"><p style="margin:0;{FONT}font-size:12px;line-height:18px;color:#777777;">'
      '*One-time Processing Fee, inclusive of Lien Marking, Lien Removal and Stamp Duty and GST</p></td></tr>',
      para("Please use the below link to make the payment.", pad="22px 48px 0 48px"),
      para(link("https://lamf.shriramcredit.in/user/loans/"), align="center"),
      para("or", pad="12px 48px 0 48px", align="center", color="#555555"),
      button("Pay Charges &rarr;", "{{PAYMENT_LINK}}"),
      para("Your pledged Mutual Fund units will be released through the lien removal process after the successful receipt of charges.", pad="22px 48px 0 48px"),
      SUPPORT],
     ""),
    ("04_Application_Rejected", "Application Rejected",
     "Update: Your Shriram Credit LAMF Application Is Rejected {{LOAN_ID}}",
     "Your Loan Against Mutual Fund application could not be approved.",
     ["{{CUSTOMER_NAME}}", "{{LOAN_ID}}"],
     [badge("Your Loan Against Mutual Fund application could not be approved", "warn"),
      para("After review, we regret to inform you that your Loan Against Mutual Fund application (<b>{{LOAN_ID}}</b>) with Shriram Credit "
           "Company Limited (SCCL) could not be taken forward.", pad="22px 48px 0 48px"),
      LIEN_PROCESS.replace("{STATUS}", "Lien release process initiated"),
      SUPPORT],
     "Reviewer question in the sheet: please explain the rationale of having this option (rejection without charges)."),
    ("05_Withdrawal_Request_Rejected", "Withdrawal Request Rejected",
     "Update: Your Withdrawal Request Was Rejected {{LOAN_ID}}",
     "Your withdrawal request could not be processed.",
     ["{{CUSTOMER_NAME}}", "{{LOAN_ID}}", "{{WITHDRAWAL_AMOUNT}}"],
     [badge("Your withdrawal request could not be processed", "warn"),
      para("We regret to inform you that your withdrawal request has been rejected.", pad="22px 48px 0 48px"),
      details("Withdrawal Details", [("Loan Account ID", "{{LOAN_ID}}"), ("Withdrawal Amount", "&#8377;{{WITHDRAWAL_AMOUNT}}"), ("Status", "Rejected")]),
      para("You may contact our support team for placing a fresh withdrawal request.", pad="22px 48px 0 48px"),
      SUPPORT],
     ""),
    # DISC-350 – a pledged DRAFT LAN rejected by OPS (Waiver BRD): with the payment link when Payable Charges ≠ 0 (partial / no
    # waive-off), without it when Payable Charges = 0 (full waive-off). SMS – the same as the rejection SMS of rows 14 / 15.
    ("06_Draft_Application_Rejected_Pay_Charges", "Application Rejected &ndash; Payment of Charges",
     "Action Required: Application Rejected – Pay Charges {{LOAN_ID}}",
     "Your Loan Against Mutual Fund application has been rejected. Please pay the charges to unpledge your Mutual Fund units.",
     ["{{CUSTOMER_NAME}}", "{{LOAN_ID}}", "{{CHARGE_NAME}}", "{{CHARGE_AMOUNT}}", "{{WAIVED_AMOUNT}}", "{{PAYABLE_AMOUNT}}",
      "{{TOTAL_CHARGES}}", "{{TOTAL_WAIVED}}", "{{TOTAL_PAYABLE}}", "{{PAYMENT_LINK}}"],
     [badge("Your Loan Against Mutual Fund application has been rejected", "warn"),
      para("We regret to inform you that your Loan Against Mutual Fund application (<b>{{LOAN_ID}}</b>) with Shriram Credit "
           "Company Limited (SCCL) has been rejected.", pad="22px 48px 0 48px"),
      para("To unpledge your Mutual Fund units, please pay the charges below:"),
      charges_table("Charges Payable"),
      para("Please use the below link to make the payment.", pad="22px 48px 0 48px"),
      para(link("https://lamf.shriramcredit.in/user/loans/"), align="center"),
      para("or", pad="12px 48px 0 48px", align="center", color="#555555"),
      button("Pay Charges &rarr;", "{{PAYMENT_LINK}}"),
      para("Your pledged Mutual Fund units will be released through the lien removal process after the successful receipt of charges.", pad="22px 48px 0 48px"),
      SUPPORT],
     "DRAFT LAN rejected with Payable Charges not equal to zero (partial / no waive-off) – Waiver BRD."),
    ("07_Draft_Application_Rejected", "Application Rejected",
     "Update: Your Shriram Credit LAMF Application Is Rejected {{LOAN_ID}}",
     "Your Loan Against Mutual Fund application has been rejected. We will initiate to unpledge your Mutual Fund units shortly.",
     ["{{CUSTOMER_NAME}}", "{{LOAN_ID}}"],
     [badge("Your Loan Against Mutual Fund application has been rejected", "warn"),
      para("We regret to inform you that your Loan Against Mutual Fund application (<b>{{LOAN_ID}}</b>) with Shriram Credit "
           "Company Limited (SCCL) has been rejected.", pad="22px 48px 0 48px"),
      para("All the applicable charges have been waived off, so there is nothing for you to pay. We will initiate to unpledge your "
           "Mutual Fund units shortly."),
      LIEN_PROCESS.replace("{STATUS}", "Lien release process initiated"),
      SUPPORT],
     "DRAFT LAN rejected with Payable Charges equal to zero (full waive-off) – Waiver BRD."),
]


def mail_html(m):
    fname, title, subject, pre, ph, blocks, _ = m
    return f"""<!DOCTYPE html>
<!--
  ============================================================
  SHRIRAM CREDIT LAMF - {fname.split('_', 1)[0]}. {_h.unescape(title).upper()}
  ============================================================
  Placeholders: {', '.join(ph)}
  Subject: {subject}
  LOGO: Host shriram-credit-logo.png on your CDN and replace the src.
  ============================================================
-->
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{_h.escape(subject)}</title>
<style type="text/css">
  body,table,td,p,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}}
  table,td{{mso-table-lspace:0pt;mso-table-rspace:0pt;}}
  img{{border:0;height:auto;line-height:100%;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;}}
  body{{margin:0;padding:0;width:100%!important;height:100%!important;}}
  @media only screen and (max-width:620px){{
    .email-container{{width:100%!important;}}
    .px{{padding-left:24px!important;padding-right:24px!important;}}
  }}
</style>
</head>
<body style="margin:0;padding:0;background-color:#efeeec;">
<span style="display:none!important;visibility:hidden;mso-hide:all;font-size:1px;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;color:transparent;">{_h.escape(pre)}</span>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#efeeec;">
  <tr>
    <td align="center" style="padding:32px 12px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="email-container" style="width:600px;max-width:600px;background-color:#ffffff;border-radius:8px;overflow:hidden;">
        <tr><td align="center" style="padding:28px 40px 20px 40px;background-color:#ffffff;"><img src="../assets/img/shriram-logo.png" width="200" alt="Shriram Credit" style="display:block;width:200px;height:auto;"></td></tr>
        <tr><td style="background-color:#FFC20E;height:5px;line-height:5px;font-size:5px;">&nbsp;</td></tr>
        <tr><td align="center" style="background-color:#1a1a1a;padding:22px 40px;"><p style="margin:0;{FONT}font-size:20px;line-height:26px;font-weight:bold;color:#FFC20E;">{title}</p></td></tr>
        <tr><td class="px" style="padding:36px 48px 0 48px;"><p style="margin:0;{FONT}font-size:16px;line-height:24px;color:#1a1a1a;font-weight:bold;">Dear {{{{CUSTOMER_NAME}}}},</p></td></tr>
        {chr(10).join('        ' + b for b in blocks).strip()}
        <tr><td class="px" style="padding:28px 48px 36px 48px;"><p style="margin:0;{FONT}font-size:15px;line-height:24px;color:#333333;">Warm regards,<br><span style="font-weight:bold;color:#1a1a1a;">Team Shriram Credit</span></p></td></tr>
        <tr><td class="px" style="background-color:#FFC20E;padding:18px 48px;"><p style="margin:0;{FONT}font-size:12px;line-height:18px;color:#1a1a1a;"><span style="font-weight:bold;">Disclaimer:</span> This is an automated reminder. Please do not reply to this message, as the mailbox is not monitored and you will not receive a response. Loan against Securities is only for personal use. The loan amount cannot be used for speculative activities, capital market-related purposes, or anti-social purposes.</p></td></tr>
        <tr><td align="center" style="background-color:#1a1a1a;padding:14px 40px;"><p style="margin:0;{FONT}font-size:12px;line-height:18px;color:#cccccc;">&copy; 2026 Shriram Credit Company Limited. All rights reserved.</p></td></tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""


def list_body(logo, back):
    rows = "".join(
        f'<tr><td class="c">{i}</td><td>{title}</td><td>{_h.escape(subject)}</td><td>{_h.escape(note) or "–"}</td>'
        f'<td class="nm-cta"><a class="nm-view" href="new-mails/{fname}.html" target="_blank" rel="noopener">View mail →</a>'
        f'<a class="nm-dl" href="new-mails/{fname}.html" download="{fname}.html">Download</a></td></tr>'
        for fname, title, subject, _, _, _, note in NEW_MAILS for i in [fname.split('_')[0].lstrip('0')])   # 3, 3b, 4 … from the file name
    return (logo + f'<p class="brd-back"><a href="{back}">← Customer Communications</a></p>'
            '<h1>New Customer Mails</h1>'
            f'<p>{len(NEW_MAILS)} mail templates from the additional scenarios sheet (LAMF_Customer_Communications_Additional_Scenarios). '
            'Kept separate from the Customer Communications table. View opens the mail; Download saves the HTML file.</p>'
            '<table class="brd-table nm-table"><thead><tr><th>#</th><th>Mail</th><th>Subject line</th><th>Note</th><th>Mail</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')
