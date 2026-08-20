# AGENTS.md

## Cursor Cloud specific instructions

This repo is **Instant Website Builder** (`skill/` + `.cursor/skills/instant-website-builder`) —
Python 3 pipeline scripts plus HTML templates/wireframes, not a traditional app.
There is no build system, no automated test suite, and no lint config. See
`README.md` and `skill/SKILL.md` for the product overview and the per-build
pipeline; `skill/SOP.md` is the human operator guide.
`skill/references/build-layout.md` is the per-client folder convention.

### Dependencies
- Runtime is system **Python 3** (`/usr/bin/python3`). The only third-party dependency is
  **Pillow**, used by `skill/scripts/enhance_photos.py`, `skill/scripts/demo_photos.py`,
  and image dimensions in `skill/scripts/harvest.py`. It is installed by the
  environment update script (`pip3 install Pillow`, which lands as a `--user` install).
  Every other script is pure Python stdlib.

### Running / serving a site (the "app")
- Scaffold a client folder:
  `python3 skill/scripts/new_build.py --url https://example.com --name "Example" --out builds`
- Validate a built site (must print `ALL PAGES OK`):
  `python3 skill/scripts/validate_site.py <site-dir>`
  New Instant Website builds should pass `--require-alt`.
- Serve a site locally, then open the `.html` in a browser:
  `python3 -m http.server <port> --directory <site-dir>`
- Enhance harvested photos (exercises Pillow):
  `python3 skill/scripts/enhance_photos.py <in_dir> <out_dir>`
- Labeled SAMPLE photos:
  `python3 skill/scripts/demo_photos.py <client-root>`
- The complete worked example lives in `examples/tpg-paints-and-stains/` (home +
  3 area pages + a service page) and is the easiest thing to validate/serve for a smoke test.

### Lint / tests
- No configured linter or test framework exists. As a syntax smoke-check, use
  `python3 -m py_compile skill/scripts/*.py`.

### Non-obvious gotchas
- **`harvest.py` image dimensions.** It prefers Pillow, then macOS `sips`, then a
  file-size fallback. On Linux without Pillow, tiny files are dropped and larger
  downloads are kept with width/height `0`. Pillow is expected in this environment.
  Harvest still needs outbound network to the target site.
- `keyword_gap_dataforseo.py` needs `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` env vars and
  makes paid API calls — skip it unless credentials are provided and spend is approved.
- Live client builds belong in `builds/<slug>/` (gitignored), never mixed into
  `skill/assets/` or another company's folder.
