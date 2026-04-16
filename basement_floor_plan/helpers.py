"""Drawing utilities and scale constants for basement floor plan SVG generation."""

# Scale: 735 px = 26' 3 3/4" = 315.75"
SCALE = 735 / 315.75  # px per inch ≈ 2.328

# Canvas (extra space for legend / notes)
CANVAS_W, CANVAS_H = 1200, 1500
OFFSET = 50  # extra margin around floor plan


def px(inches):
    """Convert real-world inches to pixel distance."""
    return round(inches * SCALE)


def px_to_dim(px_val):
    """Convert a pixel distance to a human-readable feet-inches string."""
    inches = abs(px_val) / SCALE
    ft = int(inches // 12)
    rem = inches % 12
    whole = int(rem)
    frac = rem - whole
    q = round(frac * 4) / 4
    if q >= 1:
        whole += 1
        q = 0
    parts = []
    if ft:
        parts.append(f"{ft}\u2032")
    if whole and q:
        fr = {0.25: "\u00bc", 0.5: "\u00bd", 0.75: "\u00be"}[q]
        parts.append(f"{whole}{fr}\u2033")
    elif whole:
        parts.append(f"{whole}\u2033")
    elif q:
        fr = {0.25: "\u00bc", 0.5: "\u00bd", 0.75: "\u00be"}[q]
        parts.append(f"{fr}\u2033")
    elif not ft:
        parts.append("0\u2033")
    return " ".join(parts)


# --- SVG building blocks ---

_TICK = 5  # tick half-length for dimension lines

SVG_STYLES = """\
<defs>
<style><![CDATA[
.wall{stroke:#111;stroke-width:16;fill:none;stroke-linecap:square;stroke-linejoin:miter}
.thin{stroke:#666;stroke-width:2;fill:none}
.door{stroke:#666;stroke-width:2;fill:none}
.label{font:16px Arial,sans-serif;fill:#222}
.small{font:12px Arial,sans-serif;fill:#444}
.room{font:20px Arial,sans-serif;fill:#222}
.room2{font:18px Arial,sans-serif;fill:#222}
.note{font:14px Arial,sans-serif;fill:#8a4b00}
.dim{font:12px Arial,sans-serif;fill:#333}
.dimline{stroke:#333;stroke-width:1;fill:none}
.ext{stroke:#333;stroke-width:0.75;fill:none}
.tick{stroke:#333;stroke-width:1.5}
.guide{stroke:#aaa;stroke-width:1.5;fill:none;stroke-dasharray:5 4}
.wlabel circle{fill:#fff;stroke:#c00;stroke-width:1.5}
.wlabel text{font:bold 11px Arial,sans-serif;fill:#c00;text-anchor:middle;dominant-baseline:central}
.furn{stroke:#4682b4;stroke-width:1.5;fill:#e8f0fe}
.furn-label{font:12px Arial,sans-serif;fill:#4682b4;text-anchor:middle}
]]></style>
</defs>"""


def svg_preamble():
    """Return opening SVG lines: <svg> tag, styles, background."""
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}"'
        f' viewBox="0 0 {CANVAS_W} {CANVAS_H}">',
        SVG_STYLES,
        f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="#f6f6f6"/>',
        f'<g transform="translate({OFFSET},{OFFSET})">',
    ]


def dim_h(x1, x2, y, label=None, wall_y=None, gap=8):
    """Horizontal dimension line → list of SVG strings."""
    if label is None:
        label = px_to_dim(x2 - x1)
    out = []
    if wall_y is not None:
        ey1, ey2 = min(wall_y, y) - gap, max(wall_y, y) + gap
        out.append(f'<line x1="{x1}" y1="{ey1}" x2="{x1}" y2="{ey2}" class="ext"/>')
        out.append(f'<line x1="{x2}" y1="{ey1}" x2="{x2}" y2="{ey2}" class="ext"/>')
    out.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="dimline"/>')
    out.append(f'<line x1="{x1}" y1="{y-_TICK}" x2="{x1}" y2="{y+_TICK}" class="tick"/>')
    out.append(f'<line x1="{x2}" y1="{y-_TICK}" x2="{x2}" y2="{y+_TICK}" class="tick"/>')
    cx = (x1 + x2) / 2
    out.append(f'<text x="{cx}" y="{y-7}" text-anchor="middle" class="dim">{label}</text>')
    return out


def dim_v(y1, y2, x, label=None, wall_x=None, gap=8):
    """Vertical dimension line → list of SVG strings."""
    if label is None:
        label = px_to_dim(y2 - y1)
    out = []
    if wall_x is not None:
        ex1, ex2 = min(wall_x, x) - gap, max(wall_x, x) + gap
        out.append(f'<line x1="{ex1}" y1="{y1}" x2="{ex2}" y2="{y1}" class="ext"/>')
        out.append(f'<line x1="{ex1}" y1="{y2}" x2="{ex2}" y2="{y2}" class="ext"/>')
    out.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="dimline"/>')
    out.append(f'<line x1="{x-_TICK}" y1="{y1}" x2="{x+_TICK}" y2="{y1}" class="tick"/>')
    out.append(f'<line x1="{x-_TICK}" y1="{y2}" x2="{x+_TICK}" y2="{y2}" class="tick"/>')
    cy = (y1 + y2) / 2
    out.append(f'<text x="{x-8}" y="{cy}" text-anchor="middle" class="dim"'
               f' transform="rotate(-90 {x-8} {cy})">{label}</text>')
    return out


def wlabel(x, y, letter):
    """Wall label (red circle + letter) → list of SVG strings."""
    return [
        f'<g class="wlabel"><circle cx="{x}" cy="{y}" r="10"/>',
        f'<text x="{x}" y="{y}">{letter}</text></g>',
    ]
