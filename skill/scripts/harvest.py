#!/usr/bin/env python3
"""
harvest.py — URL-only intake for the mockup-site skill.

    python3 harvest.py <company-url> <output-dir> [--max-photos 30] [--max-pages 8]

Give it one URL. It fetches the homepage + the most useful internal pages
(about / services / areas / contact / gallery), and produces:

    <output-dir>/brief.json      structured company brief (the skill's intake, filled)
    <output-dir>/report.md       human-readable summary of what was found + gaps
    <output-dir>/photos/raw/     every real photo found, downloaded, with dimensions

Zero dependencies: shells out to `curl` (Chrome UA — many builders block default
agents) and `sips` (macOS) for image dimensions. Everything else is stdlib.

What it does NOT do (Claude does these at build time):
  - visually classify photos (interior/exterior/team/before-after) and reject
    watermarked images — that needs eyes
  - pull keyword gap / competitors — that's the Semrush connector or a PDF export
"""

import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

SOCIAL_HOSTS = {
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"],
    "google_business": ["g.page", "goo.gl/maps", "google.com/maps", "maps.app.goo.gl",
                        "business.google.com", "g.co/kgs"],
    "yelp": ["yelp.com"],
    "youtube": ["youtube.com", "youtu.be"],
    "linkedin": ["linkedin.com"],
    "tiktok": ["tiktok.com"],
    "nextdoor": ["nextdoor.com"],
    "houzz": ["houzz.com"],
    "angi": ["angi.com", "angieslist.com"],
    "bbb": ["bbb.org"],
    "thumbtack": ["thumbtack.com"],
}

# slugs worth crawling beyond the homepage, in priority order
CRAWL_HINTS = ["about", "service", "area", "location", "city", "contact",
               "gallery", "project", "portfolio", "review", "testimonial", "faq"]

TRADE_WORDS = {
    "painting": ["paint", "stain", "cabinet refinish", "epoxy"],
    "roofing": ["roof", "shingle", "tile roof"],
    "hvac": ["hvac", "air conditioning", "heating", "furnace", "ac repair"],
    "plumbing": ["plumb", "drain", "water heater", "repipe"],
    "landscaping": ["landscap", "turf", "irrigation", "hardscap", "paver"],
    "flooring": ["floor", "tile install", "hardwood", "vinyl plank", "carpet"],
    "electrical": ["electric", "panel upgrade", "ev charger", "wiring"],
    "remodeling": ["remodel", "renovation", "kitchen", "bathroom", "addition"],
    "garage doors": ["garage door"],
    "windows/doors": ["window replacement", "door install"],
    "concrete": ["concrete", "driveway", "stamped"],
    "pest control": ["pest", "termite", "scorpion"],
    "cleaning": ["cleaning", "maid", "janitorial", "power wash", "pressure wash"],
    "pool": ["pool service", "pool remodel", "pool clean"],
}

US_STATES = ("AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|"
             "MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY")

# words that disqualify a capitalized phrase from being a city name — copy fragments
# like "Serving Home And Business Owners With Great Painting In Arizona" title-case
# every word, so each candidate is checked word-by-word against this list
NOT_A_CITY = set("""and the with great what your you our are is was saying home business
owner owners in on of for we us get free call today now more about contact service
services painting painters paint quality expert professional licensed insured bonded
metropolitan area areas greater why how does near me all top rated best work team family
owned local trust trusted proudly serving serve stains llc inc company estimate quote
interior exterior residential commercial guys neighbors""".split())

IMG_SKIP = re.compile(r"(sprite|icon|favicon|badge|arrow|bullet|pixel|tracking|\.svg($|\?)|"
                      r"logo-?(white|footer|small)?\.(png|webp)($|\?)|avatar|emoji)", re.I)


def fetch(url, timeout=25):
    """GET a URL through curl (Chrome UA, redirects, compression). '' on failure."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-m", str(timeout), "-A", UA, url],
            capture_output=True, timeout=timeout + 10)
        return r.stdout.decode("utf-8", "ignore") if r.returncode == 0 else ""
    except Exception:
        return ""


def download(url, path, timeout=30):
    try:
        r = subprocess.run(["curl", "-sL", "--compressed", "-m", str(timeout),
                            "-A", UA, "-o", path, url],
                           capture_output=True, timeout=timeout + 10)
        return r.returncode == 0 and os.path.getsize(path) > 3000  # <3KB = icon/error page
    except Exception:
        return False


def img_dims(path):
    """(width, height) via sips; (0, 0) if unreadable (corrupt/HTML error body)."""
    try:
        r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                           capture_output=True, text=True, timeout=15)
        w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
        h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
        return (int(w.group(1)), int(h.group(1))) if w and h else (0, 0)
    except Exception:
        return (0, 0)


def visible_text(page):
    page = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    page = re.sub(r"<[^>]+>", " ", page)
    return html.unescape(re.sub(r"\s+", " ", page))


def extract_links(page, base):
    out = []
    for m in re.finditer(r'href\s*=\s*["\']([^"\']+)["\']', page, re.I):
        href = html.unescape(m.group(1).strip())
        if href.startswith(("javascript:", "#", "data:")):
            continue
        out.append(urljoin(base, href))
    return out


def extract_jsonld(page):
    """All parsed JSON-LD blocks (flattened through @graph)."""
    blocks = []
    for m in re.finditer(
            r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S | re.I):
        try:
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict):
                blocks.extend(g for g in item.get("@graph", []) if isinstance(g, dict))
                blocks.append(item)
    return blocks


def extract_images(page, base):
    """Candidate photo URLs, largest srcset variant preferred, Webflow -p-### upsized."""
    urls = []
    for m in re.finditer(r'<img[^>]+>', page, re.I):
        tag = m.group(0)
        srcset = re.search(r'srcset\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        if srcset:
            best, best_w = None, -1
            for cand in srcset.group(1).split(","):
                parts = cand.strip().split()
                if not parts:
                    continue
                w = int(parts[1][:-1]) if len(parts) > 1 and parts[1].endswith("w") else 0
                if w >= best_w:
                    best, best_w = parts[0], w
            if best:
                urls.append(urljoin(base, html.unescape(best)))
                continue
        src = re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        if src:
            urls.append(urljoin(base, html.unescape(src.group(1))))
    for m in re.finditer(r'background(?:-image)?\s*:\s*url\(["\']?([^"\')]+)', page, re.I):
        urls.append(urljoin(base, html.unescape(m.group(1))))
    cleaned, seen = [], set()
    for u in urls:
        u = re.sub(r"^//", "https://", u)
        # Webflow/CDN size variants: hero-p-500.jpg -> hero.jpg (grab the original)
        u = re.sub(r"-p-\d{3,4}(\.(?:jpe?g|png|webp))", r"\1", u)
        if u in seen or IMG_SKIP.search(u) or not u.startswith("http"):
            continue
        if not re.search(r"\.(jpe?g|png|webp|avif)(\?|$)", u, re.I):
            continue
        seen.add(u)
        cleaned.append(u)
    return cleaned


def find_logo(page, base):
    for m in re.finditer(r'<img[^>]+>', page, re.I):
        tag = m.group(0)
        blob = " ".join(re.findall(r'(?:src|alt|class|id)\s*=\s*["\']([^"\']*)["\']', tag, re.I))
        if re.search(r"logo|brand", blob, re.I):
            src = re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']', tag, re.I)
            if src:
                return urljoin(base, html.unescape(src.group(1)))
    og = re.search(r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page, re.I)
    return urljoin(base, html.unescape(og.group(1))) if og else None


def brand_colors(page, base):
    """Top accent hexes by frequency across linked stylesheets + inline styles."""
    css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", page, re.S | re.I))
    hrefs = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', page, re.I)
    hrefs += re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', page, re.I)
    for href in list(dict.fromkeys(hrefs))[:5]:
        css += fetch(urljoin(base, html.unescape(href)))
    counts = Counter()
    for hx in re.findall(r"#([0-9a-fA-F]{6})\b", css):
        r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
        if max(r, g, b) - min(r, g, b) < 24:   # grey/white/black — not a brand color
            continue
        counts[("#" + hx).upper()] += 1
    return [{"hex": h, "count": c} for h, c in counts.most_common(8)]


def guess_trade(text):
    scores = {t: sum(text.count(w) for w in ws) for t, ws in TRADE_WORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] >= 3 else None


def find_phones(page, text):
    phones = [re.sub(r"[^\d+]", "", m) for m in re.findall(r'href=["\']tel:([^"\']+)', page, re.I)]
    phones += ["".join(m) for m in re.findall(
        r"\(?(\d{3})\)?[\s.-](\d{3})[\s.-](\d{4})", text)]
    out = []
    for p in phones:
        digits = re.sub(r"\D", "", p)[-10:]
        if len(digits) == 10 and digits not in [re.sub(r"\D", "", x)[-10:] for x in out]:
            out.append(f"({digits[:3]}) {digits[3:6]}-{digits[6:]}")
    return out


def find_emails(page, text):
    emails = re.findall(r'href=["\']mailto:([^"\'?]+)', page, re.I)
    emails += re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
    out = []
    for e in emails:
        e = e.strip().lower()
        if e not in out and not re.search(r"\.(png|jpg|webp|css|js)$|example\.|sentry|wixpress", e):
            out.append(e)
    return out


def looks_like_city(phrase):
    words = phrase.split()
    return (1 <= len(words) <= 2
            and all(w[0].isupper() for w in words)
            and not any(w.lower() in NOT_A_CITY for w in words))


def find_cities(text, own_state=None):
    """City candidates ranked by evidence strength:
    'City, ST' pairs (strong), comma-separated lists of 3+ place-like names
    (real area enumerations are comma lists), then loose 'serving ...' mentions."""
    counts = Counter()
    for city, st in re.findall(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+){0,2}),?\s+(" + US_STATES + r")\b",
                               text):
        if looks_like_city(city):
            counts[city] += 3
            own_state = own_state or st
    place = r"[A-Z][a-z]+(?: [A-Z][a-z]+)?"
    for m in re.finditer(rf"\b((?:{place}\s*,\s*){{2,}}(?:and\s+)?{place})", text):
        items = [i.strip() for i in re.split(r",|\band\b", m.group(1)) if i.strip()]
        if len(items) >= 3 and all(looks_like_city(i) for i in items):
            for i in items:
                counts[i] += 2
    for m in re.finditer(r"(?:serving|proudly serv\w+|areas?[^.]{0,20}?:)\s+([^.!?]{10,220})",
                         text, re.I):
        for city in re.findall(rf"\b{place}\b", m.group(1)):
            if looks_like_city(city) and text.count(city) >= 2:
                counts[city] += 1
    return [c for c, _ in counts.most_common(15)], own_state


def find_services(pages_html, text, trade):
    found = []
    nav_texts = []
    for page in pages_html:
        nav_texts += [html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
                      for t in re.findall(r"<a[^>]*>(.*?)</a>", page, re.S | re.I)]
        nav_texts += [html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
                      for t in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", page, re.S | re.I)]
    words = TRADE_WORDS.get(trade or "", []) + ["interior", "exterior", "commercial",
                                                "residential", "repair", "install"]
    for t in nav_texts:
        t = re.sub(r"\s+", " ", t).strip()
        # service names are short noun phrases — not questions, headlines, or emails
        if not (4 < len(t) < 42 and len(t.split()) <= 4):
            continue
        if "?" in t or "@" in t or not any(w in t.lower() for w in words):
            continue
        if re.match(r"(?:read|learn|get|view|how|does|what|why|a |the |top|revamp)", t, re.I):
            continue
        if t.lower() not in [f.lower() for f in found]:
            found.append(t)
    return found[:20]


def find_taglines(page):
    tags = []
    for pat in (r"<h1[^>]*>(.*?)</h1>", r'class=["\'][^"\']*(?:tagline|slogan|hero-sub)[^"\']*["\'][^>]*>(.*?)<'):
        for t in re.findall(pat, page, re.S | re.I):
            t = html.unescape(re.sub(r"<[^>]+>", " ", t))
            t = re.sub(r"\s+", " ", t).strip()
            if 8 < len(t) < 120 and t not in tags:
                tags.append(t)
    desc = re.search(r'name=["\']description["\'][^>]+content=["\']([^"\']+)', page, re.I)
    if desc:
        tags.append(html.unescape(desc.group(1)).strip())
    return tags[:6]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    url = sys.argv[1] if sys.argv[1].startswith("http") else "https://" + sys.argv[1]
    outdir = sys.argv[2]
    max_photos = int(sys.argv[sys.argv.index("--max-photos") + 1]) if "--max-photos" in sys.argv else 30
    max_pages = int(sys.argv[sys.argv.index("--max-pages") + 1]) if "--max-pages" in sys.argv else 8

    photos_dir = os.path.join(outdir, "photos", "raw")
    os.makedirs(photos_dir, exist_ok=True)
    host = urlparse(url).netloc.replace("www.", "")

    print(f"[1/6] fetching {url}")
    home = fetch(url)
    if not home:
        sys.exit(f"FATAL: could not fetch {url} — check the URL or try again")
    pages = {url: home}

    # pick internal pages worth crawling: hint-matched slugs first, then any other
    # same-domain page (small sites put services at /exterior-painting etc., which
    # no hint list anticipates — if the site is small enough, just crawl it all)
    internal = []
    for link in extract_links(home, url):
        p = urlparse(link)
        if p.netloc.replace("www.", "") != host:
            continue
        link = link.split("#")[0].split("?")[0].rstrip("/")
        if not p.path or p.path == "/" or link in internal:
            continue
        if re.search(r"\.(pdf|jpg|png|webp|css|js|xml)$|/(privacy|terms|sitemap)", link, re.I):
            continue
        internal.append(link)
    internal.sort(key=lambda l: min((CRAWL_HINTS.index(h) for h in CRAWL_HINTS
                                     if h in urlparse(l).path.lower()), default=len(CRAWL_HINTS)))
    print(f"[2/6] crawling {min(len(internal), max_pages)} internal pages")
    for link in internal[:max_pages]:
        page = fetch(link)
        if page:
            pages[link] = page

    all_html = list(pages.values())
    all_text = " ".join(visible_text(p) for p in all_html)

    # --- structured data first: JSON-LD often has everything ---
    ld = {}
    for block in [b for p in all_html for b in extract_jsonld(p)]:
        btype = str(block.get("@type", ""))
        if re.search(r"business|organization|store|service", btype, re.I):
            ld.setdefault("name", block.get("name"))
            ld.setdefault("telephone", block.get("telephone"))
            ld.setdefault("email", block.get("email"))
            addr = block.get("address")
            if isinstance(addr, dict):
                ld.setdefault("address", ", ".join(str(addr.get(k, "")) for k in
                              ("streetAddress", "addressLocality", "addressRegion",
                               "postalCode") if addr.get(k)))
            same = block.get("sameAs") or []
            ld.setdefault("sameAs", same if isinstance(same, list) else [same])
            area = block.get("areaServed")
            if area:
                names = [a.get("name", a) if isinstance(a, dict) else str(a)
                         for a in (area if isinstance(area, list) else [area])]
                ld.setdefault("areaServed", names)

    print("[3/6] extracting contact / socials / services / areas")
    socials = {}
    for link in [l for p, b in pages.items() for l in extract_links(b, p)] + ld.get("sameAs", []):
        for name, hosts in SOCIAL_HOSTS.items():
            if any(h in link.lower() for h in hosts) and name not in socials:
                socials[name] = link.split("?")[0]

    phones = find_phones("".join(all_html), all_text)
    if ld.get("telephone"):
        digits = re.sub(r"\D", "", ld["telephone"])[-10:]
        if len(digits) == 10:
            fmt = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            phones = [fmt] + [p for p in phones if p != fmt]
    emails = find_emails("".join(all_html), all_text)
    if ld.get("email") and ld["email"].lower() not in emails:
        emails.insert(0, ld["email"].lower())

    title = re.search(r"<title[^>]*>(.*?)</title>", home, re.S | re.I)
    site_name = ld.get("name") or (html.unescape(title.group(1)).split("|")[0].split("–")[0].strip()
                                   if title else host)
    trade = guess_trade(all_text.lower())
    cities, state = find_cities(all_text)
    if ld.get("areaServed"):
        cities = list(dict.fromkeys([str(c) for c in ld["areaServed"]] + cities))
    services = find_services(all_html, all_text, trade)
    taglines = find_taglines(home)
    colors = brand_colors(home, url)

    print("[4/6] logo + brand colors")
    logo_url = find_logo(home, url)
    logo_file = None
    if logo_url:
        ext = os.path.splitext(urlparse(logo_url).path)[1] or ".png"
        logo_file = os.path.join(outdir, "photos", "logo" + ext)
        if not download(logo_url, logo_file):
            logo_file = None

    print(f"[5/6] downloading photos (max {max_photos})")
    img_urls = []
    for page_url, body in pages.items():
        for u in extract_images(body, page_url):
            if u not in img_urls:
                img_urls.append(u)
    photos, skipped = [], 0
    for i, u in enumerate(img_urls):
        if len(photos) >= max_photos:
            break
        fname = f"{len(photos):02d}-" + re.sub(r"[^\w.-]", "", os.path.basename(
            urlparse(u).path))[-60:]
        path = os.path.join(photos_dir, fname)
        if not download(u, path):
            skipped += 1
            continue
        w, h = img_dims(path)
        if w < 300 or h < 200:      # icons, spacers, tiny thumbs
            os.remove(path)
            skipped += 1
            continue
        photos.append({"file": f"photos/raw/{fname}", "width": w, "height": h, "src": u})

    gaps = []
    if not phones:
        gaps.append("no phone found — ask the user")
    if not emails:
        gaps.append("no email found — ask the user")
    if not socials:
        gaps.append("no social links found — check GMB manually")
    if not cities:
        gaps.append("no service cities detected — ask the user or check their GMB")
    if len(photos) < 6:
        gaps.append(f"only {len(photos)} usable photos — check FB/IG for more")
    if not trade:
        gaps.append("trade unclear from copy — confirm with the user")

    brief = {
        "harvested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_url": url,
        "pages_crawled": list(pages.keys()),
        "company": {"name": site_name, "trade_guess": trade, "state_guess": state},
        "contact": {"phones": phones, "emails": emails, "address": ld.get("address")},
        "socials": socials,
        "services_detected": services,
        "areas_detected": cities,
        "taglines": taglines,
        "brand_colors": colors,
        "logo": {"url": logo_url, "file": logo_file},
        "photos": {"downloaded": photos, "skipped": skipped},
        "keywords": None,    # fill via Semrush connector or scripts/pdf_extract.py
        "competitors": None,  # fill via Semrush connector (user-approved) or ask user
        "gaps": gaps,
    }
    brief_path = os.path.join(outdir, "brief.json")
    with open(brief_path, "w") as f:
        json.dump(brief, f, indent=2)

    print("[6/6] writing report")
    lines = [f"# Harvest report — {site_name}", "",
             f"- **URL:** {url}  ·  **Trade:** {trade or '?'}  ·  **State:** {state or '?'}",
             f"- **Phones:** {', '.join(phones) or '—'}",
             f"- **Emails:** {', '.join(emails) or '—'}",
             f"- **Address:** {ld.get('address') or '—'}",
             f"- **Socials:** " + (", ".join(f"[{k}]({v})" for k, v in socials.items()) or "—"),
             f"- **Areas ({len(cities)}):** {', '.join(cities) or '—'}",
             f"- **Services ({len(services)}):** {', '.join(services) or '—'}",
             f"- **Taglines:** " + ("; ".join(taglines) or "—"),
             f"- **Brand colors:** " + (", ".join(c['hex'] for c in colors) or "—"),
             f"- **Logo:** {logo_file or logo_url or '—'}",
             f"- **Photos:** {len(photos)} downloaded, {skipped} skipped (small/failed)", ""]
    if gaps:
        lines += ["## Gaps", ""] + [f"- {g}" for g in gaps]
    with open(os.path.join(outdir, "report.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nDONE → {brief_path}")
    print(f"       {len(photos)} photos in {photos_dir}")
    for g in gaps:
        print(f"  GAP: {g}")


if __name__ == "__main__":
    main()
