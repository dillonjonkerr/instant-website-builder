# Per-client folder layout

Every mockup is one company in one folder. Never mix photos, logos, or HTML
from another build. The skill templates/assets stay in `skill/`; client files
never go there.

## Where the folder lives

| Environment | Path |
|---|---|
| This git repo (Cursor) | `builds/<company-slug>/` (gitignored) |
| Claude Code skill install | `~/Mockups/<company-slug>/` |

Create it with:

```bash
python3 skill/scripts/new_build.py --url https://COMPANY.com --name "Company LLC" --out builds
# or GBP only:
python3 skill/scripts/new_build.py --gbp "https://maps.app.goo.gl/..." --name "Company LLC"
```

## Tree

```
builds/<slug>/
  README.md                 this client only
  BUILD.md                  fabricated content, SEO, remaining photo gaps
  00-intake/
    brief.json              harvester output (the facts file)
    report.md
    operator-dump.md        optional notes from you
    photos/raw/             every downloaded original
  01-photos/
    photo-request.md        Drive/chat names to ask for
    manifest.json           slot → file + alt + source (client|extra|demo)
    client/                 keepers, renamed by slot role
    extra/                  files you sent (Drive download or chat)
    demo/                   labeled SAMPLE boards if you skipped
  02-seo/
    gap.json / seo-brief.md
  03-site/                  the thing you screenshot and pitch
    index.html              homepage (from templates/home-wireframe.html)
    areas/<city>.html
    services/<service>.html
    assets/
      style.css             copy from skill/assets/style.css, then re-theme
      logo.png
      images/               hero-home.jpg, interior-painting.jpg, …
```

## Photo naming (inside THIS client only)

Rename by role, not by the source filename:

- `hero-home.jpg`, `team.jpg`, `crew-trucks.jpg`
- `interior-painting.jpg`, `exterior-painting.jpg`, `cabinets-trim.jpg`
- `ba1-before.jpg` / `ba1-after.jpg`

Demo fills keep the `demo-` prefix (`demo-interior-painting.jpg`) so they
cannot be mistaken for the client's work.

## What not to do

- Do not put client photos in `skill/assets/` or `examples/`.
- Do not copy `crew-trucks.jpg` from TPG or any other build.
- Do not dump three companies into one `assets/` folder.
- Chat attachments are only usable once they exist as files under
  `01-photos/extra/` (save them there, then reference the path).
