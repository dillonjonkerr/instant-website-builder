#!/usr/bin/env python3
"""Generate labeled SAMPLE photos for empty wireframe slots.

Pitch mockups need to look complete. When the operator skips extra photos,
fill remaining slots with obviously-fake sample boards — never another
client's job photos, never unmarked stock.

    python3 demo_photos.py <client-root> [--slots IMG-04 IMG-05 ...]
    python3 demo_photos.py <client-root> --all-empty

Writes JPEGs into <client-root>/01-photos/demo/ and copies them into
<client-root>/03-site/assets/images/. Updates 01-photos/manifest.json.

Requires Pillow.
"""
import argparse
import json
import os
import shutil
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required: pip3 install Pillow")

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLOTS_PATH = os.path.join(SKILL_ROOT, "references", "photo_slots.json")

FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]

# (bg, accent, text) — muted contractor palettes, not loud gradients
PALETTES = {
    "IMG-01": ((28, 45, 72), (185, 28, 28), (255, 255, 255)),
    "IMG-02": ((45, 58, 74), (212, 175, 106), (255, 255, 255)),
    "IMG-03": ((62, 74, 88), (232, 213, 183), (255, 255, 255)),
    "IMG-04": ((232, 224, 212), (90, 74, 58), (40, 32, 24)),
    "IMG-05": ((176, 196, 214), (36, 62, 92), (20, 32, 48)),
    "IMG-06": ((245, 245, 242), (80, 80, 78), (30, 30, 28)),
    "IMG-07": ((120, 132, 144), (255, 255, 255), (255, 255, 255)),
    "IMG-08": ((120, 82, 48), (232, 213, 183), (255, 250, 240)),
    "IMG-09": ((90, 98, 88), (220, 220, 210), (255, 255, 255)),
    "IMG-10": ((40, 48, 56), (185, 28, 28), (255, 255, 255)),
    "IMG-11": ((22, 38, 64), (248, 113, 113), (255, 255, 255)),
    "IMG-12": ((48, 56, 64), (212, 175, 106), (255, 255, 255)),
    "IMG-13": ((236, 232, 224), (90, 74, 58), (40, 32, 24)),
    "IMG-14": ((230, 234, 238), (15, 36, 68), (15, 36, 68)),
    "IMG-16": ((72, 64, 56), (212, 175, 106), (255, 255, 255)),
}

FILE_FOR = {
    "IMG-01": "demo-hero.jpg",
    "IMG-02": "demo-team.jpg",
    "IMG-03": "demo-action-jobsite.jpg",
    "IMG-04": "demo-interior-painting.jpg",
    "IMG-05": "demo-exterior-painting.jpg",
    "IMG-06": "demo-cabinets-trim.jpg",
    "IMG-07": "demo-commercial.jpg",
    "IMG-08": "demo-fence-deck.jpg",
    "IMG-09": "demo-garage-shed.jpg",
    "IMG-10": "demo-crew-candid.jpg",
    "IMG-11": "demo-dramatic-action.jpg",
    "IMG-12": "demo-featured-project.jpg",
    "IMG-13": "demo-interior-action.jpg",
    "IMG-14": "demo-blog-thumb.jpg",
    "IMG-16": "demo-roofing-jobsite.jpg",
}


def font(size):
    for path in FONTS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def render(slot, out_path, company):
    sid = slot["id"]
    bg, accent, fg = PALETTES.get(sid, ((40, 50, 64), (185, 28, 28), (255, 255, 255)))
    w, h = 1600, 1067
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 18, h], fill=accent)
    d.rectangle([0, h - 90, w, h], fill=(0, 0, 0))

    f_kicker = font(28)
    f_title = font(56)
    f_sub = font(32)
    f_foot = font(22)

    d.text((64, 72), f"{sid}  ·  SAMPLE PHOTO", font=f_kicker, fill=accent)
    title_lines = wrap(d, slot["short"], f_title, w - 140)
    y = 160
    for line in title_lines[:3]:
        d.text((64, y), line, font=f_title, fill=fg)
        y += 70
    d.text((64, y + 16), "Design mockup — not this company's photo", font=f_sub, fill=fg)
    foot = f"{company}  ·  replace before any real launch"
    d.text((64, h - 58), foot, font=f_foot, fill=(255, 255, 255))
    img.save(out_path, "JPEG", quality=85, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("client_root")
    ap.add_argument("--slots", nargs="*", default=[], help="Slot ids, e.g. IMG-04 IMG-05")
    ap.add_argument("--all-empty", action="store_true",
                    help="Fill every slot in the manifest that has no file yet")
    args = ap.parse_args()

    root = os.path.abspath(args.client_root)
    with open(SLOTS_PATH, encoding="utf-8") as f:
        slots = {s["id"]: s for s in json.load(f)["slots"]}

    man_path = os.path.join(root, "01-photos", "manifest.json")
    manifest = {"slots": {}, "company": os.path.basename(root)}
    if os.path.exists(man_path):
        with open(man_path, encoding="utf-8") as f:
            manifest = json.load(f)
    company = manifest.get("company") or os.path.basename(root)

    wanted = list(args.slots)
    if args.slots:
        wanted = args.slots
    elif args.all_empty:
        wanted = [
            sid for sid, info in (manifest.get("slots") or {}).items()
            if sid != "IMG-15" and not (info or {}).get("file")
        ]
        if not wanted:
            wanted = [s for s in slots if s != "IMG-15"]
    else:
        wanted = [s for s in slots if s != "IMG-15"]

    demo_dir = os.path.join(root, "01-photos", "demo")
    site_img = os.path.join(root, "03-site", "assets", "images")
    os.makedirs(demo_dir, exist_ok=True)
    os.makedirs(site_img, exist_ok=True)

    written = []
    for sid in wanted:
        if sid not in slots or sid == "IMG-15":
            print(f"skip {sid} (not a photo slot)")
            continue
        fname = FILE_FOR.get(sid, f"demo-{sid.lower()}.jpg")
        dest = os.path.join(demo_dir, fname)
        render(slots[sid], dest, company)
        shutil.copy2(dest, os.path.join(site_img, fname))
        slot_info = (manifest.get("slots") or {}).setdefault(sid, {})
        slot_info.update({
            "file": f"assets/images/{fname}",
            "source": "demo",
            "alt": f"Sample {slots[sid]['short'].lower()} photo for layout — not {company}'s work",
            "notes": "Labeled SAMPLE — replace before launch",
        })
        written.append(fname)
        print(f"  {sid} → {fname}")

    os.makedirs(os.path.dirname(man_path), exist_ok=True)
    with open(man_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\n{len(written)} SAMPLE photos in {demo_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
