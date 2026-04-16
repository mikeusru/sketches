"""Walls, windows, doors, fixtures, labels, and dimensions for the basement floor plan."""

from .helpers import px, dim_h, dim_v, wlabel


class Geo:
    """All room geometry constants. Every measurement is in inches via px()."""

    # Layout offset (positions drawing within SVG canvas — not a physical measurement)
    LEFT, TOP = 50, 50

    # ── Outer shell ──
    OUTER_W = px(315.75)                # 26'3¾"
    OUTER_H = px(511)                   # 42'7"
    X_LEFT = LEFT
    X_RIGHT = LEFT + OUTER_W
    Y_TOP = TOP
    Y_BOTTOM = TOP + OUTER_H

    # ── Vertical partition (laundry | family room) ──
    X_CENTER = X_LEFT + px(147)         # 12'3" from left wall

    # ── Left-side bath / storage block ──
    STORAGE_W = px(56.25)               # 4'8¼"
    X_STORAGE_RIGHT = X_LEFT + STORAGE_W

    # ── Horizontal dividers ──
    Y_FOYER_TOP = Y_TOP + px(218.75)    # 18'2¾" from top (= bath top)
    Y_BATH_MID = Y_FOYER_TOP + px(65.25)   # 5'5¼" below foyer top
    Y_BATH2_BOTTOM = Y_BATH_MID + px(73)   # 6'1" below bath mid

    # ── Mechanical room ──
    Y_MECH_TOP = Y_FOYER_TOP + px(59.25)   # 4'11¼" below foyer top
    Y_MECH_BOTTOM = Y_MECH_TOP + px(77.25) # 6'5¼" tall
    X_MECH_LEFT = X_CENTER
    X_MECH_RIGHT = X_RIGHT

    # Mech door (on wall L)
    MECH_DOOR_Y1 = Y_MECH_BOTTOM - px(25.75)  # ~26" opening + 4¼" gap
    MECH_DOOR_Y2 = Y_MECH_BOTTOM - px(4.25)   # 4¼" from wall corner

    # ── Closet (left of mech room, between wall J and wall L) ──
    CLOSET_W = px(48)                   # 4'
    CLOSET_D = px(45)                   # 3'9"
    CLOSET_LEFT = X_MECH_LEFT - CLOSET_W
    CLOSET_BOTTOM = Y_MECH_TOP + CLOSET_D

    # Foyer → rec room door (adjacent to closet)
    FOYER_REC_DOOR_X1 = CLOSET_LEFT - px(25.75)  # ~26" door opening
    FOYER_REC_DOOR_X2 = CLOSET_LEFT

    # Storage closet door (on wall G)
    SC_DOOR_Y1 = Y_BATH2_BOTTOM + px(4.25)    # 4¼" from corner
    SC_DOOR_Y2 = SC_DOOR_Y1 + px(25.75)       # ~26" door opening

    # ── Windows ──
    STD_WIN = px(36)                    # 36" (3') standard basement window

    # Wall A (top) — laundry: 4' window, 3' from left corner
    WIN_A = (X_LEFT + px(36), X_LEFT + px(36) + px(48))

    # Wall B (right) — four standard windows
    WIN_B = [
        (Y_TOP + px(42), Y_TOP + px(42) + STD_WIN),                       # family room upper
        (Y_TOP + px(147.25), Y_TOP + px(147.25) + STD_WIN),               # family room lower
        (Y_MECH_BOTTOM - STD_WIN - px(2.5), Y_MECH_BOTTOM - px(2.5)),     # mech room
        (Y_TOP + px(409.25), Y_TOP + px(409.25) + STD_WIN),               # rec room
    ]

    # Wall C (bottom) — rec room
    _WIN_C_W = px(42)                   # 3'6" window
    _WIN_C_X2 = X_RIGHT - px(84)       # 7' from right wall
    WIN_C = (_WIN_C_X2 - _WIN_C_W, _WIN_C_X2)

    # ── Stairs ──
    STAIRS = (X_LEFT + px(195), Y_TOP + px(223.75), px(78), px(54))

    # ── Under-stairs closet (face wall at left edge of stairs) ──
    STCL_X = X_LEFT + px(195)           # aligned with stairs left edge
    STCL_FACE = px(44)                  # 44" closet face (with door)
    STCL_Y1 = Y_FOYER_TOP              # top (meets foyer top wall)
    STCL_Y2 = Y_MECH_TOP               # bottom (meets wall J)
    STCL_DOOR_H = px(30)               # 30" door
    STCL_DOOR_Y1 = Y_FOYER_TOP + px(4.25)  # 4¼" from wall
    STCL_DOOR_Y2 = STCL_DOOR_Y1 + STCL_DOOR_H

    # ── Fireplace (top of family room, wall A) ──
    FP_W = px(48)                       # 48" wide
    FP_D = px(10)                       # 10" deep projection
    FP_X = (X_CENTER + X_RIGHT) // 2 - FP_W // 2
    FP_Y = Y_TOP + px(3.5)             # 3½" from wall

    # ── BRIMNES wardrobe (reused by furniture) ──
    BRIM_W = px(46)                     # 46" body width
    BRIM_D = px(19.75)                  # 19¾" body depth


def draw_structure():
    """Return list of SVG lines for all structural elements."""
    G = Geo
    svg = []
    A = svg.append

    # ---- Outer shell ----
    A(f'<rect x="{G.LEFT}" y="{G.TOP}" width="{G.OUTER_W}" height="{G.OUTER_H}" class="wall"/>')

    # ---- Window notches ----
    # Wall A + Wall C (horizontal)
    for x1, x2, y in [(*G.WIN_A, G.Y_TOP), (*G.WIN_C, G.Y_BOTTOM)]:
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#f6f6f6" stroke-width="20"/>')
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#999" stroke-width="2"/>')
    # Wall B (vertical)
    for y1, y2 in G.WIN_B:
        A(f'<line x1="{G.X_RIGHT}" y1="{y1}" x2="{G.X_RIGHT}" y2="{y2}" stroke="#f6f6f6" stroke-width="20"/>')
        A(f'<line x1="{G.X_RIGHT}" y1="{y1}" x2="{G.X_RIGHT}" y2="{y2}" stroke="#999" stroke-width="2"/>')

    # ---- Interior walls ----
    # Center partition (laundry | family room, wall E)
    A(f'<line x1="{G.X_CENTER}" y1="{G.Y_TOP}" x2="{G.X_CENTER}" y2="{G.Y_FOYER_TOP}" class="wall"/>')
    # Guide lines (thin)
    A(f'<line x1="{G.X_CENTER-50}" y1="{G.Y_TOP}" x2="{G.X_CENTER-50}" y2="{G.Y_BOTTOM}" class="thin" opacity="0.55"/>')
    A(f'<line x1="{G.X_CENTER-2}" y1="{G.Y_TOP}" x2="{G.X_CENTER-2}" y2="{G.Y_BOTTOM}" class="thin" opacity="0.55"/>')

    # Bath/storage right wall (wall G)
    A(f'<line x1="{G.X_STORAGE_RIGHT}" y1="{G.Y_FOYER_TOP}" x2="{G.X_STORAGE_RIGHT}" y2="{G.Y_BOTTOM}" class="wall"/>')
    # Bath 1 / Bath 2 divider (wall H)
    A(f'<line x1="{G.X_LEFT}" y1="{G.Y_BATH_MID}" x2="{G.X_STORAGE_RIGHT}" y2="{G.Y_BATH_MID}" class="wall"/>')
    # Bath 2 / Storage closet divider (wall I)
    A(f'<line x1="{G.X_LEFT}" y1="{G.Y_BATH2_BOTTOM}" x2="{G.X_STORAGE_RIGHT}" y2="{G.Y_BATH2_BOTTOM}" class="wall"/>')

    # Foyer-to-rec wall (wall J, with door opening + closet)
    A(f'<line x1="{G.X_STORAGE_RIGHT}" y1="{G.Y_MECH_TOP}" x2="{G.FOYER_REC_DOOR_X1}" y2="{G.Y_MECH_TOP}" class="wall"/>')
    A(f'<line x1="{G.FOYER_REC_DOOR_X2}" y1="{G.Y_MECH_TOP}" x2="{G.X_MECH_LEFT}" y2="{G.Y_MECH_TOP}" class="wall"/>')

    # Foyer top wall (wall F) — extends to stair closet face
    A(f'<line x1="{G.X_LEFT}" y1="{G.Y_FOYER_TOP}" x2="274" y2="{G.Y_FOYER_TOP}" class="wall"/>')
    A(f'<line x1="344" y1="{G.Y_FOYER_TOP}" x2="{G.STCL_X}" y2="{G.Y_FOYER_TOP}" class="wall"/>')

    # Mechanical room walls (K, L, M)
    A(f'<line x1="{G.X_MECH_LEFT}" y1="{G.Y_MECH_TOP}" x2="{G.X_MECH_RIGHT}" y2="{G.Y_MECH_TOP}" class="wall"/>')
    A(f'<line x1="{G.X_MECH_LEFT}" y1="{G.Y_MECH_TOP}" x2="{G.X_MECH_LEFT}" y2="{G.MECH_DOOR_Y1}" class="wall"/>')
    A(f'<line x1="{G.X_MECH_LEFT}" y1="{G.MECH_DOOR_Y2}" x2="{G.X_MECH_LEFT}" y2="{G.Y_MECH_BOTTOM}" class="wall"/>')
    A(f'<line x1="{G.X_MECH_LEFT}" y1="{G.Y_MECH_BOTTOM}" x2="{G.X_MECH_RIGHT}" y2="{G.Y_MECH_BOTTOM}" class="wall"/>')

    # Closet walls (left of mech room)
    A(f'<line x1="{G.CLOSET_LEFT}" y1="{G.Y_MECH_TOP}" x2="{G.CLOSET_LEFT}" y2="{G.CLOSET_BOTTOM}" class="wall"/>')
    A(f'<line x1="{G.CLOSET_LEFT}" y1="{G.CLOSET_BOTTOM}" x2="{G.X_MECH_LEFT}" y2="{G.CLOSET_BOTTOM}" class="wall"/>')

    # ---- Fixtures ----
    # Air handler (top-left of mech room, 3' × 4')
    ah_w, ah_h = px(36), px(48)
    ah_x, ah_y = G.X_MECH_LEFT + 8, G.Y_MECH_TOP + 8
    A(f'<rect x="{ah_x}" y="{ah_y}" width="{ah_w}" height="{ah_h}" fill="#e0e0e0" stroke="#555" stroke-width="1.5" rx="2"/>')
    A(f'<text x="{ah_x + ah_w//2}" y="{ah_y + ah_h//2 - 6}" text-anchor="middle" class="small">Air</text>')
    A(f'<text x="{ah_x + ah_w//2}" y="{ah_y + ah_h//2 + 10}" text-anchor="middle" class="small">Handler</text>')

    # Fireplace (top of family room, centered on wall A)
    A(f'<rect x="{G.FP_X}" y="{G.FP_Y}" width="{G.FP_W}" height="{G.FP_D}"'
      f' fill="#d4c4b0" stroke="#555" stroke-width="2" rx="2"/>')
    fp_inner_w, fp_inner_h = px(36), px(6)
    fp_ix = G.FP_X + (G.FP_W - fp_inner_w) // 2
    fp_iy = G.FP_Y + G.FP_D - fp_inner_h - 2
    A(f'<rect x="{fp_ix}" y="{fp_iy}" width="{fp_inner_w}" height="{fp_inner_h}"'
      f' fill="#2a2a2a" stroke="#333" stroke-width="1" rx="2"/>')
    A(f'<text x="{G.FP_X + G.FP_W//2}" y="{G.FP_Y + G.FP_D + 14}"'
      f' text-anchor="middle" class="small">Fireplace</text>')

    # Stairs
    sx, sy, sw, sh = G.STAIRS
    A(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="none" class="thin"/>')
    for i in range(1, 7):
        A(f'<line x1="{sx + i * 26}" y1="{sy}" x2="{sx + i * 26}" y2="{sy+sh}" class="thin"/>')
    A(f'<line x1="{sx}" y1="{sy+sh//2}" x2="{sx+sw}" y2="{sy+sh//2}" class="thin"/>')

    # Under-stairs closet face wall (x=STCL_X, full height from wall F to wall J)
    # Wall above door
    A(f'<line x1="{G.STCL_X}" y1="{G.STCL_Y1}" x2="{G.STCL_X}" y2="{G.STCL_DOOR_Y1}" class="wall"/>')
    # Wall below door
    A(f'<line x1="{G.STCL_X}" y1="{G.STCL_DOOR_Y2}" x2="{G.STCL_X}" y2="{G.STCL_Y2}" class="wall"/>')
    # Door opening (opens left into foyer)
    stcl_door = G.STCL_DOOR_H
    A(f'<line x1="{G.STCL_X}" y1="{G.STCL_DOOR_Y1}" x2="{G.STCL_X}" y2="{G.STCL_DOOR_Y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {G.STCL_X} {G.STCL_DOOR_Y2} A {stcl_door} {stcl_door} 0 0 1 {G.STCL_X - stcl_door} {G.STCL_DOOR_Y1}" class="door"/>')

    # ---- Bath 1 fixtures ----
    # Toilet (bottom-left)
    A(f'<ellipse cx="{G.X_LEFT+30}" cy="{G.Y_BATH_MID-35}" rx="14" ry="20" class="thin"/>')
    A(f'<rect x="{G.X_LEFT+16}" y="{G.Y_BATH_MID-65}" width="28" height="14" rx="3" class="thin"/>')
    # Sink/vanity (bottom-right)
    A(f'<rect x="{G.X_STORAGE_RIGHT-42}" y="{G.Y_BATH_MID-42}" width="34" height="22" rx="2" class="thin"/>')
    A(f'<circle cx="{G.X_STORAGE_RIGHT-25}" cy="{G.Y_BATH_MID-31}" r="5" class="thin"/>')

    # ---- Bath 2 fixtures ----
    # Shower (bottom)
    sh_y = G.Y_BATH2_BOTTOM - 66
    A(f'<rect x="{G.X_LEFT+8}" y="{sh_y}" width="{G.STORAGE_W-16}" height="66" fill="none" class="thin"/>')
    A(f'<circle cx="{G.X_LEFT+G.STORAGE_W//2}" cy="{sh_y+33}" r="8" class="thin"/>')
    A(f'<line x1="{G.X_LEFT+8}" y1="{sh_y}" x2="{G.X_LEFT+G.STORAGE_W-8}" y2="{sh_y}" stroke="#666" stroke-width="1" stroke-dasharray="4 3"/>')
    # Toilet (top-left)
    A(f'<ellipse cx="{G.X_LEFT+30}" cy="{G.Y_BATH_MID+42}" rx="14" ry="20" class="thin"/>')
    A(f'<rect x="{G.X_LEFT+16}" y="{G.Y_BATH_MID+12}" width="28" height="14" rx="3" class="thin"/>')
    # Sink (top-right)
    A(f'<rect x="{G.X_STORAGE_RIGHT-42}" y="{G.Y_BATH_MID+10}" width="34" height="22" rx="2" class="thin"/>')
    A(f'<circle cx="{G.X_STORAGE_RIGHT-25}" cy="{G.Y_BATH_MID+21}" r="5" class="thin"/>')

    # ---- Doors ----
    # Storage closet door (wall G, swings into storage)
    A(f'<line x1="{G.X_STORAGE_RIGHT}" y1="{G.SC_DOOR_Y1}" x2="{G.X_STORAGE_RIGHT}" y2="{G.SC_DOOR_Y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {G.X_STORAGE_RIGHT} {G.SC_DOOR_Y1} A 60 60 0 0 1 {G.X_STORAGE_RIGHT-60} {G.SC_DOOR_Y2}" class="door"/>')

    # Bath 1 door (wall G, opens into foyer)
    A(f'<line x1="{G.X_STORAGE_RIGHT}" y1="610" x2="{G.X_STORAGE_RIGHT}" y2="670" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {G.X_STORAGE_RIGHT} 610 A 60 60 0 0 1 {G.X_STORAGE_RIGHT+60} 670" class="door"/>')

    # Foyer door from laundry (wall F)
    A(f'<line x1="284" y1="560" x2="344" y2="560" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 344 560 A 60 60 0 0 0 284 620" class="door"/>')

    # Foyer-to-rec-room door (wall J)
    A(f'<line x1="{G.FOYER_REC_DOOR_X1}" y1="{G.Y_MECH_TOP}" x2="{G.FOYER_REC_DOOR_X2}" y2="{G.Y_MECH_TOP}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {G.FOYER_REC_DOOR_X1} {G.Y_MECH_TOP} A 60 60 0 0 0 {G.FOYER_REC_DOOR_X2} {G.Y_MECH_TOP+60}" class="door"/>')

    # Sealed exterior door (wall C, dashed)
    A(f'<line x1="190" y1="{G.Y_BOTTOM}" x2="250" y2="{G.Y_BOTTOM}" stroke="#111" stroke-width="16" stroke-dasharray="8 6"/>')

    # Mech room door (wall L, opens left)
    A(f'<line x1="{G.X_MECH_LEFT}" y1="{G.MECH_DOOR_Y1}" x2="{G.X_MECH_LEFT}" y2="{G.MECH_DOOR_Y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {G.X_MECH_LEFT} {G.MECH_DOOR_Y1} A 50 50 0 0 0 {G.X_MECH_LEFT-50} {G.MECH_DOOR_Y2}" class="door"/>')

    # Closet door (bottom wall, opens into rec room)
    cl_door_w = px(30)
    cl_cx = (G.CLOSET_LEFT + G.X_MECH_LEFT) // 2
    cl_x1 = cl_cx - cl_door_w // 2
    cl_x2 = cl_x1 + cl_door_w
    A(f'<line x1="{cl_x1}" y1="{G.CLOSET_BOTTOM}" x2="{cl_x2}" y2="{G.CLOSET_BOTTOM}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {cl_x1} {G.CLOSET_BOTTOM} A {cl_door_w} {cl_door_w} 0 0 0 {cl_x2} {G.CLOSET_BOTTOM+cl_door_w}" class="door"/>')

    # Bath 2 door (wall G, below sink)
    b2_y1 = G.Y_BATH_MID + 70
    b2_y2 = b2_y1 + 60
    A(f'<line x1="{G.X_STORAGE_RIGHT}" y1="{b2_y1}" x2="{G.X_STORAGE_RIGHT}" y2="{b2_y2}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {G.X_STORAGE_RIGHT} {b2_y1} A 60 60 0 0 1 {G.X_STORAGE_RIGHT+60} {b2_y2}" class="door"/>')

    # Foyer double door (wall F, center)
    A(f'<line x1="255" y1="{G.Y_FOYER_TOP}" x2="335" y2="{G.Y_FOYER_TOP}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 255 {G.Y_FOYER_TOP} A 40 40 0 0 0 295 {G.Y_FOYER_TOP+40}" class="door"/>')
    A(f'<path d="M 335 {G.Y_FOYER_TOP} A 40 40 0 0 1 295 {G.Y_FOYER_TOP+40}" class="door"/>')

    # ---- Room labels ----
    A('<text x="147" y="330" class="room2">Laundry</text>')
    A('<text x="560" y="330" class="room2">Family Room</text>')
    A('<text x="234" y="640" class="room2">FOYER</text>')
    A(f'<text x="{G.X_STORAGE_RIGHT-62}" y="{G.Y_BOTTOM-16}" class="small">Storage</text>')
    A(f'<text x="{G.X_STORAGE_RIGHT-62}" y="{G.Y_BOTTOM-4}" class="small">Closet</text>')
    A(f'<text x="{G.X_LEFT+14}" y="{G.Y_FOYER_TOP + 95}" class="small">Bath 1</text>')
    A(f'<text x="{G.X_LEFT+14}" y="{(G.Y_BATH_MID+G.Y_BATH2_BOTTOM)//2+5}" class="small">Bath 2</text>')
    A('<text x="543" y="760" class="small">MECHANICAL ROOM</text>')
    cl_lx = (G.CLOSET_LEFT + G.X_MECH_LEFT) // 2
    cl_ly = (G.Y_MECH_TOP + G.CLOSET_BOTTOM) // 2 + 5
    A(f'<text x="{cl_lx}" y="{cl_ly}" text-anchor="middle" class="small">Closet</text>')
    # Under-stairs closet label
    stcl_lx = G.STCL_X + (G.STAIRS[2] // 2)
    stcl_ly = (G.STCL_Y1 + G.STCL_Y2) // 2 + 5
    A(f'<text x="{stcl_lx}" y="{stcl_ly - 6}" text-anchor="middle" class="small">Stair</text>')
    A(f'<text x="{stcl_lx}" y="{stcl_ly + 7}" text-anchor="middle" class="small">Closet</text>')
    A(f'<text x="{(G.X_STORAGE_RIGHT + G.X_RIGHT)//2 + 30}" y="{G.Y_BOTTOM - 30}" class="room">Rec Room</text>')

    # ---- Wall labels ----
    svg += wlabel((G.X_LEFT + G.X_RIGHT) // 2, G.Y_TOP - 3, 'A')
    svg += wlabel(G.X_RIGHT + 3, (G.Y_TOP + G.Y_BOTTOM) // 2, 'B')
    svg += wlabel((G.X_LEFT + G.X_RIGHT) // 2, G.Y_BOTTOM + 3, 'C')
    svg += wlabel(G.X_LEFT - 3, (G.Y_TOP + G.Y_BOTTOM) // 2, 'D')
    svg += wlabel(G.X_CENTER + 14, (G.Y_TOP + G.Y_FOYER_TOP) // 2, 'E')
    svg += wlabel((G.X_LEFT + 274) // 2, G.Y_FOYER_TOP - 14, 'F')
    svg += wlabel(G.X_STORAGE_RIGHT + 14, (G.Y_FOYER_TOP + G.Y_BOTTOM) // 2, 'G')
    svg += wlabel((G.X_LEFT + G.X_STORAGE_RIGHT) // 2, G.Y_BATH_MID - 14, 'H')
    svg += wlabel((G.X_LEFT + G.X_STORAGE_RIGHT) // 2, G.Y_BATH2_BOTTOM + 14, 'I')
    svg += wlabel((G.X_STORAGE_RIGHT + G.CLOSET_LEFT) // 2, G.Y_MECH_TOP + 14, 'J')
    svg += wlabel((G.X_MECH_LEFT + G.X_MECH_RIGHT) // 2, G.Y_MECH_TOP - 14, 'K')
    svg += wlabel(G.X_MECH_LEFT + 14, (G.Y_MECH_BOTTOM + G.CLOSET_BOTTOM) // 2, 'L')
    svg += wlabel((G.X_MECH_LEFT + G.X_MECH_RIGHT) // 2, G.Y_MECH_BOTTOM + 14, 'M')

    # ---- Dimension lines ----
    _draw_dimensions(svg)

    return svg


def _draw_dimensions(svg):
    """Append all dimension lines to svg list."""
    G = Geo

    # == Wall A (top) ==
    row1 = G.Y_TOP - 25
    row2 = G.Y_TOP - 50
    svg += dim_h(G.X_LEFT, G.X_CENTER, row1, wall_y=G.Y_TOP)
    svg += dim_h(G.X_CENTER, G.X_RIGHT, row1, wall_y=G.Y_TOP)
    svg += dim_h(G.X_LEFT, G.WIN_A[0], row2, wall_y=G.Y_TOP)
    svg += dim_h(*G.WIN_A, row2, wall_y=G.Y_TOP)
    svg += dim_h(G.WIN_A[1], G.X_CENTER, row2, wall_y=G.Y_TOP)

    # == Wall C (bottom) ==
    row3 = G.Y_BOTTOM + 30
    row4 = G.Y_BOTTOM + 55
    row5 = G.Y_BOTTOM + 80
    svg += dim_h(G.X_LEFT, G.X_RIGHT, row3, wall_y=G.Y_BOTTOM)
    svg += dim_h(G.X_LEFT, G.X_STORAGE_RIGHT, row4, wall_y=G.Y_BOTTOM)
    svg += dim_h(*G.WIN_C, row5, wall_y=G.Y_BOTTOM)
    svg += dim_h(G.WIN_C[1], G.X_RIGHT, row5, wall_y=G.Y_BOTTOM)

    # == Wall B (right) — window detail ==
    col1 = G.X_RIGHT + 30
    col2 = G.X_RIGHT + 55
    # Family room windows
    svg += dim_v(G.Y_TOP, G.WIN_B[0][0], col1, wall_x=G.X_RIGHT)
    svg += dim_v(*G.WIN_B[0], col1, wall_x=G.X_RIGHT)
    svg += dim_v(G.WIN_B[0][1], G.WIN_B[1][0], col1, wall_x=G.X_RIGHT)
    svg += dim_v(*G.WIN_B[1], col1, wall_x=G.X_RIGHT)
    # Mech room window
    svg += dim_v(*G.WIN_B[2], col1, wall_x=G.X_RIGHT)
    # Rec room window
    svg += dim_v(*G.WIN_B[3], col1, wall_x=G.X_RIGHT)
    svg += dim_v(G.WIN_B[3][1], G.Y_BOTTOM, col1, wall_x=G.X_RIGHT)
    # Major vertical sections
    svg += dim_v(G.Y_TOP, G.Y_MECH_TOP, col2, wall_x=G.X_RIGHT)
    svg += dim_v(G.Y_MECH_TOP, G.Y_MECH_BOTTOM, col2, wall_x=G.X_RIGHT)
    svg += dim_v(G.Y_MECH_BOTTOM, G.Y_BOTTOM, col2, wall_x=G.X_RIGHT)

    # == Wall D (left) ==
    col3 = G.X_LEFT - 30
    col4 = G.X_LEFT - 55
    svg += dim_v(G.Y_TOP, G.Y_BOTTOM, col3, wall_x=G.X_LEFT)
    svg += dim_v(G.Y_TOP, G.Y_FOYER_TOP, col4, wall_x=G.X_LEFT)
    svg += dim_v(G.Y_FOYER_TOP, G.Y_BATH_MID, col4, wall_x=G.X_LEFT)
    svg += dim_v(G.Y_BATH_MID, G.Y_BATH2_BOTTOM, col4, wall_x=G.X_LEFT)
    svg += dim_v(G.Y_BATH2_BOTTOM, G.Y_BOTTOM, col4, wall_x=G.X_LEFT)

    # == Interior ==
    svg += dim_h(G.X_MECH_LEFT, G.X_MECH_RIGHT, G.Y_MECH_TOP - 20, wall_y=G.Y_MECH_TOP)

    # == Closet (left of mech room) ==
    # Width (horizontal, above closet)
    svg += dim_h(G.CLOSET_LEFT, G.X_MECH_LEFT, G.Y_MECH_TOP - 20, wall_y=G.Y_MECH_TOP)
    # Depth (vertical, left of closet)
    svg += dim_v(G.Y_MECH_TOP, G.CLOSET_BOTTOM, G.CLOSET_LEFT - 20, wall_x=G.CLOSET_LEFT)

    # == Under-stairs closet ==
    svg += dim_v(G.STCL_Y1, G.STCL_Y2, G.STCL_X - 20, wall_x=G.STCL_X)
