# Wireframe Handoff — the design DNA

The canonical homepage design every Instant Website build follows. Colors are never
part of the wireframe (they come from each client's brand); the **structure is fixed**
— extras like financing banners may be added between sections, but sections are never
removed or reordered.

| File | What it is |
|---|---|
| `wireframe-painting-homepage.svg` | The annotated wireframe — 18 numbered sections, hatched boxes = photo slots (IMG-01…IMG-15) |
| `wireframe_render.png` | Same wireframe as a PNG for quick viewing |
| `wireframe-viewer.html` | Standalone browser viewer for the wireframe |
| `photo_slots.json` | The 16 photo-slot specs: subject, framing, minimum size, do/don'ts, and when stock is allowed vs. client-photo-required (incl. IMG-16 roofing swaps) |
| `Photo-Direction-Image-Map.pdf` / `.pptx` | The Photo Direction deck — one slide per IMG slot with full prompts and examples |

A build-ready HTML implementation of this wireframe lives at
[`../skill/templates/home-wireframe.html`](../skill/templates/home-wireframe.html).
Area and service page templates: `skill/templates/area-page.html` and
`skill/templates/service-page.html`. Replace those three files in place when
new designs land. Each client build is isolated under `builds/<slug>/`
(see `skill/references/build-layout.md`).
