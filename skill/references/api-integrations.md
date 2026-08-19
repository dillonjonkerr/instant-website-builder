# API Integration — automated keyword data (DataForSEO)

Verified Aug 2026. One integration upgrades the SEO stage from manual exports to fully
automatic. It is gated on credentials the user sets up once; if the credentials aren't
present, fall back down the hierarchy silently — never sign the user up for anything
or ask them to buy a plan mid-build.

## Keyword-gap source hierarchy (use the first available)

1. **DataForSEO** (`scripts/keyword_gap_dataforseo.py`) — cheapest + scriptable.
   Available when `DATAFORSEO_LOGIN`/`DATAFORSEO_PASSWORD` env vars exist
   (check: `[ -n "$DATAFORSEO_LOGIN" ] && echo yes`).
2. **Semrush MCP connector** (`competitors_research` → `organic_research`) — already
   wired into Claude. Calls cost paid Semrush units: tell the user before pulling and
   respect a "no".
3. **Semrush PDF/CSV export** in the kickoff message → `scripts/pdf_extract.py`.
4. **No data** → generic local-service rules in `references/seo-content.md`.

## DataForSEO (pay-as-you-go keyword data)

- One-time setup (user does this, not Claude): account at dataforseo.com → min
  deposit $50, no subscription → credentials from `app.dataforseo.com/api-access` →
  exported as `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` env vars in `~/.zshrc`
  (never hardcoded, never committed).
- Cost per client mockup: **~$0.26–0.30** (Labs live calls = $0.012 + $0.00012/row;
  two 1,000-row domain_intersection calls ≈ $0.26). The bundled script prints the
  actual cost the API reports. A $50 deposit ≈ 190 clients.
- In the pipeline, run it right after the harvester (stage 3), competitors from the
  user if named, otherwise `--discover`:

```bash
python3 scripts/keyword_gap_dataforseo.py client.com comp1.com comp2.com --out <site-dir>/intake
python3 scripts/keyword_gap_dataforseo.py client.com --discover --out <site-dir>/intake  # auto-find competitors
```

  Output `gap.json` / `gap-brief.md`: keywords each competitor ranks for that the
  client doesn't, with US volumes + CPC, flagged when BOTH competitors rank (those
  are the priority targets). Feed the top terms through the mapping rules in
  `references/seo-content.md` exactly as if they came from a Semrush PDF, and report
  the top competitor + targets chosen to the user in the final message.
- Key API facts if calling directly: HTTP Basic auth; `domain_intersection` is
  pairwise with `intersections:false` meaning "target1 ranks, target2 doesn't" —
  so target1=competitor, target2=client; `location_code` 2840 = US; volumes are
  embedded in Labs responses (no separate volume call needed); errors surface as
  `tasks[0].status_code != 20000` with a message — quote it to the user (usually
  means empty balance or wrong credentials).
- First live run after setup: test on a known domain (e.g. thepaintguysaz.com) and
  sanity-check the output against known facts before trusting it in a build.

## What stays manual/judgment no matter what

Keyword CHOICE (which gap terms fit this client's actual services), local angles for
area pages, and every photo decision. APIs supply numbers; the build supplies sense.
