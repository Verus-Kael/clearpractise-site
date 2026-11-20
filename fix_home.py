#!/usr/bin/env python3
import re, shutil

PATH = "/home/verus/cpws-site/index.html"
s = open(PATH).read()
changes = []

shutil.copy(PATH, PATH + ".bak")
changes.append("backup written")

OLD = "Nothing online is unhackable. Attack surface, however, is a design choice."
NEW = "Nothing online is bulletproof. But every script, tracker and plug-in you don't load is one less thing that can hurt you."
if OLD in s:
    s = s.replace(OLD, NEW, 1); changes.append("hero swapped")
elif NEW in s:
    changes.append("hero already done")
else:
    print("ERROR: hero line not found - nothing written"); exit(1)

OFFER = '<p class="offer">We build websites and we host them - properly secured, minimal dependencies. And if you\'ve already got a site somewhere else, we\'ll move it here for free as part of our onboarding offer.</p>'
BADGE = '<span class="soon">Now taking early enquiries</span>'
if OFFER in s:
    changes.append("offer already done")
elif BADGE in s:
    s = s.replace(BADGE, BADGE + "\n  " + OFFER, 1); changes.append("offer inserted")
else:
    print("ERROR: badge not found - nothing written"); exit(1)

NEW_FOOTER = '''<footer>
  <div class="links">
    <p><a href="PLACEHOLDER_BF" rel="sponsored nofollow">Proton Unlimited - Black Friday Deals</a> (affiliate)</p>
    <p><a href="https://go.getproton.me/aff_c?offer_id=50&amp;aff_id=17205&amp;url_id=1484" rel="sponsored nofollow">Proton Workspace for Business</a> (affiliate)</p>
    <p><a href="https://go.getproton.me/aff_c?offer_id=50&amp;aff_id=17205&amp;url_id=1126" rel="sponsored nofollow">Proton Mail Business - Free Trial</a> (affiliate)</p>
  </div>
  <nav>
    <a href="/blog/">Writing</a> |
    <a href="/about.html">About</a> |
    <a href="/contact.html">Contact</a> |
    <a href="/privacy-policy.html">Privacy</a>
  </nav>
  <p class="copyright">&copy; 2026 CPWS - Secure Web Stacks</p>
</footer>'''

m = re.search(r'<footer>.*?</footer>', s, re.S)
if not m:
    print("ERROR: no footer found - nothing written"); exit(1)
cur = m.group(0)
if "url_id=1126" in cur:
    changes.append("footer already done")
else:
    bf = re.search(r'href="(https://go\.getproton\.me/aff_c\?offer_id=26[^"]*)"', cur)
    if bf:
        NEW_FOOTER = NEW_FOOTER.replace("PLACEHOLDER_BF", bf.group(1))
        changes.append("footer replaced, BF link preserved")
    else:
        NEW_FOOTER = NEW_FOOTER.replace("PLACEHOLDER_BF", "https://go.getproton.me/aff_c?offer_id=26&amp;aff_id=17205&amp;url_id=1198")
        changes.append("footer replaced, default BF link used")
    s = s[:m.start()] + NEW_FOOTER + s[m.end():]

CSS = '''  /* footer + offer */
  .offer { margin-top:1.4rem; font-size:1rem; }
  .links { margin-top:1.5rem; font-size:0.85rem; }
  .links p { margin:0.3rem 0; }
  .links a { color:var(--muted); text-decoration:underline; text-underline-offset:3px; }
  .links a:hover { color:var(--text); }
  footer nav { margin-top:1rem; font-size:0.85rem; }
  footer nav a { color:var(--muted); text-decoration:none; margin:0 0.4rem; }
  footer nav a:hover { color:var(--accent); }
  footer .copyright { margin-top:0.8rem; font-size:0.75rem; opacity:0.6; }
'''
if ".offer { margin-top" not in s:
    s = s.replace("</style>", CSS + "</style>")
    changes.append("CSS added")

open(PATH, "w").write(s)
print(" | ".join(changes))
print("ALL-DONE")
