# Asset Harvest — getting the company's real logo, photos, brand, and voice

The mockup only sells if it looks like *their* company, not a template. Everything below
exists because a generic-looking mockup gets ignored and a wrong photo (someone else's
copyrighted image) creates liability for the client. Budget real time on this stage.

## 0. Run the harvester first — one command does steps 1–2 and half of 5

```bash
python3 scripts/harvest.py https://COMPANY.com <site-dir>/intake
```

It fetches the homepage + up to 8 internal pages (services/areas/about/contact), and
writes `<site-dir>/intake/`:

- `brief.json` — name, trade guess, phones, emails, address, social links (incl. from
  JSON-LD `sameAs`), detected services, detected cities, taglines, brand-color hexes by
  frequency, logo, and a `gaps` list of what it could NOT find
- `report.md` — the same, human-readable
- `photos/raw/` — every real photo ≥300px downloaded with dimensions (icons skipped);
  Webflow `-p-###` thumbnails are auto-upsized to originals

Then do the judgment work the script can't:

1. **Read `report.md`** and treat every `gaps` entry as a to-do (WebSearch their GMB/FB
   if socials are missing; ask the user only if searching fails).
2. **Visually inspect every photo in `photos/raw/`** — reject watermarks and
   duplicates per section 3 below, then CAST each keeper into a wireframe photo slot
   (IMG-01 hero crew/truck, IMG-02 team, IMG-03 ladder action, IMG-04…09 service
   cards, IMG-10 candid, IMG-11 dramatic, IMG-12 featured projects…). Slot specs
   with framing/size/do-don'ts: `references/photo_slots.json`. Copy keepers into
   `assets/` renamed by slot role (section 6). Slots marked "client photo required"
   with no genuine photo get the `.noimg` placeholder — never stock.
3. **Sanity-check detected cities/services** — the detectors are heuristic; drop
   anything that isn't a real place or service.
4. Anything the user stated in chat **overrides** the harvest.

The manual commands below are the fallback when the script fails on an unusual site,
and the reference for what it does internally.

## 1. Fetch their existing site

```bash
curl -sL --max-time 20 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" "https://COMPANY.com/" -o site.html
```

The browser UA matters — Webflow/Wix/Squarespace sites often block default curl.
Also fetch obvious subpages (grep internal links first):

```bash
grep -o -E 'href="/[a-z0-9/_-]*"' site.html | sort -u   # find /gallery, /about, /services
```

## 2. Extract everything useful from the HTML

```bash
# image URLs (CDN-hosted, all formats)
grep -o -E 'https?://[^"'"'"' )]+\.(jpg|jpeg|png|webp|avif)' site.html | sed 's/[?].*//' | sort -u

# headings = their actual voice and section names — reuse their phrasing where it's good
grep -o -E '<h[1-4][^>]*>.{0,120}' site.html | sed 's/<[^>]*>//g'

# brand colors, ranked by frequency; top non-neutral hexes are the brand
grep -o -E '#[0-9a-fA-F]{6}' site.html | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -12
```

Webflow CDN tip: images come in sized variants (`...-p-500.jpg`, `-p-800`, `-p-1080`).
Download the `-p-1080` or the un-suffixed original, never the 500px thumbnail.

## 3. LOOK at every single image before using it

Read each downloaded image with the Read tool. Non-negotiable, because:

- **Watermarks = copyright liability.** MLS/ARMLS/Zillow watermarks ("2024 ARMLS" in a
  corner) mean it's a real-estate listing photo owned by a listing broker — NOT the
  company's work. Stock watermarks (Shutterstock/Getty) same deal. Delete them and tell
  the user why. This has happened in practice: a client folder contained four MLS photos.
- **Duplicates**: the "different" photos are often the same file or the logo twice.
- **Before/after pairs must be the SAME building from the SAME angle.** Verify visually.
  A mismatched "pair" (two different houses) destroys credibility — split them into
  separate gallery items instead.
- **Truck wraps and yard signs are gold**: they carry real taglines, phone numbers, and
  slogans (e.g. "Best in the West — Better Than the Rest", "Residential Repaint
  Specialist"). Read them off the photo and use them verbatim in the hero/topbar.
- **Crew photos humanize** — use one in the intro/about section with a caption.

When there's no genuine photo for a slot (e.g. no interior shots exist), do NOT fill it
with a stock image or an unrelated photo. Use the `.svc-ph.noimg` branded placeholder
panel from style.css with a visible label like "Interior photo needed" — deliberately
obvious so it can't ship by accident, and it reads as a to-do, not a bug.

## 4. Socials & reviews

- Facebook/Instagram pages: fetch for extra photos, about text, and follower proof.
  These often fail from curl (login walls) — use the Browser pane tools if needed.
- Google Business/Yelp: note the star rating and review count for the trust bar, and
  read a few real reviews to mimic their tone in the mockup's fake reviews.
- Fake reviews are fine for a mockup: 3 reviews, 5 stars, first name + last initial,
  a service + city tag line (e.g. "Exterior repaint · Scottsdale"), written in the
  voice of the company's real reviews. Keep the small label "Sample reviews shown for
  layout purposes" in the section subhead so nobody mistakes them for real.

## 5. Logo and colors

- Check the logo PNG for a real alpha channel: `sips -g hasAlpha logo.png` — a white-box
  logo on a dark nav looks broken. If it's white-background only, put it in a white
  rounded chip (`.flogo` in the footer does this).
- Confirm brand colors from BOTH the site CSS frequency count and the logo itself (Read
  the logo, name its colors). If they conflict, the logo wins — it's on their trucks.
- Map colors onto the stylesheet slots (see page-structure.md → Re-theming).

## 6. Enhance + optimize everything (automatic)

After the keep/reject pass, run the enhancement script over the keepers — it fixes
EXIF rotation, auto-levels dim/hazy job-site shots, adds a subtle color/contrast
lift and web-tuned sharpening, downsizes, strips EXIF, and writes optimized JPEGs
(transparent logos pass through as PNG, untouched):

```bash
python3 scripts/enhance_photos.py <site-dir>/intake/photos/raw <site-dir>/assets --hero <hero-file>
```

Read the printed table + `enhance-report.json`: any image flagged `TOO_SMALL`
(long edge < 900px) must NOT go in hero/banner slots — use it in small slots only,
or chase a bigger original (GMB and Facebook usually have full-res versions; the
harvest report's `gaps` list points there). Never upscale to fake quality.

Target: whole site under ~4 MB (the script's defaults land there). Fallback if
Pillow is ever missing — sips (macOS, no installs needed):

```bash
sips -s format jpeg -s formatOptions 82 -Z 1920 hero.png --out hero.jpg   # hero max 1920
sips -s formatOptions 80 -Z 1500 crew.jpg --out crew.jpg                  # sections max 1400-1500
```

Rename files by ROLE, not source (`hero-home.jpg`, `crew-trucks.jpg`, `ba1-before.jpg`,
`ba1-after.jpg`) so the HTML reads clearly.

## 7. Images the user pastes into chat

An image attached in the conversation is NOT on disk — you can see it but cannot use it
in the site. Ask for the file path, or find it (`find ~/Downloads ~/Desktop -newermt ...`
with a tight scope — never a whole-home find, it times out). If it can't be found, say
which photo you still need and continue with what exists.
