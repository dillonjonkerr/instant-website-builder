#!/usr/bin/env python3
"""WORKED EXAMPLE — area + service page generator (TPG Paints & Stains, AZ).

How to use this file for a new company:
  1. Do NOT generate into a shared folder. Scaffold with scripts/new_build.py.
  2. This file is the TPG quality bar for area/service copy — rewrite every
     content dict; never copy TPG photos or TPG sentences onto another client.
  3. New builds copy templates/area-page.html and templates/service-page.html
     into 03-site/areas/ and 03-site/services/.

Relies on assets/style.css from this skill (same class names).
"""
import os

OUT = '/Users/dillonjonker/Mockup'          # company build folder
HOME = 'tpg-paints-mockup.html'             # home page filename
PHONE_T = '+16028839259'                    # tel: format
PHONE_D = '(602) 883-9259'                  # display format

STARS = ''.join(['<svg viewBox="0 0 24 24"><path d="M12 2l3 6.5 7 .9-5 4.8 1.2 7L12 18l-6.2 3.2L7 14.2l-5-4.8 7-.9z"/></svg>'] * 5)
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="#B91C1C" stroke-width="2.9"><path d="M5 12h13M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_W = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fff" stroke-width="2.7"><path d="M5 12h13M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fff" stroke-width="2.2"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.7.7a2 2 0 011.8 2.1z" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHECK_G = '<svg viewBox="0 0 24 24" fill="none" stroke="#4ADE80" stroke-width="2.6"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHECK_R = '<svg viewBox="0 0 24 24" fill="none" stroke="#B91C1C" stroke-width="2.6"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="#B91C1C" stroke-width="2.4"><path d="M12 22s8-4.5 8-11a8 8 0 10-16 0c0 6.5 8 11 8 11z" stroke-linejoin="round"/></svg>'
TICK = '<i class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.4"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg></i>'

CITY_OPTS = ['Scottsdale', 'Arcadia', 'Chandler', 'Gilbert', 'Mesa', 'Tempe',
             'Surprise', 'Goodyear', 'Cave Creek', 'Other Arizona City']


def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
'''


TOPBAR = f'''
<div class="ubar">
  <div class="wrap">
    <ul>
      <li><i class="blip"></i> <b>Licensed, Bonded &amp; Insured</b></li>
      <li><span class="stars">{STARS}</span> 5.0 Rated by Arizona Homeowners</li>
      <li>Free Color Consultation On Every Job</li>
    </ul>
    <ul><li><b>Residential Repaint Specialist</b> &mdash; Serving All of Arizona</li></ul>
  </div>
</div>
'''


def nav():
    return f'''
<nav class="nav">
  <div class="wrap">
    <a href="{HOME}" class="nav-logo"><img src="assets/logo.png" alt="TPG Paints &amp; Stains LLC"></a>
    <div class="menu">
      <div class="dd">
        <a href="exterior-painting.html">Services
          <svg class="caret" viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 1l5 5 5-5" stroke-linecap="round"/></svg>
        </a>
        <div class="dd-menu">
          <a href="exterior-painting.html">Exterior Painting<small>Stucco, block, siding, trim &amp; painted brick</small></a>
          <a href="{HOME}#services">Interior Painting<small>Walls, ceilings, trim &amp; doors</small></a>
          <a href="{HOME}#services">Residential Painting<small>Whole-home interior &amp; exterior packages</small></a>
          <a href="{HOME}#services">Commercial Painting<small>Offices, retail, HOAs &amp; multi-unit</small></a>
          <hr>
          <a href="exterior-painting.html#faq" class="dd-all">Best Paint For Arizona &rarr;</a>
        </div>
      </div>
      <div class="dd">
        <a href="{HOME}#areas">Areas
          <svg class="caret" viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 1l5 5 5-5" stroke-linecap="round"/></svg>
        </a>
        <div class="dd-menu">
          <a href="painters-scottsdale-az.html">Painters in Scottsdale<small>HOA submittals handled</small></a>
          <a href="painters-arcadia-az.html">Painters in Arcadia<small>Painted brick &amp; ranch specialists</small></a>
          <a href="painters-gilbert-az.html">Painters in Gilbert<small>Stucco repaint specialists</small></a>
          <hr>
          <a href="{HOME}#areas" class="dd-all">All Service Areas &rarr;</a>
        </div>
      </div>
      <a href="{HOME}#work">Projects</a>
      <a href="{HOME}#why">Why Us</a>
      <a href="#faq">FAQ</a>
    </div>
    <div class="nav-right">
      <a href="tel:{PHONE_T}" class="nav-ph"><small>Call or Text</small><strong>{PHONE_D}</strong></a>
      <a href="#quote" class="btn btn-red">Free Quote</a>
    </div>
    <button class="burger" aria-label="Menu"><i></i><i></i><i></i></button>
  </div>
</nav>
'''


def crumb(trail):
    parts = [f'<a href="{HOME}">Home</a>']
    for label, href in trail[:-1]:
        parts.append('<span>/</span>')
        parts.append(f'<a href="{href}">{label}</a>')
    parts.append('<span>/</span>')
    parts.append(f'<span>{trail[-1][0]}</span>')
    return f'<div class="crumb"><div class="wrap">{"".join(parts)}</div></div>\n'


def form(city_sel=None, service_sel=None, heading='Get In Touch With Us',
         sub='Enter your contact information below'):
    svcs = ['Interior Painting', 'Exterior Painting', 'Interior + Exterior',
            'Cabinets &amp; Staining', 'Commercial Painting', 'Not Sure &mdash; Need a Recommendation']
    sopts = ''.join(f'<option{" selected" if s == service_sel else ""}>{s}</option>' for s in svcs)
    copts = ''.join(f'<option{" selected" if c == city_sel else ""}>{c}</option>' for c in CITY_OPTS)
    return f'''    <div class="quote" id="quote">
      <div class="quote-hd"><h2>{heading}</h2><p>{sub}</p></div>
      <form class="quote-bd" id="qform" novalidate>
        <div class="frow">
          <div class="fld"><label for="fn">First Name</label><input id="fn" type="text" placeholder="First Name" required></div>
          <div class="fld"><label for="ln">Last Name</label><input id="ln" type="text" placeholder="Last Name" required></div>
        </div>
        <div class="frow">
          <div class="fld"><label for="ph">Phone</label><input id="ph" type="tel" placeholder="(123) 456-7890" required></div>
          <div class="fld"><label for="em">Email</label><input id="em" type="email" placeholder="you@company.com" required></div>
        </div>
        <div class="fld"><label for="sv">Select Your Service</label><select id="sv">{sopts}</select></div>
        <div class="fld"><label for="ct">City</label><select id="ct">{copts}</select></div>
        <div class="fld"><label for="ds">Project Details <span style="text-transform:none;letter-spacing:0;font-weight:600">(optional)</span></label>
          <textarea id="ds" placeholder="Two-story stucco, west-facing walls badly faded, plus 4 bedrooms inside..."></textarea></div>
        <button type="submit" class="btn btn-red btn-block">Get My Free Quote {ARROW_W}</button>
        <p class="fine">By submitting you agree to be contacted about your project. We never share your info.</p>
      </form>
      <div class="sent" id="qsent">
        <div class="sent-ic">{CHECK_R}</div>
        <h3>Request Received</h3>
        <p>Thanks! A TPG estimator will reach out shortly to schedule your walkthrough and free color consultation.</p>
      </div>
      <div class="quote-ft">
        <svg viewBox="0 0 24 24" fill="none" stroke="#0F2444" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-linejoin="round"/></svg>
        Licensed &middot; Bonded &middot; Insured in the State of Arizona
      </div>
    </div>
'''


def subhero(h1, em, sub, bullets, img, alt, city_sel=None, service_sel=None):
    bl = '\n'.join(f'        <li>{TICK}{b}</li>' for b in bullets)
    return f'''
<header class="subhero">
  <img class="hero-img" src="assets/{img}" alt="{alt}">
  <div class="hero-scrim"></div>
  <div class="wrap">
    <div class="hero-copy">
      <div class="pill-row">
        <span class="pill">{CHECK_G} Always On Time</span>
        <span class="pill">{CHECK_G} Licensed &amp; Insured</span>
        <span class="pill">{CHECK_G} Site Left Clean</span>
      </div>
      <h1>{h1} <em>{em}</em></h1>
      <span class="tag">Best In The West &mdash; Better Than The Rest</span>
      <p class="sub">{sub}</p>
      <ul class="hlist">
{bl}
      </ul>
      <div class="hero-act">
        <a href="#quote" class="btn btn-red">Get My Free Estimate {ARROW_W}</a>
        <a href="tel:{PHONE_T}" class="btn btn-ghost">{PHONE_SVG} {PHONE_D}</a>
      </div>
    </div>
{form(city_sel, service_sel)}  </div>
</header>
'''


TRUST_ITEMS = [
    ('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2" stroke-linecap="round"/>', 'Always On Time'),
    ('<path d="M17 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2" stroke-linecap="round"/><circle cx="9.5" cy="7" r="4"/><path d="M22 21v-2a4 4 0 00-3-3.9" stroke-linecap="round"/>', 'Trusted By Homeowners'),
    ('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" stroke-linecap="round"/>', 'Licensed, Bonded &amp; Insured'),
    ('<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2" stroke-linecap="round"/>', 'Free Color Consultation'),
    ('<path d="M4 20l6-6M13 3l8 8-9 9H4v-8z" stroke-linecap="round" stroke-linejoin="round"/>', 'Paint Job Site Left Clean'),
    ('<path d="M12 3l2.4 5.4 5.6.6-4.2 3.9 1.1 5.6L12 15.8 7.1 18.5l1.1-5.6L4 9l5.6-.6z" stroke-linejoin="round"/>', 'High Quality Materials'),
]
TRUST = '<div class="trust"><div class="wrap">' + ''.join(
    f'<div class="tcell"><div class="tcell-ic"><svg viewBox="0 0 24 24" fill="none" stroke="#B91C1C" stroke-width="2.2">{p}</svg></div><b>{t}</b></div>'
    for p, t in TRUST_ITEMS) + '</div></div>\n'


def faq(items, h2):
    qs = ''.join(
        f'      <details class="qa"{" open" if i == 0 else ""}><summary>{q}</summary>\n        <p>{a}</p></details>\n'
        for i, (q, a) in enumerate(items))
    return f'''
<section class="sec" id="faq">
  <div class="wrap">
    <div class="sec-head center"><div class="eyebrow">Common Questions</div><h2>{h2}</h2></div>
    <div class="faq">
{qs}    </div>
  </div>
</section>
'''


def related(cards, title='Explore More'):
    cs = ''.join(
        f'      <a class="rel" href="{h}"><b>{t}</b><p>{d}</p><span>View page {ARROW}</span></a>\n'
        for t, d, h in cards)
    return f'''
<section class="sec sec-gray">
  <div class="wrap">
    <div class="sec-head center"><div class="eyebrow">Keep Looking</div><h2>{title}</h2></div>
    <div class="rel-grid">
{cs}    </div>
  </div>
</section>
'''


def cta(h2, p):
    return f'''
<section class="cta">
  <div class="wrap">
    <div><h2>{h2}</h2><p>{p}</p></div>
    <div class="cta-act">
      <a href="#quote" class="btn btn-white">Get My Free Quote</a>
      <a href="tel:{PHONE_T}" class="btn btn-ghost">{PHONE_SVG} {PHONE_D}</a>
    </div>
  </div>
</section>
'''


FOOTER = f'''
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <span class="flogo"><img src="assets/logo.png" alt="TPG Paints &amp; Stains LLC"></span>
        <p class="fabout">Arizona&rsquo;s premier painting service. Professional interior, exterior, residential, and
          commercial house painting built for Arizona&rsquo;s climate &mdash; from free color consultation through final cleanup.</p>
        <div class="fbadges"><span class="fbadge">Licensed</span><span class="fbadge">Bonded</span><span class="fbadge">Insured</span></div>
      </div>
      <div><h4>Services</h4>
        <div class="flist">
          <a href="{HOME}#services">Interior Painting</a><a href="exterior-painting.html">Exterior Painting</a>
          <a href="{HOME}#services">Residential Painting</a><a href="{HOME}#services">Commercial Painting</a>
          <a href="{HOME}#paint-guide">Best Paint For Arizona</a>
        </div></div>
      <div><h4>Service Areas</h4>
        <div class="flist">
          <a href="painters-scottsdale-az.html">Painters in Scottsdale</a>
          <a href="painters-arcadia-az.html">Painters in Arcadia</a>
          <a href="painters-gilbert-az.html">Painters in Gilbert</a>
          <a href="{HOME}#areas">Mesa &amp; Tempe</a>
          <a href="{HOME}#areas">Surprise &amp; Goodyear</a>
          <a href="{HOME}#areas">Cave Creek</a>
        </div></div>
      <div><h4>Get In Touch</h4>
        <div class="fcon">
          <a href="tel:{PHONE_T}"><svg viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2.2"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.7.7a2 2 0 011.8 2.1z" stroke-linecap="round" stroke-linejoin="round"/></svg><span><b>{PHONE_D}</b><br>Call or text</span></a>
          <a href="mailto:contact@thepaintguysaz.com"><svg viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2.2"><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M3 6l9 6.5L21 6" stroke-linecap="round"/></svg><span>contact@thepaintguysaz.com</span></a>
          <span><svg viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2.2"><path d="M12 22s8-4.5 8-11a8 8 0 10-16 0c0 6.5 8 11 8 11z" stroke-linejoin="round"/><circle cx="12" cy="11" r="2.6"/></svg><span>Arizona, United States</span></span>
          <span><svg viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2" stroke-linecap="round"/></svg><span>Mon&ndash;Sat, 7:00am &ndash; 6:00pm</span></span>
        </div></div>
    </div>
    <div class="fbot">
      <span>&copy; 2026 TPG Paints &amp; Stains LLC. All rights reserved. &mdash; Design mockup.</span>
      <span><a href="#">Privacy Policy</a><a href="#">Terms</a><a href="#quote">Free Quote</a></span>
    </div>
  </div>
</footer>

<div class="callbar">
  <a href="tel:{PHONE_T}" class="btn btn-navy">{PHONE_SVG} Call Now</a>
  <a href="#quote" class="btn btn-red">Free Quote</a>
</div>

<script>
document.getElementById('qform').addEventListener('submit', function(e){{
  e.preventDefault();
  var ok = true;
  this.querySelectorAll('[required]').forEach(function(f){{
    if(!f.value.trim()){{ f.style.borderColor = '#D02D27'; ok = false; }} else {{ f.style.borderColor = ''; }}
  }});
  if(!ok) return;
  this.style.display = 'none';
  document.getElementById('qsent').classList.add('on');
}});
</script>

</body>
</html>
'''


def nb_grid(names):
    return '<div class="nb-grid">' + ''.join(
        f'<span class="nb">{PIN} {n}</span>' for n in names) + '</div>'


def lp_grid(items):
    return '<div class="lp-grid">' + ''.join(
        f'<div class="lp"><b>{t}</b><p>{d}</p></div>' for t, d in items) + '</div>'


# ══════════════════════════════════════════════════════════════════════
# AREA PAGES — every dict below is company-specific content. Rewrite all
# of it for a new company; the structure (keys) is what you keep.
# ══════════════════════════════════════════════════════════════════════
AREAS = [
  dict(
    slug='painters-scottsdale-az.html', city='Scottsdale',
    title='House Painters in Scottsdale, AZ | Interior &amp; Exterior Painting Company | TPG',
    desc='Top-rated house painters in Scottsdale, AZ. Local painting company for interior and exterior house painting — HOA-compliant color submittals, licensed, bonded &amp; insured. Free color consultation.',
    h1='House Painters In', em='Scottsdale, AZ',
    img='hero-home.jpg', alt='Freshly painted Scottsdale home at twilight',
    sub='Searching for a house painter near you in Scottsdale? TPG Paints &amp; Stains is a local, '
        'Arizona-owned painting company that handles the HOA paperwork, the brutal west-facing sun exposure, '
        'and the finish detail Scottsdale homes are held to.',
    bullets=[
      'HOA color submittals prepared and submitted for you &mdash; we do this weekly',
      'Desert-contemporary and Santa Fe palettes matched to Scottsdale&rsquo;s light',
      'Gated-community access, badging, and quiet-hours scheduling handled',
    ],
    intro_h2='The Scottsdale Painting Company That Knows The HOA Rules',
    intro=[
      'Scottsdale is the toughest city in the Valley to paint &mdash; not because of the walls, but because of the '
      'paperwork. Most communities here run an architectural review committee with an approved palette, and a '
      'repaint started without an approved submittal can get red-tagged mid-job. We prepare and file the submittal '
      'for you, including body, trim, and pop-out colors with manufacturer codes and LRV values.',
      'On the technical side, Scottsdale&rsquo;s housing stock is mostly stucco over block or frame, and the '
      'west and south elevations take a beating. Homes along the McDowell corridor and up in Troon see reflected '
      'heat off granite landscaping that can push surface temps well past air temperature. That changes both which '
      'sheen we recommend and which months we&rsquo;ll agree to spray an exterior.',
    ],
    intro_h3='What Scottsdale Homes Usually Need',
    intro_list=[
      '<b>Stucco crack repair and re-texture</b> &mdash; hairline settling cracks bridged before primer, matched to existing knockdown or sand finish.',
      '<b>Pop-out and parapet detail</b> &mdash; the trim bands and parapet caps that fail first on desert-contemporary elevations.',
      '<b>Iron and gate refinishing</b> &mdash; courtyard gates, railings, and view fencing rust-treated and recoated.',
      '<b>Garage door and front-door refinish</b> &mdash; the two surfaces that take the most direct afternoon sun.',
    ],
    nbs=['Old Town Scottsdale', 'McCormick Ranch', 'DC Ranch', 'Gainey Ranch',
         'Troon North', 'Grayhawk', 'Silverleaf', 'North Scottsdale'],
    lps=[
      ('HOA Submittals Handled', 'We prepare the color submittal package with manufacturer codes and LRV values, '
       'file it with your architectural committee, and wait for written approval before we schedule the spray days.'),
      ('Gated Access, Sorted', 'Guard-gate lists, contractor badging, vehicle registration, and quiet-hours '
       'windows &mdash; we&rsquo;ve worked inside most of the gated communities in North Scottsdale.'),
      ('Built For West Exposure', 'Higher-LRV colors and UV-stable pigments on the elevations that get hammered, '
       'so your north side and your west side still match in year six.'),
    ],
    faq_h2='Scottsdale House Painting FAQ',
    faqs=[
      ('Do you handle the HOA approval for my Scottsdale repaint?',
       'Yes, and we&rsquo;d strongly recommend letting us. We build the submittal package &mdash; body, trim, '
       'pop-out, and door colors with manufacturer names, codes, and light reflectance values &mdash; and file it '
       'with your architectural review committee. We don&rsquo;t schedule spray days until approval comes back in '
       'writing, which protects you from a red-tag and a repaint at your own cost.'),
      ('How much does it cost to paint a house in Scottsdale?',
       'Exterior repaints on typical Scottsdale single-family homes generally land in a wide range depending on '
       'square footage, story count, stucco condition, and how much iron and trim detail is involved. A '
       'two-story home needing crack repair and elastomeric will sit well above a single-story in sound '
       'condition. We measure on site and give you an itemized number rather than a per-square-foot guess.'),
      ('When is the best time of year to paint an exterior in Scottsdale?',
       'October through April. Once surface temperatures climb past about 90&deg;F the paint film flashes off too '
       'quickly to level and adhere properly, which shortens its life significantly. We do book summer exteriors, '
       'but we shift to early mornings and chase the shade around the house.'),
      ('Can you match the desert-contemporary colors used in my community?',
       'Yes. Most Scottsdale communities publish an approved palette, and we can pull from it or colour-match an '
       'existing body colour off a clean chip from your wall. During the free color consultation we&rsquo;ll put '
       'large samples up on the actual elevation, because desert light changes a colour dramatically between a '
       'fan deck indoors and a west wall at 4pm.'),
    ],
    close_h2='Ready For A Scottsdale Repaint Done Properly?',
    close_p='Free, no-pressure estimate and color consultation from a licensed, bonded, and insured '
            'Scottsdale painting crew that handles your HOA submittal and shows up on time.',
  ),
  dict(
    slug='painters-arcadia-az.html', city='Arcadia',
    title='House Painters in Arcadia, AZ | Painted Brick &amp; Ranch Home Specialists | TPG',
    desc='House painters in Arcadia, AZ specializing in painted brick, historic ranch homes, and exterior repaints. Licensed, bonded &amp; insured local painting company. Free color consultation.',
    h1='House Painters In', em='Arcadia, AZ',
    img='after-white.jpg', alt='Painted white brick Arcadia ranch home with dark trim',
    sub='Arcadia is brick, block, and mid-century ranch &mdash; and it is the neighbourhood where a bad paint '
        'job shows most. TPG Paints &amp; Stains specialises in painted brick, historic trim detail, and the '
        'crisp white-and-black exteriors Arcadia is known for.',
    bullets=[
      'Painted brick done correctly &mdash; masonry primer, breathable coatings, no peeling',
      'Mid-century and ranch trim detail: fascia, soffit, beams, and steel windows',
      'Mature citrus and landscaping protected, not trampled',
    ],
    intro_h2='Arcadia&rsquo;s Painted Brick And Ranch Home Specialists',
    intro=[
      'Arcadia&rsquo;s housing stock is different from the rest of the Valley: 1950s and 60s brick ranches on '
      'big irrigated lots, mature citrus, and a steady stream of remodels turning red brick into crisp white '
      'or deep charcoal. That transformation is the single most requested job we do here &mdash; and the one '
      'most often done wrong by crews who treat brick like stucco.',
      'Brick is porous and it needs to breathe. Seal it with the wrong film and trapped moisture pushes the '
      'paint off in sheets within a couple of seasons, taking the brick face with it. We use a masonry-specific '
      'conditioner and a breathable mineral or high-quality acrylic system, and we never paint brick that is '
      'still damp from irrigation or a wash.',
    ],
    intro_h3='What Arcadia Homes Usually Need',
    intro_list=[
      '<b>Painted brick conversions</b> &mdash; full wash, mortar repointing where needed, masonry conditioner, then a breathable finish coat.',
      '<b>Original steel window refinishing</b> &mdash; rust treatment and enamel on the mid-century steel casements worth keeping.',
      '<b>Fascia, soffit, and exposed beam work</b> &mdash; the wood detail on ranch rooflines that fails first under irrigation humidity.',
      '<b>Interior plaster and lath care</b> &mdash; older wall substrates that need patching and the right primer, not just two coats over cracks.',
    ],
    nbs=['Arcadia Proper', 'Arcadia Lite', 'Camelback East', 'Biltmore',
         'Royal Palm', 'Camelback Corridor', 'Ingleside', 'Phoenix Country Club'],
    lps=[
      ('Brick That Stays Painted', 'Masonry conditioner and breathable coatings, applied only to dry substrate. '
       'That is the whole difference between a painted-brick exterior that lasts a decade and one that flakes in year two.'),
      ('Respect For Original Detail', 'Steel casements, exposed beams, and period trim profiles get hand-worked, '
       'not sprayed over. If it is worth keeping, it is worth masking properly.'),
      ('Your Citrus Survives', 'Mature trees and flood-irrigated lawns get covered and worked around. '
       'We schedule around irrigation days so we are never painting a wet wall.'),
    ],
    faq_h2='Arcadia House Painting FAQ',
    faqs=[
      ('Should I paint my Arcadia brick house?',
       'It is a genuinely permanent decision, so it is worth thinking about &mdash; painted brick cannot easily '
       'be returned to bare brick without aggressive stripping that can damage the face. That said, done '
       'properly it is one of the highest-impact exterior changes available, and it is extremely common in '
       'Arcadia now. If you want the look, the thing that matters is the system: masonry conditioner, a '
       'breathable topcoat, and dry substrate. Skip any of those and it will fail.'),
      ('Will painted brick peel in Arizona?',
       'Only if it is done wrong. Brick needs to release moisture; if you trap it under a non-breathable film, '
       'vapour pressure pushes the coating off and can spall the brick face. We use masonry-specific primers '
       'and breathable finish systems, and on flood-irrigated Arcadia lots we schedule around irrigation so we '
       'are never coating a saturated wall.'),
      ('Can you match the original trim colours on a mid-century ranch?',
       'Yes. We can colour-match from a clean chip, and if you want to stay period-appropriate we can pull from '
       'documented mid-century palettes. Most Arcadia remodels go the other direction &mdash; white or '
       'off-white body with black or bronze trim and a wood front door &mdash; and we do a lot of those.'),
      ('Do you work around mature citrus and flood irrigation?',
       'Constantly. Arcadia lots are full of established trees and many are still on flood irrigation. We tarp '
       'and protect landscaping, keep overspray controlled, and plan the schedule around your irrigation turn '
       'so walls have time to dry before we coat them.'),
    ],
    close_h2='Thinking About Painted Brick In Arcadia?',
    close_p='Free, no-pressure estimate and color consultation from a licensed, bonded, and insured local '
            'crew that has painted a lot of Arcadia brick &mdash; correctly.',
  ),
  dict(
    slug='painters-gilbert-az.html', city='Gilbert',
    title='House Painters in Gilbert, AZ | Stucco Repaint Specialists | TPG Paints &amp; Stains',
    desc='House painters in Gilbert, AZ. Stucco repaint specialists for Agritopia, Seville, Morrison Ranch, Power Ranch and more. Licensed, bonded &amp; insured. Free color consultation.',
    h1='House Painters In', em='Gilbert, AZ',
    img='before-brick.jpg', alt='Two-story Gilbert home prepped and masked for exterior painting',
    sub='Gilbert is full of 1998&ndash;2015 stucco tract homes hitting the age where the original builder '
        'paint has given up. TPG Paints &amp; Stains is the stucco repaint specialist Gilbert homeowners call '
        'when the south wall has gone chalky.',
    bullets=[
      'Builder-grade stucco repaints &mdash; the most common job in Gilbert, and our specialty',
      'Chalk testing and masonry conditioner so the new coat actually bonds',
      'HOA palettes for Agritopia, Seville, Power Ranch, Morrison Ranch and more',
    ],
    intro_h2='Gilbert&rsquo;s Stucco Repaint Specialists',
    intro=[
      'If your Gilbert home was built between the late 1990s and the mid 2010s, it almost certainly went up '
      'with a single coat of builder-grade paint over new stucco. That coating typically starts failing '
      'somewhere between year eight and year twelve &mdash; chalky to the touch on the south and west walls, '
      'faded pop-outs, and hairline cracks around windows where the stucco settled.',
      'The critical step on these homes is a chalk test. Rub the wall; if your hand comes away powdery, the '
      'original coating has oxidised and nothing will bond to it until it is washed and sealed with a masonry '
      'conditioner. Crews that skip this step and just spray two coats over chalk produce a job that looks '
      'perfect for one year and then peels in sheets. It is the single most common failure we get called in to fix.',
    ],
    intro_h3='What Gilbert Homes Usually Need',
    intro_list=[
      '<b>Chalk test and masonry conditioner</b> &mdash; non-negotiable on any home with original builder paint.',
      '<b>Hairline crack bridging</b> &mdash; settlement cracks around windows and at wall transitions, sealed and re-textured.',
      '<b>Pop-out and fascia refresh</b> &mdash; the trim bands and fascia that fade a shade or two faster than the body.',
      '<b>Garage door and shutter recoat</b> &mdash; the most sun-hammered surfaces on a typical Gilbert elevation.',
    ],
    nbs=['Agritopia', 'Seville', 'Power Ranch', 'Morrison Ranch',
         'Val Vista Lakes', 'Layton Lakes', 'The Islands', 'Higley Groves'],
    lps=[
      ('We Chalk Test Every Time', 'Before we quote, we test the existing coating. If it is chalking, the '
       'quote includes a wash and masonry conditioner &mdash; because without it, the new paint has nothing to grip.'),
      ('HOA Palettes On File', 'Agritopia, Seville, Power Ranch, Morrison Ranch and the rest all run approved '
       'colour lists. We know the process and prepare your submittal as part of the job.'),
      ('Whole-Street Efficiency', 'A lot of our Gilbert work comes from neighbours seeing the crew next door. '
       'Ask about scheduling alongside a neighbour &mdash; same mobilisation, better pricing for both of you.'),
    ],
    faq_h2='Gilbert House Painting FAQ',
    faqs=[
      ('How do I know if my Gilbert stucco needs a full repaint?',
       'Rub your hand firmly on a south- or west-facing wall. If it comes away with chalky powder, the original '
       'coating has oxidised and is at the end of its life. Other signs: the body colour on the sun-facing walls '
       'no longer matches the north side, hairline cracks are opening around windows, or you can see the '
       'texture through thin spots. Most builder-grade paint in Gilbert reaches this point between years eight and twelve.'),
      ('What is a chalk test and why does it matter so much?',
       'It is exactly what it sounds like &mdash; rubbing the wall to see whether the old coating has degraded '
       'into powder. It matters because paint cannot bond to chalk. If a crew sprays fresh paint over a chalking '
       'wall without washing and applying a masonry conditioner, the new coating will look great for a season '
       'and then peel away in sheets, taking your money with it. We test before quoting, every time.'),
      ('Do you handle my Gilbert community&rsquo;s HOA colour approval?',
       'Yes. Agritopia, Seville, Power Ranch, Morrison Ranch, Layton Lakes and most other Gilbert communities '
       'maintain an approved palette and require a submittal before exterior work. We prepare the package and '
       'file it, and we wait for written approval before scheduling.'),
      ('Can you paint my house while we&rsquo;re still living in it?',
       'For exteriors, absolutely &mdash; you will just want to keep windows closed on spray days and move '
       'vehicles off the driveway. For interiors we work room by room with everything masked and covered, using '
       'low-VOC products so the family and pets stay comfortable throughout.'),
    ],
    close_h2='Gilbert Stucco Looking Chalky?',
    close_p='Free, no-pressure estimate with a chalk test included, plus a color consultation and your HOA '
            'submittal handled by a licensed, bonded, and insured local crew.',
  ),
]

for a in AREAS:
    others = [x for x in AREAS if x['slug'] != a['slug']]
    rel_cards = [(f"Painters in {o['city']}", f"Local house painting crews serving {o['city']} and the surrounding communities.", o['slug']) for o in others]
    rel_cards.append(('Exterior Painting in Arizona',
                      'Stucco, block, siding, trim, and painted brick &mdash; our full exterior process explained.',
                      'exterior-painting.html'))
    html = (head(a['title'], a['desc']) + TOPBAR + nav()
            + crumb([('Service Areas', f'{HOME}#areas'), (f"Painters in {a['city']}", '')])
            + subhero(a['h1'], a['em'], a['sub'], a['bullets'], a['img'], a['alt'], city_sel=a['city'])
            + TRUST
            + f'''
<section class="sec">
  <div class="wrap split">
    <div class="prose">
      <div class="eyebrow">{a['city']}, Arizona</div>
      <h2 style="margin-top:11px">{a['intro_h2']}</h2>
      {''.join(f'<p>{p}</p>' for p in a['intro'])}
      <h3>{a['intro_h3']}</h3>
      <ul>{''.join(f'<li>{i}</li>' for i in a['intro_list'])}</ul>
    </div>
    <div class="ph">
      <span class="badge-float">{a['city']} Project</span>
      <img src="assets/{'exterior-inprogress.jpg' if a['city'] != 'Arcadia' else 'after-white.jpg'}" alt="TPG house painting project in {a['city']}, Arizona">
      <div class="ph-cap">Full prep, masking, and priming on a {a['city']} repaint before a single finish coat goes on.</div>
    </div>
  </div>
</section>

<section class="sec sec-gray">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Neighbourhoods We Serve</div>
      <h2>House Painting Across {a['city']}</h2>
      <p>Local crews covering {a['city']} and the surrounding communities. Don&rsquo;t see your neighbourhood? Call us &mdash; we likely cover it.</p>
    </div>
    {nb_grid(a['nbs'])}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Why {a['city']} Chooses TPG</div>
      <h2>What We Do Differently Here</h2>
    </div>
    {lp_grid(a['lps'])}
  </div>
</section>
'''
            + faq(a['faqs'], a['faq_h2'])
            + related(rel_cards)
            + cta(a['close_h2'], a['close_p'])
            + FOOTER)
    open(os.path.join(OUT, a['slug']), 'w', encoding='utf-8').write(html)
    print('wrote', a['slug'], len(html), 'chars')


# ══════════════════════════════════════════════════════════════════════
# SERVICE PAGE — Exterior Painting (rewrite all content per company; a
# different trade gets a different flagship service page, e.g. "Roof
# Replacement" for a roofer.)
# ══════════════════════════════════════════════════════════════════════
svc_html = (head('Exterior Painting in Arizona | Stucco, Block &amp; Painted Brick | TPG Paints &amp; Stains',
                 'Exterior house painting in Arizona. Stucco, block, siding, trim and painted brick — full prep, '
                 'masonry priming and UV-stable coatings. Licensed, bonded &amp; insured. Free color consultation.')
            + TOPBAR + nav()
            + crumb([('Services', f'{HOME}#services'), ('Exterior Painting', '')])
            + subhero('Exterior House Painting In', 'Arizona',
                      'Exterior paint in Arizona does not fail because of the paint &mdash; it fails because of the prep. '
                      'TPG Paints &amp; Stains does the wash, the crack repair, and the masonry priming that decides '
                      'whether your repaint lasts three years or ten.',
                      ['Chalk-tested and masonry-primed &mdash; so the new coat actually bonds',
                       'UV-stable pigments and LRV guidance for west-facing walls',
                       'Stucco, block, siding, trim, fascia, iron, and painted brick'],
                      'exterior-inprogress.jpg',
                      'Exterior stucco repaint in progress on an Arizona home',
                      service_sel='Exterior Painting')
            + TRUST
            + f'''
<section class="sec">
  <div class="wrap split">
    <div class="prose">
      <div class="eyebrow">Our Exterior Process</div>
      <h2 style="margin-top:11px">Why Exterior Paint Fails In Arizona &mdash; And How We Stop It</h2>
      <p>Almost every failed exterior repaint we get called to fix in the Valley failed for one of three reasons:
        the crew painted over a chalking surface, they skipped the primer on bare or patched stucco, or they
        sprayed in July when the surface was too hot for the film to level and cure. None of those are paint
        problems. They are process problems.</p>
      <p>Our exterior sequence is deliberately slow at the start. We test the existing coating, wash the whole
        envelope, repair and re-texture cracks, prime everything bare or chalky, and only then start putting
        colour on the wall. That front-loaded work is invisible in the final photos and it is the entire reason
        the job is still intact in year eight.</p>
      <h3>What&rsquo;s Included In Every Exterior Repaint</h3>
      <ul>
        <li><b>Full pressure wash</b> &mdash; the entire envelope, then dry time. We do not coat a damp wall.</li>
        <li><b>Chalk test on every elevation</b> &mdash; oxidised coating gets a masonry conditioner before anything else.</li>
        <li><b>Crack repair and re-texture</b> &mdash; hairline settlement cracks bridged and matched to your existing finish.</li>
        <li><b>Caulking and sealing</b> &mdash; window and door perimeters, penetrations, and wall transitions.</li>
        <li><b>Full masking</b> &mdash; windows, roof edges, lighting, hardware, landscaping, and hardscape.</li>
        <li><b>Two finish coats</b> &mdash; sprayed and back-rolled where the substrate calls for it.</li>
        <li><b>Joint final walkthrough</b> &mdash; touch-ups handled on the spot, site swept before we leave.</li>
      </ul>
    </div>
    <div class="ph">
      <span class="badge-float">Prep Stage</span>
      <img src="assets/before-brick.jpg" alt="Arizona home fully masked and prepped before exterior painting">
      <div class="ph-cap">Masking and prep on a two-story exterior &mdash; the stage that decides how long the finish lasts.</div>
    </div>
  </div>
</section>

<section class="sec sec-gray">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Surfaces We Coat</div>
      <h2>Exterior Painting For Every Arizona Substrate</h2>
      <p>Each substrate needs a different primer and a different system. Here&rsquo;s how we approach the ones we see most.</p>
    </div>
    {lp_grid([
      ('Stucco &amp; Synthetic Stucco', 'The Valley default. Wash, chalk test, crack bridge, masonry conditioner, '
       'then premium 100% acrylic &mdash; or elastomeric when there is real cracking to span.'),
      ('Painted Brick', 'Porous and it must breathe. Masonry conditioner plus a breathable finish system, applied '
       'only to fully dry brick. Get this wrong and it spalls the brick face.'),
      ('Block &amp; Masonry Walls', 'Boundary walls and block elevations take reflected heat off hardscape. '
       'Block filler where needed, then a high-build coating that tolerates the movement.'),
      ('Wood Fascia, Soffit &amp; Beams', 'Sanded, spot-primed on bare wood, and caulked. The detail that fails '
       'first on ranch and territorial rooflines.'),
      ('Iron, Gates &amp; Railings', 'Rust converted or removed, metal-specific primer, then a direct-to-metal '
       'enamel that will not chalk out in two summers.'),
      ('Garage &amp; Front Doors', 'The two hottest surfaces on most elevations. Sprayed for a smooth finish, '
       'in a sheen and colour chosen to handle direct afternoon sun.'),
    ])}
  </div>
</section>

<section class="sec sec-navy">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow" style="color:#F87171">Typical Scope Tiers</div>
      <h2>What An Arizona Exterior Repaint Involves</h2>
      <p>Scope tiers shown to illustrate what changes the price. Every quote is measured on site and itemised &mdash;
        these are not fixed prices.</p>
    </div>
    <div class="pricing">
      <div class="pr"><h3>Sound Single-Story</h3>
        <div class="amt">Tier 1<small> &nbsp;lowest scope</small></div>
        <ul>
          <li>{CHECK_R}Existing coating still intact, minimal chalk</li>
          <li>{CHECK_R}Wash, spot prime, caulk, two finish coats</li>
          <li>{CHECK_R}Body, trim, fascia and pop-outs</li>
          <li>{CHECK_R}Typically the fastest turnaround</li>
        </ul>
        <p class="note">Illustrative scope tier for this mockup.</p></div>
      <div class="pr feat"><h3>Chalking Or Faded</h3>
        <div class="amt">Tier 2<small> &nbsp;most common</small></div>
        <ul>
          <li>{CHECK_R}Chalking coating on sun-facing elevations</li>
          <li>{CHECK_R}Full wash plus masonry conditioner throughout</li>
          <li>{CHECK_R}Hairline crack repair and re-texture</li>
          <li>{CHECK_R}Garage doors, shutters and iron included</li>
        </ul>
        <p class="note">Illustrative scope tier for this mockup.</p></div>
      <div class="pr"><h3>Two-Story Or Distressed</h3>
        <div class="amt">Tier 3<small> &nbsp;highest scope</small></div>
        <ul>
          <li>{CHECK_R}Two-story access, staging or lifts required</li>
          <li>{CHECK_R}Significant cracking &mdash; elastomeric system</li>
          <li>{CHECK_R}Stucco patching and substantial re-texture</li>
          <li>{CHECK_R}Extensive wood, iron and detail work</li>
        </ul>
        <p class="note">Illustrative scope tier for this mockup.</p></div>
    </div>
    <div style="margin-top:38px;display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
      <a href="#quote" class="btn btn-red">Get My Itemised Quote</a>
      <a href="tel:{PHONE_T}" class="btn btn-ghost">Talk To A Painter Now</a>
    </div>
  </div>
</section>
'''
            + faq([
                ('What is the best exterior paint for Arizona?',
                 'For most Valley homes a premium 100% acrylic latex is the right answer &mdash; it stays flexible '
                 'through big temperature swings and resists UV fade far better than economy coatings. Step up to '
                 'elastomeric only when you need to bridge hairline cracking in stucco or block; it is thicker, '
                 'costlier, and unnecessary on sound walls. Beyond the product, four things decide longevity: '
                 'UV-stable pigments, a light reflectance value above roughly 55 on sun-hammered elevations, a '
                 'masonry conditioner over any chalking or bare stucco, and painting between October and April '
                 'while surface temps stay under 90&deg;F.'),
                ('How long will an exterior repaint last in Arizona?',
                 'With proper prep and premium coatings, seven to ten years on stucco is realistic, and longer on '
                 'shaded elevations. Cheap paint or skipped prep in this climate can start chalking and fading in '
                 'as little as three years. The variable is almost never the brand of paint &mdash; it is whether '
                 'the surface was washed, tested, and primed before the colour went on.'),
                ('Do I need elastomeric paint on my stucco?',
                 'Only if you have real cracking to span. Elastomeric is a thick, flexible, high-build coating '
                 'that bridges hairline cracks and resists wind-driven moisture, which makes it genuinely valuable '
                 'on a cracked stucco or block wall. On sound stucco it is largely wasted money and it can trap '
                 'moisture if the wall has drainage issues. We will tell you honestly which camp your house is in.'),
                ('When should exterior painting be done in Arizona?',
                 'October through April is the window. Once surface temperatures exceed about 90&deg;F the paint '
                 'film flashes off before it can level and properly adhere, which measurably shortens its life. '
                 'We do book summer exteriors when a home needs it, but we start at first light and follow the '
                 'shade around the building rather than spraying a wall in direct sun.'),
                ('Will you repair stucco cracks before painting?',
                 'Yes &mdash; that is part of every exterior scope. Hairline settlement cracks get sealed and '
                 'bridged, larger cracks get patched, and we re-texture the repair to match your existing knockdown '
                 'or sand finish so the fix does not read as a patch once the colour is on.'),
              ], 'Arizona Exterior Painting FAQ')
            + related([
                ('Painters in Scottsdale', 'HOA submittals handled and desert-contemporary palettes matched to Scottsdale light.', 'painters-scottsdale-az.html'),
                ('Painters in Arcadia', 'Painted brick and mid-century ranch specialists in Arcadia and the Camelback corridor.', 'painters-arcadia-az.html'),
                ('Painters in Gilbert', 'Builder-grade stucco repaint specialists across Agritopia, Seville and Power Ranch.', 'painters-gilbert-az.html'),
              ], 'Exterior Painting Near You')
            + cta('Ready For An Exterior That Survives Arizona?',
                  'Free, no-pressure estimate including a chalk test and color consultation from a licensed, '
                  'bonded, and insured Arizona crew that shows up on time.')
            + FOOTER)

open(os.path.join(OUT, 'exterior-painting.html'), 'w', encoding='utf-8').write(svc_html)
print('wrote exterior-painting.html', len(svc_html), 'chars')
