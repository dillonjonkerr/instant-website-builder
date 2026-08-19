---
name: mockup-site
description: Build a complete, ready-to-pitch mockup website for a local service business (painter, roofer, landscaper, HVAC, flooring, any local contractor) from as little as a single URL — a bundled harvester scrapes their site for contact info, socials, services, cities, brand colors, and photos automatically. Harvests the company's real logo, photos, phone, taglines and brand colors from their site and socials, rejects watermarked/stock images, applies SEO keyword targets if provided, and generates a validated 5-page site (home + 3 area pages + flagship service page) with quote forms, dropdown nav, review section under the hero, and a before/after slider — then serves it on localhost. Use this skill whenever the user names a business and asks for a mockup, website, landing page, redesign, "build a site for", "same as the others", or pastes a company brief or business URL with intent to build — even if they never say the word "mockup".
---

# Mockup Site Builder

Turn a company brief + URLs into a pitch-ready multi-page website mockup that looks
like the company built it themselves: their logo, their photos, their taglines, their
brand colors, their cities. The bar is "could be their real site tomorrow", not
"obviously a template". The worked example is TPG Paints & Stains (Arizona painter) —
every bundled resource comes from that real build.

## Intake — a URL is enough

The minimum input is **one URL** (or a company name to find the URL). Start every build
by running the harvester — it auto-fills the whole intake:

```bash
python3 scripts/harvest.py https://COMPANY.com <site-dir>/intake
```

It crawls their site, extracts phone/email/address, social links, services, cities,
taglines, brand colors, the logo, and downloads every real photo — writing `brief.json`,
`report.md`, and `photos/raw/` (details + the follow-up judgment steps:
`references/asset-harvest.md` §0). Treat its `gaps` list as to-dos: WebSearch their
GMB/FB for whatever it missed; ask the user only if that fails too.

Anything the user supplies directly **overrides** the harvest:

```
Phone / email / address     Socials: FB / IG / GMB      Service areas / cities
Services                    Notes / taglines / USPs
Keyword data:               (Semrush connector pull — ask before spending API units —
                             or a Semrush PDF/CSV path for scripts/pdf_extract.py)
Extra photos:               (folder path — chat attachments are NOT on disk)
```

If something critical is missing after harvesting (no website AND no photos), ask —
otherwise proceed and flag gaps at the end.

## Pipeline

Run these stages in order. Each stage's detail lives in a reference file — read it
when you reach that stage, not before.

### 1. Harvest → read `references/asset-harvest.md`
`scripts/harvest.py` (run at intake) already fetched the site, socials links, contact
info, brand colors, taglines, and photos. Your job is the judgment layer: **visually
inspect every image in `photos/raw/`** — reject MLS/ARMLS/stock watermarks (copyright
liability), catch duplicates, verify before/after pairs are the same building/angle,
mine truck-wrap slogans. Chase down `gaps` from the report (GMB/FB via WebSearch or the
Browser pane). Then run `scripts/enhance_photos.py` on the keepers (auto-levels, color
lift, sharpen, resize, EXIF strip — flags `TOO_SMALL` images that must stay out of
hero/banner slots; see asset-harvest.md §6), rename by role into `assets/`.

### 2. Brand
Colors from site-CSS frequency + the logo itself (logo wins conflicts). Check logo
alpha channel. Map onto the stylesheet's semantic slots and find/replace the hardcoded
accent hexes — see "Re-theming" in `references/page-structure.md`.

### 3. SEO targets → read `references/seo-content.md`
Source hierarchy (details + setup in `references/api-integrations.md`): ① DataForSEO
via `scripts/keyword_gap_dataforseo.py` if `DATAFORSEO_LOGIN`/`PASSWORD` env vars
exist (~$0.26/client); ② the Semrush MCP connector (units cost money — tell the user
before pulling, respect a "no"); ③ a Semrush PDF (`scripts/pdf_extract.py`) or CSV;
④ generic local-service rules. With data in hand: head terms → title/H1/H2s; near-me
terms → copy phrasing; any keyword the client ranks for but a competitor ranks higher
→ dedicated section + FAQ.

### 4. Build → read `references/page-structure.md`
Five pages sharing `assets/style.css` (copy it into the site's `assets/`):
- **Home** — START FROM `templates/home-wireframe.html`: a validated, self-contained
  build of THE WIREFRAME (`references/wireframe-painting-homepage.svg`, section-by-
  section in page-structure.md) with usage steps in its header comment. Copy it, swap
  the `:root` brand vars, replace every `[Token]`, cast real photos into the labeled
  IMG-01…IMG-15 placeholder panels per `references/photo_slots.json`. Section order
  is fixed for every site; extras (financing banners, deals, before/after slider) may
  be added but sections never removed. Reviews stay directly below the hero (user
  requirement), fake-but-plausible in the company's real review voice, labeled as
  samples.
- **3 area pages** — each with a genuinely different local angle (housing stock, rules,
  climate). Copy `scripts/example_gen_pages.py` into the build folder and rewrite every
  content dict; its TPG entries show the quality bar. Never city-swap one template.
- **1 flagship service page** — scope tiers labeled illustrative, never fake prices.

Site lives in its own folder (default `~/Mockups/<company-slug>/`), never mixed with
another company. Photos that don't exist get the honest `.noimg` placeholder panel —
never stock images, never another company's photos.

### 5. QA + deliver
```bash
python3 scripts/validate_site.py <site-dir>     # must print ALL PAGES OK
```
Serve via `.claude/launch.json` (`python3 -m http.server <port> --directory <site-dir>`),
screenshot the home page to confirm rendering, send files with SendUserFile, and give
the user a table of localhost URLs. Close with: top competitor (if keyword data),
SEO decisions made, which photo slots still need real photos, and what was fabricated
(reviews, stats) that must be replaced before any real launch.

## Hard rules

- **Never ship a watermarked or third-party-copyrighted image.** Delete and say why.
- **Never invent dollar prices** — scope tiers only, labeled illustrative.
- **Fabricated content stays labeled**: sample reviews note, "— Design mockup." in the
  footer copyright, placeholder financing terms marked as placeholder.
- **Real contact info everywhere**: their actual phone (tel: links), email, cities.
- **Validate before delivering** — broken links or missing assets kill the pitch.

## Bundled resources

| File | What it is |
|---|---|
| `scripts/harvest.py` | URL-only intake: scrapes site → brief.json + report.md + photos/raw/ |
| `assets/style.css` | The complete shared stylesheet (nav, dropdowns, hero, quote form, slider, sub-page components, mobile call bar) |
| `scripts/example_gen_pages.py` | Worked example generator (TPG) — copy + rewrite per company |
| `scripts/validate_site.py` | Nesting / links / assets / anchors validator |
| `scripts/pdf_extract.py` | Zero-dependency Semrush PDF text extractor |
| `scripts/keyword_gap_dataforseo.py` | Keyword gap via DataForSEO API (~$0.26/client) — needs env credentials |
| `references/api-integrations.md` | DataForSEO setup, costs, keyword-source hierarchy |
| `templates/home-wireframe.html` | Build-ready homepage implementing the wireframe — copy per company, swap tokens/photos |
| `references/wireframe-painting-homepage.svg` | THE canonical homepage wireframe — fixed section order for every build |
| `references/photo_slots.json` | Photo direction: IMG-01…IMG-16 slot specs (subject, framing, min size, do/don'ts, stock policy) |
| `references/asset-harvest.md` | Harvest commands, watermark policy, image inspection rules |
| `references/page-structure.md` | Wireframe section-by-section, sub-page anatomy, re-theming, delivery checklist |
| `references/seo-content.md` | Keyword-data → copy mapping rules |
