# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Claude Code skill** (`skill/mockup-site`) — a set of Python 3 pipeline
scripts plus HTML templates/wireframes, not a traditional app. There is no build system,
no automated test suite, and no lint config. See `README.md` and `skill/SKILL.md` for the
product overview and the per-build pipeline; `skill/SOP.md` is the human operator guide.

### Dependencies
- Runtime is system **Python 3** (`/usr/bin/python3`). The only third-party dependency is
  **Pillow**, used solely by `skill/scripts/enhance_photos.py`. It is installed by the
  environment update script (`pip3 install Pillow`, which lands as a `--user` install).
  Every other script is pure Python stdlib.

### Running / serving a site (the "app")
- Validate a built site (must print `ALL PAGES OK`):
  `python3 skill/scripts/validate_site.py <site-dir>`
- Serve a site locally, then open the `.html` in a browser:
  `python3 -m http.server <port> --directory <site-dir>`
- Enhance harvested photos (exercises Pillow):
  `python3 skill/scripts/enhance_photos.py <in_dir> <out_dir>`
- The complete worked example lives in `examples/tpg-paints-and-stains/` (home +
  3 area pages + a service page) and is the easiest thing to validate/serve for a smoke test.

### Lint / tests
- No configured linter or test framework exists. As a syntax smoke-check, use
  `python3 -m py_compile skill/scripts/*.py`.

### Non-obvious gotchas
- **`harvest.py` is macOS-oriented.** It shells out to `curl` (present on Linux) but uses
  macOS-only `sips` for image dimensions. On this Linux VM `sips` is absent, so `img_dims`
  returns `(0, 0)` and every downloaded photo is dropped by the `w < 300 / h < 200` filter —
  `brief.json`/`report.md` text fields still populate, but no photos are saved. It also
  needs outbound network to the target site (egress may be restricted here). This is an
  upstream tool limitation, not a broken environment.
- `keyword_gap_dataforseo.py` needs `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` env vars and
  makes paid API calls — skip it unless credentials are provided and spend is approved.
