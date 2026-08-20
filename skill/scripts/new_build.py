#!/usr/bin/env python3
"""Scaffold an isolated Instant Website Builder client folder.

Every company gets its own tree. Never mix two clients' photos, intake, or HTML.

    python3 new_build.py --url https://company.com [--name "Company LLC"] [--out builds]
    python3 new_build.py --gbp "https://maps.app.goo.gl/..." --name "Company LLC"
    python3 new_build.py --url https://company.com --harvest   # also run harvest.py

Default --out is ./builds (repo) or ~/Mockups when that folder already exists.
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARVEST = os.path.join(SKILL_ROOT, "scripts", "harvest.py")

DIRS = [
    "00-intake/photos/raw",
    "01-photos/client",
    "01-photos/extra",
    "01-photos/demo",
    "02-seo",
    "03-site/areas",
    "03-site/services",
    "03-site/assets/images",
]


def slugify(text):
    text = (text or "").strip().lower()
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"^www\.", "", text)
    host = text.split("/")[0]
    if "." in host and " " not in host:
        text = host.rsplit(".", 1)[0]  # thepaintguysaz.com -> thepaintguysaz
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text or "client")[:60]


def default_out():
    mockups = os.path.expanduser("~/Mockups")
    if os.path.isdir(mockups):
        return mockups
    return os.path.abspath("builds")


def write(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", help="Company website URL")
    ap.add_argument("--gbp", help="Google Business Profile / Maps URL")
    ap.add_argument("--name", help="Company name (used for the folder slug)")
    ap.add_argument("--out", default=None, help="Parent folder for client builds")
    ap.add_argument("--harvest", action="store_true",
                    help="Run harvest.py into 00-intake/ after scaffolding")
    args = ap.parse_args()

    if not args.url and not args.gbp and not args.name:
        ap.error("give --url, --gbp, and/or --name")

    parent = os.path.abspath(args.out or default_out())
    slug = slugify(args.name or args.url or args.gbp)
    root = os.path.join(parent, slug)
    os.makedirs(root, exist_ok=True)
    for d in DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    source = args.url or args.gbp or ""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    write(os.path.join(root, "README.md"), f"""# {args.name or slug}

Isolated Instant Website Builder folder for **one** company. Do not copy photos
or HTML from another client in here.

| Folder | What lives here |
|---|---|
| `00-intake/` | Harvester output: `brief.json`, `report.md`, raw photos |
| `01-photos/client/` | Keepers from their site/GBP, renamed by slot |
| `01-photos/extra/` | Photos you dropped (Drive download or chat files) |
| `01-photos/demo/` | Labeled SAMPLE photos used only when you skipped a slot |
| `02-seo/` | Keyword gap / title decisions |
| `03-site/` | The mockup: `index.html`, `areas/`, `services/`, `assets/` |

- Website: {args.url or "—"}
- Google Business Profile: {args.gbp or "—"}
- Scaffolded: {now}
""")

    write(os.path.join(root, "BUILD.md"), f"""# Build notes — {args.name or slug}

Fill this in as the build proceeds. Deliver it with the pitch.

- **Source website:** {args.url or "—"}
- **GBP:** {args.gbp or "—"}
- **Operator dump:** (pending / skipped / received)
- **Photo extras:** (pending / skipped / Drive / chat)
- **Fabricated (must replace before a real launch):** sample reviews, placeholder stats
- **SEO titles used:**
- **Photo slots still SAMPLE or empty:**
""")

    write(os.path.join(root, "00-intake", "operator-dump.md"),
          "# Operator dump (optional)\n\n"
          "Paste extra facts here if the operator provides them: owner name, years "
          "in business, warranty, extra cities, USPs, competitors, notes.\n"
          "If they said skip, leave this file with a single line: `skipped`.\n")

    write(os.path.join(root, "01-photos", "manifest.json"), """{
  "slots": {},
  "policy": "Each slot lists file, source (client|extra|demo|placeholder), and alt text. Never reuse another company's photos."
}
""")

    print(f"CLIENT ROOT → {root}")
    print(f"  intake     {os.path.join(root, '00-intake')}")
    print(f"  photos     {os.path.join(root, '01-photos')}")
    print(f"  site       {os.path.join(root, '03-site')}")

    harvest_url = args.url or args.gbp
    if args.harvest and harvest_url:
        intake = os.path.join(root, "00-intake")
        cmd = [sys.executable, HARVEST, harvest_url, intake]
        print("\nRunning harvester:", " ".join(cmd))
        r = subprocess.run(cmd)
        if r.returncode != 0:
            sys.exit(r.returncode)
    elif source and not args.harvest:
        print(f"\nNext: python3 {HARVEST} {source} {os.path.join(root, '00-intake')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
