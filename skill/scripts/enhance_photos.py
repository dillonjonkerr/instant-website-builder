#!/usr/bin/env python3
"""Auto-enhance harvested photos so they look pro on the mockup site.

For every image in <in_dir>:
  1. Fix EXIF rotation (sideways phone photos)
  2. Auto-levels (rescues dim/hazy job-site shots)      — autocontrast, gentle
  3. Subtle color + contrast lift (paint colors pop)     — +6% sat, +3% contrast
  4. Downscale to --max long edge (never upscales)       — LANCZOS
  5. Sharpen AFTER resize (unsharp mask, web-tuned)
  6. Export optimized JPEG (or --webp), EXIF stripped

Never fakes quality: images whose long edge is under --min-edge are copied
through and flagged TOO_SMALL in the report — swap those for better originals
or keep them out of hero/banner slots (see references/photo_slots.json).

Usage:
  python3 enhance_photos.py <in_dir> <out_dir> [--max 1600] [--quality 82]
                            [--min-edge 900] [--webp] [--hero FILE ...]
  --hero: filenames (basename match) exported at 1920px instead of --max.

Writes <out_dir>/enhance-report.json and prints a summary table.
Requires Pillow (present on this machine); falls back to telling you to use
sips manually if Pillow is missing.
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
except ImportError:
    sys.exit("Pillow not installed - fall back to: sips -s format jpeg -s formatOptions 82 -Z 1600 <file>")

EXTS = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".tif", ".tiff", ".heic")


def has_transparency(img: Image.Image) -> bool:
    if img.mode == "P":
        return "transparency" in img.info
    if img.mode in ("RGBA", "LA"):
        alpha = img.getchannel("A")
        return alpha.getextrema()[0] < 255
    return False


def enhance(img: Image.Image) -> Image.Image:
    img = ImageOps.autocontrast(img, cutoff=1)          # auto-levels, clips 1% tails
    img = ImageEnhance.Color(img).enhance(1.06)         # subtle saturation
    img = ImageEnhance.Contrast(img).enhance(1.03)      # subtle contrast
    return img


def process(path, out_path, max_edge, quality, webp):
    img = Image.open(path)
    img.load()
    img = ImageOps.exif_transpose(img)
    orig_w, orig_h = img.size

    # Transparent logos/graphics: keep alpha, keep PNG, no tone changes
    if has_transparency(img):
        out_path = os.path.splitext(out_path)[0] + ".png"
        if max(img.size) > max_edge:
            img.thumbnail((max_edge, max_edge), Image.LANCZOS)
        img.save(out_path, "PNG", optimize=True)
        return (orig_w, orig_h), img.size, out_path

    if img.mode != "RGB":
        img = img.convert("RGB")
    img = enhance(img)
    if max(img.size) > max_edge:
        img.thumbnail((max_edge, max_edge), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=90, threshold=3))
    if webp:
        img.save(out_path, "WEBP", quality=quality, method=6)
    else:
        img.save(out_path, "JPEG", quality=quality, optimize=True, progressive=True)
    return (orig_w, orig_h), img.size, out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("in_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--max", type=int, default=1600, help="long-edge px for section images")
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--min-edge", type=int, default=900, help="below this long edge -> flag TOO_SMALL")
    ap.add_argument("--webp", action="store_true")
    ap.add_argument("--hero", nargs="*", default=[], help="basenames to export at 1920px")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    ext = ".webp" if args.webp else ".jpg"
    report, failures = [], []

    names = sorted(f for f in os.listdir(args.in_dir)
                   if f.lower().endswith(EXTS) and not f.startswith("."))
    if not names:
        sys.exit(f"no images found in {args.in_dir}")

    for name in names:
        src = os.path.join(args.in_dir, name)
        base = os.path.splitext(name)[0]
        dst = os.path.join(args.out_dir, base + ext)
        max_edge = 1920 if name in args.hero or base in [os.path.splitext(h)[0] for h in args.hero] else args.max
        try:
            (ow, oh), (nw, nh), dst = process(src, dst, max_edge, args.quality, args.webp)
        except Exception as e:  # corrupt download, unsupported codec
            failures.append({"file": name, "error": str(e)})
            continue
        entry = {
            "file": name, "out": os.path.basename(dst),
            "in_px": f"{ow}x{oh}", "out_px": f"{nw}x{nh}",
            "in_kb": round(os.path.getsize(src) / 1024),
            "out_kb": round(os.path.getsize(dst) / 1024),
            "flags": [],
        }
        if max(ow, oh) < args.min_edge:
            entry["flags"].append("TOO_SMALL")   # fine for thumbnails, not hero/banner
        report.append(entry)

    with open(os.path.join(args.out_dir, "enhance-report.json"), "w") as f:
        json.dump({"images": report, "failures": failures}, f, indent=2)

    wf = max((len(r["file"]) for r in report), default=4)
    print(f"{'FILE':<{wf}}  {'IN':>10} {'OUT':>10} {'IN KB':>7} {'OUT KB':>7}  FLAGS")
    for r in report:
        print(f"{r['file']:<{wf}}  {r['in_px']:>10} {r['out_px']:>10} "
              f"{r['in_kb']:>7} {r['out_kb']:>7}  {','.join(r['flags'])}")
    for fl in failures:
        print(f"FAILED: {fl['file']} - {fl['error']}")
    small = [r["file"] for r in report if r["flags"]]
    if small:
        print(f"\n{len(small)} image(s) TOO_SMALL for hero/banner slots - use only in "
              f"small slots or chase better originals (GMB/Facebook often has them).")


if __name__ == "__main__":
    main()
