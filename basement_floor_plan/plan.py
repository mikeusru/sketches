from pathlib import Path
import argparse


def main():
    # Canvas + scale
    W, H = 980, 1290
    left, top = 50, 50
    outer_w, outer_h = 735, 1190

    # Scale: 735 px = 26' 3 3/4" = 315.75"
    SCALE = 735 / 315.75  # px per inch ≈ 2.328

    def px_to_dim(px):
        """Convert a pixel distance to a feet-inches string."""
        inches = abs(px) / SCALE
        ft = int(inches // 12)
        rem = inches % 12
        whole = int(rem)
        frac = rem - whole
        # snap to nearest 1/4"
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

    # Key geometry (approximate, based on image + user corrections)
    x_left = left
    x_right = left + outer_w
    y_top = top
    y_bottom = top + outer_h

    # Main vertical split seen in plan
    x_center = 392

    # Left-side storage/bath block
    storage_w = 131   # ~4'8" on this drawing scale
    x_storage_right = x_left + storage_w
    y_bath_top = 559  # shared wall with laundry = foyer top
    y_bath_mid = 711
    y_bath2_bottom = 870  # divider between 2nd bathroom and storage

    # Foyer/hall top horizontal
    y_foyer_top = 559

    # Mechanical room / rec room
    y_mech_top = 697
    y_mech_bottom = 877   # 13' above bottom wall
    x_mech_left = 392
    x_mech_right = x_right  # user said outside width more like 12', basically full right bay

    # Door opening from hall into mech on LEFT side wall, not bottom
    mech_door_y1 = y_mech_bottom - 60
    mech_door_y2 = y_mech_bottom - 10

    # Rec room useful depth marker from user:
    # bottom wall to bottom mechanical room wall is about 13'
    # We'll annotate that, not fully solve global scaling yet.

    svg = []
    A = svg.append

    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    A('''<defs>
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
</defs>''')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f6f6f6"/>')

    # Window positions
    # Wall A (top): existing window
    win_a_x1, win_a_x2 = 134, 246
    # Wall C (bottom): 7' from right wall
    win_c_w = 98  # keep existing width
    win_c_x2 = x_right - round(7 * 12 * SCALE)  # 7' from right
    win_c_x1 = win_c_x2 - win_c_w
    # Wall B (right): three windows
    win_b = [(162, 207), (408, 462), (1008, 1082)]

    # Outer shell
    A(f'<rect x="{left}" y="{top}" width="{outer_w}" height="{outer_h}" class="wall"/>')

    # Window notches
    for x1, x2, y in [(win_a_x1, win_a_x2, y_top), (win_c_x1, win_c_x2, y_bottom)]:
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#f6f6f6" stroke-width="20"/>')
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#999" stroke-width="2"/>')
    for y1, y2 in win_b:
        A(f'<line x1="{x_right}" y1="{y1}" x2="{x_right}" y2="{y2}" stroke="#f6f6f6" stroke-width="20"/>')
        A(f'<line x1="{x_right}" y1="{y1}" x2="{x_right}" y2="{y2}" stroke="#999" stroke-width="2"/>')

    # Main center partition / hall guide
    A(f'<line x1="{x_center}" y1="{y_top}" x2="{x_center}" y2="{y_foyer_top}" class="wall"/>')
    A(f'<line x1="{x_center-50}" y1="{y_top}" x2="{x_center-50}" y2="{y_bottom}" class="thin" opacity="0.55"/>')
    A(f'<line x1="{x_center-2}" y1="{y_top}" x2="{x_center-2}" y2="{y_bottom}" class="thin" opacity="0.55"/>')

    # Left side bath/storage block
    # bath top wall is shared with laundry (foyer wall handles x_left to 274)
    # extend the shared wall across the bath/storage block right wall
    A(f'<line x1="{x_storage_right}" y1="{y_bath_top}" x2="{x_storage_right}" y2="{y_bottom}" class="wall"/>')
    # bathroom 1 / bathroom 2 divider
    A(f'<line x1="{x_left}" y1="{y_bath_mid}" x2="{x_storage_right}" y2="{y_bath_mid}" class="wall"/>')
    # bathroom 2 / storage closet divider
    A(f'<line x1="{x_left}" y1="{y_bath2_bottom}" x2="{x_storage_right}" y2="{y_bath2_bottom}" class="wall"/>')

    # Foyer-to-rec-room wall (with door opening)
    foyer_rec_door_x1 = 240
    foyer_rec_door_x2 = 300
    A(f'<line x1="{x_storage_right}" y1="{y_mech_top}" x2="{foyer_rec_door_x1}" y2="{y_mech_top}" class="wall"/>')
    A(f'<line x1="{foyer_rec_door_x2}" y1="{y_mech_top}" x2="{x_mech_left}" y2="{y_mech_top}" class="wall"/>')

    # Foyer top wall
    A(f'<line x1="{x_left}" y1="{y_foyer_top}" x2="274" y2="{y_foyer_top}" class="wall"/>')
    A(f'<line x1="344" y1="{y_foyer_top}" x2="462" y2="{y_foyer_top}" class="wall"/>')

    # Mechanical room walls
    A(f'<line x1="{x_mech_left}" y1="{y_mech_top}" x2="{x_mech_right}" y2="{y_mech_top}" class="wall"/>')
    # left wall with door opening from left side
    A(f'<line x1="{x_mech_left}" y1="{y_mech_top}" x2="{x_mech_left}" y2="{mech_door_y1}" class="wall"/>')
    A(f'<line x1="{x_mech_left}" y1="{mech_door_y2}" x2="{x_mech_left}" y2="{y_mech_bottom}" class="wall"/>')
    A(f'<line x1="{x_mech_left}" y1="{y_mech_bottom}" x2="{x_mech_right}" y2="{y_mech_bottom}" class="wall"/>')

    # Air handler (top-left of mech room, 3' wide x 4' deep)
    ah_w = round(3 * 12 * SCALE)   # 3'
    ah_h = round(4 * 12 * SCALE)   # 4'
    ah_x = x_mech_left + 8  # slight padding from wall
    ah_y = y_mech_top + 8
    A(f'<rect x="{ah_x}" y="{ah_y}" width="{ah_w}" height="{ah_h}" fill="#e0e0e0" stroke="#555" stroke-width="1.5" rx="2"/>')
    A(f'<text x="{ah_x + ah_w//2}" y="{ah_y + ah_h//2 - 6}" text-anchor="middle" class="small">Air</text>')
    A(f'<text x="{ah_x + ah_w//2}" y="{ah_y + ah_h//2 + 10}" text-anchor="middle" class="small">Handler</text>')

    # Stairs block
    stairs_x, stairs_y, stairs_w, stairs_h = 504, 571, 182, 126
    A(f'<rect x="{stairs_x}" y="{stairs_y}" width="{stairs_w}" height="{stairs_h}" fill="none" class="thin"/>')
    for i in range(1, 7):
        x = stairs_x + i * 26
        A(f'<line x1="{x}" y1="{stairs_y}" x2="{x}" y2="{stairs_y+stairs_h}" class="thin"/>')
    A(f'<line x1="{stairs_x}" y1="{stairs_y+63}" x2="{stairs_x+stairs_w}" y2="{stairs_y+63}" class="thin"/>')

    # Doors
    # storage closet door from rec room (top of storage, near wall I)
    sc_door_y1 = y_bath2_bottom + 10
    sc_door_y2 = sc_door_y1 + 60
    A(f'<line x1="{x_storage_right}" y1="{sc_door_y1}" x2="{x_storage_right}" y2="{sc_door_y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {x_storage_right} {sc_door_y1} A 60 60 0 0 1 {x_storage_right-60} {sc_door_y2}" class="door"/>')

    # bath door (on right wall, opens into foyer)
    A(f'<line x1="{x_storage_right}" y1="610" x2="{x_storage_right}" y2="670" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {x_storage_right} 610 A 60 60 0 0 1 {x_storage_right+60} 670" class="door"/>')

    # foyer double-door from laundry (only one — no laundry-to-bath door)
    A(f'<line x1="284" y1="560" x2="344" y2="560" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 344 560 A 60 60 0 0 0 284 620" class="door"/>')

    # foyer-to-rec-room door
    A(f'<line x1="{foyer_rec_door_x1}" y1="{y_mech_top}" x2="{foyer_rec_door_x2}" y2="{y_mech_top}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {foyer_rec_door_x1} {y_mech_top} A 60 60 0 0 0 {foyer_rec_door_x2} {y_mech_top+60}" class="door"/>')

    # exterior/bottom door (SEALED OFF — shown as dashed wall)
    A(f'<line x1="190" y1="{y_bottom}" x2="250" y2="{y_bottom}" stroke="#111" stroke-width="16" stroke-dasharray="8 6"/>')

    # mech room door from LEFT side
    A(f'<line x1="{x_mech_left}" y1="{mech_door_y1}" x2="{x_mech_left}" y2="{mech_door_y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {x_mech_left} {mech_door_y1} A 50 50 0 0 0 {x_mech_left-50} {mech_door_y2}" class="door"/>')

    # Foyer double door
    A(f'<line x1="255" y1="{y_foyer_top}" x2="335" y2="{y_foyer_top}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 255 {y_foyer_top} A 40 40 0 0 0 295 {y_foyer_top+40}" class="door"/>')
    A(f'<path d="M 335 {y_foyer_top} A 40 40 0 0 1 295 {y_foyer_top+40}" class="door"/>')

    # Labels
    A('<text x="147" y="330" class="room2">Laundry</text>')
    A('<text x="560" y="330" class="room2">Family Room</text>')
    A('<text x="234" y="640" class="room2">FOYER</text>')
    A(f'<text x="{x_storage_right-62}" y="{y_bottom-16}" class="small">Storage</text>')
    A(f'<text x="{x_storage_right-62}" y="{y_bottom-4}" class="small">Closet</text>')
    A(f'<text x="{x_left+14}" y="{y_bath_top + 95}" class="small">Bath 1</text>')
    A(f'<text x="{x_left+14}" y="{(y_bath_mid+y_bath2_bottom)//2+5}" class="small">Bath 2</text>')
    A('<text x="543" y="760" class="small">MECHANICAL ROOM</text>')
    A(f'<text x="{(x_storage_right + x_right)//2 + 30}" y="{y_bottom - 30}" class="room">Rec Room</text>')

    # --- Bath 1 fixtures (toilet + sink on bottom) ---
    # Toilet bottom-left
    A(f'<ellipse cx="{x_left+30}" cy="{y_bath_mid-35}" rx="14" ry="20" class="thin"/>')
    A(f'<rect x="{x_left+16}" y="{y_bath_mid-65}" width="28" height="14" rx="3" class="thin"/>')  # tank

    # Sink/vanity bottom-right
    A(f'<rect x="{x_storage_right-42}" y="{y_bath_mid-42}" width="34" height="22" rx="2" class="thin"/>')
    A(f'<circle cx="{x_storage_right-25}" cy="{y_bath_mid-31}" r="5" class="thin"/>')  # basin

    # --- Bath 2 fixtures (shower bottom, toilet top-left, sink top-right) ---
    # Shower at bottom
    sh_y = y_bath2_bottom - 66
    A(f'<rect x="{x_left+8}" y="{sh_y}" width="{storage_w-16}" height="66" fill="none" class="thin"/>')
    A(f'<circle cx="{x_left+storage_w//2}" cy="{sh_y+33}" r="8" class="thin"/>')  # drain
    A(f'<line x1="{x_left+8}" y1="{sh_y}" x2="{x_left+storage_w-8}" y2="{sh_y}" stroke="#666" stroke-width="1" stroke-dasharray="4 3"/>')

    # Toilet top-left
    A(f'<ellipse cx="{x_left+30}" cy="{y_bath_mid+42}" rx="14" ry="20" class="thin"/>')
    A(f'<rect x="{x_left+16}" y="{y_bath_mid+12}" width="28" height="14" rx="3" class="thin"/>')

    # Sink/vanity top-right
    A(f'<rect x="{x_storage_right-42}" y="{y_bath_mid+10}" width="34" height="22" rx="2" class="thin"/>')
    A(f'<circle cx="{x_storage_right-25}" cy="{y_bath_mid+21}" r="5" class="thin"/>')

    # Bath 2 door (on right wall, moved down so sink fits above)
    b2_door_y1 = y_bath_mid + 70
    b2_door_y2 = b2_door_y1 + 60
    A(f'<line x1="{x_storage_right}" y1="{b2_door_y1}" x2="{x_storage_right}" y2="{b2_door_y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {x_storage_right} {b2_door_y1} A 60 60 0 0 1 {x_storage_right+60} {b2_door_y2}" class="door"/>')

    # --- Wall labels ---
    def wlabel(x, y, letter):
        A(f'<g class="wlabel"><circle cx="{x}" cy="{y}" r="10"/>')
        A(f'<text x="{x}" y="{y}">{letter}</text></g>')

    # Exterior walls
    wlabel((x_left + x_right) // 2, y_top - 3, 'A')       # top
    wlabel(x_right + 3, (y_top + y_bottom) // 2, 'B')      # right
    wlabel((x_left + x_right) // 2, y_bottom + 3, 'C')     # bottom
    wlabel(x_left - 3, (y_top + y_bottom) // 2, 'D')       # left

    # Center partition (laundry/family divider)
    wlabel(x_center + 14, (y_top + y_foyer_top) // 2, 'E')

    # Foyer top wall
    wlabel((x_left + 274) // 2, y_foyer_top - 14, 'F')

    # Bath/storage right wall
    wlabel(x_storage_right + 14, (y_bath_top + y_bottom) // 2, 'G')

    # Bath1 / Bath2 divider
    wlabel((x_left + x_storage_right) // 2, y_bath_mid - 14, 'H')

    # Bath2 / Storage divider
    wlabel((x_left + x_storage_right) // 2, y_bath2_bottom + 14, 'I')

    # Foyer-to-rec wall
    wlabel((x_storage_right + x_mech_left) // 2, y_mech_top + 14, 'J')

    # Mech room top wall
    wlabel((x_mech_left + x_mech_right) // 2, y_mech_top - 14, 'K')

    # Mech room left wall
    wlabel(x_mech_left - 14, (y_mech_top + y_mech_bottom) // 2, 'L')

    # Mech room bottom wall
    wlabel((x_mech_left + x_mech_right) // 2, y_mech_bottom + 14, 'M')

    # --- Dimension line helpers ---
    T = 5  # tick half-length

    def dim_h(x1, x2, y, label=None, wall_y=None, gap=8):
        """Horizontal dimension: extension lines, line, ticks, label."""
        if label is None:
            label = px_to_dim(x2 - x1)
        if wall_y is not None:
            ey1 = min(wall_y, y) - gap
            ey2 = max(wall_y, y) + gap
            A(f'<line x1="{x1}" y1="{ey1}" x2="{x1}" y2="{ey2}" class="ext"/>')
            A(f'<line x1="{x2}" y1="{ey1}" x2="{x2}" y2="{ey2}" class="ext"/>')
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="dimline"/>')
        A(f'<line x1="{x1}" y1="{y-T}" x2="{x1}" y2="{y+T}" class="tick"/>')
        A(f'<line x1="{x2}" y1="{y-T}" x2="{x2}" y2="{y+T}" class="tick"/>')
        cx = (x1 + x2) / 2
        A(f'<text x="{cx}" y="{y-7}" text-anchor="middle" class="dim">{label}</text>')

    def dim_v(y1, y2, x, label=None, wall_x=None, gap=8):
        """Vertical dimension: extension lines, line, ticks, label."""
        if label is None:
            label = px_to_dim(y2 - y1)
        if wall_x is not None:
            ex1 = min(wall_x, x) - gap
            ex2 = max(wall_x, x) + gap
            A(f'<line x1="{ex1}" y1="{y1}" x2="{ex2}" y2="{y1}" class="ext"/>')
            A(f'<line x1="{ex1}" y1="{y2}" x2="{ex2}" y2="{y2}" class="ext"/>')
        A(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="dimline"/>')
        A(f'<line x1="{x-T}" y1="{y1}" x2="{x+T}" y2="{y1}" class="tick"/>')
        A(f'<line x1="{x-T}" y1="{y2}" x2="{x+T}" y2="{y2}" class="tick"/>')
        cy = (y1 + y2) / 2
        A(f'<text x="{x-8}" y="{cy}" text-anchor="middle" class="dim"'
          f' transform="rotate(-90 {x-8} {cy})">{label}</text>')

    # =============================================
    # WALL A (top) — segmented dimensions
    # =============================================
    row1 = y_top - 25   # main bay widths
    row2 = y_top - 50   # window detail row

    # Bay widths
    dim_h(x_left, x_center, row1, wall_y=y_top)          # left bay
    dim_h(x_center, x_right, row1, wall_y=y_top)         # right bay

    # Wall A window segments
    dim_h(x_left, win_a_x1, row2, wall_y=y_top)          # wall to window
    dim_h(win_a_x1, win_a_x2, row2, wall_y=y_top)        # window width
    dim_h(win_a_x2, x_center, row2, wall_y=y_top)        # window to center

    # =============================================
    # WALL C (bottom) — segmented dimensions
    # =============================================
    row3 = y_bottom + 30  # overall width
    row4 = y_bottom + 55  # window detail + storage

    # Overall width
    dim_h(x_left, x_right, row3, wall_y=y_bottom)

    # Storage width
    dim_h(x_left, x_storage_right, row4, wall_y=y_bottom)

    # Wall C window segments
    row5 = y_bottom + 80
    dim_h(win_c_x1, win_c_x2, row5, wall_y=y_bottom)     # window width
    dim_h(win_c_x2, x_right, row5, wall_y=y_bottom)       # window to right wall (7')

    # =============================================
    # WALL B (right) — vertical window segments
    # =============================================
    col_b1 = x_right + 30  # first column
    col_b2 = x_right + 55  # second column

    # Top window
    dim_v(y_top, win_b[0][0], col_b1, wall_x=x_right)          # wall to window 1
    dim_v(win_b[0][0], win_b[0][1], col_b1, wall_x=x_right)    # window 1 height

    # Middle window
    dim_v(win_b[0][1], win_b[1][0], col_b1, wall_x=x_right)    # between windows 1-2
    dim_v(win_b[1][0], win_b[1][1], col_b1, wall_x=x_right)    # window 2 height

    # Bottom window (rec room)
    dim_v(win_b[2][0], win_b[2][1], col_b1, wall_x=x_right)    # window 3 height
    dim_v(win_b[2][1], y_bottom, col_b1, wall_x=x_right)       # window 3 to bottom

    # Major vertical sections
    dim_v(y_top, y_mech_top, col_b2, wall_x=x_right)            # top to mech
    dim_v(y_mech_top, y_mech_bottom, col_b2, wall_x=x_right)   # mech height
    dim_v(y_mech_bottom, y_bottom, col_b2, wall_x=x_right)     # rec room height

    # =============================================
    # WALL D (left) — vertical sections
    # =============================================
    col_d1 = x_left - 30
    col_d2 = x_left - 55

    # Overall
    dim_v(y_top, y_bottom, col_d1, wall_x=x_left)

    # Sections
    dim_v(y_top, y_foyer_top, col_d2, wall_x=x_left)         # laundry
    dim_v(y_foyer_top, y_bath_mid, col_d2, wall_x=x_left)    # bath 1
    dim_v(y_bath_mid, y_bath2_bottom, col_d2, wall_x=x_left) # bath 2
    dim_v(y_bath2_bottom, y_bottom, col_d2, wall_x=x_left)   # storage

    # =============================================
    # Interior horizontal dims
    # =============================================
    # Mech room width (inside above mech)
    dim_h(x_mech_left, x_mech_right, y_mech_top - 20, wall_y=y_mech_top)

    # --- Optional furniture ---
    furn = []
    FA = furn.append

    # BRIMNES wardrobe dimensions (used for bed centering too)
    brim_w_px = round(46 * SCALE)      # 46" width → ~107px (along y)
    brim_d_px = round(19.75 * SCALE)   # 19¾" depth → ~46px (along x)

    # King size bed: 76" x 80"
    # Against wall M, headboard at top, shifted right in rec room
    bed_w = round(76 * SCALE)   # 76" wide
    bed_h = round(80 * SCALE)   # 80" long
    bed_x = x_right - bed_w - round(24 * SCALE)  # 24" walkway to wall B
    bed_y = y_mech_bottom + 10
    FA(f'<rect x="{bed_x}" y="{bed_y}" width="{bed_w}" height="{bed_h}" rx="4" class="furn"/>')
    # pillows (against wall M)
    pw, ph = 78, 24
    FA(f'<rect x="{bed_x+6}" y="{bed_y+6}" width="{pw}" height="{ph}" rx="6" class="furn"/>')
    FA(f'<rect x="{bed_x+bed_w-pw-6}" y="{bed_y+6}" width="{pw}" height="{ph}" rx="6" class="furn"/>')
    FA(f'<text x="{bed_x+bed_w//2}" y="{bed_y+bed_h//2+5}" class="furn-label">King Bed</text>')

    # TV on wall C, centered under bed (bed already positioned to avoid window)
    tv_w = round(56.7 * SCALE)  # 65" diagonal ≈ 56.7" wide
    tv_h = 8
    tv_x = bed_x + bed_w // 2 - tv_w // 2
    tv_y = y_bottom - tv_h - 4  # hanging off wall C
    FA(f'<rect x="{tv_x}" y="{tv_y}" width="{tv_w}" height="{tv_h}" rx="1" fill="#333" stroke="#222" stroke-width="1"/>')
    FA(f'<text x="{tv_x+tv_w//2}" y="{tv_y-8}" class="furn-label">65\u2033 TV</text>')

    # Dresser on wall C, right of W4/W5 zone
    dr_w = round(5 * 12 * SCALE)   # 5' wide
    dr_h = round(1.5 * 12 * SCALE) # 1.5' deep
    dr_x = x_storage_right + brim_d_px + 20  # past wardrobe depth + gap
    dr_y = y_bottom - dr_h - 10
    FA(f'<rect x="{dr_x}" y="{dr_y}" width="{dr_w}" height="{dr_h}" rx="3" class="furn"/>')
    FA(f'<text x="{dr_x+dr_w//2}" y="{dr_y+dr_h//2+4}" class="furn-label">Dresser</text>')

    # === Laundry room furniture ===
    # Stacked washer/dryer (bottom of laundry, near wall F, against wall D)
    # ~27" x 30" footprint
    wd_w = round(27 * SCALE)   # ~63px
    wd_h = round(30 * SCALE)   # ~70px
    wd_x = x_left + 10
    wd_y = y_foyer_top - wd_h - 10  # near bottom wall F, against wall D
    FA(f'<rect x="{wd_x}" y="{wd_y}" width="{wd_w}" height="{wd_h}" rx="3" class="furn"/>')
    FA(f'<text x="{wd_x+wd_w//2}" y="{wd_y+wd_h//2-4}" class="furn-label">W/D</text>')
    FA(f'<text x="{wd_x+wd_w//2}" y="{wd_y+wd_h//2+10}" class="furn-label">Stacked</text>')

    # Smith cage / power rack (top-right of laundry, against wall E + wall A)
    # ~7' wide x 4' deep
    sm_w = round(4 * 12 * SCALE)   # 4' deep (along x, away from wall E)
    sm_h = round(7 * 12 * SCALE)   # 7' long (along y)
    sm_x = x_center - sm_w - 10    # against wall E
    sm_y = y_top + 10               # against wall A
    FA(f'<rect x="{sm_x}" y="{sm_y}" width="{sm_w}" height="{sm_h}" rx="2" class="furn"/>')
    FA(f'<text x="{sm_x+sm_w//2}" y="{sm_y+sm_h//2-4}" class="furn-label">Smith</text>')
    FA(f'<text x="{sm_x+sm_w//2}" y="{sm_y+sm_h//2+10}" class="furn-label">Cage</text>')

    # Standing desk (left side of laundry, against wall D, below window A)
    # Wall A window spans x 134-246; desk must start below y_top or right of 246
    # ~4' wide x 2' deep, placed against wall D below the window
    dk_w = round(2 * 12 * SCALE)   # 2' deep (along x, away from wall D)
    dk_h = round(4 * 12 * SCALE)   # 4' wide (along y)
    dk_x = x_left + 10              # against wall D
    dk_y = y_top + 10               # against wall A (desk is to LEFT of window, x 60-116, window starts at 134)
    FA(f'<rect x="{dk_x}" y="{dk_y}" width="{dk_w}" height="{dk_h}" rx="2" class="furn"/>')
    FA(f'<text x="{dk_x+dk_w//2}" y="{dk_y+dk_h//2-4}" class="furn-label">Standing</text>')
    FA(f'<text x="{dk_x+dk_w//2}" y="{dk_y+dk_h//2+10}" class="furn-label">Desk</text>')

    # Laundry room TV (middle of wall D, facing right)
    ltv_w, ltv_h = 8, 100
    ltv_x = x_left + 10  # inset from wall D centerline (≥8px)
    ltv_y = (y_top + y_foyer_top) // 2 - ltv_h // 2
    FA(f'<rect x="{ltv_x}" y="{ltv_y}" width="{ltv_w}" height="{ltv_h}" rx="1" fill="#333" stroke="#222" stroke-width="1"/>')
    FA(f'<text x="{ltv_x+ltv_w+12}" y="{ltv_y+ltv_h//2+4}" class="furn-label">TV</text>')

    # Family room TV on wall E (center partition, facing right)
    ftv_w, ftv_h = 8, 132  # vertical orientation
    ftv_x = x_center + 4  # hanging off right side of wall E
    ftv_y = (y_top + y_foyer_top) // 2 - ftv_h // 2
    FA(f'<rect x="{ftv_x}" y="{ftv_y}" width="{ftv_w}" height="{ftv_h}" rx="1" fill="#333" stroke="#222" stroke-width="1"/>')
    FA(f'<text x="{ftv_x+ftv_w+12}" y="{ftv_y+ftv_h//2+4}" class="furn-label">TV</text>')

    # Family room media console under TV on wall E
    # ~60" wide x 18" deep
    mc_w = round(18 * SCALE)   # 18" deep (along x, away from wall E)
    mc_h = round(60 * SCALE)   # 60" wide (along y)
    mc_x = ftv_x + ftv_w + 2  # just right of TV
    mc_y = ftv_y + (ftv_h - mc_h) // 2  # centered on TV
    FA(f'<rect x="{mc_x}" y="{mc_y}" width="{mc_w}" height="{mc_h}" rx="2" class="furn"/>')
    FA(f'<text x="{mc_x+mc_w//2}" y="{mc_y+mc_h//2-4}" class="furn-label">Media</text>')
    FA(f'<text x="{mc_x+mc_w//2}" y="{mc_y+mc_h//2+10}" class="furn-label">Console</text>')

    # Family room couch (against wall B, facing TV on wall E)
    # ~84" wide x 36" deep
    couch_w = round(36 * SCALE)    # 36" deep (along x)
    couch_h = round(84 * SCALE)    # 84" wide (along y)
    couch_x = x_right - couch_w - 10  # against wall B
    # Center between the two wall B windows (y 207 to 408)
    couch_y = (win_b[0][1] + win_b[1][0]) // 2 - couch_h // 2
    FA(f'<rect x="{couch_x}" y="{couch_y}" width="{couch_w}" height="{couch_h}" rx="4" class="furn"/>')
    FA(f'<text x="{couch_x+couch_w//2}" y="{couch_y+couch_h//2+5}" class="furn-label">Couch</text>')

    # === Storage closet: 2x IKEA BRIMNES wardrobe + vanity desk ===
    # Wardrobes against wall D (left wall), stacked along y-axis
    brim_x = x_left + 8
    brim_y1 = y_bath2_bottom + 40  # shifted down to clear storage closet door swing
    brim_y2 = brim_y1 + brim_w_px + 2  # 2px gap
    for i, by in enumerate((brim_y1, brim_y2), 1):
        FA(f'<rect x="{brim_x}" y="{by}" width="{brim_d_px}" height="{brim_w_px}" rx="2" class="furn"/>')
        FA(f'<text x="{brim_x+brim_d_px//2}" y="{by+brim_w_px//2+4}" class="furn-label">W{i}</text>')

    # Vanity / makeup desk against wall C in storage closet
    # ~48" wide x 20" deep
    van_w = round(48 * SCALE)   # 48" wide (along x)
    van_h = round(20 * SCALE)   # 20" deep (along y)
    van_x = x_left + 8
    van_y = y_bottom - van_h - 10  # against wall C
    FA(f'<rect x="{van_x}" y="{van_y}" width="{van_w}" height="{van_h}" rx="2" class="furn"/>')
    FA(f'<text x="{van_x+van_w//2}" y="{van_y+van_h//2+4}" class="furn-label">Vanity</text>')

    # === Rec room: 2x IKEA BRIMNES wardrobe against wall G ===
    # Wall G is x_storage_right; wardrobes below the storage closet door
    # Storage closet door: y 880-940 on wall G; start wardrobes below that
    rec_brim_x = x_storage_right + 8  # just right of wall G
    rec_brim_y1 = sc_door_y2 + 10     # below closet door swing
    rec_brim_y2 = rec_brim_y1 + brim_w_px + 4
    for i, by in enumerate((rec_brim_y1, rec_brim_y2), 3):
        FA(f'<rect x="{rec_brim_x}" y="{by}" width="{brim_d_px}" height="{brim_w_px}" rx="2" class="furn"/>')
        FA(f'<text x="{rec_brim_x+brim_d_px//2}" y="{by+brim_w_px//2+4}" class="furn-label">W{i}</text>')

    return svg, furn

def cli():
    parser = argparse.ArgumentParser(description="Generate basement floor plan SVG")
    parser.add_argument("--furniture", action="store_true",
                        help="Include furniture in the SVG")
    parser.add_argument("--both", action="store_true",
                        help="Generate both furnished and unfurnished SVGs")
    args = parser.parse_args()

    svg, furn = main()
    out_dir = Path(__file__).resolve().parent

    if args.both:
        # Unfurnished
        bare = svg + ['</svg>']
        p1 = out_dir / "basement_plan.svg"
        p1.write_text("\n".join(bare), encoding="utf-8")
        print(f"Saved to {p1}")
        # Furnished
        full = svg + furn + ['</svg>']
        p2 = out_dir / "basement_plan_furnished.svg"
        p2.write_text("\n".join(full), encoding="utf-8")
        print(f"Saved to {p2}")
    elif args.furniture:
        full = svg + furn + ['</svg>']
        p = out_dir / "basement_plan_furnished.svg"
        p.write_text("\n".join(full), encoding="utf-8")
        print(f"Saved to {p}")
    else:
        bare = svg + ['</svg>']
        p = out_dir / "basement_plan.svg"
        p.write_text("\n".join(bare), encoding="utf-8")
        print(f"Saved to {p}")


if __name__ == "__main__":
    cli()
