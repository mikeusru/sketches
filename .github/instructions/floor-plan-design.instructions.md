---
description: "Use when editing or creating SVG floor plan scripts (plan.py). Covers spatial layout rules, furniture placement, labeling, and physical accuracy for architectural floor plans."
applyTo: "**/plan.py"
---

# Floor Plan Design Rules

## Physical accuracy

- All furniture dimensions MUST be converted from real inches using `SCALE` (px per inch). Never eyeball pixel values.
- Account for **material thickness**: walls are ~16px stroke. Place furniture with clearance from wall centerlines (≥8px inset from wall line to represent a few inches of real clearance).
- When the user gives a product link, fetch the page to get exact dimensions in inches before drawing.

## Placement constraints — never violate these

- **Windows**: Never place furniture in front of a window. Cross-check furniture y/x ranges against all `win_*` coordinate ranges.
- **Doors**: Never place furniture where a door swings. Check door arc paths and leave the full swing radius clear.
- **Clearance**: Leave at least 24" (scaled) of walkable clearance in front of doors and in hallways/passages between furniture.
- **Walls**: Furniture "against a wall" should be inset from the wall stroke, not overlapping the wall line.

## Labels and text

- Labels must **never overlap** other labels, furniture, walls, or fixtures.
- When a room is crowded, use short labels (abbreviations, single-line) or move the room label to an open corner.
- Furniture labels go inside the furniture rectangle. If the piece is too narrow, use a short abbreviation or a single line.
- Dimension lines must not pass through furniture or labels. Adjust `row`/`col` offsets if they collide.

## Layout strategy

- Before placing furniture, mentally compute the available space: identify walls, doors, windows, and existing furniture. Then pick a position that respects all constraints.
- When placing multiple identical items (e.g. wardrobes), stack them tightly with 2–4px gaps and verify the total span fits within the room bounds.
- Center beds (and their opposing TVs) in the open floor area between wardrobes/dressers and the far wall, not pinned to a corner.

## After every edit

- Regenerate SVGs and briefly sanity-check coordinates: does the last item fit within its room's bounding walls? Do any items share overlapping pixel ranges?
