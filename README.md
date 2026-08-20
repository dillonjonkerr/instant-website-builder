# Instant Website Builder

**Paste a website URL or Google Business Profile → get a pitch-ready mockup.**

A system by Paint & Profits for building high-converting **example websites** for
local service businesses (painters, roofers, HVAC, any contractor). It harvests
the company's real brand — logo, colors, photos, phone, taglines, cities — asks
you for optional extras, and builds a validated site on a fixed wireframe.
Each client lives in **its own folder** so three websites never share one
`crew-trucks.jpg`.

<p align="center">
  <img src="docs/tpg-home.png" alt="Example build — TPG Paints & Stains homepage" width="720">
  <br><em>Built by the system from one URL: real logo, real photos, real brand colors, SEO-targeted copy.</em>
</p>

## How to use it

In Cursor:

```
/instant-website-builder
https://their-site.com
```

or a Google Business Profile / Maps link. The agent harvests, then **asks**
for an optional info dump and extra photos (Drive, chat, or `skip`). Full
operator guide: [skill/SOP.md](skill/SOP.md).

In Claude Code the same flow is: `Build a mockup site for <url>`.

## What's in this repo

| Folder | What it is |
|---|---|
| [`skill/`](skill/) | **The engine.** Playbook, scripts, templates. Cursor slash skill also lives at `.cursor/skills/instant-website-builder/`. |
| [`wireframe-handoff/`](wireframe-handoff/) | **The design DNA.** Annotated homepage wireframe + `photo_slots.json`. |
| [`docs/`](docs/) | Screenshots. |
| [`examples/tpg-paints-and-stains/`](examples/tpg-paints-and-stains/) | **The worked example** (quality bar — do not reuse its photos on other clients). |
| [`builds/`](builds/) | Live client folders (gitignored). One slug per company. |

## Inside `skill/`

| File | Purpose |
|---|---|
| `SKILL.md` | The playbook — isolate, harvest, optional dump, optional photos, build, QA |
| `SOP.md` | Human operator guide |
| `scripts/new_build.py` | Scaffolds `builds/<slug>/` (intake, photos, site) |
| `scripts/harvest.py` | Website or GBP → `brief.json` + photos |
| `scripts/photo_plan.py` | Photo-request names for Drive/chat |
| `scripts/demo_photos.py` | Labeled SAMPLE fills when you skip extras |
| `scripts/keyword_gap_dataforseo.py` | Keyword gap (~$0.26/client) |
| `scripts/validate_site.py` | Nesting, links, assets, alt text |
| `templates/` | Home wireframe + area + service page templates (replace in place when you have new designs) |
| `references/build-layout.md` | Per-client folder convention |

## The pipeline (what the agent does per build)

1. **Isolate** — new folder for this company only
2. **Harvest** — scrape site or GBP; inspect photos; chase gaps
3. **Ask you** — optional info dump (`skip` is fine)
4. **Ask you** — extra photos via Drive/chat, or skip with SAMPLE images
5. **SEO** — keyword gap if available; titles and H1s from head terms
6. **Build** — wireframe homepage + **every** service page + **every** area page
7. **QA** — validator with alt-text check, localhost, screenshot

## Hard rules (why the mockups are safe to pitch)

- One company, one folder — never mix client photos
- Never ship watermarked or third-party photos (MLS/stock = copyright liability)
- Never invent dollar prices — scope tiers only, labeled illustrative
- Fabricated content stays labeled (sample reviews, "— Design mockup." footer)
- Real contact info everywhere when we found it
- SAMPLE photos (if you skipped extras) stay labeled as samples

## Costs

| Thing | Cost |
|---|---|
| Build a mockup | Model usage only |
| Keyword gap (DataForSEO) | ~$0.26 per client (pay-as-you-go, $50 min deposit) |
| Keyword gap (fallback) | Free — manual Semrush PDF export |

## The wireframe

Every homepage follows this exact 18-section structure (annotated; hatched boxes =
photo slots matched to the Photo Direction deck):

<p align="center">
  <img src="wireframe-handoff/wireframe_render.png" alt="Annotated homepage wireframe" width="720">
</p>

---

*Wireframe v1 synthesized from the Legacy Painting and Pro Vision Painting drafts.*
*© Paint & Profits. All rights reserved.*
