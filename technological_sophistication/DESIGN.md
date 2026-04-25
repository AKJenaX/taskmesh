---
name: Technological Sophistication
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
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
  tertiary: '#b9c7e0'
  on-tertiary: '#233144'
  tertiary-container: '#95a4bb'
  on-tertiary-container: '#2c3a4e'
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
  tertiary-fixed: '#d5e3fd'
  tertiary-fixed-dim: '#b9c7e0'
  on-tertiary-fixed: '#0d1c2f'
  on-tertiary-fixed-variant: '#3a485c'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-margin: 32px
  gutter: 24px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
  glass-padding: 20px
---

## Brand & Style
The brand personality is rooted in precision and high-performance productivity. This design system aims to evoke a sense of calm mastery over complex schedules, positioning the product as a technologically advanced tool for professionals. 

The aesthetic is a hybrid of **Minimalism** and **Glassmorphism**. It prioritizes clarity through generous whitespace and a restricted color palette, while utilizing translucent layers and subtle gradients to create a sense of depth and architectural hierarchy. The interface should feel like a premium physical instrument—substantial, polished, and responsive.

## Colors
The palette is anchored by **Deep Charcoal** (#0F172A) and **Slate Grays**, providing a stable, high-contrast foundation that reduces eye strain during long periods of focus. The **Vibrant Emerald Green** (#10B981) serves as the primary action color, used sparingly to draw attention to progress, completion, and primary CTAs.

In Dark Mode, surfaces utilize varying shades of charcoal to establish hierarchy. In Light Mode, these transition to soft off-whites and cool grays. Subtle linear gradients (135-degree angle) are applied to primary buttons and active states to enhance the "advanced" feel. Glassmorphism is achieved through semi-transparent fills on overlays, allowing background colors to bleed through with high-density blurs.

## Typography
**Inter** is selected for its exceptional legibility and systematic appearance, perfectly aligning with the professional nature of task scheduling. The hierarchy is strictly enforced through weight variations rather than excessive size changes. 

Headlines use semi-bold and bold weights with tighter letter spacing to feel "locked-in" and authoritative. Body text maintains a standard 1.5 line-height ratio for optimal readability. Small labels utilize an uppercase styling with increased tracking to differentiate metadata from primary task descriptions.

## Layout & Spacing
This design system employs a **fluid 12-column grid** for large screens and a single-column layout for mobile, utilizing an 8px base unit for all spatial relationships. High-quality spacing is a hallmark of this system, meaning margins and paddings are intentionally generous to prevent information density from feeling overwhelming.

Layouts should favor "breathing room" around task lists and calendar views. Containers and cards use a standard 24px gutter to maintain clear separation, while internal content uses 16px or 20px padding to ensure the "glass" edges have a defined safe area.

## Elevation & Depth
Depth is created through **Glassmorphism** and **Tonal Layering**. Instead of traditional heavy shadows, this system uses:
- **Backdrop Blurs:** 20px to 40px blur radius on surfaces with 70-80% opacity.
- **Inner Borders:** 1px translucent white (10% opacity) "shimmer" borders on the top and left edges of cards to simulate a light source.
- **Ambient Shadows:** Low-opacity (15%) diffused shadows with a slight tint of the primary Emerald Green for active elements, or Deep Charcoal for static elements.

Floating Action Buttons (FABs) and Modals sit on the highest Z-axis, utilizing the strongest backdrop blurs to effectively "mute" the content underneath.

## Shapes
The shape language is defined by large, modern radii. The base `rounded-md` is 8px, but the signature of this design system is the **16px radius (`rounded-lg`)** used for primary cards and containers. 

Buttons and input fields follow this 16px standard to create a soft, approachable feel that contrasts with the technical, dark color palette. Fully pill-shaped (`rounded-full`) geometry is reserved strictly for status chips and tags to distinguish them from interactive buttons.

## Components
- **Buttons:** Primary buttons feature a subtle vertical gradient of Emerald Green. They use 16px rounded corners and 12px vertical padding. Secondary buttons use a ghost style with a subtle slate border.
- **Cards:** The core of the scheduling app. Cards are semi-transparent with a 20px backdrop blur. They must include a 1px border (#FFFFFF10) to define their edges against dark backgrounds.
- **Chips:** Used for task categories (e.g., "Work," "Personal"). These are pill-shaped with low-opacity background tints of the secondary color.
- **Input Fields:** Large 16px rounded corners. In dark mode, they use a slightly lighter charcoal than the background with a 1px border that glows Emerald Green when focused.
- **Lists:** Task lists should avoid heavy dividers. Instead, use vertical spacing and subtle tonal shifts on hover to indicate interactivity.
- **Task Timeline:** A custom component featuring a vertical line with "nodes" that glow Emerald when a task is completed, utilizing a neon-like outer glow effect.