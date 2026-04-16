"""Basement floor plan — declarative definition.

Everything is in inches, relative to the NW interior corner (0, 0).
The renderer converts to pixels via SCALE.

Conventions:
- Outer walls A/B/C/D run clockwise: A (north, NW→NE), B (east, NE→SE),
  C (south, SE→SW), D (west, SW→NW).
- Interior walls use the same alphabetical labels as the earlier sketches.
"""

from .helpers import px
from .model import FloorPlan


# ---------------------------------------------------------------------------
# Compat layer for furniture.py — interior-relative pixel coordinates
# (0-based; the renderer wraps everything in <g transform> so canvas pixels
# = MARGIN + these values).
# ---------------------------------------------------------------------------
class Geo:
    X_LEFT = 0
    X_RIGHT = px(315.75)
    Y_TOP = 0
    Y_BOTTOM = px(511)
    X_CENTER = px(147)
    X_STORAGE_RIGHT = px(56.25)
    X_MECH_LEFT = X_CENTER
    Y_FOYER_TOP = px(218.75)
    Y_BATH_MID = px(284)
    Y_BATH2_BOTTOM = px(357)
    Y_MECH_TOP = px(278)
    Y_MECH_BOTTOM = px(355.25)
    BRIM_W = px(46)
    BRIM_D = px(19.75)
    SC_DOOR_Y2 = Y_BATH2_BOTTOM + px(30)
    WIN_B = [
        (px(42),              px(42 + 36)),
        (px(147.25),          px(147.25 + 36)),
        (Y_MECH_BOTTOM - px(38.5), Y_MECH_BOTTOM - px(2.5)),
        (px(409.25),          px(409.25 + 36)),
    ]


def build_plan() -> FloorPlan:
    p = FloorPlan("Basement")

    # ===== Outer shell (26' 3¾" × 42' 7") =====
    p.pt("NW", 0, 0)
    p.pt("NE", 315.75, 0)
    p.pt("SE", 315.75, 511)
    p.pt("SW", 0, 511)

    # ===== Horizontal divider y-coords =====
    Y_F = 218.75        # wall F (foyer top)   — 18' 2¾"
    Y_H = Y_F + 65.25   # wall H (bath1/2)     — 284
    Y_I = Y_H + 73      # wall I (bath2/stor)  — 357
    Y_K = Y_F + 59.25   # wall K (mech top)    — 278
    Y_M = Y_K + 77.25   # wall M (mech bot)    — 355.25
    X_E = 147           # wall E (center partition)
    X_G = 56.25         # wall G (bath/storage right)

    # ===== Interior junction points =====
    p.pt("E_top",    X_E, 0)          # center partition top
    p.pt("E_bot",    X_E, Y_F)        # center partition bottom (meets F)
    p.pt("F_W",      0,   Y_F)        # wall F west end
    p.pt("F_STCL",   195, Y_F)        # wall F east end (at stair closet)
    p.pt("G_top",    X_G, Y_F)
    p.pt("G_bot",    X_G, 511)
    p.pt("H_W",      0,   Y_H)
    p.pt("H_E",      X_G, Y_H)
    p.pt("I_W",      0,   Y_I)
    p.pt("I_E",      X_G, Y_I)
    p.pt("K_W",      X_E, Y_K)
    p.pt("K_E",      315.75, Y_K)
    p.pt("M_W",      X_E, Y_M)
    p.pt("M_E",      315.75, Y_M)
    p.pt("J_W",      X_G, Y_K)        # wall J west (at storage right)

    # ===== Closet (south of wall J, west of wall L, 48" × 45") =====
    CLOSET_W_IN = 48
    CLOSET_D_IN = 45
    p.pt("CL_NW", X_E - CLOSET_W_IN, Y_K)              # (99, 278)
    p.pt("CL_SW", X_E - CLOSET_W_IN, Y_K + CLOSET_D_IN) # (99, 323)
    p.pt("CL_SE", X_E,               Y_K + CLOSET_D_IN) # (147, 323)

    # ===== Stair closet (face wall at x=195, from F down to J) =====
    p.pt("STCL_top", 195, Y_F)
    p.pt("STCL_bot", 195, Y_K)

    # ===== Outer walls =====
    p.wall("A", "NW", "NE")   # north
    p.wall("B", "NE", "SE")   # east
    p.wall("C", "SE", "SW")   # south (drawn E→W so offsets measure from SE)
    p.wall("D", "SW", "NW")   # west

    # ===== Interior walls =====
    p.wall("E",  "E_top", "E_bot")              # center partition (laundry | family)
    p.wall("F",  "F_W",   "F_STCL")             # foyer top (ends at stair closet)
    p.wall("G",  "G_top", "G_bot")              # bath/storage right
    p.wall("H",  "H_W",   "H_E")                # bath1/bath2 divider
    p.wall("I",  "I_W",   "I_E")                # bath2/storage divider
    p.wall("J",  "J_W",   "CL_NW")              # foyer-rec (west portion)
    # (The east portion of J under the closet is shared with closet top; skip duplicate.)
    p.wall("K",  "K_W",   "K_E")                # mech top
    p.wall("L",  "K_W",   "M_W")                # mech left (= partition below foyer)
    p.wall("M",  "M_W",   "M_E")                # mech bottom
    # Closet walls
    p.wall("CL_left",   "CL_NW", "CL_SW")
    p.wall("CL_bottom", "CL_SW", "CL_SE")
    # Stair closet face wall
    p.wall("STCL", "STCL_top", "STCL_bot")

    # ===== Features on walls =====
    # Wall A (north) — laundry window, 4' wide, 3' from west corner
    p.window("A", offset=36, width=48)

    # Wall B (east) — four standard 36" windows
    STD_WIN = 36
    p.window("B", offset=42,     width=STD_WIN)   # family room upper
    p.window("B", offset=147.25, width=STD_WIN)   # family room lower
    # mech room window — ends 2.5" from wall M (wall M is at y=355.25, so from NE it's 355.25 - 2.5 = 352.75)
    p.window("B", offset=Y_M - STD_WIN - 2.5, width=STD_WIN)
    p.window("B", offset=409.25, width=STD_WIN)   # rec room

    # Wall C (south, SE→SW, offsets measured leftward from SE)
    p.window("C", offset=84, width=42)   # rec room window, 7' from SE corner

    # Wall F (foyer top) — two doors + foyer double door
    # Offsets measured from F_W (0, 218.75) rightward
    # Foyer double door (main entry from laundry, 34.38" with two leaves)
    p.door("F", offset=88.05,  width=34.38, hinge="start", swing="S", leaves=2)
    # Laundry-to-foyer side door
    p.door("F", offset=100.52, width=25.77, hinge="end",   swing="S")

    # Wall G (bath/storage right) — three doors
    # Offsets measured from G_top (56.25, 218.75) downward
    p.door("G", offset=21.80,  width=25.77, hinge="start", swing="E")  # Bath 1
    p.door("G", offset=95.15,  width=25.77, hinge="start", swing="E")  # Bath 2
    p.door("G", offset=142.50, width=25.77, hinge="end",   swing="W")  # Storage closet

    # Wall J — foyer-to-rec door (25.77" wide)
    # J runs from J_W (56.25, 278) east to CL_NW (99, 278). Length = 42.75".
    # Door sits at east end, hinge against closet.
    p.door("J", offset=17, width=25.77, hinge="end", swing="S")

    # Wall L (mech left) — mech door at bottom
    # L runs from K_W (147, 278) down to M_W (147, 355.25). Length = 77.25".
    p.door("L", offset=51.5, width=21.5, hinge="end", swing="W")

    # Closet bottom wall — 30" door centered
    # CL_bottom runs from CL_SW (99, 323) east to CL_SE (147, 323). Length = 48".
    p.door("CL_bottom", offset=9, width=30, hinge="start", swing="S")

    # Stair closet face — 30" door near top
    # STCL runs from STCL_top (195, 218.75) down to STCL_bot (195, 278). Length = 59.25".
    p.door("STCL", offset=4.25, width=30, hinge="start", swing="W")

    # ===== Stairs =====
    p.add_stairs(x=195, y=223.75, w=78, h=54, steps=7, direction="up")

    # ===== Rooms =====
    p.room("Laundry",     bounds=["NW", "E_top", "E_bot", "F_W"])
    p.room("Family Room", bounds=["E_top", "NE", "K_E", "K_W", "E_bot"],
           label_style="room2")
    p.room("FOYER",       bounds=["F_W", "F_STCL", "STCL_bot", "J_W", "G_top"],
           label_style="room2", label_pos=(80, 250))
    p.room("Bath 1",      bounds=["F_W", "G_top", "H_E", "H_W"],
           label_style="small", label_pos=(8, Y_F + 45))
    p.room("Bath 2",      bounds=["H_W", "H_E", "I_E", "I_W"],
           label_style="small", label_pos=(8, (Y_H + Y_I) / 2))
    p.room("Rec Room",    bounds=["J_W", "CL_NW", "CL_SW", "CL_SE", "M_W", "M_E", "SE", "SW", "G_bot"],
           label_style="room", label_pos=(220, 480))
    p.label("Storage",    X_G - 30, 505, style="small", anchor="middle")
    p.label("Closet",     X_G - 30, 510, style="small", anchor="middle")
    p.label("MECHANICAL ROOM", (X_E + 315.75) / 2, Y_K + 30, style="small")
    # Closet (under wall J)
    p.label("Closet", (X_E - CLOSET_W_IN / 2), Y_K + CLOSET_D_IN / 2 + 2, style="small")
    # Stair closet
    p.label("Stair", 195 + 78 / 2, (Y_F + Y_K) / 2 - 4, style="small")
    p.label("Closet", 195 + 78 / 2, (Y_F + Y_K) / 2 + 8, style="small")

    # ===== Wall letter labels (manually positioned) =====
    p.label("A", (0 + 315.75) / 2, -3,            wall_label=True)
    p.label("B", 315.75 + 3,       (0 + 511) / 2, wall_label=True)
    p.label("C", (0 + 315.75) / 2, 511 + 3,       wall_label=True)
    p.label("D", -3,               (0 + 511) / 2, wall_label=True)
    p.label("E", X_E + 7,          Y_F / 2,       wall_label=True)
    p.label("F", (0 + 100) / 2,    Y_F - 6,       wall_label=True)
    p.label("G", X_G + 7,          (Y_F + 511) / 2, wall_label=True)
    p.label("H", X_G / 2,          Y_H - 6,       wall_label=True)
    p.label("I", X_G / 2,          Y_I + 6,       wall_label=True)
    p.label("J", (X_G + X_E - CLOSET_W_IN) / 2, Y_K + 6, wall_label=True)
    p.label("K", (X_E + 315.75) / 2, Y_K - 6,     wall_label=True)
    p.label("L", X_E + 7,          (Y_M + Y_K + CLOSET_D_IN) / 2, wall_label=True)
    p.label("M", (X_E + 315.75) / 2, Y_M + 6,     wall_label=True)

    # ===== Fixtures =====
    # Air handler (mech room, 36" × 48", top-left corner)
    p.fixture("rect", x=X_E + 3, y=Y_K + 3, w=36, h=48, label="Air\nHandler")

    # Fireplace (top of family room, wall A, 48" × 10")
    FP_W_IN, FP_D_IN = 48, 10
    FP_X = (X_E + 315.75) / 2 - FP_W_IN / 2
    p.fixture("fireplace", x=FP_X, y=3.5, w=FP_W_IN, h=FP_D_IN, label="Fireplace")

    # Bath 1 fixtures (row layout: toilet left, sink right)
    p.fixture("toilet", x=6,           y=Y_F + 21, w=12, h=17)
    p.fixture("sink",   x=X_G - 18,    y=Y_F + 25, w=14, h=9)

    # Bath 2 fixtures: toilet top-left, sink top-right, shower bottom
    p.fixture("toilet", x=6,           y=Y_H + 9,  w=12, h=17)
    p.fixture("sink",   x=X_G - 18,    y=Y_H + 9,  w=14, h=9)
    p.fixture("shower", x=3,           y=Y_I - 28, w=X_G - 6, h=28)

    # ===== Dimensions (outer shell, key interior) =====
    # Wall A — overall and window breakdown
    p.dim("NW",    "E_top", offset=-10, axis="h")
    p.dim("E_top", "NE",    offset=-10, axis="h")

    # Wall D — major vertical sections
    p.dim("NW", "F_W",  offset=-12, axis="v")
    p.dim("F_W", "H_W", offset=-12, axis="v")
    p.dim("H_W", "I_W", offset=-12, axis="v")
    p.dim("I_W", "SW",  offset=-12, axis="v")

    # Wall B — major vertical sections
    p.dim("NE",  "K_E", offset=24, axis="v")
    p.dim("K_E", "M_E", offset=24, axis="v")
    p.dim("M_E", "SE",  offset=24, axis="v")

    # Wall C — overall
    p.dim("SW", "SE", offset=13, axis="h")

    # Closet
    p.dim("CL_NW", "CL_SE", offset=-10, axis="h")  # width
    p.dim("CL_NW", "CL_SW", offset=-10, axis="v")  # depth

    # Stair closet
    p.dim("STCL_top", "STCL_bot", offset=-10, axis="v")

    return p
