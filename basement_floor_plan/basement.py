"""Basement floor plan — declarative definition.

All geometry is in inches relative to the NW interior corner (0, 0).
The renderer converts to pixels via SCALE.

## Locked vs loose measurements

Every position has a `locked` flag (default True):
- `locked=True`  — intentional, verified. Treat as authoritative.
- `locked=False` — placeholder / estimate. This value should absorb changes
  when neighboring locked values shift, and renders dashed orange so it's
  visually obvious.

Rule of thumb when editing: if an edit propagates and only one of the
affected values is unlocked, change *that one* — not the locked ones.

## Outer wall directions

Walls A/B/C/D run clockwise around the exterior so that "offset from start"
moves in a consistent direction relative to the room interior:
- A: NW → NE (offset moves east along the north wall)
- B: NE → SE (offset moves south along the east wall)
- C: SW → SE (offset moves east along the south wall)
- D: NW → SW (offset moves south along the west wall)
"""

from .helpers import px
from .model import FloorPlan


# ===========================================================================
# Compat shim for the legacy furniture.py (which still uses pixel-space Geo).
# When furniture.py is migrated to the declarative model this can be removed.
# ===========================================================================
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
    # East-wall windows, in pixel y-ranges (top, bottom)
    WIN_B = [
        (px(42),                        px(42 + 36)),
        (px(147.25),                    px(147.25 + 36)),
        (Y_MECH_BOTTOM - px(38.5),      Y_MECH_BOTTOM - px(2.5)),
        (px(409.25),                    px(409.25 + 36)),
    ]


# ===========================================================================
# Named dimensions (inches). Change these here — everything follows.
# ===========================================================================
W_HOUSE = 315.75     # 26' 3¾" — exterior width  (LOCKED)
H_HOUSE = 511        # 42' 7"  — exterior depth  (LOCKED)

X_E = 147            # center partition (laundry ↔ family room)  LOCKED
X_G = 56.25          # bath/storage column right edge             LOCKED
X_CL = 99            # interior closet west wall                  LOCKED

Y_F = 218.75         # wall F: foyer top / laundry bottom         LOCKED
Y_K = 278            # wall K: mech top / foyer bottom            LOCKED
Y_M = 355.25         # wall M: mech bottom                        LOCKED
Y_H = 284            # wall H: bath 1 / bath 2 divider            LOCKED
Y_I = 357            # wall I: bath 2 / storage closet divider    LOCKED
Y_CL = 323           # interior closet south wall (45" deep)      LOCKED

# Stair block (treads visible in family room)
STAIR = dict(x=195, y=223.75, w=78, h=54, steps=7)


# ===========================================================================
def build_plan() -> FloorPlan:
    p = FloorPlan("Basement")

    # -------- Outer corners --------
    p.pt("NW", 0,       0)
    p.pt("NE", W_HOUSE, 0)
    p.pt("SE", W_HOUSE, H_HOUSE)
    p.pt("SW", 0,       H_HOUSE)

    # -------- Interior junction points --------
    # Center partition (wall E)
    p.pt("E_top", X_E, 0)
    p.pt("E_bot", X_E, Y_F)

    # Wall F (foyer top) — runs full house width
    p.pt("F_W",   0,       Y_F)       # west end (at wall D)
    p.pt("F_E",   W_HOUSE, Y_F)       # east end (meets wall B)

    # Wall G (bath/storage right)
    p.pt("G_top", X_G, Y_F)
    p.pt("G_bot", X_G, H_HOUSE)

    # Bath dividers
    p.pt("H_W", 0,   Y_H)
    p.pt("H_E", X_G, Y_H)
    p.pt("I_W", 0,   Y_I)
    p.pt("I_E", X_G, Y_I)

    # Wall J (foyer ↔ rec-room) — one continuous line; closet sits on it
    p.pt("J_W", X_G, Y_K)             # west end (meets wall G)
    p.pt("J_E", X_E, Y_K)             # east end (meets wall L top)

    # Wall K (mech top)
    p.pt("K_E", W_HOUSE, Y_K)

    # Wall L (mech west) — runs from J_E down to M_W
    p.pt("M_W", X_E,     Y_M)
    p.pt("M_E", W_HOUSE, Y_M)

    # Interior closet (protrudes into rec room from wall J)
    p.pt("CL_NW", X_CL, Y_K)
    p.pt("CL_SW", X_CL, Y_CL)
    p.pt("CL_SE", X_E,  Y_CL)

    # -------- Walls --------
    # Outer shell (all locked — measured exterior)
    p.wall("A", "NW", "NE")           # north
    p.wall("B", "NE", "SE")           # east
    p.wall("C", "SW", "SE")           # south (W→E for consistent offset direction)
    p.wall("D", "NW", "SW")           # west

    # Interior — north half
    p.wall("E", "E_top", "E_bot")     # center partition
    # Wall F runs the full width of the house from wall D to wall B.
    # Crosses walls G, E, and the stair closet face as T-junctions; the
    # renderer auto-splits its label at each.
    p.wall("F", "F_W", "F_E")

    # Interior — bath/storage column
    p.wall("G", "G_top", "G_bot")     # bath/storage right edge
    p.wall("H", "H_W",   "H_E")       # bath 1 / bath 2
    p.wall("I", "I_W",   "I_E")       # bath 2 / storage closet

    # Interior — foyer-to-rec and mech walls
    p.wall("J", "J_W",   "J_E")       # foyer ↔ rec (closet sits on top)
    p.wall("K", "J_E",   "K_E")       # mech top
    p.wall("L", "J_E",   "M_W")       # mech west (also closet east)
    p.wall("M", "M_W",   "M_E")       # mech bottom

    # Interior closet (48" × 45" protrusion on wall J)
    p.wall("CL_W", "CL_NW", "CL_SW")
    p.wall("CL_S", "CL_SW", "CL_SE")

    # -------- Windows (all 36" standard basement except where noted) --------
    # Wall A — 48" laundry window, 36" from west corner
    p.window("A", offset=36,  width=48)
    # Wall B — four 36" windows (offsets measured from NE going south)
    p.window("B", offset=42,     width=36)    # family room upper
    p.window("B", offset=147.25, width=36)    # family room lower
    p.window("B", offset=316.75, width=36)    # mech room  (ends 2.5" above wall M)
    p.window("B", offset=409.25, width=36)    # rec room
    # Wall C — 42" rec-room window, 7' (84") from east corner
    #   In W→E direction, offset from SW = W_HOUSE - 84 - 42 = 189.75
    p.window("C", offset=189.75, width=42)

    # -------- Doors --------
    # Wall F — 30" laundry/foyer door. Placed so the eastern segment (F.3)
    # is 36" long, anchored to wall E: door spans [81, 111] → F.3 = [111, 147].
    p.door("F", offset=81, width=30, hinge="end", swing="S", locked=False)
    # Open doorway between foyer and family room (no door).
    # Width chosen so the east span of wall F is 102" (confirmed measurement).
    p.opening("F", offset=147, width=W_HOUSE - 147 - 102)

    # Wall G — three doors: bath 1, bath 2, storage closet (all opening east into foyer/rec)
    # Offsets from G_top (inches downward). Marked loose — I have no confirmed placements.
    p.door("G", offset=22,  width=26, hinge="start", swing="E", locked=False)  # Bath 1
    p.door("G", offset=95,  width=26, hinge="start", swing="E", locked=False)  # Bath 2
    p.door("G", offset=143, width=26, hinge="end",   swing="W", locked=False)  # Storage

    # Wall J — foyer-to-rec door, west of the interior closet
    # Offset from J_W. Loose — placement not verified.
    p.door("J", offset=17, width=30, hinge="end", swing="S", locked=False)

    # Wall L — mech door near its south end (hinged against wall M, swings into rec)
    p.door("L", offset=51, width=26, hinge="end", swing="W", locked=False)

    # Closet south wall — 30" door centered-ish on the 48" wall
    p.door("CL_S", offset=9, width=30, hinge="start", swing="S", locked=False)

    # -------- Stairs --------
    p.add_stairs(**STAIR)

    # -------- Rooms --------
    p.room("Laundry",
           bounds=["NW", "E_top", "E_bot", "F_W"])
    p.room("Family Room",
           bounds=["E_top", "NE", "K_E", "E_bot"],
           label_style="room2", label_pos=(225, 110))
    p.room("FOYER",
           bounds=["F_W", "F_E", "K_E", "J_W", "G_top"],
           label_style="room2", label_pos=(125, 250))
    p.room("Bath 1", bounds=["F_W", "G_top", "H_E", "H_W"],
           label_style="small", label_pos=(28, Y_F + 30))
    p.room("Bath 2", bounds=["H_W", "H_E", "I_E", "I_W"],
           label_style="small", label_pos=(28, (Y_H + Y_I) / 2))
    p.room("Storage Closet", bounds=["I_W", "I_E", "G_bot", "SW"],
           label="Storage\nCloset", label_style="small",
           label_pos=(28, (Y_I + H_HOUSE) / 2))
    p.room("Rec Room",
           bounds=["J_W", "CL_NW", "CL_SW", "CL_SE", "M_W", "M_E",
                   "SE", "SW", "G_bot"],
           label_style="room", label_pos=(200, 460))
    p.room("Mechanical Room",
           bounds=["J_E", "K_E", "M_E", "M_W"],
           label="MECHANICAL ROOM", label_style="small",
           label_pos=((X_E + W_HOUSE) / 2, (Y_K + Y_M) / 2))
    p.room("Closet",
           bounds=["CL_NW", "J_E", "CL_SE", "CL_SW"],
           label="Closet", label_style="small",
           label_pos=((X_CL + X_E) / 2, (Y_K + Y_CL) / 2))

    # -------- Fixtures --------
    # Air handler (mech room NW, 36" × 48")
    p.fixture("rect", x=X_E + 3, y=Y_K + 3, w=36, h=48, label="Air\nHandler")
    # Fireplace (wall A, centered in family room)
    fp_w = 48
    p.fixture("fireplace",
              x=(X_E + W_HOUSE) / 2 - fp_w / 2, y=3.5,
              w=fp_w, h=10, label="Fireplace")
    # Bath 1: toilet top-left, sink top-right
    p.fixture("toilet", x=6,          y=Y_F + 10, w=12, h=17)
    p.fixture("sink",   x=X_G - 18,   y=Y_F + 12, w=14, h=9)
    # Bath 2: toilet + sink top, shower at bottom
    p.fixture("toilet", x=6,          y=Y_H + 8,  w=12, h=17)
    p.fixture("sink",   x=X_G - 18,   y=Y_H + 10, w=14, h=9)
    p.fixture("shower", x=3,          y=Y_I - 28, w=X_G - 6, h=28)

    # -------- Dimensions --------
    # Outer shell
    p.dim("NW", "E_top", offset=-10, axis="h")
    p.dim("E_top", "NE", offset=-10, axis="h")
    p.dim("SW", "SE",    offset=10,  axis="h")
    # Wall D (left) — vertical stack
    p.dim("NW",  "F_W", offset=-12, axis="v")
    p.dim("F_W", "H_W", offset=-12, axis="v")
    p.dim("H_W", "I_W", offset=-12, axis="v")
    p.dim("I_W", "SW",  offset=-12, axis="v")
    # Wall B (right) — major sections
    p.dim("NE",  "K_E", offset=24,  axis="v")
    p.dim("K_E", "M_E", offset=24,  axis="v")
    p.dim("M_E", "SE",  offset=24,  axis="v")
    # Interior closet
    p.dim("CL_NW", "CL_SE", offset=-10, axis="h")   # 48" width
    p.dim("CL_NW", "CL_SW", offset=-10, axis="v")   # 45" depth

    return p
