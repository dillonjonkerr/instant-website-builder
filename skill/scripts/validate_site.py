#!/usr/bin/env python3
"""Validate every .html page in a mockup site directory.

Checks, per page:
  - HTML tag nesting (mismatched / unclosed / stray tags)
  - every assets/... src or href actually exists on disk
  - every internal *.html link points at a real file
  - every #anchor link on the page has a matching id= target

Usage: python3 validate_site.py /path/to/site-dir
Exit code 0 = all pages pass, 1 = issues found.
"""
import os, re, sys
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr',
        'path','circle','rect','ellipse','line','polygon','polyline','stop','use'}

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack = []; s.errs = []
    def handle_starttag(s, t, a):
        if t not in VOID: s.stack.append((t, s.getpos()))
    def handle_endtag(s, t):
        if t in VOID: return
        if not s.stack:
            s.errs.append(f"stray </{t}> {s.getpos()}"); return
        if s.stack[-1][0] == t:
            s.stack.pop()
        else:
            s.errs.append(f"</{t}> {s.getpos()} but <{s.stack[-1][0]}> open from {s.stack[-1][1]}")

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.chdir(root)
    pages = [f for f in sorted(os.listdir('.')) if f.endswith('.html')]
    if not pages:
        print(f"no .html files in {root}"); return 1
    allok = True
    for f in pages:
        src = open(f, encoding='utf-8').read()
        p = P(); p.feed(src)
        missing = [a for a in set(re.findall(r'(?:src|href)="(assets/[^"]+)"', src))
                   if not os.path.exists(a)]
        links = {h.split('#')[0] for h in re.findall(r'href="([\w.-]+\.html(?:#[\w-]+)?)"', src)}
        badlinks = [l for l in links if l and not os.path.exists(l)]
        anchors = set(re.findall(r'\bid="([\w-]+)"', src))
        deadanch = set(re.findall(r'href="#([\w-]+)"', src)) - anchors
        ok = not (p.errs or p.stack or missing or badlinks or deadanch)
        allok &= ok
        print(("PASS " if ok else "FAIL ") + f)
        if p.errs:    print("   nesting:", p.errs[:3])
        if p.stack:   print("   unclosed:", [x[0] for x in p.stack][:5])
        if missing:   print("   missing assets:", missing)
        if badlinks:  print("   broken page links:", badlinks)
        if deadanch:  print("   dead #anchors:", sorted(deadanch))
    print("\nALL PAGES OK" if allok else "\nISSUES FOUND — fix before delivering")
    return 0 if allok else 1

if __name__ == '__main__':
    sys.exit(main())
