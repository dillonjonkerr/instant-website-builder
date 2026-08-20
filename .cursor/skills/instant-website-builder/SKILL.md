---
name: instant-website-builder
description: Build a pitch-ready mockup website for a local service business from a website URL or Google Business Profile. Harvests contact, photos, services, and cities into an isolated per-company folder; asks for an optional info dump and extra photos (Drive, chat, or skip with labeled SAMPLE images); then builds home + all service pages + all area pages on the Paint & Profits wireframe with SEO titles and image alt text. Use when the user types /instant-website-builder or /Instant Website Builder, pastes a company URL or GBP, or asks for a mockup / example / instant website for a contractor.
---

# Instant Website Builder (Cursor)

You are running inside the **instant-website-builder** repo. Follow the
playbook in `skill/SKILL.md` immediately — do not improvise a different
site structure.

1. Read `skill/SKILL.md` and `skill/references/build-layout.md`.
2. Scaffold `builds/<slug>/` with `python3 skill/scripts/new_build.py …`.
3. Harvest the URL or GBP into that folder's `00-intake/`.
4. **Stop and ask** for an optional info dump (`skip` allowed).
5. **Stop and ask** for extra photos — Drive, chat, or `skip` (labeled SAMPLE fills).
6. Build from `skill/templates/` onto the wireframe: home + every service page
   + every area page, SEO titles, alt text, one folder per company.
7. `python3 skill/scripts/validate_site.py builds/<slug>/03-site --require-alt`

Human operator steps: `skill/SOP.md`.
New HTML templates from Dillon replace files in `skill/templates/` in place.
