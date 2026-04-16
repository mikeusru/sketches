"""Scale, canvas constants, unit conversion, and SVG styles.

Nothing drawing-related — the renderer composes SVG from these primitives.
"""

# Scale: 735 px = 26' 3 3/4" = 315.75"
SCALE = 735 / 315.75  # px per inch ≈ 2.328

# Canvas
CANVAS_W, CANVAS_H = 1200, 1500


def px(inches):
    """Convert real-world inches to pixel distance (rounded int)."""
    return round(inches * SCALE)


def px_to_dim(px_val):
    """Convert a pixel distance to a human-readable feet-inches string."""
    return inches_to_dim(abs(px_val) / SCALE)


def inches_to_dim(inches):
    """Convert inches (float) directly to a feet-inches string."""
    inches = abs(inches)
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


SVG_STYLES = """\
<defs>
<style><![CDATA[
.wall{stroke:#111;stroke-width:16;fill:none;stroke-linecap:square;stroke-linejoin:miter}
.wall-loose{stroke:#b85c00;stroke-width:10;fill:none;stroke-dasharray:8 5;stroke-linecap:square}
.thin{stroke:#666;stroke-width:2;fill:none}
.door{stroke:#666;stroke-width:2;fill:none}
.label{font:16px Arial,sans-serif;fill:#222}
.small{font:12px Arial,sans-serif;fill:#444}
.room{font:20px Arial,sans-serif;fill:#222}
.room2{font:18px Arial,sans-serif;fill:#222}
.note{font:14px Arial,sans-serif;fill:#8a4b00}
.dim{font:12px Arial,sans-serif;fill:#333}
.dim-loose{font:12px Arial,sans-serif;fill:#b85c00;font-style:italic}
.dimline{stroke:#333;stroke-width:1;fill:none}
.ext{stroke:#333;stroke-width:0.75;fill:none}
.tick{stroke:#333;stroke-width:1.5}
.wlabel circle, .wlabel ellipse{fill:#fff;stroke:#c00;stroke-width:1.5}
.wlabel text{font:bold 11px Arial,sans-serif;fill:#c00;text-anchor:middle;dominant-baseline:central}
.segdim{font:bold 11px Arial,sans-serif;fill:#111;text-anchor:middle;dominant-baseline:central}
.segdim-loose{font:11px Arial,sans-serif;fill:#888;font-style:italic;text-anchor:middle;dominant-baseline:central}
.furn{stroke:#4682b4;stroke-width:1.5;fill:#e8f0fe}
.furn-label{font:12px Arial,sans-serif;fill:#4682b4;text-anchor:middle}
]]></style>
</defs>"""
