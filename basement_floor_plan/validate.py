"""Geometry consistency checks for a FloorPlan.

Run `validate(plan)` → list of human-readable issue strings.
An empty list means the plan is internally consistent.

Checks performed:
  1. Zero-length walls
  2. Non-axis-aligned walls (the renderer assumes H or V walls)
  3. Features (door/window/opening) reference unknown walls
  4. Features fit within their wall (0 ≤ offset, offset+width ≤ length)
  5. Features on the same wall overlap each other
  6. Duplicate walls (same two endpoints)
  7. Overlapping walls (collinear walls sharing > 0 inches of span)
  8. Door swing not perpendicular to its wall
  9. Room bounds / dimension endpoints reference unknown points

(T-junctions — a point lying on the interior of a wall — are not flagged.
The renderer auto-splits segment labels at such points, so physical walls
can stay modeled as single entities when that matches reality.)
"""

from .model import FloorPlan

EPS = 0.5   # inches — tolerance for "same point" / collinearity


def _wall_geom(plan, wall):
    p1 = plan.points[wall.p1]
    p2 = plan.points[wall.p2]
    dx, dy = p2.x - p1.x, p2.y - p1.y
    length = (dx * dx + dy * dy) ** 0.5
    return p1, p2, dx, dy, length


def _axis(p1, p2):
    if abs(p1.y - p2.y) < EPS:
        return "h"
    if abs(p1.x - p2.x) < EPS:
        return "v"
    return None


def _feats_on(plan, wall_name):
    return [(kind, f) for kind, f in plan.features_on(wall_name)]


def validate(plan: FloorPlan) -> list[str]:
    """Return list of hard errors (empty = clean)."""
    return _run_checks(plan)[0]


def validate_all(plan: FloorPlan) -> tuple[list[str], list[str]]:
    """Return (errors, warnings).

    Errors are true geometry bugs (overlapping walls, features off the end,
    unknown point refs, etc).  Warnings are advisory — currently just
    unsplit T-junctions, which aren't fatal but degrade per-segment labeling.
    """
    return _run_checks(plan)


def _run_checks(plan: FloorPlan) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # --- 1, 2: basic wall sanity ---
    for w in plan.walls.values():
        p1, p2, _dx, _dy, length = _wall_geom(plan, w)
        if length < EPS:
            errors.append(f"Wall {w.name}: zero-length ({p1.name}=={p2.name})")
            continue
        if _axis(p1, p2) is None:
            errors.append(f"Wall {w.name}: not axis-aligned "
                          f"({p1.name}→{p2.name})")

    # --- 3, 4, 9: feature-on-wall checks ---
    all_feats = (
        [("door", d) for d in plan.doors]
        + [("window", w) for w in plan.windows]
        + [("opening", o) for o in plan.openings]
    )
    for kind, f in all_feats:
        if f.wall not in plan.walls:
            errors.append(f"{kind} on unknown wall '{f.wall}'")
            continue
        w = plan.walls[f.wall]
        p1, p2, _dx, _dy, length = _wall_geom(plan, w)
        if f.offset < -EPS or f.offset + f.width > length + EPS:
            errors.append(
                f"{kind} on wall {w.name}: range "
                f"[{f.offset:.1f}, {f.offset + f.width:.1f}] "
                f"exceeds wall length {length:.1f}"
            )
        if kind == "door":
            axis = _axis(p1, p2)
            if axis == "h" and f.swing not in ("N", "S"):
                errors.append(
                    f"door on horizontal wall {w.name}: "
                    f"swing='{f.swing}' must be N or S"
                )
            elif axis == "v" and f.swing not in ("E", "W"):
                errors.append(
                    f"door on vertical wall {w.name}: "
                    f"swing='{f.swing}' must be E or W"
                )

    # --- 5: features on same wall overlap ---
    by_wall: dict[str, list] = {}
    for kind, f in all_feats:
        if f.wall in plan.walls:
            by_wall.setdefault(f.wall, []).append((kind, f))
    for wall_name, feats in by_wall.items():
        feats.sort(key=lambda kf: kf[1].offset)
        for (k1, f1), (k2, f2) in zip(feats, feats[1:]):
            if f1.offset + f1.width > f2.offset + EPS:
                errors.append(
                    f"wall {wall_name}: {k1} @[{f1.offset:.1f},"
                    f"{f1.offset + f1.width:.1f}] overlaps "
                    f"{k2} @[{f2.offset:.1f},{f2.offset + f2.width:.1f}]"
                )

    # --- 6: duplicate walls (same unordered endpoint pair) ---
    seen: dict[frozenset, str] = {}
    for w in plan.walls.values():
        key = frozenset([w.p1, w.p2])
        if key in seen:
            errors.append(f"duplicate walls: '{seen[key]}' and '{w.name}' "
                          f"share endpoints {set(key)}")
        else:
            seen[key] = w.name

    # --- 7: overlapping (collinear, sharing span) walls ---
    walls = list(plan.walls.values())
    for i, wa in enumerate(walls):
        p1a, p2a, *_ = _wall_geom(plan, wa)
        axis_a = _axis(p1a, p2a)
        if axis_a is None:
            continue
        for wb in walls[i + 1:]:
            p1b, p2b, *_ = _wall_geom(plan, wb)
            axis_b = _axis(p1b, p2b)
            if axis_a != axis_b:
                continue
            if axis_a == "h":
                if abs(p1a.y - p1b.y) > EPS:
                    continue
                a_lo, a_hi = sorted([p1a.x, p2a.x])
                b_lo, b_hi = sorted([p1b.x, p2b.x])
            else:
                if abs(p1a.x - p1b.x) > EPS:
                    continue
                a_lo, a_hi = sorted([p1a.y, p2a.y])
                b_lo, b_hi = sorted([p1b.y, p2b.y])
            overlap = min(a_hi, b_hi) - max(a_lo, b_lo)
            if overlap > EPS:
                errors.append(
                    f"walls {wa.name} and {wb.name} overlap by "
                    f"{overlap:.1f}\" (collinear, shared span)"
                )

    # --- 10: rooms / dims reference unknown points ---
    for r in plan.rooms:
        for n in r.bounds:
            if n not in plan.points:
                errors.append(f"room '{r.name}': unknown point '{n}' in bounds")
    for d in plan.dimensions:
        for n in (d.p1, d.p2):
            if n not in plan.points:
                errors.append(f"dimension: unknown point '{n}'")

    return errors, warnings


def format_issues(issues: list[str]) -> str:
    if not issues:
        return "OK — no issues found."
    return "\n".join(f"  • {s}" for s in issues)
