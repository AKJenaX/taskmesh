---
name: Prism Noir
colors:
  surface: '#131315'
  surface-dim: '#131315'
  surface-bright: '#39393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1b1b1d'
  surface-container: '#201f21'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353436'
  on-surface: '#e5e2e3'
  on-surface-variant: '#c6c6cd'
  inverse-surface: '#e5e2e3'
  inverse-on-surface: '#303032'
  outline: '#909097'
  outline-variant: '#46464c'
  surface-tint: '#c0c6de'
  primary: '#c0c6de'
  on-primary: '#2a3043'
  primary-container: '#020617'
  on-primary-container: '#72778d'
  inverse-primary: '#585e73'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#4cd7f6'
  on-tertiary: '#003640'
  tertiary-container: '#00080b'
  on-tertiary-container: '#00849a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dce1fb'
  primary-fixed-dim: '#c0c6de'
  on-primary-fixed: '#151b2d'
  on-primary-fixed-variant: '#40465a'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#acedff'
  tertiary-fixed-dim: '#4cd7f6'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5c'
  background: '#131315'
  on-background: '#e5e2e3'
  surface-variant: '#353436'
typography:
  h1:
    fontFamily: Space Grotesk
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h2:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.01em
  h3:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0em
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
  gutter: 24px
  margin: 32px
---

## Brand & Style

This design system is built upon the aesthetic of "Futuristic Noir"—a synthesis of deep, obsidian-like foundations and hyper-vibrant, chromatic accents. It targets high-end technical products and luxury digital experiences where precision and sophistication are paramount. The emotional response is intended to be one of "controlled power": dark, quiet environments punctuated by sudden, sharp bursts of light and intelligence.

The visual style leverages **Glassmorphism** and **High-Contrast Minimalism**. Elements appear as though they are carved from synthetic obsidian or dark-tinted glass. Specular highlights (simulating light hitting a physical edge) and razor-thin borders provide the necessary definition within the deep-dark workspace.

## Colors

The palette is anchored by a nearly-black "Obsidian" base. Contrast is achieved not through large blocks of color, but through "Prism" accents—holographic purples, cyans, and emeralds that signify action and state changes.

- **Backgrounds:** Primarily `#020617`. Use subtle linear gradients toward `#0F172A` to create depth.
- **Accents:** Use **Holographic Purple** (`#A855F7`) for primary actions, **Vibrant Cyan** (`#06B6D4`) for technical readouts, and **Emerald** (`#10B981`) for success states.
- **Borders:** Extremely thin (1px) using high-contrast neutrals like `#1E293B` or semi-transparent whites to simulate glass edges.

## Typography

The typography strategy pairs the technical, wide geometry of **Space Grotesk** with the utilitarian precision of **Inter**. 

- **Headings:** Space Grotesk is used for all H1-H3 levels. Its wide stance and geometric construction provide a futuristic, luxury-tech feel.
- **UI & Body:** Inter is utilized for all functional text, body copy, and data inputs to ensure maximum legibility at small sizes. 
- **Labels:** Use Inter in all-caps with increased letter spacing for small labels or category headers to mimic cockpit instrumentation.

## Layout & Spacing

This design system utilizes a rigorous **4px grid system**. Layouts should be structured using a **12-column fluid grid** for internal dashboards or a fixed 1440px container for marketing pages. 

- **Density:** High density is preferred. Use tight spacing units (`8px`, `16px`) to group related technical data.
- **Rhythm:** Vertical rhythm should be strictly maintained in increments of 8px.
- **Margins:** Large outer margins (`32px`+) are encouraged to allow the obsidian background to frame the content, enhancing the luxury feel.

## Elevation & Depth

Depth is not communicated through traditional shadows, but through **translucency and specular highlights**.

- **Z-Axis Hierarchy:** Higher elevation layers are more opaque and have lighter borders. 
- **Glassmorphism:** Use a `backdrop-blur` (ranging from 12px to 40px) on surface layers. The background color of these layers should be a semi-transparent version of the primary background (`rgba(2, 6, 23, 0.7)`).
- **Specular Highlights:** Apply a 1px inner-border (top and left edges only) using a high-opacity white or cyan (`rgba(255, 255, 255, 0.1)`) to simulate light catching the edge of a glass pane.
- **Glow:** High-priority elements (like active chips) may use a very soft, colored outer glow (blur: 20px, spread: -5px) matching the prism accent color.

## Shapes

The shape language is sharp and disciplined. Softness is avoided to maintain a "technical" and "hard-surface" aesthetic.

- **Base Radius:** Components like buttons, inputs, and small cards use a **4px** radius.
- **Container Radius:** Larger surfaces or modals use an **8px** radius.
- **Exceptions:** No circles or pill shapes are used, except for notification pips or status indicators.

## Components

### Buttons
Primary buttons feature a subtle gradient of the Prism colors (e.g., Purple to Cyan) with a white 1px border. Secondary buttons are "Ghost" style: transparent backgrounds with a thin `#1E293B` border that turns white on hover.

### Cards
Cards are the primary vehicle for Glassmorphism. They must have a `backdrop-blur`, a 1px solid border (`#1E293B`), and a "specular" top-border highlight.

### Inputs
Fields are obsidian-dark with a bottom-only border by default. On focus, the border expands to all four sides and glows with a Cyan (`#06B6D4`) accent. Text should be Inter 14px.

### Chips & Tags
Technical tags should look like "readouts." Use a mono-spaced variant of Inter or Space Grotesk, 10px size, encased in a sharp 2px-radius box with a semi-transparent Emerald or Cyan background.

### Navigation
The sidebar or top-nav should use a higher level of translucency. Active links are indicated by a vertical "Prism" bar (gradient) on the left side of the menu item.