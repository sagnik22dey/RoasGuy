# Figma Reference — Roasguy Landing Page

Source: Figma file `BkUtIr1RSy5HzazPxwkFos`, canvas **LP 4** (`1734:66`).
Two desktop pages rebuilt here:

| Page | Figma node | Size | Built file |
|---|---|---|---|
| Desktop (main landing) | `1735:67` | 1440 × 12656 | `desktop.html` |
| Thank you | `1841:20` | 1440 × 2650 | `thankyou.html` |

## Folder layout
- `images/` — asset images pulled from Figma (node-render, scale 2, auto-cropped).
- `segments/` — full-page renders (`*-full.png`) + readable horizontal slices (`*-band-N.png`) used to verify the build against the design.
- `css/` — `tokens.css` (shared design tokens), `desktop.css`, `thankyou.css`.

## Fonts
Whole design uses **Instrument Sans** only (Google Fonts), weights **500 (Medium)** and **600 (SemiBold)**.
Sizes seen: 16, 24, 36, 40, 54.23, 55, 64. Emoji glyphs (🎉 ✅ 📞 📧) use the system emoji font.

## Color / gradient palette
- Page background: `#F8F8FF`
- Text: `#000000`; on-gradient text `#FFFFFF`; accent red `#FF0000` ("Important:")
- enroll button gradient: `linear-gradient(90deg, #1ACFFF 0%, #0076FF 100%)`
- WhatsApp button gradient: `linear-gradient(181deg, #46CC5E 0%, #1F991E 100%)`
- top bar / divider gradient: `linear-gradient(180deg, #487FD5 0%, #B47DDA 100%)` (also seen at 90°, 124°, 87°, 252°)
- card gradient: `linear-gradient(-90deg, #CBECFF, #FCE2FF)`
- gradient stroke: `linear-gradient(90deg, #56C4FF, #F183FF)`
- shadows: `4.3px 4.3px 7.1px rgba(0,0,0,0.25)`, `6px 6px 10.7px rgba(0,0,0,0.29)`, whatsapp btn `2.5px 5.7px 15.1px rgba(8,164,255,0.48)`

## Image map (figma node → file)
### Shared
- hero bg `ccd9dba4…` → `images/hero-bg.png` (desktop), `images/thankyou-hero-bg.png` (thank-you crop)
- logo/footer banner `75c2cf82…` → `images/logo.png`, `images/footer-banner.png`, `images/thankyou-footer-banner.png`

### Desktop sections (top → bottom)
- Hero (band-0): logo top-left, "enroll" CTA top-right, hero heading + subhead over `hero-bg.png`
- Problem Reframe (band-1): heading + divider + `kid-thinking-1/2/3.png` trio
- What You'll Learn (band-2/3): heading, checklist block, enroll CTA
- Results / testimonials (band-3/4): `testimonial-84/85/86/87.png` screenshots between gradient dividers
- What makes this different (band-5): `kid-thinking-4/6.png`, gradient-stroke card
- About the Trainer (band-5/6): `trainer-meta-ads.png` + bio card
- Pricing Justification (band-6): content + CTA
- FAQ + footer (band-7): contact text + `footer-banner.png`

### Thank-you sections
- Top gradient bar with "No upsell…100% refund" text
- Hero bg + `thankyou-logo-banner.png`
- "🎉 You're In!" heading + registration confirmation
- "Important: Join The WhatsApp Group Now" + checklist + green WhatsApp CTA button
- Footer banner `thankyou-footer-banner.png`

## Notes / open items
- The 4 testimonial images are full screenshots rendered from Figma Groups (84-87).
- Figma REST API used directly (MCP `download_figma_images` is broken — missing `strtok3` dep). Helper: `.rustic/tmp/figma-dl.ps1`.
- API is rate-limited (429) under bursts; node-JSON dumps retry with 60s backoff.
