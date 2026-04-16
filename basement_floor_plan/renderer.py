"""Render a FloorPlan to SVG lines.

All inputs are in inches. Output is pixel-space SVG (via SCALE).
"""

from .helpers import SCALE, CANVAS_W, CANVAS_H, SVG_STYLES, px_to_dim, inches_to_dim
from .model import FloorPlan, Label

MARGIN_PX = 100  # canvas margin around the floor plan


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _P(inches):
    """inches → pixels (rounded int)."""
    return round(inches * SCALE)


def _excel_letter(n: int) -> str:
    """0→A, 1→B, ..., 25→Z, 26→AA, 27→AB, ..."""
    s = ""
    n += 1
    while n > 0:
        n -= 1
        s = chr(65 + (n % 26)) + s
        n //= 26
    return s


def _plan_center(plan):
    pts = list(plan.points.values())
    return (sum(p.x for p in pts) / len(pts), sum(p.y for p in pts) / len(pts))


_JUNCTION_EPS = 0.5    # inches — tolerance for "point lies on wall"


def _t_junction_points(plan, wall, p1, p2, length):
    """Return list of (offset, point.locked) for points that lie on this
    wall's interior (T-junctions). Offsets sorted ascending."""
    out = []
    if abs(p1.y - p2.y) < _JUNCTION_EPS:
        y = p1.y
        lo, hi = sorted([p1.x, p2.x])
        for pt in plan.points.values():
            if pt.name in (wall.p1, wall.p2):
                continue
            if abs(pt.y - y) > _JUNCTION_EPS:
                continue
            if lo + _JUNCTION_EPS < pt.x < hi - _JUNCTION_EPS:
                off = pt.x - p1.x if p2.x > p1.x else p1.x - pt.x
                out.append((off, pt.locked))
    elif abs(p1.x - p2.x) < _JUNCTION_EPS:
        x = p1.x
        lo, hi = sorted([p1.y, p2.y])
        for pt in plan.points.values():
            if pt.name in (wall.p1, wall.p2):
                continue
            if abs(pt.x - x) > _JUNCTION_EPS:
                continue
            if lo + _JUNCTION_EPS < pt.y < hi - _JUNCTION_EPS:
                off = pt.y - p1.y if p2.y > p1.y else p1.y - pt.y
                out.append((off, pt.locked))
    out.sort()
    return out


def _t_junction_offsets(plan, wall, p1, p2, length):
    """Offset-only variant used by the wall cut-out renderer."""
    return [o for o, _ in _t_junction_points(plan, wall, p1, p2, length)]


def _wall_vec(plan, wall):
    """Return (p1, p2, unit_x, unit_y, length_in_inches)."""
    p1 = plan.points[wall.p1]
    p2 = plan.points[wall.p2]
    dx, dy = p2.x - p1.x, p2.y - p1.y
    length = (dx * dx + dy * dy) ** 0.5
    if length == 0:
        raise ValueError(f"Wall '{wall.name}' has zero length")
    return p1, p2, dx / length, dy / length, length


def _feat_endpoints(p1, ux, uy, feat):
    """Return start/end inch-coords of a feature along its wall."""
    sx = p1.x + ux * feat.offset
    sy = p1.y + uy * feat.offset
    ex = p1.x + ux * (feat.offset + feat.width)
    ey = p1.y + uy * (feat.offset + feat.width)
    return (sx, sy), (ex, ey)


# ---------------------------------------------------------------------------
# Door arc
# ---------------------------------------------------------------------------

_SWING_VEC = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}


def _door_arc(p1, ux, uy, door):
    """Return SVG path strings for a door's swing arc(s)."""
    (sx, sy), (ex, ey) = _feat_endpoints(p1, ux, uy, door)
    sdx, sdy = _SWING_VEC[door.swing]
    paths = []

    if door.leaves == 1:
        if door.hinge == "start":
            hx, hy, tx, ty = sx, sy, ex, ey
        else:
            hx, hy, tx, ty = ex, ey, sx, sy
        ox = hx + sdx * door.width
        oy = hy + sdy * door.width
        paths.append(_arc_svg(tx, ty, ox, oy, hx, hy, door.width))
    else:
        # Two leaves: hinge at each end, tips meet in the middle.
        mx = (sx + ex) / 2
        my = (sy + ey) / 2
        leaf = door.width / 2
        o1x = sx + sdx * leaf
        o1y = sy + sdy * leaf
        paths.append(_arc_svg(mx, my, o1x, o1y, sx, sy, leaf))
        o2x = ex + sdx * leaf
        o2y = ey + sdy * leaf
        paths.append(_arc_svg(mx, my, o2x, o2y, ex, ey, leaf))

    return paths


def _arc_svg(tip_x, tip_y, open_x, open_y, hinge_x, hinge_y, radius_in):
    v1x, v1y = tip_x - hinge_x, tip_y - hinge_y
    v2x, v2y = open_x - hinge_x, open_y - hinge_y
    cross = v1x * v2y - v1y * v2x
    sweep = 1 if cross > 0 else 0
    r = _P(radius_in)
    return (f'<path d="M {_P(tip_x)} {_P(tip_y)} '
            f'A {r} {r} 0 0 {sweep} {_P(open_x)} {_P(open_y)}" class="door"/>')


# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------

_TICK = 5


def _dim_line(plan, dim):
    p1 = plan.points[dim.p1]
    p2 = plan.points[dim.p2]
    dim_class = "dim" if dim.locked else "dim-loose"
    # Loose dimension if either point unlocked or the dim itself unlocked
    if not dim.locked or not p1.locked or not p2.locked:
        dim_class = "dim-loose"

    if dim.axis == "h":
        x1, x2 = _P(p1.x), _P(p2.x)
        y = _P((p1.y + p2.y) / 2 + dim.offset)
        wall_y = _P(p1.y)
    else:
        y1, y2 = _P(p1.y), _P(p2.y)
        x = _P((p1.x + p2.x) / 2 + dim.offset)
        wall_x = _P(p1.x)

    gap = 8
    if dim.axis == "h":
        ey1, ey2 = min(wall_y, y) - gap, max(wall_y, y) + gap
        label = px_to_dim(x2 - x1)
        return [
            f'<line x1="{x1}" y1="{ey1}" x2="{x1}" y2="{ey2}" class="ext"/>',
            f'<line x1="{x2}" y1="{ey1}" x2="{x2}" y2="{ey2}" class="ext"/>',
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="dimline"/>',
            f'<line x1="{x1}" y1="{y-_TICK}" x2="{x1}" y2="{y+_TICK}" class="tick"/>',
            f'<line x1="{x2}" y1="{y-_TICK}" x2="{x2}" y2="{y+_TICK}" class="tick"/>',
            f'<text x="{(x1+x2)/2}" y="{y-7}" text-anchor="middle" class="{dim_class}">{label}</text>',
        ]
    else:
        ex1, ex2 = min(wall_x, x) - gap, max(wall_x, x) + gap
        label = px_to_dim(y2 - y1)
        cy = (y1 + y2) / 2
        return [
            f'<line x1="{ex1}" y1="{y1}" x2="{ex2}" y2="{y1}" class="ext"/>',
            f'<line x1="{ex1}" y1="{y2}" x2="{ex2}" y2="{y2}" class="ext"/>',
            f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="dimline"/>',
            f'<line x1="{x-_TICK}" y1="{y1}" x2="{x+_TICK}" y2="{y1}" class="tick"/>',
            f'<line x1="{x-_TICK}" y1="{y2}" x2="{x+_TICK}" y2="{y2}" class="tick"/>',
            f'<text x="{x-8}" y="{cy}" text-anchor="middle" class="{dim_class}"'
            f' transform="rotate(-90 {x-8} {cy})">{label}</text>',
        ]


# ---------------------------------------------------------------------------
# Polygon centroid (for auto-placed room labels)
# ---------------------------------------------------------------------------

def _polygon_centroid(pts):
    n = len(pts)
    if n < 3:
        return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
    a = 0.0
    cx = cy = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        cross = x1 * y2 - x2 * y1
        a += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    a *= 0.5
    if abs(a) < 1e-9:
        return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
    return (cx / (6 * a), cy / (6 * a))


# ---------------------------------------------------------------------------
# Fixtures & stairs
# ---------------------------------------------------------------------------

def _render_fixture(f):
    x, y, w, h = _P(f.x), _P(f.y), _P(f.w), _P(f.h)
    out = []
    if f.kind == "toilet":
        tank_w, tank_h = w, h
        cx = x + tank_w // 2
        bowl_cy = y + tank_h + _P(10)
        out.append(f'<rect x="{x}" y="{y}" width="{tank_w}" height="{tank_h}" rx="3" class="thin"/>')
        out.append(f'<ellipse cx="{cx}" cy="{bowl_cy}" rx="{_P(7)}" ry="{_P(10)}" class="thin"/>')
    elif f.kind == "sink":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" class="thin"/>')
        out.append(f'<circle cx="{x + w // 2}" cy="{y + h // 2}" r="5" class="thin"/>')
    elif f.kind == "shower":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" class="thin"/>')
        out.append(f'<circle cx="{x + w // 2}" cy="{y + h // 2}" r="8" class="thin"/>')
        out.append(f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}"'
                   f' stroke="#666" stroke-width="1" stroke-dasharray="4 3"/>')
    elif f.kind == "fireplace":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"'
                   f' fill="#d4c4b0" stroke="#555" stroke-width="2" rx="2"/>')
        inner_w = round(w * 0.75)
        inner_h = max(_P(2.5), 4)
        ix = x + (w - inner_w) // 2
        iy = y + h - inner_h - 2
        out.append(f'<rect x="{ix}" y="{iy}" width="{inner_w}" height="{inner_h}"'
                   f' fill="#2a2a2a" stroke="#333" stroke-width="1" rx="2"/>')
        if f.label:
            out.append(f'<text x="{x + w // 2}" y="{y + h + 14}"'
                       f' text-anchor="middle" class="small">{f.label}</text>')
    elif f.kind == "rect":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"'
                   f' fill="#e0e0e0" stroke="#555" stroke-width="1.5" rx="2"/>')
        if f.label:
            lines = f.label.split("\n")
            cx = x + w // 2
            cy = y + h // 2
            total_h = (len(lines) - 1) * 13
            start_y = cy - total_h // 2 + 4
            for i, line in enumerate(lines):
                out.append(f'<text x="{cx}" y="{start_y + i * 13}"'
                           f' text-anchor="middle" class="small">{line}</text>')
    return out


def _render_stairs(st):
    x, y = _P(st.x), _P(st.y)
    w, h = _P(st.w), _P(st.h)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" class="thin"/>']
    for i in range(1, st.steps):
        step_x = x + round(i * w / st.steps)
        out.append(f'<line x1="{step_x}" y1="{y}" x2="{step_x}" y2="{y + h}" class="thin"/>')
    out.append(f'<line x1="{x}" y1="{y + h // 2}" x2="{x + w}" y2="{y + h // 2}" class="thin"/>')
    return out


# ---------------------------------------------------------------------------
# Room & label rendering
# ---------------------------------------------------------------------------

def _render_room_label(plan, room):
    if room.label_pos is not None:
        lx, ly = _P(room.label_pos[0]), _P(room.label_pos[1])
    elif room.bounds:
        coords = [(plan.points[n].x, plan.points[n].y) for n in room.bounds]
        cx, cy = _polygon_centroid(coords)
        lx, ly = _P(cx), _P(cy)
    else:
        return []
    text = room.label or room.name
    return [f'<text x="{lx}" y="{ly}" text-anchor="middle" class="{room.label_style}">{text}</text>']


def _render_label(lab: Label):
    x, y = _P(lab.x), _P(lab.y)
    if lab.wall_label:
        return [
            '<g class="wlabel">',
            f'<circle cx="{x}" cy="{y}" r="10"/>',
            f'<text x="{x}" y="{y}">{lab.text}</text>',
            '</g>',
        ]
    return [f'<text x="{x}" y="{y}" text-anchor="{lab.anchor}" class="{lab.style}">{lab.text}</text>']


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render(plan: FloorPlan):
    """Return SVG line list — includes opening <svg> and closing </g>.

    Caller is responsible for appending </svg> after any additional layers
    (e.g. furniture) drawn inside the translated group.
    """
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}"'
        f' viewBox="0 0 {CANVAS_W} {CANVAS_H}">',
        SVG_STYLES,
        f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="#f6f6f6"/>',
        f'<g transform="translate({MARGIN_PX},{MARGIN_PX})">',
    ]

    # Walls (with feature cut-outs overdrawn in background color).
    # Wall labels are rendered separately by `render_wall_labels()` so the
    # CLI can paint them on top of furniture.
    for wall in plan.walls.values():
        p1, p2, ux, uy, length = _wall_vec(plan, wall)
        wclass = "wall" if wall.locked else "wall-loose"
        out.append(
            f'<line x1="{_P(p1.x)}" y1="{_P(p1.y)}" x2="{_P(p2.x)}" y2="{_P(p2.y)}"'
            f' class="{wclass}"/>'
        )
        for kind, feat in plan.features_on(wall.name):
            (sx, sy), (ex, ey) = _feat_endpoints(p1, ux, uy, feat)
            out.append(
                f'<line x1="{_P(sx)}" y1="{_P(sy)}" x2="{_P(ex)}" y2="{_P(ey)}"'
                f' stroke="#f6f6f6" stroke-width="20"/>'
            )
            if kind == "window":
                out.append(
                    f'<line x1="{_P(sx)}" y1="{_P(sy)}" x2="{_P(ex)}" y2="{_P(ey)}"'
                    f' stroke="#999" stroke-width="2"/>'
                )
            elif kind == "door":
                out += _door_arc(p1, ux, uy, feat)

    for f in plan.fixtures:
        out += _render_fixture(f)

    for st in plan.stairs:
        out += _render_stairs(st)

    for room in plan.rooms:
        out += _render_room_label(plan, room)

    for lab in plan.labels:
        out += _render_label(lab)

    for dim in plan.dimensions:
        out += _dim_line(plan, dim)

    out.append('</g>')
    return out


def close_svg():
    return ['</svg>']


def render_wall_labels(plan: FloorPlan):
    """Return SVG lines for per-segment wall labels + length annotations.

    Layers: (1) a red-bordered ellipse with the segment name, and (2) a
    small text below it showing the segment length. Length style depends
    on whether both endpoints of the segment are locked:
      - locked  → bold black (`.segdim`)
      - loose   → gray italic (`.segdim-loose`)
    Segments break at features (doors/windows/openings) and at T-junction
    points. Label text: `<wall-name>` for single-segment walls,
    `<wall-name>.<idx>` otherwise. Door and window spans don't consume an
    index (so adding/removing a door won't shift segment numbers);
    openings do consume an index.
    """
    out = []
    cx_plan, cy_plan = _plan_center(plan)
    for wall in plan.walls.values():
        p1, p2, ux, uy, length = _wall_vec(plan, wall)
        junctions = _t_junction_points(plan, wall, p1, p2, length)

        # Collect (offset, locked, kind) split markers.
        # kind: "end" | "junction" | "feat"
        splits = [
            (0.0, plan.points[wall.p1].locked, "end"),
            (length, plan.points[wall.p2].locked, "end"),
        ]
        for off, lk in junctions:
            splits.append((off, lk, "junction"))

        feat_ranges = []  # (start, end, kind, locked)
        opening_ranges = []
        for kind, f in plan.features_on(wall.name):
            a, b = f.offset, f.offset + f.width
            splits.append((a, f.locked, "feat"))
            splits.append((b, f.locked, "feat"))
            feat_ranges.append((a, b, kind, f.locked))
            if kind == "opening":
                opening_ranges.append((a, b))

        # Sort & dedupe nearby split points (keep strongest locked info).
        splits.sort(key=lambda s: s[0])
        merged = []
        for off, lk, kind in splits:
            if merged and abs(merged[-1][0] - off) < 0.1:
                # same point — conservative: locked only if both are
                m_off, m_lk, m_kind = merged[-1]
                merged[-1] = (m_off, m_lk and lk, m_kind)
            else:
                merged.append((off, lk, kind))

        # Build segments with index numbering rule.
        segs = []  # (idx, a, b, visible, a_locked, b_locked)
        idx = 0
        for (a, a_lk, _), (b, b_lk, _) in zip(merged, merged[1:]):
            if b - a < 0.1:
                continue
            mid = (a + b) / 2
            covered_kind = None
            for fa, fb, k, _ in feat_ranges:
                if fa - 0.1 < mid < fb + 0.1:
                    covered_kind = k
                    break
            visible = covered_kind is None
            # Openings consume an index; doors/windows do not.
            if visible or covered_kind == "opening":
                idx += 1
            if visible and b - a >= 2:
                segs.append((idx, a, b, a_lk, b_lk))

        total_idx = idx
        for idx_i, a, b, a_lk, b_lk in segs:
            mid = (a + b) / 2
            mx = p1.x + ux * mid
            my = p1.y + uy * mid
            perp_x, perp_y = -uy, ux
            if (mx - cx_plan) * perp_x + (my - cy_plan) * perp_y < 0:
                perp_x, perp_y = uy, -ux
            lx = _P(mx + perp_x * 6)
            ly = _P(my + perp_y * 6)
            text = wall.name if total_idx <= 1 else f"{wall.name}.{idx_i}"
            rx = max(10, 5 + 4 * len(text))
            out += [
                '<g class="wlabel">',
                f'<ellipse cx="{lx}" cy="{ly}" rx="{rx}" ry="10"/>',
                f'<text x="{lx}" y="{ly}">{text}</text>',
                '</g>',
            ]
            # Length annotation, offset further out from the wall.
            dx = _P(mx + perp_x * 20) - lx
            dy = _P(my + perp_y * 20) - ly
            dim_x = lx + dx
            dim_y = ly + dy
            seg_locked = wall.locked and a_lk and b_lk
            cls = "segdim" if seg_locked else "segdim-loose"
            out.append(
                f'<text x="{dim_x}" y="{dim_y}" class="{cls}">{inches_to_dim(b - a)}</text>'
            )
    return out
