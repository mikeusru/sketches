# Workspace Instructions

This workspace generates SVG floor plans and furniture layouts from Python scripts.

## General Rules

- Each subdirectory (e.g. `basement_floor_plan/`, `entryway_closet_plan/`) contains a `plan.py` that programmatically builds SVG markup.
- SVGs are generated via CLI entry points defined in `pyproject.toml`. Always regenerate with `uv run <entry-point> --both` after edits.
- Do NOT open the browser to show SVGs after regenerating — the user keeps them open separately and they auto-refresh.
- Use the existing `SCALE` constant (px per inch) for all real-world measurements. Never hardcode pixel values — always convert from inches.
- When the user references a product link, fetch its dimensions from the page and convert to inches before placing.

## Basement floor plan — declarative model

The `basement_floor_plan/` package uses a declarative model. Edits to the plan are made by adding/modifying points, walls, and features in `basement.py`. You should almost never do pixel math — the renderer handles it.

- `model.py` — `FloorPlan` class with `pt()`, `wall()`, `door()`, `window()`, `opening()`, `room()`, `add_stairs()`, `fixture()`, `dim()`, `label()`.
- `renderer.py` — converts a `FloorPlan` to SVG lines (walls with cut-outs, door arcs, dimension lines, room labels).
- `basement.py` — the actual floor plan definition. All geometry in **inches** relative to the NW interior corner.
- `furniture.py` — furniture placement. Uses a pixel-space `Geo` compat shim from `basement.py`.
- `plan.py` — thin CLI entry point.

### Adding or moving features

- **Add a point**: `plan.pt("name", x, y)` for absolute, or `plan.pt("name", anchor="other", dx=…, dy=…)` for offset-from-another.
- **Add a wall**: `plan.wall("name", "p1", "p2")`. Walls are axis-aligned segments between two points.
- **Add a door / window / opening**: `plan.door("wall_name", offset=…, width=…, hinge="start|end", swing="N|S|E|W", leaves=1|2)`. Offset is inches from `p1` along the wall.

### Locked vs loose

Every point, wall, door, window, opening, and dimension carries `locked: bool` (default `True`).

- **Locked** (default): intentional, verified. Treat as authoritative — don't change unless the user asks.
- **Loose** (`locked=False`): a placeholder or estimate. This value should absorb changes when a neighboring locked value shifts. Renders dashed orange (walls) or italic orange (dimensions) so it's visually obvious which numbers aren't confirmed.

**Edit propagation rule**: when a change affects multiple values and it's ambiguous which to update, change the *loose* one, not the locked one. If every affected value is locked, ask the user to clarify before changing anything.

### Design rules

- Prefer adding named points over hardcoding coordinates. Points make relative reasoning trivial.
- Derive new points from existing ones via `anchor=…, dx=…, dy=…` when possible — moving the anchor moves everything downstream.
- When the user describes a change in inches (e.g. "move the wall 6" south"), just change the corresponding point or named dimension constant at the top of `basement.py` — never touch pixels.
- One wall per physical line segment. Don't define two walls that cover the same span. If a wall has a door, put the door on the wall as a feature — don't split the wall into two segments with a gap.

## Post-Task Retrospective

After completing any coding task, briefly reflect on the work:

- **What could have been done differently?** Identify any structure, refactor, or rethink that would have made the task easier.
- **Would a change to the instructions help?** If a rule was missing, ambiguous, or led to a mistake, flag it.
- **Is there a codebase improvement worth suggesting?** Even small changes (naming, constants, helpers, file layout) count if they would benefit future iterations.

If there is a worthwhile change, suggest it to the user — no matter how big or small.
