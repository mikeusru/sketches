"""Furniture placement for the basement floor plan."""

from .helpers import px
from .basement import Geo


def draw_furniture():
    """Return list of SVG lines for all furniture items."""
    G = Geo
    furn = []
    _rec_room(furn, G)
    _laundry(furn, G)
    _family_room(furn, G)
    _storage_closet(furn, G)
    return furn


# ---- Rec room ----

def _rec_room(furn, G):
    """King bed, TV, dresser, and wardrobes."""
    A = furn.append

    # King size bed (76" × 80") against wall M, 24" walkway to wall B
    bed_w, bed_h = px(76), px(80)
    bed_x = G.X_RIGHT - bed_w - px(24)
    bed_y = G.Y_MECH_BOTTOM + 10
    A(f'<rect x="{bed_x}" y="{bed_y}" width="{bed_w}" height="{bed_h}" rx="4" class="furn"/>')
    pw, ph = 78, 24
    A(f'<rect x="{bed_x+6}" y="{bed_y+6}" width="{pw}" height="{ph}" rx="6" class="furn"/>')
    A(f'<rect x="{bed_x+bed_w-pw-6}" y="{bed_y+6}" width="{pw}" height="{ph}" rx="6" class="furn"/>')
    A(f'<text x="{bed_x+bed_w//2}" y="{bed_y+bed_h//2+5}" class="furn-label">King Bed</text>')

    # 65″ TV on wall C, centered under bed
    tv_w = px(56.7)   # 65" diagonal ≈ 56.7" wide
    tv_h = 8
    tv_x = bed_x + bed_w // 2 - tv_w // 2
    tv_y = G.Y_BOTTOM - tv_h - 4
    A(f'<rect x="{tv_x}" y="{tv_y}" width="{tv_w}" height="{tv_h}" rx="1" fill="#333" stroke="#222" stroke-width="1"/>')
    A(f'<text x="{tv_x+tv_w//2}" y="{tv_y-8}" class="furn-label">65\u2033 TV</text>')

    # Dresser on wall C, past wardrobe depth zone
    dr_w, dr_h = px(60), px(18)   # 5' × 1.5'
    dr_x = G.X_STORAGE_RIGHT + G.BRIM_D + 20
    dr_y = G.Y_BOTTOM - dr_h - 10
    A(f'<rect x="{dr_x}" y="{dr_y}" width="{dr_w}" height="{dr_h}" rx="3" class="furn"/>')
    A(f'<text x="{dr_x+dr_w//2}" y="{dr_y+dr_h//2+4}" class="furn-label">Dresser</text>')

    # 2× BRIMNES wardrobes against wall G (below storage closet door)
    bx = G.X_STORAGE_RIGHT + 8
    by_start = G.SC_DOOR_Y2 + 10
    for i in range(2):
        by = by_start + i * (G.BRIM_W + 4)
        A(f'<rect x="{bx}" y="{by}" width="{G.BRIM_D}" height="{G.BRIM_W}" rx="2" class="furn"/>')
        A(f'<text x="{bx+G.BRIM_D//2}" y="{by+G.BRIM_W//2+4}" class="furn-label">W{i+3}</text>')


# ---- Laundry ----

def _laundry(furn, G):
    """Washer/dryer, Smith cage, standing desk, TV."""
    A = furn.append

    # Stacked washer/dryer (against wall D near wall F)
    wd_w, wd_h = px(27), px(30)
    wd_x = G.X_LEFT + 10
    wd_y = G.Y_FOYER_TOP - wd_h - 10
    A(f'<rect x="{wd_x}" y="{wd_y}" width="{wd_w}" height="{wd_h}" rx="3" class="furn"/>')
    A(f'<text x="{wd_x+wd_w//2}" y="{wd_y+wd_h//2-4}" class="furn-label">W/D</text>')
    A(f'<text x="{wd_x+wd_w//2}" y="{wd_y+wd_h//2+10}" class="furn-label">Stacked</text>')

    # Smith cage (against wall E + wall A, 4' deep × 7' long)
    sm_w, sm_h = px(48), px(84)
    sm_x = G.X_CENTER - sm_w - 10
    sm_y = G.Y_TOP + 10
    A(f'<rect x="{sm_x}" y="{sm_y}" width="{sm_w}" height="{sm_h}" rx="2" class="furn"/>')
    A(f'<text x="{sm_x+sm_w//2}" y="{sm_y+sm_h//2-4}" class="furn-label">Smith</text>')
    A(f'<text x="{sm_x+sm_w//2}" y="{sm_y+sm_h//2+10}" class="furn-label">Cage</text>')

    # Standing desk (against wall D + wall A, left of window)
    dk_w, dk_h = px(24), px(48)    # 2' deep × 4' wide
    dk_x = G.X_LEFT + 10
    dk_y = G.Y_TOP + 10
    A(f'<rect x="{dk_x}" y="{dk_y}" width="{dk_w}" height="{dk_h}" rx="2" class="furn"/>')
    A(f'<text x="{dk_x+dk_w//2}" y="{dk_y+dk_h//2-4}" class="furn-label">Standing</text>')
    A(f'<text x="{dk_x+dk_w//2}" y="{dk_y+dk_h//2+10}" class="furn-label">Desk</text>')

    # TV on wall D (mid-height, facing right)
    ltv_w, ltv_h = 8, 100
    ltv_x = G.X_LEFT + 10
    ltv_y = (G.Y_TOP + G.Y_FOYER_TOP) // 2 - ltv_h // 2
    A(f'<rect x="{ltv_x}" y="{ltv_y}" width="{ltv_w}" height="{ltv_h}" rx="1" fill="#333" stroke="#222" stroke-width="1"/>')
    A(f'<text x="{ltv_x+ltv_w+12}" y="{ltv_y+ltv_h//2+4}" class="furn-label">TV</text>')


# ---- Family room ----

def _family_room(furn, G):
    """TV, media console, and couch."""
    A = furn.append

    # TV on wall E (center partition, facing right)
    ftv_w, ftv_h = 8, 132
    ftv_x = G.X_CENTER + 4
    ftv_y = (G.Y_TOP + G.Y_FOYER_TOP) // 2 - ftv_h // 2
    A(f'<rect x="{ftv_x}" y="{ftv_y}" width="{ftv_w}" height="{ftv_h}" rx="1" fill="#333" stroke="#222" stroke-width="1"/>')
    A(f'<text x="{ftv_x+ftv_w+12}" y="{ftv_y+ftv_h//2+4}" class="furn-label">TV</text>')

    # Media console under TV on wall E
    mc_w, mc_h = px(18), px(60)    # 18" deep × 60" wide
    mc_x = ftv_x + ftv_w + 2
    mc_y = ftv_y + (ftv_h - mc_h) // 2
    A(f'<rect x="{mc_x}" y="{mc_y}" width="{mc_w}" height="{mc_h}" rx="2" class="furn"/>')
    A(f'<text x="{mc_x+mc_w//2}" y="{mc_y+mc_h//2-4}" class="furn-label">Media</text>')
    A(f'<text x="{mc_x+mc_w//2}" y="{mc_y+mc_h//2+10}" class="furn-label">Console</text>')

    # Couch against wall B (centered between upper two windows, covers edges OK)
    couch_w, couch_h = px(36), px(84)  # 36" deep × 84" wide (3-person)
    couch_x = G.X_RIGHT - couch_w - 10
    couch_y = (G.WIN_B[0][1] + G.WIN_B[1][0]) // 2 - couch_h // 2
    A(f'<rect x="{couch_x}" y="{couch_y}" width="{couch_w}" height="{couch_h}" rx="4" class="furn"/>')
    A(f'<text x="{couch_x+couch_w//2}" y="{couch_y+couch_h//2+5}" class="furn-label">Couch</text>')


# ---- Storage closet ----

def _storage_closet(furn, G):
    """Wardrobes and vanity desk."""
    A = furn.append

    # 2× BRIMNES wardrobes against wall D
    bx = G.X_LEFT + 8
    by_start = G.Y_BATH2_BOTTOM + 40   # below door swing
    for i in range(2):
        by = by_start + i * (G.BRIM_W + 2)
        A(f'<rect x="{bx}" y="{by}" width="{G.BRIM_D}" height="{G.BRIM_W}" rx="2" class="furn"/>')
        A(f'<text x="{bx+G.BRIM_D//2}" y="{by+G.BRIM_W//2+4}" class="furn-label">W{i+1}</text>')

    # Vanity / makeup desk against wall C
    van_w, van_h = px(48), px(20)
    van_x = G.X_LEFT + 8
    van_y = G.Y_BOTTOM - van_h - 10
    A(f'<rect x="{van_x}" y="{van_y}" width="{van_w}" height="{van_h}" rx="2" class="furn"/>')
    A(f'<text x="{van_x+van_w//2}" y="{van_y+van_h//2+4}" class="furn-label">Vanity</text>')
