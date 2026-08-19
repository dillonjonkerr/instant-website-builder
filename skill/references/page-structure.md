# Page Structure — the exact site anatomy

Five pages minimum: **home + 3 area pages + 1 flagship-service page**. All share
`assets/style.css` (bundled with this skill) so they stay visually identical.

## Home page = THE WIREFRAME (fixed for every site)

The homepage follows `references/wireframe-painting-homepage.svg` — the user's
canonical wireframe (open it or `references/photo_slots.json` when unsure). Rules:

- **The section order below is fixed** for every site, every trade. Colors are NOT
  part of the wireframe — theme everything from the client's brand (see Re-theming).
- **Additions are welcome, removals are not**: extra banners (financing, seasonal
  deals, limited-time offers), a before/after slider, whatever the client's material
  supports — slot extras between sections, never replace one.
- Every `IMG-nn` below is a photo slot defined in `references/photo_slots.json`
  (subject, framing, min size, do/don'ts, stock-fallback policy). Match harvested
  photos to slots by those specs. Slots marked "client photo required" (IMG-01, 02,
  10, 12) get the `.noimg` placeholder if no genuine photo exists — never stock.
  Trades other than painting swap subjects, not structure (see IMG-16 roofing note).

1. **Top offer bar** — thin, dark: their real perk ("0% APR financing available ·
   Satisfaction guaranteed") + "Call today · {phone}". Placeholder terms stay labeled.
2. **Sticky nav** — logo left; `Home · Residential ▾ · Commercial ▾ · Past Work ·
   Areas ▾ · About · Contact`; right: phone button. Dropdowns only list pages that
   actually exist in the build (Residential ▾ → service pages; Areas ▾ → the 3 area
   pages, one-line descriptions). Drop the Commercial item if the client does no
   commercial work; never link to a page that wasn't built.
3. **Hero** (IMG-01: crew + wrapped truck bg, ~55% dark overlay) — kicker chip
   ("TRANSFORM YOUR {CITY} HOME"), H1 "Trusted House Painters in {City, ST} You Can
   Trust" (swap in keyword targets), 3 check pills (warranty · licensed+insured ·
   locally owned), Google + Facebook 5.0★ badge rows, "BOOK A FREE ESTIMATE" CTA.
   Right: quote form card ("GET YOUR FREE PAINTING ESTIMATE").
4. **Credibility strip** — logo/badge row: BBB A+, Google ★5.0, trade association
   (PCA etc.), Licensed+Insured, OSHA… only badges the client plausibly holds.
5. **Reviews** — "What People Are Saying About Our Painters in {City}", 4+ carousel
   cards with 5★ and a G mark. Mockup: fake-but-plausible reviews in their real
   review voice, subtly labeled as samples; production swaps to live Google reviews
   (real names — no "Jacob Jones" placeholders).
6. **About / meet the team** (IMG-02: team photo, optional video-play overlay) —
   kicker, "Get to Know {Company Name}", story copy, CTAs (estimate + learn more).
7. **Stats bar** (dark) — 100% satisfaction · {N}+ years · {N}+ projects · 5 star.
8. **Services intro + capture form** — H2 "Comprehensive Painting Services for {City}
   Homes and Businesses"; left: compact "Ready To Get Started?" lead form; right:
   IMG-03 (painters on ladders, mid-job).
9. **Service cards** (each links to its service page or the flagship page) — H2
   "Professional Interior & Exterior Painting Services in {State}"; 6 cards:
   Interior (IMG-04) · Exterior (IMG-05) · Cabinets/Trim & Doors (IMG-06) ·
   Commercial (IMG-07) · Fence & Deck (IMG-08) · Garage & Shed (IMG-09). Swap card
   set to the client's actual services; keep the 6-card grid.
10. **Why homeowners trust us** — H2 "Why {City} Homeowners Trust Our Painting Team";
    center IMG-10 (candid crew, branded gear) flanked by 4 feature cards (warranty,
    licensed & insured, premium materials, meticulous prep).
11. **Mid-page CTA banner** (dark navy + diagonal accent slash, IMG-11 photo showing
    through the right half) — "READY TO GET STARTED? / Transform Your {City}
    Property", consultation + phone buttons. Keep photo subject right of center.
12. **Projects / see our work** — H2 "Quality Results That Speak for Themselves";
    3 wide (~21:9) featured project cards (IMG-12 a/b/c: house · deck-or-interior ·
    commercial), each titled "{Project} — {Category}"; "EXPLORE GALLERY" CTA.
    Alt pattern when the client has verified pairs: BEFORE/AFTER (same angle, same
    light) — the `.baslider` drag slider fits here.
13. **Process steps** (dark, icons, no photos) — "How We Deliver Outstanding
    Results": 01 consultation & site inspection · 02 clear upfront quote · 03 prep &
    protect · 04 quality application · 05 final walkthrough & cleanup.
14. **Why choose us / differentiators** — kicker "THE {COMPANY} DIFFERENCE", H2 "Why
    Choose the Best Painters in {City, ST}"; center IMG-13 (interior cutting-in,
    clean site) between 4 cards from their actual claims.
15. **FAQ** (no photos) — two-column, 8 items, first open; answers are substantive
    SEO content. ⚠ Copy check: FAQs must name THIS client's real city/state — a
    draft once shipped asking "What areas do you serve in Indiana?" on a Florida site.
16. **Blog / resources** — "Expert Painting Advice for {City} Homeowners"; 3 article
    cards (IMG-14 a/b/c) — thumbnails must match each article's topic AND the trade
    (no interior photos on a roofing article).
17. **Service areas + map** (dark) — "Proudly Serving {City} and Surrounding Areas";
    chips = the client's REAL towns, linking to the area pages ("Painters in
    {City}"); below: live Google Maps embed centered on their actual city (IMG-15 —
    always re-center per client), then an inline "Get Your Free Estimate Today" form.
18. **Footer** — logo, company links, residential-services column, commercial-services
    column; contact bar (phone ✉ email 📍 address); copyright ending in "— Design
    mockup." + "Designed & managed by Paint & Profits".
19. **Mobile call bar** (`.callbar`) — fixed bottom Call Now / Free Quote (< 920px).

## Area pages (3 per site)

Each area page must have a genuinely different angle — what makes painting (or roofing,
etc.) in THAT city different: its housing stock, its rules, its climate quirk. TPG
example: Scottsdale = HOA submittals; Arcadia = painted brick + mid-century ranches;
Gilbert = chalking builder-grade stucco. If you can't name the local angle, research the
city's housing stock before writing. Never city-swap one template — thin duplicates are
SEO-useless and clients notice.

Structure: breadcrumb → subhero (H1 "Trade In {City}", city preselected in form) →
trust strip → local-angle split (prose + photo) → neighbourhood grid (8 real
neighbourhoods) → 3 "what we do differently here" cards → 4 city-specific FAQs →
related-pages cards → CTA → footer.

## Service page (1+ per site)

Flagship service (the one with the most search volume / their specialty). Structure:
breadcrumb → subhero (service preselected in form) → trust → "why this fails / how we
do it" prose split with included-scope checklist → substrate/variant grid (6 cards) →
3 scope tiers (`.pricing`, labeled as illustrative, NEVER fake dollar prices) →
5 FAQs → related cards → CTA.

## The quote form (every page)

Header "Get In Touch With Us / Enter your contact information below" (matches the
pattern of real lead-gen contractor sites). Fields: First/Last, Phone, Email, Service
select, City select, optional details textarea. Preselect the page's city/service.
Submitting swaps to a confirmation state (no backend). Include the fine-print consent
line and the Licensed·Bonded·Insured footer strip.

## Re-theming style.css for a new brand

The stylesheet uses semantic slots — set them to the brand's colors whatever the hues:

```css
--navy  : the brand's DARK color   (nav text, dark sections, footers)
--red   : the brand's ACCENT color (CTAs, links, icons)
```

Also find-and-replace the hardcoded accent hexes that live inside inline SVG strokes
and rgba() shadows: `#B91C1C` (accent), `#F87171` (accent-light on dark), `#0F2444`
(dark), `rgba(185,28,28,` (accent shadows). Grep for them after re-theming:
`grep -c 'B91C1C' *.html assets/style.css` should return 0 for a non-red brand.

## Delivery checklist

1. `python3 scripts/validate_site.py <site-dir>` → ALL PAGES OK
2. Serve on localhost via `.claude/launch.json` (python3 -m http.server on a free
   port, `--directory` at the site dir) — file:// pages can't be screenshotted and
   cross-page links behave differently.
3. Screenshot the served home page top; confirm logo, colors, hero photo render.
4. Send the HTML files to the user with SendUserFile and give them the localhost URLs
   in a table.
