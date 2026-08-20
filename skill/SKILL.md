---
name: instant-website-builder
description: Build a pitch-ready mockup website for a local service business from a website URL or Google Business Profile. Harvests contact info, photos, services, cities, and brand; asks the operator for an optional info dump and extra photos (Drive, chat, or skip); then builds a wireframe-matching site with home + every service page + every area page, SEO titles, and image alt text — each company in its own isolated folder. Use when the user types /instant-website-builder, /Instant Website Builder, pastes a company URL or GBP link, or asks to build a mockup / example site / instant website for a contractor.
---

# Instant Website Builder

Turn a **website URL or Google Business Profile** into a pitch-ready multi-page
mockup that looks like the company built it themselves: their logo, their photos,
their phone, their cities, their brand colors. These are **example sites to show
clients**, not launch-ready production sites. The bar is "looks like the sites
we've already built" — same wireframe, their brand.

The worked example is TPG Paints & Stains (`examples/tpg-paints-and-stains/`).
Do not copy TPG photos into a new client.

**Templates:** start from `templates/home-wireframe.html`, `templates/area-page.html`,
and `templates/service-page.html`. Dillon will drop updated templates into
`templates/` — always use whatever is there now; do not invent a new layout.

## Skill root

Scripts, templates, and references live next to this file (`scripts/`,
`templates/`, `references/`, `assets/`). In the git repo that is `skill/`.

Never write a client's files into the skill folder. Every company gets its own
tree — see `references/build-layout.md`.

| Where you are | Client root |
|---|---|
| This repo | `builds/<slug>/` |
| Claude Code install | `~/Mockups/<slug>/` |

```bash
python3 scripts/new_build.py --url https://COMPANY.com --name "Company LLC" --out builds
python3 scripts/new_build.py --gbp "https://maps.app.goo.gl/..." --name "Company LLC" --out builds
```

## Kickoff — URL or GBP is enough

The operator types `/instant-website-builder` (or "build a mockup for") plus:

- a **website URL**, or
- a **Google Business Profile / Maps** link, or
- a **business name** (find the URL + GBP yourself)

Then run the pipeline in order. Two steps **stop and wait** for an optional
reply (`skip` is a valid answer). Do not skip the ask.

Anything already in the kickoff message (notes, extra cities, a photo folder
path, a Drive link) **overrides harvest** and means you should not ask for that
item again.

---

## Pipeline

### 0. Isolate the client — read `references/build-layout.md`

Run `new_build.py` first. All harvest, photos, and HTML for this company go
only under that folder. If you are building a second or third website in the
same session, scaffold a **new** slug. Never reuse `crew-trucks.jpg` (or any
file) from another client or from the TPG example.

### 1. Harvest — read `references/asset-harvest.md`

```bash
python3 scripts/harvest.py <website-or-gbp-url> <client-root>/00-intake
python3 scripts/photo_plan.py <client-root>
```

The harvester writes `00-intake/brief.json` + `report.md` + `photos/raw/`.
Treat `gaps` as to-dos: WebSearch their GBP/Facebook for whatever it missed.

If the input was GBP-only, the script tries to find a real website from the
Maps page. You still chase hours, reviews, extra photos, and a site URL in
the browser if HTML is a JS shell.

Then **look at every image** in `photos/raw/` — reject MLS/stock watermarks,
cast keepers into IMG-01…IMG-16 per `references/photo_slots.json`, copy
keepers into `01-photos/client/` renamed by role, and run
`scripts/enhance_photos.py` on keepers before they enter `03-site/assets/images/`.

### 2. STOP — optional info dump

Show a short harvest recap (name, phone, email, address, cities, services,
photo count, gaps). Then ask **once**:

> If you have extra info, paste it — owner name, years in business, warranty,
> extra cities, USPs, competitors, notes, anything the site doesn't say.
> Or type **skip**.

Wait. Write their reply (or `skipped`) to `00-intake/operator-dump.md`.
Their dump overrides `brief.json`.

### 3. STOP — optional extra photos

After classifying harvested photos, ask **once** using the names in
`01-photos/photo-request.md`:

> I still need photos named like this (Drive folder, chat, or files):
> `interior-painting`, `exterior-painting`, `team`, `crew-trucks`, …
> Or type **skip** and I will fill remaining slots with labeled SAMPLE photos.

Wait.

- **Drive link:** try to fetch if it is public; if not, ask them to drop the
  files into `<client-root>/01-photos/extra/` (or attach in chat). Chat images
  are only usable once saved as files in `01-photos/extra/`.
- **Skip:** `python3 scripts/demo_photos.py <client-root> --all-empty`
  SAMPLE boards are allowed on a pitch mockup. They must stay labeled
  ("SAMPLE PHOTO — Design mockup") in the image itself and in alt text.
  Never use another company's photos as "demo".
- **Client-required slots** (IMG-01, 02, 10, 12): prefer real photos; SAMPLE
  is OK on skip so the pitch isn't full of empty hatched boxes.

Update `01-photos/manifest.json` with `file`, `source` (`client`|`extra`|`demo`),
and **alt text** for every slot you use.

### 4. Brand

Colors from site CSS frequency + the logo (logo wins). Map onto `--navy` /
`--red` in `03-site/assets/style.css` (copy from `assets/style.css` first).
See "Re-theming" in `references/page-structure.md`.

### 5. SEO — read `references/seo-content.md`

Source hierarchy in `references/api-integrations.md`. Head terms →
`<title>` / H1 / H2. Near-me phrasing in copy. Area titles:
`{Trade} in {City}, {ST} | {Secondary} | {Brand}`. Save decisions in
`02-seo/seo-brief.md`.

### 6. Build — read `references/page-structure.md`

Site lives in `<client-root>/03-site/`:

| Page | Path | Template |
|---|---|---|
| Home | `index.html` | `templates/home-wireframe.html` — 18 sections, never removed |
| Every area | `areas/<trade>-<city>-<st>.html` | `templates/area-page.html` |
| Every service | `services/<service-slug>.html` | `templates/service-page.html` |

Rules:

- **All service cards on the home page link to a real service page** you built
  (not just one flagship with the rest as `#services` hashes). Cap 8.
- **All harvested cities get an area page** with a unique local angle. Cap 8
  (HQ + strongest remaining). Research housing stock / HOA / climate before
  writing. Never city-swap.
- Nav dropdowns only list pages that exist.
- Every `<img>` has specific alt text (service + city + what is shown).
  Demo photos say they are samples.
- Photos are `03-site/assets/images/<role>.jpg` — this client's folder only.
- Footer: "— Design mockup." Sample reviews stay labeled.

### 7. QA + deliver

```bash
python3 scripts/validate_site.py <client-root>/03-site --require-alt   # must print ALL PAGES OK
```

Serve `03-site/` on localhost, screenshot home, give a table of URLs
(home, each area, each service). Close with: photo slots that are SAMPLE or
empty, what was fabricated, SEO titles chosen, top competitor if known.

---

## Hard rules

- **One company, one folder.** No shared `assets/` across clients.
- **Never ship a watermarked or third-party-copyrighted image.** Delete and say why.
- **Never invent dollar prices** — scope tiers only, labeled illustrative.
- **Fabricated content stays labeled.**
- **Real contact info everywhere** when harvest found it.
- **Validate before delivering.**
- **Do not wait for templates** — use `templates/` as they are; Dillon will
  replace them later.

## Bundled resources

| File | What it is |
|---|---|
| `scripts/new_build.py` | Scaffolds the isolated client folder |
| `scripts/harvest.py` | Website or GBP → `brief.json` + photos |
| `scripts/photo_plan.py` | Photo-request names + empty manifest |
| `scripts/demo_photos.py` | Labeled SAMPLE fills when operator skips |
| `scripts/enhance_photos.py` | Auto-level / sharpen / resize keepers |
| `scripts/validate_site.py` | Nesting / links / assets / alt text |
| `scripts/keyword_gap_dataforseo.py` | Keyword gap (~$0.26) if env creds exist |
| `scripts/pdf_extract.py` | Semrush PDF fallback |
| `scripts/example_gen_pages.py` | TPG quality bar (do not copy its content) |
| `templates/home-wireframe.html` | Homepage — THE wireframe |
| `templates/area-page.html` | Area page |
| `templates/service-page.html` | Service page |
| `assets/style.css` | Shared stylesheet for sub-pages |
| `references/build-layout.md` | Folder convention |
| `references/photo_slots.json` | IMG-01…IMG-16 |
| `references/page-structure.md` | Section order + re-theming |
| `references/seo-content.md` | Keyword → copy mapping |
| `references/asset-harvest.md` | Inspection + watermark rules |
| `references/api-integrations.md` | DataForSEO / Semrush |
