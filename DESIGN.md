---
name: Cyber Vintage
colors:
  surface: '#121212'
  surface-dim: '#1a1a1a'
  surface-bright: '#2a2a2a'
  surface-container-lowest: '#0a0a0a'
  surface-container-low: '#141414'
  surface-container: '#1a1a1a'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#333333'
  on-surface: '#f5f5f5'
  on-surface-variant: '#c0c0c0'
  inverse-surface: '#f5f5f5'
  inverse-on-surface: '#121212'
  outline: '#ff3300'
  outline-variant: '#333333'
  surface-tint: '#ff3300'
  primary: '#ff3300'
  on-primary: '#0a0a0a'
  primary-container: '#4d0f00'
  on-primary-container: '#ff9980'
  inverse-primary: '#ff8066'
  secondary: '#00ffcc'
  on-secondary: '#003329'
  secondary-container: '#004d3d'
  on-secondary-container: '#80ffe6'
  tertiary: '#ffcc00'
  on-tertiary: '#332900'
  tertiary-container: '#4d3d00'
  on-tertiary-container: '#ffe680'
  error: '#ff3300'
  on-error: '#ffffff'
  error-container: '#4d0f00'
  on-error-container: '#ff9980'
  primary-fixed: '#ff3300'
  primary-fixed-dim: '#cc2900'
  on-primary-fixed: '#0a0a0a'
  on-primary-fixed-variant: '#4d0f00'
  secondary-fixed: '#00ffcc'
  secondary-fixed-dim: '#00ccaa'
  on-secondary-fixed: '#003329'
  on-secondary-fixed-variant: '#004d3d'
  tertiary-fixed: '#ffcc00'
  tertiary-fixed-dim: '#ccaa00'
  on-tertiary-fixed: '#332900'
  on-tertiary-fixed-variant: '#4d3d00'
  background: '#0a0a0a'
  on-background: '#f5f5f5'
  surface-variant: '#2a2a2a'
typography:
  display-xl:
    fontFamily: Bebas Neue
    fontSize: 120px
    fontWeight: '400'
    lineHeight: 110px
    letterSpacing: 0.01em
  display-lg:
    fontFamily: Bebas Neue
    fontSize: 80px
    fontWeight: '400'
    lineHeight: 80px
    letterSpacing: 0.02em
  headline-lg:
    fontFamily: Bebas Neue
    fontSize: 48px
    fontWeight: '400'
    lineHeight: 48px
    letterSpacing: 0.03em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
    letterSpacing: 0px
  body-md:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0px
  label-bold:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0.05em
  display-lg-mobile:
    fontFamily: Bebas Neue
    fontSize: 64px
    fontWeight: '400'
    lineHeight: 64px
rounded:
  sm: 0px
  DEFAULT: 0px
  md: 0px
  lg: 0px
  xl: 0px
  full: 0px
spacing:
  container-max: 1440px
  gutter: 32px
  margin-mobile: 16px
  stack-sm: 16px
  stack-md: 32px
  stack-lg: 64px
---

# Design System: Cyber Brutalism

## 1. Overview & Creative North Star
**The Creative North Star: "The Analog Grid meets The Digital Void"**

This system fuses the structural confidence of a vintage comic store layout (massive block typography, hard grids, heavy borders) with the high-tech, forensic aesthetic required for an intelligence-analysis engine. 

It rejects "soft SaaS" norms. Every container is a hard rectangle. Every border is a neon wire. The UI should feel like a specialized, high-stakes terminal.

## 2. Colors & Borders
The palette is rooted in pitch black, accented by aggressive neon strokes.

*   **Backgrounds:** Pitch Black (`#0a0a0a`) and Deep Charcoal (`#121212`) form the canvas.
*   **The Grid:** Instead of missing borders, this system relies on **Thick, High-Contrast Borders**. Use 2px to 4px solid borders in Neon Red/Orange (`#ff3300`) or Deep Grey (`#333333`) to separate sections.
*   **Accents:** Cyber Cyan (`#00ffcc`) is used for "verified" data, and Neon Red (`#ff3300`) is used for high-risk / manipulation warnings.

## 3. Typography
Typography is the primary visual element, drawing from vintage poster aesthetics but executed in high-contrast neon.

*   **Display (Bebas Neue):** Used for massive, brutalist headlines. Always uppercase. Very tight line-height.
*   **Body & Utility (Space Grotesk):** A monospaced, technical feel that conveys "analysis" and "raw data."

## 4. Components
*   **Containers/Cards:** Always 0px border radius (sharp corners). Heavy 2px solid neon borders. No soft drop shadows. Use hard, solid block shadows (e.g., 8px solid `#ff3300` offset to the bottom right) for interactive cards.
*   **Buttons:** Thick solid borders. Background is transparent or solid neon. Text is highly legible, bold Space Grotesk. Hover states should invert the colors instantly (no soft transitions).
*   **Data Displays:** Use rigid tables or grid blocks with visible borders. "Scam Analysis" metrics should be displayed in massive numerical typography inside boxed grid units.
