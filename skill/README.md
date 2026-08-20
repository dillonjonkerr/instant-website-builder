# The Skill — Instant Website Builder

This folder is the engine: a [Claude Code](https://claude.com/claude-code) skill
and the playbook Cursor follows for `/instant-website-builder`.

## Start here

| Read this | If you are |
|---|---|
| [`SOP.md`](SOP.md) | **A human operator** — kickoff, optional dump, optional photos, review |
| [`SKILL.md`](SKILL.md) | **The agent** — isolated folders, harvest, stops, build, QA |
| [`references/build-layout.md`](references/build-layout.md) | **Folder convention** — one company, one tree |

## Folders

| Folder | Contents |
|---|---|
| [`scripts/`](scripts/) | `new_build.py` · `harvest.py` · `photo_plan.py` · `demo_photos.py` · `validate_site.py` · keyword + enhance tools |
| [`templates/`](templates/) | Homepage wireframe + area page + service page — replace these in place when new designs land |
| [`references/`](references/) | Wireframe, photo slots, harvest guide, page anatomy, SEO, layout |
| [`assets/`](assets/) | Shared stylesheet copied **into each client's** `03-site/assets/` |

## Install on a new machine (Claude Code)

```bash
mkdir -p ~/.claude/skills && cp -r skill ~/.claude/skills/mockup-site
```

Then: `Build a mockup site for <company-url>` (or a GBP link).

In this repo (Cursor), use `/instant-website-builder` — no copy step needed.
