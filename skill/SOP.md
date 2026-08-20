# SOP — Instant Website Builder

**Purpose:** produce a pitch-ready mockup website (home + service pages + area
pages) for a local service business in one session.
**Owner:** Dillon / Paint & Profits
**What you get:** an example site to show the client, matching our wireframe —
not a launch-ready production site.

---

## Phase 0 — Prep (usually nothing)

1. **All you need is their website URL or Google Business Profile link.**
   The harvester pulls phone, email, address, socials, services, cities,
   taglines, brand colors, logo, and photos. Gaps get searched (GBP / Facebook)
   and then asked about.
2. **Optional — extra photos** (ones not on their site):
   - a Google Drive folder (name files/folders `interior-painting`,
     `exterior-painting`, `team`, `crew-trucks`, …), or
   - attach them in chat, or
   - skip — the build fills holes with labeled SAMPLE photos so the pitch
     still looks complete.
3. **Optional — info dump** when asked: owner name, years in business, extra
   cities, warranty, USPs, competitors. Or type `skip`.
4. **Optional — keyword data:** DataForSEO env vars (automatic, ~$0.26), or a
   Semrush PDF path, or say no.

## Phase 1 — Kickoff (one line)

5. In Cursor, run **`/instant-website-builder`** and paste the URL or GBP:

   ```
   /instant-website-builder
   https://their-site.com
   ```

   or

   ```
   /instant-website-builder
   https://maps.app.goo.gl/...
   ```

   Optional extra lines, only if you have them:

   ```
   Extra photos: <Drive link or folder path>
   Notes: <anything you know that the site doesn't say>
   Keyword data: <PDF path, or "skip">
   ```

   In Claude Code the same prompt works as `Build a mockup site for <url>`
   (the skill still triggers). If it doesn't: *"use the instant-website-builder skill"*.

## Phase 2 — While it builds

6. It will:
   1. Create a **new folder for this company only** (`builds/<slug>/`)
   2. Harvest the site or GBP into that folder
   3. **Ask you for an optional info dump** — answer or `skip`
   4. **Ask you for extra photos** — Drive, chat, or `skip`
   5. Build home + every service page + every area page on the wireframe
   6. Validate, serve on localhost, screenshot
7. You can interject mid-build ("accent is green", "add Chandler").

Each website's photos live only in that company's folder. Building three
sites will not dump three `crew-trucks.jpg` files into one shared `assets/`.

## Phase 3 — Review (the 10-point check)

8. Open the localhost URL. Click through **every** nav item and both dropdowns.
9. Verify:
   - [ ] Homepage follows the wireframe top-to-bottom
   - [ ] Logo is theirs and renders on the white nav
   - [ ] Colors match their brand
   - [ ] Phone + email are real; phones are tap-to-call
   - [ ] Reviews sit below the hero, labeled as samples
   - [ ] Every service card goes to a real service page
   - [ ] Every area page has a different local angle (not city-swapped)
   - [ ] Photos have alt text; SAMPLE photos are obviously labeled
   - [ ] No watermarked/stock-as-if-real photos
   - [ ] Footer says "— Design mockup."
10. Give edits in plain language.

## Phase 4 — Deliver the pitch

11. Ask for screenshots, a zip of `03-site/`, or a live deploy if you want a
    clickable URL for the prospect.
12. **Before any version goes live as their real site:** replace SAMPLE photos
    and sample reviews, confirm photo permissions, remove "— Design mockup."

## Where things live

| Thing | Path |
|---|---|
| The skill | `skill/` in this repo (`~/.claude/skills/mockup-site/` if installed) |
| Each company's files | `builds/<slug>/` (or `~/Mockups/<slug>/`) |
| That company's website | `builds/<slug>/03-site/` |
| Homepage template | `skill/templates/home-wireframe.html` (replace in place when you have new ones) |

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill didn't trigger | `/instant-website-builder` or "use the instant-website-builder skill" |
| localhost link dead | "restart the mockup server" |
| Photos in chat aren't in the site | They must be saved under that client's `01-photos/extra/` |
| Drive link is private | Download the files into `01-photos/extra/` and say "they're in extra/" |
| Wrong brand colors | "match the logo" or paste hex codes |
| Harvester missed something | Paste the missing link/info — it overrides |
| Company has no website | GBP or Facebook link is enough to start |
| Two clients' photos got mixed | Stop. Each client is `builds/<their-slug>/` only — never copy across |
