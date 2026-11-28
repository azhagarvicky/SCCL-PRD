"""DISC-528: adds the module-wise access check (assets/access.js) to every module page of the site.
Run at the end of build_pages.py and build_prd.py (it can also be run on its own). Idempotent – an existing tag is replaced.
Module of each page:
  prd      SCCL_LAMF_LOS_PRD.html
  brd      brd.html, brd-*.html
  journey  the numbered LOS screen pages, screens.html, charges-payment*.html, charges-receipt*.html
  comms    communications.html, internal-communications.html, internal/*.html, new-mails.html, new-mails/*.html, mails/*.html
  calc     calculator.html
  lms      lms-screens.html, lms.html, lms-app/*.html
  (open)   index.html (home), access.html, cloud.html (checks each part itself), admin.html
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = 1
TAG = re.compile(r'<script src="(?:\.\./)?assets/access\.js[^"]*" data-m="[a-z]+"></script>\n?')


def module_of(rel):
    name = os.path.basename(rel)
    d = os.path.dirname(rel)
    if d in ('internal', 'new-mails', 'mails'):
        return 'comms'
    if d == 'lms-app':
        return 'lms'
    if d:
        return None
    if name == 'SCCL_LAMF_LOS_PRD.html':
        return 'prd'
    if name == 'brd.html' or name.startswith('brd-'):
        return 'brd'
    if name in ('communications.html', 'internal-communications.html', 'new-mails.html'):
        return 'comms'
    if name == 'calculator.html':
        return 'calc'
    if name in ('lms-screens.html', 'lms.html'):
        return 'lms'
    if name == 'screens.html' or name.startswith('charges-payment') or name.startswith('charges-receipt') or re.match(r'^\d+(\.\d+)*\) ', name):
        return 'journey'
    return None


def apply():
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        rel_dir = os.path.relpath(dp, ROOT)
        if rel_dir.startswith(('tools', 'assets', 'exports', '.')) and rel_dir != '.':
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            rel = f if rel_dir == '.' else os.path.join(rel_dir, f)
            m = module_of(rel)
            p = os.path.join(dp, f)
            s = open(p, encoding='utf-8').read()
            t = TAG.sub('', s)
            if m:
                pre = '../' if os.path.dirname(rel) else ''
                tag = '<script src="%sassets/access.js?v=%d" data-m="%s"></script>\n' % (pre, VER, m)
                t = re.sub(r'(<head[^>]*>\n?)', lambda x: x.group(1) + tag, t, count=1)
            if t != s:
                open(p, 'w', encoding='utf-8').write(t)
                n += 1
    print('access check: %d page(s) updated' % n)


if __name__ == '__main__':
    apply()
