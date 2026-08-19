# SOP — Building a Client Mockup Site with the `mockup-site` Skill

**Purpose:** produce a pitch-ready 5-page mockup website for a local service business
in one Claude session, with zero process re-explaining.
**Owner:** Dillon / Paint & Profits
**Time:** ~5–10 min of your prep + one Claude session + ~5 min review

---

## Phase 0 — Prep (usually nothing)

1. **All you need is their website URL.** The skill's harvester scrapes the site
   itself: phone, email, address, FB/IG/GMB links, services, cities, taglines, brand
   colors, logo, and every real photo. Whatever it can't find, Claude searches for
   (their GMB, Facebook) and reports as gaps.
2. **Optional — extra photos** (ones not on their site): put them in ONE folder on
   disk, e.g. `~/Desktop/<company>-photos/`.
   ⚠️ Photos pasted into the chat are NOT usable in the site — Claude can see them but
   they don't exist as files. Always use a folder path.
3. **Optional — keyword data** (in order of cheapness):
   - **DataForSEO (best, one-time setup):** open an account at dataforseo.com ($50
     minimum deposit, pay-as-you-go), get API credentials at
     app.dataforseo.com/api-access, and set them once:
     `export DATAFORSEO_LOGIN="..."` / `export DATAFORSEO_PASSWORD="..."` in your
     `~/.zshrc`. After that every build pulls its own keyword gap automatically for
     about **$0.26 per client** — no exports, no extra steps.
   - **Semrush connector:** Claude can pull the gap live (it asks first — Semrush
     API units cost real money).
   - **Semrush website:** run *Keyword Gap* (client vs 2 biggest local competitors),
     export as PDF, leave it in `~/Downloads` and mention the path.

## Phase 1 — Kickoff (one line)

4. Open Claude Code (any folder) and paste:

   ```
   Build a mockup site for <url>
   ```

   Optional add-ons on extra lines, only if you have them:

   ```
   Extra photos: <folder path>
   Keyword data: <PDF path, or "pull it from Semrush">
   Notes: <taglines, USPs, corrections — anything you know that the site doesn't say>
   ```

   The skill triggers on this automatically. If it doesn't, say:
   *"use the mockup-site skill"*.

## Phase 2 — While it builds

5. Claude will: run the harvester (site scrape → contact/socials/services/cities/
   colors/photos) → chase gaps via web search → inspect every photo (rejecting
   watermarked/duplicate images) → apply keyword targets → build home + 3 area pages +
   1 service page → validate → serve on localhost with a screenshot.
6. **You can interject mid-build** — corrections sent while it's working get folded
   in ("use the newer crew photo", "their accent is green not red", "add Chandler").

## Phase 3 — Review (the 10-point check)

7. Open the localhost URL Claude gives you. Click through **every** nav item and both
   dropdowns, all 5 pages.
8. Verify:
   - [ ] Homepage follows the wireframe top-to-bottom (offer bar → hero+form →
     badges → reviews → about → stats → services+form → 6 service cards → trust →
     CTA banner → projects → process → why-us → FAQ → blog → areas+map → footer)
   - [ ] Logo is theirs and renders cleanly on the white nav
   - [ ] Colors match their brand (check against their logo/trucks)
   - [ ] Phone + email are real and every phone number is tap-to-call
   - [ ] Reviews section sits directly below the hero, labeled as samples
   - [ ] Cities/areas are correct; area links read "{Trade} in {City}"
   - [ ] Each area page has a genuinely different local angle (not city-swapped)
   - [ ] No watermarked/stock photos anywhere
   - [ ] Missing-photo slots show the labeled placeholder panels (not wrong photos)
   - [ ] Before/after pairs are the same building, same angle
   - [ ] Footer says "— Design mockup."
9. Give edits in plain language. Iterate until happy.

## Phase 4 — Deliver the pitch

10. Ask Claude for whichever you need: full-page screenshots, a zip of the site
    folder, or a live deploy (Vercel) if you want a URL the prospect can click.
11. **Before any version goes live as their real site:** replace sample reviews with
    live ones (the Elfsight embed is left in the code, commented), replace placeholder
    stats/financing terms, confirm photo permissions, remove "— Design mockup."

## Where things live

| Thing | Path |
|---|---|
| The skill (playbook, stylesheet, scripts) | `~/.claude/skills/mockup-site/` |
| Each company's site | `~/Mockups/<company-slug>/` (TPG: `~/Mockup/`) |
| Local preview | `.claude/launch.json` → `http://localhost:<port>/` |

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill didn't trigger | Say "use the mockup-site skill" |
| localhost link dead (new session) | "restart the mockup server" |
| Photos can't be found | Give the exact folder path; don't paste images into chat |
| Semrush PDF unreadable | Re-export as PDF (not print-to-PDF); Claude's extractor handles native Semrush exports |
| Wrong brand colors | Point at the truth: "match the logo" or paste hex codes |
| Harvester missed something (no socials/cities found) | It reports gaps honestly — paste the missing link/info in chat and it overrides |
| Company has no website | Give the GMB/Facebook link + a photo folder instead of a URL |
