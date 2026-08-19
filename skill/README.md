# The Skill — the engine of Instant Website Builder

This folder is a [Claude Code skill](https://claude.com/claude-code). Installed at
`~/.claude/skills/mockup-site/`, it triggers automatically whenever you tell Claude
to build a site for a business.

## Start here

| Read this | If you are |
|---|---|
| [`SOP.md`](SOP.md) | **A human operator** — the 5-phase guide: prep → kickoff → build → review → deliver |
| [`SKILL.md`](SKILL.md) | **Claude / a developer** — the full playbook: intake, pipeline stages, hard rules |

## Folders

| Folder | Contents |
|---|---|
| [`scripts/`](scripts/) | `harvest.py` (URL → brand/photos/contact scraper) · `keyword_gap_dataforseo.py` (SEO gap via API) · `pdf_extract.py` (Semrush PDF reader) · `validate_site.py` (pre-delivery QA) · `example_gen_pages.py` (sub-page generator) |
| [`templates/`](templates/) | `home-wireframe.html` — the master homepage template every build copies |
| [`references/`](references/) | The wireframe SVG + photo-slot specs, harvest guide, page anatomy, SEO mapping rules, API setup |
| [`assets/`](assets/) | Shared stylesheet for sub-pages |

## Install on a new machine

```bash
mkdir -p ~/.claude/skills && cp -r skill ~/.claude/skills/mockup-site
```

Then in Claude Code: `Build a mockup site for <company-url>`
