# SEO Content Rules — turning keyword data into page copy

Get keyword data via the source hierarchy in `references/api-integrations.md`
(DataForSEO script → Semrush connector → Semrush PDF/CSV → none) and apply it BEFORE
writing final copy. A DataForSEO `gap.json`/`gap-brief.md` maps 1:1 onto the rules
below: its "keywords the client doesn't rank for" = the Missing list, and keywords
flagged `ranked_by_all_competitors` are the top-priority targets. If no data exists,
apply the generic local-service rules at the bottom — they hold for every local trade.

## Reading a Semrush Keyword Gap PDF

No poppler/pypdf on the machine? `python3 scripts/pdf_extract.py report.pdf` decodes
Semrush export PDFs (FlateDecode + ToUnicode CMaps, position-grouped rows).
What to pull out:

- **Organic keyword counts per domain** → tells you who the real competitor is and how
  far behind the client is. Report this to the user in one line.
- **Keyword Overlap / Missing / Weak lists with volumes** → these are the content targets.
- **Shared keywords with positions** → any keyword where the client already ranks but a
  competitor ranks higher is the single highest-priority content target (they're on the
  board; better content can move them).

## Applying the targets (the TPG worked example)

| Finding | Action taken |
|---|---|
| "painting company" 40,500/mo + "house painting" 18,100/mo missing | Both head terms into `<title>`, H1, and section H2s — the page previously only said "house painters" |
| "painter near me" 27,100 + "local painters" 18,100 + "house painter near me" 12,100 | Near-me/local phrasing woven into hero sub, intro copy, areas H2 ("Local Painters Near You Across Arizona"); area links renamed "Painters in {City}" |
| `best exterior paint for arizona` — client #49, competitor #14 | Built a full on-page section (H2, 4 mini-cards of substantive advice) AND a first-position FAQ answering the exact query |

General mapping:

- **Head terms** (highest volume): `<title>`, meta description, H1, 1–2 H2s. The title
  formula: `{Head Term} | {Secondary Term} | {Brand}`.
- **Near-me / local intent**: phrase naturally in copy ("Searching for a house painter
  near you?"), never keyword-stuff. Area links = "{Trade} in {City}".
- **Question keywords / anything the client already ranks for**: a dedicated section
  plus an FAQ item whose `<summary>` is the literal query and whose answer is genuinely
  useful (200+ words of real expertise). Thin answers don't move rankings.
- **Every FAQ answer is a mini content asset** — write them with real domain knowledge
  (climate, materials, local rules), not filler.

## Generic local-service rules (no keyword data provided)

1. Title/H1 carry: {trade} + {company type word: "company"} + {state or metro}.
2. "near me"/"local" phrasing in hero and areas sections.
3. Area pages target "{trade} {city} {st}" in title, H1, meta.
4. One substantive question-section targeting the trade's most-Googled question
   ("best exterior paint for arizona", "how much does a roof replacement cost in
   {metro}", "how often should AC be serviced in {metro}").
5. FAQ of 5–6 real questions with expert answers.

## Reporting back

Save a one-page brief (targets found → decisions made) to the scratchpad and summarize
it for the user in the final message: which keywords were targeted where, and who the
top competitor is by the numbers.
