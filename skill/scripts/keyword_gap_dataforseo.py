#!/usr/bin/env python3
"""
keyword_gap_dataforseo.py — pull a keyword gap via the DataForSEO Labs API.

    export DATAFORSEO_LOGIN="you@example.com"
    export DATAFORSEO_PASSWORD="xxxx"
    python3 keyword_gap_dataforseo.py client.com comp1.com comp2.com [--out DIR]
    python3 keyword_gap_dataforseo.py client.com --discover [--out DIR]   # auto-find competitors

Returns keywords each competitor ranks for that the client does NOT, with US search
volumes/CPC — the same data as a Semrush Keyword Gap export, but pay-as-you-go
(~$0.13 per 1,000 rows; a 2-competitor pull ≈ $0.26–0.30).

Writes <out>/gap.json + <out>/gap-brief.md and prints the top of the gap.
Zero dependencies (urllib). Credentials come from env vars only — never hardcode.
NOTE: written from the official docs; first run against a live account should be
watched (API responses occasionally add fields).
"""

import base64
import json
import os
import re
import sys
import urllib.request

API = "https://api.dataforseo.com/v3"
US, EN = 2840, "en"
# directories/aggregators that show up as "competitors" but aren't real ones
NOT_COMPETITORS = re.compile(
    r"yelp|angi|homeadvisor|thumbtack|houzz|facebook|wikipedia|reddit|yellowpages|"
    r"bbb\.org|nextdoor|porch|craftjack|expertise|mapquest|instagram|linkedin|"
    r"forbes|pinterest|amazon|lowes|homedepot|sherwin|benjaminmoore|behr", re.I)


def call(path, payload, creds):
    req = urllib.request.Request(
        API + path, data=json.dumps([payload]).encode(),
        headers={"Authorization": "Basic " + creds, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    task = data["tasks"][0]
    if task["status_code"] != 20000:
        sys.exit(f"API error on {path}: {task['status_code']} {task['status_message']}")
    result = task.get("result") or []
    return (result[0].get("items") or []) if result else [], task.get("cost", 0)


def clean_domain(d):
    return re.sub(r"^https?://(www\.)?|/.*$", "", d.strip().lower())


def main():
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not pw:
        sys.exit("Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD env vars first "
                 "(from app.dataforseo.com/api-access). Never pass them as arguments.")
    creds = base64.b64encode(f"{login}:{pw}".encode()).decode()

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    client = clean_domain(args[0])
    competitors = [clean_domain(a) for a in args[1:]]
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "."
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 300
    min_vol = int(sys.argv[sys.argv.index("--min-volume") + 1]) if "--min-volume" in sys.argv else 30
    os.makedirs(outdir, exist_ok=True)
    total_cost = 0.0

    if "--discover" in sys.argv and not competitors:
        items, cost = call("/dataforseo_labs/google/competitors_domain/live", {
            "target": client, "location_code": US, "language_code": EN,
            "exclude_top_domains": True, "limit": 30}, creds)
        total_cost += cost
        for it in items:
            d = it.get("domain", "")
            if d and d != client and not NOT_COMPETITORS.search(d):
                competitors.append(d)
            if len(competitors) == 2:
                break
        if not competitors:
            sys.exit("No plausible competitors discovered — pass them explicitly.")
        print(f"discovered competitors: {', '.join(competitors)}")

    gap = {}
    for comp in competitors:
        # intersections:false → keywords target1 (competitor) ranks for, target2 (client) doesn't
        items, cost = call("/dataforseo_labs/google/domain_intersection/live", {
            "target1": comp, "target2": client, "intersections": False,
            "location_code": US, "language_code": EN, "item_types": ["organic"],
            "filters": [["keyword_data.keyword_info.search_volume", ">", min_vol]],
            "order_by": ["keyword_data.keyword_info.search_volume,desc"],
            "limit": limit}, creds)
        total_cost += cost
        for it in items:
            kd = it.get("keyword_data", {})
            kw = kd.get("keyword")
            info = kd.get("keyword_info", {}) or {}
            serp = it.get("first_domain_serp_element", {}) or {}
            if not kw:
                continue
            row = gap.setdefault(kw, {
                "keyword": kw, "volume": info.get("search_volume"),
                "cpc": info.get("cpc"), "found_via": []})
            row["found_via"].append({"competitor": comp,
                                     "rank": serp.get("rank_absolute"),
                                     "url": serp.get("url")})
        print(f"{comp}: {len(items)} gap keywords (cost so far ${total_cost:.2f})")

    rows = sorted(gap.values(), key=lambda r: -(r["volume"] or 0))
    both = [r for r in rows if len(r["found_via"]) > 1]
    out = {"client": client, "competitors": competitors, "min_volume": min_vol,
           "api_cost_usd": round(total_cost, 3),
           "keywords": rows, "ranked_by_all_competitors": [r["keyword"] for r in both]}
    with open(os.path.join(outdir, "gap.json"), "w") as f:
        json.dump(out, f, indent=2)

    lines = [f"# Keyword gap — {client} vs {', '.join(competitors)}",
             f"\n{len(rows)} keywords competitors rank for that the client doesn't "
             f"(volume > {min_vol}). API cost ${total_cost:.2f}.\n",
             "| Keyword | US volume | CPC | Ranked by |", "|---|---|---|---|"]
    for r in rows[:40]:
        lines.append(f"| {r['keyword']} | {r['volume']:,} | "
                     f"${(r['cpc'] or 0):.2f} | {len(r['found_via'])} competitor(s) |")
    brief = "\n".join(lines) + "\n"
    with open(os.path.join(outdir, "gap-brief.md"), "w") as f:
        f.write(brief)
    print(brief[:2000])
    print(f"\nDONE → {outdir}/gap.json, {outdir}/gap-brief.md (total cost ${total_cost:.2f})")


if __name__ == "__main__":
    main()
