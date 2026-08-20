#!/usr/bin/env python3
"""Turn harvested photos + wireframe slots into a photo request for the operator.

    python3 photo_plan.py <client-root>

Reads:
  <client-root>/00-intake/brief.json          (if present)
  <client-root>/00-intake/photos/raw/
  skill/references/photo_slots.json

Writes:
  <client-root>/01-photos/photo-request.md    — what to ask the operator
  <client-root>/01-photos/manifest.json       — slot table (empty until classified)

The agent still has to LOOK at each photo and fill the manifest. This script
only lists files and the Drive-folder names to request.
"""
import json
import os
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLOTS_PATH = os.path.join(SKILL_ROOT, "references", "photo_slots.json")

# Drive / chat folder names the operator should use when sending extras.
DRIVE_NAME = {
    "IMG-01": "crew-trucks",
    "IMG-02": "team",
    "IMG-03": "action-jobsite",
    "IMG-04": "interior-painting",
    "IMG-05": "exterior-painting",
    "IMG-06": "cabinets-trim",
    "IMG-07": "commercial",
    "IMG-08": "fence-deck",
    "IMG-09": "garage-shed",
    "IMG-10": "crew-candid",
    "IMG-11": "dramatic-action",
    "IMG-12": "featured-projects",
    "IMG-13": "interior-action",
    "IMG-14": "blog-thumbs",
    "IMG-15": "map",  # not a photo
    "IMG-16": "roofing-jobsite",
}


def list_images(folder):
    if not os.path.isdir(folder):
        return []
    exts = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".tif", ".tiff")
    return sorted(f for f in os.listdir(folder)
                  if f.lower().endswith(exts) and not f.startswith("."))


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: photo_plan.py <client-root>")
    root = os.path.abspath(sys.argv[1])
    intake = os.path.join(root, "00-intake")
    photos_dir = os.path.join(intake, "photos", "raw")
    extra_dir = os.path.join(root, "01-photos", "extra")
    out_dir = os.path.join(root, "01-photos")
    os.makedirs(out_dir, exist_ok=True)

    with open(SLOTS_PATH, encoding="utf-8") as f:
        slots = json.load(f)["slots"]

    brief = {}
    brief_path = os.path.join(intake, "brief.json")
    if os.path.exists(brief_path):
        with open(brief_path, encoding="utf-8") as f:
            brief = json.load(f)

    harvested = list_images(photos_dir)
    extras = list_images(extra_dir)
    logo = brief.get("logo") or {}
    company = (brief.get("company") or {}).get("name") or os.path.basename(root)
    trade = (brief.get("company") or {}).get("trade_guess") or "this trade"

    requestable = [s for s in slots if s["id"] != "IMG-15"]
    lines = [
        f"# Photo request — {company}",
        "",
        "Optional. Reply **skip** to fill remaining slots with labeled SAMPLE photos.",
        "Or drop files named by category (Drive folder or chat):",
        "",
    ]
    for s in requestable:
        name = DRIVE_NAME.get(s["id"], s["id"].lower())
        lines.append(f"- `{name}` — {s['short']} ({s['id']}, {s['section']})")
    lines += [
        "",
        "## What we already harvested",
        "",
        f"- Raw site/GBP photos: **{len(harvested)}** in `00-intake/photos/raw/`",
        f"- Extra drops so far: **{len(extras)}** in `01-photos/extra/`",
        f"- Logo: {logo.get('file') or logo.get('url') or 'not found'}",
        f"- Trade guess: {trade}",
        "",
    ]
    if harvested:
        lines.append("### Raw files")
        lines.append("")
        for n in harvested:
            lines.append(f"- `{n}`")
        lines.append("")
    lines += [
        "## How to send extras",
        "",
        "1. Google Drive folder (anyone-with-the-link) **or**",
        "2. Attach images in chat **or**",
        "3. Copy files into this client's `01-photos/extra/` yourself.",
        "",
        "Name files or subfolders: `interior-painting`, `exterior-painting`, "
        "`team`, `crew-trucks`, `cabinets-trim`, etc. Do **not** mix another "
        "company's photos into this folder.",
        "",
        "Watermarked MLS/stock images will be rejected even if you send them.",
        "",
    ]
    req_path = os.path.join(out_dir, "photo-request.md")
    with open(req_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    manifest = {
        "company": company,
        "trade": trade,
        "harvested_raw": harvested,
        "extra_files": extras,
        "slots": {
            s["id"]: {
                "section": s["section"],
                "short": s["short"],
                "drive_name": DRIVE_NAME.get(s["id"]),
                "file": None,
                "source": None,
                "alt": None,
                "notes": None,
            }
            for s in slots
        },
        "policy": "source is client | extra | demo | placeholder. Never reuse another company's photos.",
    }
    man_path = os.path.join(out_dir, "manifest.json")
    with open(man_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"WROTE {req_path}")
    print(f"WROTE {man_path}")
    print(f"{len(harvested)} harvested photos, {len(requestable)} photo slots to fill")
    return 0


if __name__ == "__main__":
    sys.exit(main())
