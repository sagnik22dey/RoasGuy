---
trigger: always_on
---

# RoasGuy Project - Agent Rules

## Project Overview

This is a Figma-to-code landing page for **RoasGuy** (a Meta Ads webinar product).
The live server is run via `py app.py` in `a:\FreeLancing\RoasGuy`.
The primary files are:

- `a:\FreeLancing\RoasGuy\figma_reference\desktop.html` - shared HTML for all viewports
- `a:\FreeLancing\RoasGuy\figma_reference\css\desktop.css` - desktop-only styles (1025px and above)
- `a:\FreeLancing\RoasGuy\figma_reference\css\mobile.css` - mobile/tablet styles (1024px and below)
- `a:\FreeLancing\RoasGuy\figma_reference\css\tokens.css` - design tokens (do not modify unless explicitly asked)

---

## Viewport Strategy

The page uses three breakpoints:

| Viewport | Breakpoint       | CSS File     |
|----------|------------------|--------------|
| Desktop  | 1025px and above | desktop.css  |
| Tablet   | 601px to 1024px  | mobile.css   |
| Mobile   | 600px and below  | mobile.css   |

desktop.css is always loaded. mobile.css overrides desktop styles using media queries inside mobile.css only.

**The HTML file is shared across all breakpoints** - never add viewport-conditional HTML.

---

## Desktop Layout and Sizing Rules

1. **All sizing must use `vw` units**, never `px`. The design viewport base is `1440px = 100vw`, so `1px = 0.0694vw`. Always convert Figma px values using this formula before writing any CSS.
2. **Do not use trailing zeros in `vw` values**. Write `1.25vw` not `1.250vw`, `6.25vw` not `6.250vw`.
3. **The entire page uses `position: absolute` (`.abs`) elements** placed using `top`/`left` in `vw` offsets inside a single `.frame.dk` container. This is intentional - do not switch to flexbox/grid at the page level or add a normal document flow.
4. **Section-level layout** (cards, grids, columns within a section) may use `display: flex` or `display: grid` with `vw` gaps and sizes.
5. **The `.frame.dk` height** in `desktop.css` must be updated whenever new sections are added that extend the page length.

---

## Mobile and Tablet Layout and Sizing Rules

1. **All mobile sizing uses `vw` units as well**, but based on the **mobile viewport**. The mobile design base is `390px = 100vw` (standard iPhone canvas), so `1px = 0.2564vw` at mobile.
2. **Do not use trailing zeros in `vw` values** - same rule applies.
3. **Mobile layout exits the absolute-positioning system.** Inside `@media (max-width: 1024px)`:
   - The `.frame.dk` becomes `position: relative; height: auto;` so content flows normally.
   - All `.abs` elements become `position: relative; top: auto; left: auto;` - normal document flow.
   - Section-level layout uses `display: flex` (column by default) or `display: grid`.
4. **Tablet view (601px to 1024px)**: Aim to match the desktop layout as closely as possible - use the same section order and two-column grids where they fit. If a section is too complex, fall back to the mobile single-column layout.
5. **Mobile view (600px and below)**: Single-column stacked layout. All sections stack top-to-bottom following the section order.
6. **The `.frame.dk` height must NOT be set** in mobile - let it be `height: auto` so content determines the height.

---

## Design Token Usage

Always reference design tokens from `tokens.css`. Never hardcode gradient or shadow values inline:

| Token              | Usage                                                    |
|--------------------|----------------------------------------------------------|
| `var(--grad-bar)`    | Section heading underline divider                        |
| `var(--grad-card)`   | Card/section background gradients (soft pink-blue)       |
| `var(--grad-stroke)` | Gradient borders on pill bubbles and highlighted boxes   |
| `var(--page-bg)`     | Page background fill (used inside gradient-border trick) |
| `var(--shadow-card)` | Standard card drop shadow                                |
| `var(--shadow-soft)` | Softer shadow for images and FAQs                        |

**Gradient border trick** (used for pill bubbles and highlighted boxes):

```css
background-clip: padding-box, border-box;
background-origin: padding-box, border-box;
background-image:
  linear-gradient(var(--page-bg), var(--page-bg)), var(--grad-stroke);
border: 0.2vw solid transparent;
```

---

## Desktop Section Structure Pattern

Each section follows this standard pattern in HTML:

```html
<!-- Section Title -->
<div class="abs sec-head [section]-head">
  <h2>Section Title</h2>
  <div class="divider"></div>
</div>

<!-- Section Content -->
<div class="abs [section]-content-or-block">...content...</div>
```

And in CSS (`desktop.css`):

```css
.[section]-head {
  top: [calculated vw offset];
  left: 0;
}
.[section]-content-or-block {
  top: [calculated vw offset];
  left: 0;
  width: 100vw;
}
```

---

## Mobile Section Structure Pattern

In `mobile.css`, the `.abs` positioning is undone and sections reflow as a normal document.
All rules must be scoped inside `@media (max-width: 1024px)`.

Base reset in `mobile.css`:

```css
@media (max-width: 1024px) {
  .frame.dk {
    position: relative;
    height: auto;
  }

  .abs {
    position: relative;
    top: auto;
    left: auto;
  }

  /* Section-specific overrides follow */
  .[section]-head {
    width: 100%;
    text-align: center;
    padding: 6vw 0 2vw;
  }

  .[section]-content-or-block {
    width: 100%;
    padding: 0 4vw;
    box-sizing: border-box;
  }
}
```

The **section order in the HTML** determines the visual stacking order in mobile.
Never reorder HTML elements to fix mobile layout.

---

## Mobile CSS File (mobile.css) Rules

1. **`mobile.css` is the only file that changes for mobile work.** Never touch `desktop.css` or `desktop.html` when implementing mobile sections.
2. **All mobile rules live inside media queries** - never write bare (non-media-query) rules in `mobile.css`.
3. Use two breakpoints:
   - `@media (max-width: 1024px)` - catches both tablet and mobile
   - `@media (max-width: 600px)` - mobile-only overrides (narrower or more compact styling)
4. **`mobile.css` must be linked in `desktop.html`** after `desktop.css`:
   ```html
   <link rel="stylesheet" href="/figma_reference/css/desktop.css" />
   <link rel="stylesheet" href="/figma_reference/css/mobile.css" />
   ```
5. **Cascade is intentional** - desktop styles load first, mobile overrides them via specificity/media queries.

---

## Image Handling Rules

1. **Never remove image placeholders** without explicit instruction. Use `https://picsum.photos/[w]/[h]` as standin for images/icons that are pending from the client.
2. **Real images** are served from `/figma_reference/images/` and referenced with that path.
3. **Do not delete existing image references** (e.g., `kid-thinking-1.png`, `logo.png`, etc.) even when restructuring a section - just re-place them in the new layout.
4. **In mobile**, images should be `width: 100%` or a fixed `vw` width. Never use `px` widths for images on mobile.

---

## Section Order (Current)

The page flows in this order top-to-bottom (same for both desktop and mobile):

1. Nav
2. Top Bar (refund banner)
3. Hero
4. **Relatability** (cards + dashed vertical line + pill bubbles)
5. **Problem Reframe** (3-column grid: left images | center text | right image)
6. What You Will Learn
7. Results / Testimonials
8. What Makes This Different
9. About the Trainer
10. Pricing Justification
11. FAQ
12. Footer

---

## Section-Specific Layout Notes

### Desktop - Relatability Section

- Central vertical **dashed line** runs behind all elements using `position: absolute` inside `.relatability-section`
- Cards (`.rel-card`) use `var(--grad-card)` background and are `62vw` wide, centered
- Pill bubbles (`.rel-bubble`) use the gradient border trick and `border-radius: 999vw`
- Flow: Card 1 > Bubble > Card 2 > Bubble (all stacked vertically, centered)

### Mobile - Relatability Section

- Remove the vertical dashed line (`.vertical-dashed-line { display: none; }`)
- Cards stack full-width with `width: 92vw; margin: 0 auto`
- Pill bubbles remain centered, shrink font and padding proportionally
- Flow is the same: Card 1 > Bubble > Card 2 > Bubble, stacked vertically

### Desktop - Problem Reframe Section

- Uses a **3-column CSS Grid**: `[Left images col] | [Center text col] | [Right image col]`
- Grid template: `18vw 1fr 18vw` with `padding: 0 12vw`
- **Left column**: Image 1 (top) + Image 3 (bottom) - aligned to right edge of column
- **Center column**: All text blocks flow vertically with `gap: 5vw` between blocks
- **Right column**: Image 2 only - pushed down with `padding-top` to align beside middle text
- The highlighted box uses the gradient border trick with `border-radius: 0.8vw` (rectangular, not pill)

### Mobile - Problem Reframe Section

- Collapses from 3-column grid to **single column**, stacked vertically
- Image ordering: Show image 1, then text blocks, then image 2, then image 3 (follow visual reference)
- Adjust layout per the screenshot/visual reference provided by the user

---

## Mobile Workflow Rules

1. **When implementing a mobile section**, always:
   - Read the user-provided screenshot/visual reference for that section first
   - Check the current HTML structure in `desktop.html` to understand class names and DOM order
   - Write all overrides in `mobile.css` - never in `desktop.css`
2. **Section-by-section delivery**: Implement one section at a time, confirm with the user before proceeding to the next.
3. **When the user provides a screenshot**, analyze it for: column count, image positions, font sizes (relative to screen), spacing, and any decorative elements (lines, bubbles, borders).
4. **Never reorder HTML elements** to fix mobile layout - use CSS `order` property inside flex/grid containers if reordering is needed.
5. **Test the desktop view is unaffected** - after every mobile change, mentally verify the `@media` wrapper is correctly scoped.

---

## General Workflow Rules (Desktop and Mobile)

1. **Always read both `desktop.html` and `desktop.css` before making any changes** to understand current positions and avoid overlap with adjacent sections.
2. **Never remove a section** that the user has not explicitly asked to delete. If restructuring, preserve all content.
3. **Section `top` offsets in CSS are cumulative (desktop only)** - if you shift one section, check whether all sections below it need to be shifted as well.
4. **When user provides a screenshot**, analyze it for: column count, image positions (left/right/center), text alignment, element order, and any decorative elements (lines, bubbles, borders) before writing any code.
5. **Ask before deleting** - if your implementation requires removing an existing section or significantly restructuring the page order, ask for confirmation first.
6. **Do not use inline styles** for layout or positioning. All layout rules belong in the appropriate CSS file under the correct section comment block.
7. **No Unnecessary Blank Spaces** - When adding or shifting sections (desktop), always calculate the exact `top` offset. In mobile, use `padding`/`margin` instead of fixed `top` values.
