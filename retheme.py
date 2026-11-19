#!/usr/bin/env python3
import re, sys

DARK_CSS = """<style>
  :root { --bg:#0d0f14; --text:#e8e9ec; --muted:#8a8f9a; --accent:#6d4aff; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; line-height:1.6; }
  .container { max-width:42rem; margin:0 auto; padding:5rem 2rem 3rem; }
  .article-content h1 { font-size:1.9rem; margin-bottom:0.5rem; letter-spacing:0.02em; }
  .article-content h2 { font-size:1.25rem; margin:2.25rem 0 0.75rem; color:var(--accent); }
  .article-content h3 { font-size:1.05rem; margin:1.75rem 0 0.5rem; }
  .article-content p { margin-bottom:1rem; }
  .article-content ul, .article-content ol { padding-left:1.4rem; margin-bottom:1rem; }
  .article-content li { margin-bottom:0.5rem; }
  .article-content a { color:var(--accent); text-decoration:none; }
  .article-content a:hover { text-decoration:underline; text-underline-offset:3px; }
  .meta { color:var(--muted); font-size:0.9rem; margin-bottom:2rem; }
  .warning-box { border-left:3px solid #c0392b; background:#161a22; padding:1rem 1.25rem; margin:1.25rem 0; border-radius:0 6px 6px 0; }
  .tip-box { border-left:3px solid var(--accent); background:#161a22; padding:1rem 1.25rem; margin:1.25rem 0; border-radius:0 6px 6px 0; }
  .checklist-box { border:1px solid #1f232d; padding:1.25rem 1.5rem; margin:1.25rem 0; border-radius:8px; }
  .affiliate-box { border:1px solid #1f232d; padding:1.25rem 1.5rem; margin:2rem 0; border-radius:8px; }
  .affiliate-link { display:inline-block; margin-top:0.5rem; padding:0.6rem 1.2rem; border:1px solid var(--accent); border-radius:6px; color:var(--accent); font-weight:600; text-decoration:none; }
  .affiliate-link:hover { background:#161a22; }
  .cta-button { display:inline-block; width:max-content; margin-top:0.75rem; padding:0.7rem 1.4rem; border:1px solid var(--accent); color:var(--accent); border-radius:6px; text-decoration:none; font-weight:600; }
  .cta-button:hover { background:#161a22; }
  .founder-note { border:1px dashed #1f232d; padding:1rem 1.25rem; margin:1.25rem 0; border-radius:8px; font-style:italic; color:var(--muted); }
  blockquote { border-left:3px solid var(--accent); padding-left:1rem; margin:1.25rem 0; color:var(--muted); font-style:italic; }
  code { background:#161a22; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.9em; }
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
  footer { max-width:42rem; margin:0 auto; padding:1.5rem 2rem; border-top:1px solid #1f232d; font-size:0.85rem; color:var(--muted); }
  footer nav { margin-bottom:0.5rem; }
  footer nav a { color:var(--muted); margin-right:1rem; text-decoration:underline; text-underline-offset:3px; }
  footer nav a:hover { color:var(--text); }
</style>"""

HEADER = """<header class="site">
  <a class="brand" href="/">CPWS</a>
  <input type="checkbox" id="navtog" class="nav-toggle">
  <label class="nav-btn" for="navtog" aria-label="Menu"><span></span></label>
  <nav>
    <a href="/">Home</a>
    <a href="/blog/" class="current">Writing</a>
    <a href="/about.html">About</a>
    <a href="/contact.html">Contact</a>
    <a href="/privacy-policy.html">Privacy</a>
  </nav>
</header>"""

FOOTER = """<footer>
  <nav><a href="/">Home</a><a href="/blog/">Writing</a><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/privacy-policy.html">Privacy</a><a href="/terms-of-service.html">Terms</a></nav>
  <p>&copy; 2026 CPWS - Secure Web Stacks</p>
</footer>"""

path = sys.argv[1]
s = open(path).read()
assert 'header class="site"' not in s, path + ": already rethemed"
s2 = re.sub(r'<style>.*?</style>', lambda m: DARK_CSS, s, count=1, flags=re.S)
assert s2 != s, path + ": style block not found"
s2 = re.sub(r'\s*<nav>.*?</nav>', '\n' + HEADER, s2, count=1, flags=re.S)
s2 = re.sub(r'<footer>.*?</footer>', FOOTER, s2, count=1, flags=re.S)
open(path, 'w').write(s2)
print(path + ": RETHEMED")
