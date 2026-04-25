---
name: Obsidian Precision
colors:
  surface: '#0c1324'
  surface-dim: '#0c1324'
  surface-bright: '#33394c'
  surface-container-lowest: '#070d1f'
  surface-container-low: '#151b2d'
  surface-container: '#191f31'
  surface-container-high: '#23293c'
  surface-container-highest: '#2e3447'
  on-surface: '#dce1fb'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#dce1fb'
  inverse-on-surface: '#2a3043'
  outline: '#86948a'
  outline-variant: '#3c4a42'
  surface-tint: '#4edea3'
  primary: '#4edea3'
  on-primary: '#003824'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#006c49'
  secondary: '#b7c8e1'
  on-secondary: '#213145'
  secondary-container: '#3a4a5f'
  on-secondary-container: '#a9bad3'
  tertiary: '#bec6e0'
  on-tertiary: '#283044'
  tertiary-container: '#9ba2bb'
  on-tertiary-container: '#31394d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#0c1324'
  on-background: '#dce1fb'
  surface-variant: '#2e3447'
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
  mono-label:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: -0.01em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin: 40px
  container-max: 1440px
  stack-xs: 8px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

The design system is engineered for elite professionals who demand a focused, distraction-free environment. The brand personality is clinical, authoritative, and sophisticated, mirroring the feel of high-end mechanical instruments or luxury automotive interfaces.

The aesthetic utilizes **Glassmorphism** as its foundational layer, but executed with restraint to maintain a "weighted" feel. Rather than ethereal floating elements, surfaces feel like heavy, smoked sapphire glass. The high-contrast relationship between the void-like background and the vibrant emerald accents creates a sense of "digital jewelry"—where every interaction feels intentional, precise, and expensive.

## Colors

The palette is anchored by the **Deepest Midnight Navy (#020617)**, which serves as the infinite canvas. This is not a flat black, but a rich, deep space that provides more soul and depth. 

**Emerald Green (#10B981)** is used exclusively for "Precision Strikes"—critical actions, status indicators, and success states. It should be used sparingly to maintain its impact. **Subtle Slate Grays** bridge the gap between the background and typography, providing a hierarchy for non-essential information. All interactive surfaces utilize a semi-transparent blur to simulate depth without losing the "Pro" focus.

## Typography

This design system relies entirely on **Inter** to deliver a utilitarian yet premium feel. The typography strategy emphasizes high-contrast readability. Headlines use tight tracking and bold weights to feel architectural. 

Body text remains crisp white (#FFFFFF) for maximum legibility against the dark backgrounds. Secondary information is pushed back using slate-gray tones rather than reduced opacity to ensure the "glass" behind the text remains clear. Utility labels use an uppercase, tracked-out style to mimic technical readouts on professional equipment.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. While the outer container respects a maximum width of 1440px to prevent eye strain on ultra-wide monitors, internal components utilize a strict 12-column grid.

Spacing is generous, creating a "Gallery" feel where data has room to breathe. Use a 4px baseline shift for micro-adjustments, but favor the 8px rhythm for component spacing. High-density views (like spreadsheets or code editors) should compress the stack-md units but maintain the 40px outer margins to preserve the premium frame.

## Elevation & Depth

Elevation in this design system is achieved through **Optical Refraction** rather than traditional shadows.

1.  **Base Layer:** The deepest navy background (#020617).
2.  **Surface Layer:** A 60% opacity fill of Slate 900 with a 32px backdrop blur. This creates the "Smoked Glass" effect.
3.  **Edge Definition:** Surfaces must be defined by a 1px inner border (stroke). The top edge should have a slightly higher opacity (12%) than the bottom edge (4%) to simulate a top-down light source.
4.  **Luminescence:** Instead of drop shadows, active elements use a faint emerald outer glow (`box-shadow: 0 0 20px rgba(16, 185, 129, 0.15)`) to appear as if they are backlit.

## Shapes

The shape language is "Soft-Mechanical." We avoid the playfulness of large radii in favor of **tight, precision corners**. 

Standard components use a 4px (0.25rem) radius to feel sharp and technical. Cards and larger glass panels use 8px (0.5rem). This subtle rounding retains a human touch while leaning heavily into a "Pro" aesthetic. Buttons should never be fully rounded (pills); they should remain rectangular with 4px corners to maintain their architectural weight.

## Components

### Buttons
Primary buttons are solid Emerald Green with black text for maximum contrast. Secondary buttons are "Ghost Glass"—transparent with a subtle 1px border and white text. Every button press should trigger a slight scale-down (98%) and a brief increase in the background blur intensity.

### Input Fields
Inputs are dark-recessed wells. On focus, the 1px border transitions from Slate-800 to Emerald Green, accompanied by a subtle "scanning" glow effect. Use a monospaced variant of Inter for numerical inputs to emphasize precision.

### Cards & Panels
Glass panels are the primary container. They should never have a shadow; they are defined solely by their backdrop blur and the "Inner Light" border. Headers within cards are separated by a hairline 1px divider with 5% opacity.

### Navigation
The sidebar should be a continuous vertical pane of smoked glass. Active states are indicated by a vertical 2px "light bar" on the far left in Emerald Green.

### Micro-interactions
Transitions should be "Snappy but Smooth"—use a custom cubic-bezier (0.2, 0, 0, 1). Elements don't just appear; they fade in with a slight vertical slide (4px) to simulate a physical mounting of the UI onto the glass.