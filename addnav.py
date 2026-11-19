#!/usr/bin/env python3
import re, sys

CSS = """
  /* site nav */
  header.site { position:absolute; top:0; left:0; right:0; display:flex; align-items:center; justify-content:space-between; padding:1.1rem 1.5rem; z-index:10; }
  header.site .brand { color:var(--text); text-decoration:none; font-weight:700; letter-spacing:0.08em; font-size:1.05rem; }
  header.site .brand:hover { color:var(--accent); }
  .nav-toggle { display:none; }
  .nav-btn { display:none; width:42px; height:38px; cursor:pointer; position:relative; }
  .nav-btn span { position:absolute; top:18px; left:9px; right:9px; height:2px; background:var(--text); transition:transform .2s ease, background .2s ease; }
  .nav-btn span::before, .nav-btn span::after { content:""; position:absolute; left:0; right:0; height:2px; background:var(--text); transition:transform .2s ease; }
  .nav-btn span::before { top:-8px; }
  .nav-btn span::after { top:8px; }
  header.site nav { display:flex; gap:1.4rem; }
  header.site nav a { color:var(--muted); text-decoration:none; font-size:0.95rem; }
  header.site nav a:hover { color:var(--text); }
  header.site nav a.current { color:var(--accent); }
  @media (max-width:720px) {
    .nav-btn { display:block; }
    header.site nav { display:none; position:absolute; top:100%; left:0; right:0; flex-direction:column; gap:0; background:var(--bg); border-bottom:1px solid #1f232d; }
    .nav-toggle:checked ~ nav { display:flex; }
    header.site nav a { padding:0.8rem 1.5rem; }
    header.site nav a:hover { background:#161a22; color:var(--text); }
    .nav-toggle:checked ~ .nav-btn span { background:transparent; }
    .nav-toggle:checked ~ .nav-btn span::before { transform:translateY(8px) rotate(45deg); }
    .nav-toggle:checked ~ .nav-btn span::after { transform:translateY(-8px) rotate(-45deg); }
  }
"""

LINKS = [("Home", "/"), ("Writing", "/blog/"), ("About", "/about.html"), ("Contact", "/contact.html")]

def build_header(current):
    items = []
    for label, href in LINKS:
        cls = ' class="current"' if label == current else ""
        items.append('    <a href="%s"%s>%s</a>' % (href, cls, label))
    return ('<header class="site">\n'
            '  <a class="brand" href="/">CPWS</a>\n'
            '  <input type="checkbox" id="navtog" class="nav-toggle">\n'
            '  <label class="nav-btn" for="navtog" aria-label="Menu"><span></span></label>\n'
            '  <nav>\n' + "\n".join(items) + '\n  </nav>\n'
            '</header>')

path, current = sys.argv[1], sys.argv[2]
s = open(path).read()
assert '</style>' in s and '<body>' in s, path + ": missing anchors"
assert 'header class="site"' not in s, path + ": nav already added"
s = re.sub(r'[ \t]*<nav>.*?</nav>\r?\n?', '', s, count=1, flags=re.S)
s = s.replace('</style>', CSS + '</style>')
s = s.replace('<body>', '<body>\n' + build_header(current))
open(path, 'w').write(s)
print(path + ": NAV-ADDED")
