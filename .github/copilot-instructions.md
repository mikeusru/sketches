# Workspace Instructions

This workspace generates SVG floor plans and furniture layouts from Python scripts.

## General Rules

- Each subdirectory (e.g. `basement_floor_plan/`, `entryway_closet_plan/`) contains a `plan.py` that programmatically builds SVG markup.
- SVGs are generated via CLI entry points defined in `pyproject.toml`. Always regenerate with `uv run <entry-point> --both` after edits.
- Do NOT open the browser to show SVGs after regenerating — the user keeps them open separately and they auto-refresh.
- Use the existing `SCALE` constant (px per inch) for all real-world measurements. Never hardcode pixel values for furniture — always convert from inches.
- When the user references a product link, fetch its dimensions from the page and convert to inches before placing.

## Post-Task Retrospective

After completing any coding task, briefly reflect on the work:

- **What could have been done differently?** Identify any structure, refactor, or rethink that would have made the task easier.
- **Would a change to the instructions help?** If a rule was missing, ambiguous, or led to a mistake, flag it.
- **Is there a codebase improvement worth suggesting?** Even small changes (naming, constants, helpers, file layout) count if they would benefit future iterations.

If there is a worthwhile change, suggest it to the user — no matter how big or small.
