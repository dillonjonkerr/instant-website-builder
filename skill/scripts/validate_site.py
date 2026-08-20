#!/usr/bin/env python3
"""Validate every .html page in a mockup site directory (nested areas/services too).

Checks, per page:
  - HTML tag nesting (mismatched / unclosed / stray tags)
  - every local src/href file actually exists on disk (resolved from that page)
  - every internal *.html link points at a real file
  - every #anchor link on the page has a matching id= target
  - <img> tags have non-empty alt text (--require-alt, used for new builds)

Usage:
  python3 validate_site.py /path/to/site-dir
  python3 validate_site.py /path/to/site-dir --require-alt

Exit code 0 = all pages pass, 1 = issues found.
"""
import argparse
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr", "path", "circle", "rect", "ellipse", "line",
        "polygon", "polyline", "stop", "use"}

SKIP_HREF = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "#")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errs = []
        self.imgs = []  # (src, alt or None)

    def handle_starttag(self, t, a):
        attrs = dict(a)
        if t == "img":
            self.imgs.append((attrs.get("src") or "", attrs.get("alt")))
        if t not in VOID:
            self.stack.append((t, self.getpos()))

    def handle_endtag(self, t):
        if t in VOID:
            return
        if not self.stack:
            self.errs.append(f"stray </{t}> {self.getpos()}")
            return
        if self.stack[-1][0] == t:
            self.stack.pop()
        else:
            self.errs.append(
                f"</{t}> {self.getpos()} but <{self.stack[-1][0]}> open from {self.stack[-1][1]}")


def html_pages(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "00-intake", "01-photos", "02-seo")]
        for name in filenames:
            if name.endswith(".html"):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def local_file_refs(html):
    refs = set()
    for path in re.findall(r'''(?:src|href)=["']([^"']+)["']''', html, re.I):
        if path.startswith(SKIP_HREF) or path.startswith("#"):
            continue
        path = path.split("#")[0].split("?")[0]
        if path:
            refs.add(unquote(path))
    return refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--require-alt", action="store_true",
                    help="Fail if any <img> is missing a non-empty alt attribute")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    # If they pointed at a client folder, validate the site subfolder.
    site = os.path.join(root, "03-site")
    if os.path.isdir(site) and not any(f.endswith(".html") for f in os.listdir(root)
                                       if os.path.isfile(os.path.join(root, f))):
        root = site

    pages = html_pages(root)
    if not pages:
        print(f"no .html files in {root}")
        return 1

    allok = True
    for path in pages:
        rel = os.path.relpath(path, root)
        src = open(path, encoding="utf-8").read()
        p = P()
        p.feed(src)
        page_dir = os.path.dirname(path)

        missing = []
        for ref in local_file_refs(src):
            # ignore pure in-page hashes already skipped; check files
            target = os.path.normpath(os.path.join(page_dir, ref))
            if not os.path.exists(target):
                missing.append(ref)

        links = {h.split("#")[0] for h in re.findall(
            r'''href=["']([\w./-]+\.html(?:#[\w-]*)?)["']''', src)}
        badlinks = []
        for link in links:
            if not link:
                continue
            target = os.path.normpath(os.path.join(page_dir, link.split("#")[0]))
            if not os.path.exists(target):
                badlinks.append(link)

        anchors = set(re.findall(r'\bid=["\']([\w-]+)["\']', src))
        deadanch = set(re.findall(r'href=["\']#([\w-]+)["\']', src)) - anchors

        noalt = []
        if args.require_alt:
            for img_src, alt in p.imgs:
                if alt is None or not str(alt).strip():
                    noalt.append(img_src[:80] or "(no src)")

        ok = not (p.errs or p.stack or missing or badlinks or deadanch or noalt)
        allok &= ok
        print(("PASS " if ok else "FAIL ") + rel)
        if p.errs:
            print("   nesting:", p.errs[:3])
        if p.stack:
            print("   unclosed:", [x[0] for x in p.stack][:5])
        if missing:
            print("   missing files:", missing[:8])
        if badlinks:
            print("   broken page links:", badlinks)
        if deadanch:
            print("   dead #anchors:", sorted(deadanch)[:8])
        if noalt:
            print("   images missing alt:", noalt[:8])

    print("\nALL PAGES OK" if allok else "\nISSUES FOUND — fix before delivering")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
