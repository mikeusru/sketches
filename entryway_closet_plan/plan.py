import math, os
from fractions import Fraction

def fmt_in(x, denom=16):
    sign = "-" if x < 0 else ""
    x = abs(x)
    n = round(x * denom)
    whole = n // denom
    rem = n % denom
    if rem == 0:
        return f'{sign}{whole}"'
    frac = Fraction(rem, denom)
    if whole == 0:
        return f'{sign}{frac.numerator}/{frac.denominator}"'
    return f'{sign}{whole} {frac.numerator}/{frac.denominator}"'

# Dimensions
overall_w = 17.0
overall_h = 60.0
closet_opening_w = 24.0
lower_h = 26.0
upper_h = 34.0
lower_d = 23.0
upper_d = 13.5
ply34 = 0.75
ply12 = 0.5
ply14 = 0.25
slide_side = 0.5
drawer_front_t = 0.75

inside_w = overall_w - 2*ply34
lower_inside_h = lower_h - 2*ply34
drawer_gap = 0.125
drawer_front_h = (lower_inside_h - 3*drawer_gap) / 2
drawer_front_w = inside_w - 2*drawer_gap
drawer_box_w = inside_w - 2*slide_side
drawer_box_d = 22.0
drawer_box_h = 10.5
upper_inside_h = upper_h - 2*ply34
cubby_clear_h = (upper_inside_h - 2*ply34) / 3
step_back = lower_d - upper_d

S = 18
W = 1900
H = 1400
svg = []

def add(s): svg.append(s)
def esc(t): return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def line(x1,y1,x2,y2,stroke="#222",sw=2,dash=None):
    style = f'stroke:{stroke};stroke-width:{sw};fill:none'
    if dash: style += f';stroke-dasharray:{dash}'
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" style="{style}" />')
def rect(x,y,w,h,stroke="#222",sw=2,fill="none",rx=0):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" style="stroke:{stroke};stroke-width:{sw};fill:{fill}" />')
def poly(points, stroke="#222", sw=2, fill="none"):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x,y in points)
    add(f'<polygon points="{pts}" style="stroke:{stroke};stroke-width:{sw};fill:{fill}" />')
def text(x,y,t,size=18,anchor="start",weight="normal",fill="#222"):
    add(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(t)}</text>')
def text_multiline(x,y,lines,size=16,leading=1.3,anchor="start",weight="normal",fill="#222"):
    dy=size*leading
    for i,ln in enumerate(lines):
        text(x,y+i*dy,ln,size=size,anchor=anchor,weight=weight,fill=fill)
def arrowhead(x,y,angle,stroke="#444"):
    L=8; Wd=5
    x2 = x - L*math.cos(angle) + Wd*math.sin(angle)
    y2 = y - L*math.sin(angle) - Wd*math.cos(angle)
    x3 = x - L*math.cos(angle) - Wd*math.sin(angle)
    y3 = y - L*math.sin(angle) + Wd*math.cos(angle)
    add(f'<polygon points="{x:.1f},{y:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}" style="fill:{stroke};stroke:{stroke};stroke-width:1" />')
def dim_h(x1,x2,y,label,ext_y1=None,ext_y2=None,color="#4a4a4a",text_offset=-10):
    if ext_y1 is not None: line(x1,ext_y1,x1,y,stroke=color,sw=1.5)
    if ext_y2 is not None: line(x2,ext_y2,x2,y,stroke=color,sw=1.5)
    line(x1,y,x2,y,stroke=color,sw=1.5)
    arrowhead(x1,y,math.pi,stroke=color); arrowhead(x2,y,0,stroke=color)
    text((x1+x2)/2,y+text_offset,label,size=15,anchor="middle",fill=color)
def dim_v(y1,y2,x,label,ext_x1=None,ext_x2=None,color="#4a4a4a",text_offset=-10):
    if ext_x1 is not None: line(ext_x1,y1,x,y1,stroke=color,sw=1.5)
    if ext_x2 is not None: line(ext_x2,y2,x,y2,stroke=color,sw=1.5)
    line(x,y1,x,y2,stroke=color,sw=1.5)
    arrowhead(x,y1,-math.pi/2,stroke=color); arrowhead(x,y2,math.pi/2,stroke=color)
    cx=x+text_offset; cy=(y1+y2)/2
    add(f'<text x="{cx:.1f}" y="{cy:.1f}" transform="rotate(-90 {cx:.1f},{cy:.1f})" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="{color}">{esc(label)}</text>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<rect width="100%" height="100%" fill="white"/>')

text(60, 40, "Entryway Closet Tower — measured SVG with material thickness", size=30, weight="bold")
text(60, 68, "Assumed materials: 3/4\" plywood carcass + cubby shelves, 1/2\" plywood drawer boxes, 1/4\" drawer bottoms, 1/2\" side-mount slide clearance per side", size=16, fill="#555")
text(60, 92, "Builder-check drawing only: useful for measurement logic, cut planning, and proportion checks before final construction drawings.", size=15, fill="#666")

front_x = 120; front_base = 1260
side_x = 660; side_base = 1260
drawer_x = 1180

# FRONT
text(front_x, 165, "A. Front elevation", size=22, weight="bold")
text(front_x, 190, "Shown inside a 24\" closet opening (dashed). Unit width stays 17\".", size=14, fill="#666")
closet_px_w = closet_opening_w*S; tower_px_w = overall_w*S; tower_px_h = overall_h*S
closet_left = front_x + (tower_px_w - closet_px_w)/2; tower_left=front_x; tower_right=front_x+tower_px_w; tower_top=front_base-tower_px_h
add(f'<rect x="{closet_left:.1f}" y="{tower_top:.1f}" width="{closet_px_w:.1f}" height="{tower_px_h:.1f}" style="stroke:#b8bcc5;stroke-width:2;fill:none;stroke-dasharray:7 7" />')
rect(tower_left,tower_top,tower_px_w,tower_px_h,stroke="#111",sw=3,fill="#fafafa")
y_seam=front_base-lower_h*S
line(tower_left,y_seam,tower_right,y_seam,stroke="#444",sw=2)
text(tower_right+18, y_seam+4, "stack joint", size=12, fill="#666")
inner_left=tower_left+ply34*S; inner_right=tower_right-ply34*S
lower_open_top=front_base-(lower_h-ply34)*S; lower_open_bottom=front_base-ply34*S
rect(inner_left, lower_open_top, inside_w*S, lower_inside_h*S, stroke="#777", sw=1.5, fill="#fff")
bf_y = front_base - (ply34 + drawer_gap + drawer_front_h)*S
tf_y = front_base - (ply34 + drawer_gap + drawer_front_h + drawer_gap + drawer_front_h)*S
df_x = tower_left + (ply34 + drawer_gap)*S; df_w = drawer_front_w*S; df_h = drawer_front_h*S
rect(df_x,bf_y,df_w,df_h,stroke="#333",sw=2,fill="#efefef"); rect(df_x,tf_y,df_w,df_h,stroke="#333",sw=2,fill="#efefef")
for cy in [bf_y+df_h/2, tf_y+df_h/2]:
    line(df_x+df_w/2-18, cy, df_x+df_w/2+18, cy, stroke="#555", sw=4)
upper_open_top=front_base-(overall_h-ply34)*S
rect(inner_left, upper_open_top, inside_w*S, upper_inside_h*S, stroke="#777", sw=1.5, fill="#fff")
shelf1_y = front_base - (lower_h + ply34 + cubby_clear_h)*S
shelf2_y = front_base - (lower_h + ply34 + cubby_clear_h + ply34 + cubby_clear_h)*S
rect(inner_left, shelf1_y, inside_w*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")
rect(inner_left, shelf2_y, inside_w*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")

dim_h(closet_left, closet_left+closet_px_w, tower_top-75, f'closet opening {fmt_in(closet_opening_w)}', ext_y1=tower_top, ext_y2=tower_top, text_offset=-12)
dim_h(tower_left, tower_right, front_base+48, f'unit width {fmt_in(overall_w)}', ext_y1=front_base, ext_y2=front_base, text_offset=22)
dim_h(inner_left, inner_right, front_base+82, f'inside width {fmt_in(inside_w)}', ext_y1=lower_open_bottom, ext_y2=lower_open_bottom, text_offset=22)
dim_v(tower_top, front_base, tower_left-70, f'overall height {fmt_in(overall_h)}', ext_x1=tower_left, ext_x2=tower_left, text_offset=-12)
dim_v(y_seam, front_base, tower_right+55, f'lower box {fmt_in(lower_h)}', ext_x1=tower_right, ext_x2=tower_right, text_offset=14)
dim_v(tower_top, y_seam, tower_right+90, f'upper box {fmt_in(upper_h)}', ext_x1=tower_right, ext_x2=tower_right, text_offset=14)
dim_v(upper_open_top, shelf2_y, tower_left-30, f'{fmt_in(cubby_clear_h)} clear', ext_x1=inner_left, ext_x2=inner_left, text_offset=-10)
dim_v(shelf2_y+ply34*S, shelf1_y, tower_left-30, f'{fmt_in(cubby_clear_h)} clear', ext_x1=inner_left, ext_x2=inner_left, text_offset=-10)
dim_v(shelf1_y+ply34*S, y_seam+ply34*S, tower_left-30, f'{fmt_in(cubby_clear_h)} clear', ext_x1=inner_left, ext_x2=inner_left, text_offset=-10)
dim_v(tf_y, tf_y+df_h, tower_right+130, f'{fmt_in(drawer_front_h)} front', ext_x1=df_x+df_w, ext_x2=df_x+df_w, text_offset=14)
dim_v(bf_y, bf_y+df_h, tower_right+130, f'{fmt_in(drawer_front_h)} front', ext_x1=df_x+df_w, ext_x2=df_x+df_w, text_offset=14)
text(tower_left, front_base+118, "Drawer fronts shown as inset slab fronts with 1/8\" reveals.", size=13, fill="#666")

# SIDE
text(side_x, 165, "B. Side section", size=22, weight="bold")
text(side_x, 190, "Front aligned; upper cubbies step back at the rear.", size=14, fill="#666")
sx=side_x; sb=side_base
poly([(sx,sb),(sx+lower_d*S,sb),(sx+lower_d*S,sb-lower_h*S),(sx,sb-lower_h*S)],stroke="#111",sw=3,fill="#fafafa")
poly([(sx,sb-lower_h*S),(sx+upper_d*S,sb-lower_h*S),(sx+upper_d*S,sb-overall_h*S),(sx,sb-overall_h*S)],stroke="#111",sw=3,fill="#fafafa")
# panels
rect(sx, sb-ply34*S, lower_d*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")
rect(sx, sb-lower_h*S, lower_d*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")
rect(sx, sb-lower_h*S, upper_d*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")
rect(sx, sb-overall_h*S, upper_d*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")
s1=sb-(lower_h+ply34+cubby_clear_h)*S; s2=sb-(lower_h+ply34+cubby_clear_h+ply34+cubby_clear_h)*S
rect(sx, s1, upper_d*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3"); rect(sx, s2, upper_d*S, ply34*S, stroke="#555", sw=1.5, fill="#f3f3f3")
drawer_y0=sb-(ply34+0.75)*S
rect(sx+drawer_front_t*S, drawer_y0-drawer_box_h*S, drawer_box_d*S, drawer_box_h*S, stroke="#337ab7", sw=2, fill="#eef6ff")
rect(sx, drawer_y0-drawer_front_h*S*0.82, drawer_front_t*S, drawer_front_h*S*0.82, stroke="#333", sw=1.5, fill="#efefef")
text(sx+drawer_box_d*S/2, drawer_y0-drawer_box_h*S-12, f'typical drawer box {fmt_in(drawer_box_d)} deep', size=13, anchor="middle", fill="#337ab7")
dim_h(sx, sx+lower_d*S, sb+48, f'lower depth {fmt_in(lower_d)}', ext_y1=sb, ext_y2=sb, text_offset=22)
dim_h(sx, sx+upper_d*S, sb-overall_h*S-55, f'upper depth {fmt_in(upper_d)}', ext_y1=sb-overall_h*S, ext_y2=sb-overall_h*S, text_offset=-12)
dim_h(sx+upper_d*S, sx+lower_d*S, sb-lower_h*S-55, f'step back {fmt_in(step_back)}', ext_y1=sb-lower_h*S, ext_y2=sb-lower_h*S, text_offset=-12)
dim_v(sb-ply34*S, sb, sx+lower_d*S+45, f'{fmt_in(ply34)} ply', ext_x1=sx+lower_d*S, ext_x2=sx+lower_d*S, text_offset=12)
dim_v(s1, s1+ply34*S, sx+upper_d*S+45, f'{fmt_in(ply34)} shelf', ext_x1=sx+upper_d*S, ext_x2=sx+upper_d*S, text_offset=12)
dim_v(sb-overall_h*S, sb, sx-60, f'{fmt_in(overall_h)} overall', ext_x1=sx, ext_x2=sx, text_offset=-12)
dim_v(sb-lower_h*S, sb, sx+lower_d*S+82, f'{fmt_in(lower_h)} lower', ext_x1=sx+lower_d*S, ext_x2=sx+lower_d*S, text_offset=14)
dim_v(sb-overall_h*S, sb-lower_h*S, sx+upper_d*S+82, f'{fmt_in(upper_h)} upper', ext_x1=sx+upper_d*S, ext_x2=sx+upper_d*S, text_offset=14)
text_multiline(sx, sb+110, [
    "Construction logic shown here:",
    "• lower box and upper box are separate plywood carcasses",
    "• screw upper box down into lower box after squaring",
    "• anchor finished stack to closet studs",
    "• 22\" side-mount slides assume open back / no rear panel"
], size=13, fill="#666")

# drawer details
text(drawer_x, 165, "C. Drawer sizing detail", size=22, weight="bold")
text(drawer_x, 190, "This is the logic that typically matters most before cutting parts.", size=14, fill="#666")
dx=drawer_x; dy=250; ow=inside_w*S; od=8*S
rect(dx,dy,ow,od,stroke="#222",sw=2,fill="#fafafa")
rect(dx,dy,slide_side*S,od,stroke="#8b6",sw=1.5,fill="#eef7df")
rect(dx+(inside_w-slide_side)*S,dy,slide_side*S,od,stroke="#8b6",sw=1.5,fill="#eef7df")
rect(dx+slide_side*S,dy+8,drawer_box_w*S,od-16,stroke="#337ab7",sw=2,fill="#eef6ff")
text(dx+ow/2,dy-16,"Top view at drawer opening",size=15,anchor="middle",weight="bold")
dim_h(dx,dx+ow,dy+od+35,f'clear opening width {fmt_in(inside_w)}',ext_y1=dy+od,ext_y2=dy+od,text_offset=18)
dim_h(dx+slide_side*S,dx+(slide_side+drawer_box_w)*S,dy-30,f'drawer box width {fmt_in(drawer_box_w)}',ext_y1=dy,ext_y2=dy,text_offset=-10)
dim_h(dx,dx+slide_side*S,dy-60,f'{fmt_in(slide_side)} slide',ext_y1=dy,ext_y2=dy,text_offset=-10)
dim_h(dx+(slide_side+drawer_box_w)*S,dx+ow,dy-60,f'{fmt_in(slide_side)} slide',ext_y1=dy,ext_y2=dy,text_offset=-10)

fvx=drawer_x; fvy=520
rect(fvx,fvy,drawer_front_w*S,drawer_front_h*S,stroke="#333",sw=2,fill="#efefef")
line(fvx+drawer_front_w*S/2-18,fvy+drawer_front_h*S/2,fvx+drawer_front_w*S/2+18,fvy+drawer_front_h*S/2,stroke="#555",sw=4)
text(fvx+drawer_front_w*S/2,fvy-16,"Inset drawer front",size=15,anchor="middle",weight="bold")
dim_h(fvx,fvx+drawer_front_w*S,fvy+drawer_front_h*S+35,f'{fmt_in(drawer_front_w)} wide x {fmt_in(drawer_front_h)} high',ext_y1=fvy+drawer_front_h*S,ext_y2=fvy+drawer_front_h*S,text_offset=18)
dim_v(fvy,fvy+drawer_front_h*S,fvx+drawer_front_w*S+40,f'{fmt_in(drawer_front_h)}',ext_x1=fvx+drawer_front_w*S,ext_x2=fvx+drawer_front_w*S,text_offset=12)

boxx=drawer_x+380; boxy=470
rect(boxx,boxy,drawer_box_d*S,drawer_box_h*S,stroke="#337ab7",sw=2,fill="#eef6ff")
rect(boxx,boxy+drawer_box_h*S-ply14*S,drawer_box_d*S,ply14*S,stroke="#557",sw=1.5,fill="#f4f4ff")
text(boxx+drawer_box_d*S/2,boxy-16,"Drawer box side view",size=15,anchor="middle",weight="bold")
dim_h(boxx,boxx+drawer_box_d*S,boxy+drawer_box_h*S+35,f'{fmt_in(drawer_box_d)} deep',ext_y1=boxy+drawer_box_h*S,ext_y2=boxy+drawer_box_h*S,text_offset=18)
dim_v(boxy,boxy+drawer_box_h*S,boxx+drawer_box_d*S+40,f'{fmt_in(drawer_box_h)} high',ext_x1=boxx+drawer_box_d*S,ext_x2=boxx+drawer_box_d*S,text_offset=12)
dim_v(boxy+drawer_box_h*S-ply14*S,boxy+drawer_box_h*S,boxx+drawer_box_d*S+80,f'{fmt_in(ply14)} bottom',ext_x1=boxx+drawer_box_d*S,ext_x2=boxx+drawer_box_d*S,text_offset=12)

fwx=drawer_x+380; fwy=770
rect(fwx,fwy,drawer_box_w*S,drawer_box_h*S*0.9,stroke="#337ab7",sw=2,fill="#eef6ff")
rect(fwx,fwy,ply12*S,drawer_box_h*S*0.9,stroke="#225e8a",sw=1.5,fill="#dbefff")
rect(fwx+(drawer_box_w-ply12)*S,fwy,ply12*S,drawer_box_h*S*0.9,stroke="#225e8a",sw=1.5,fill="#dbefff")
text(fwx+drawer_box_w*S/2,fwy-16,"Drawer box front view",size=15,anchor="middle",weight="bold")
dim_h(fwx,fwx+drawer_box_w*S,fwy+drawer_box_h*S*0.9+35,f'outside width {fmt_in(drawer_box_w)}',ext_y1=fwy+drawer_box_h*S*0.9,ext_y2=fwy+drawer_box_h*S*0.9,text_offset=18)
dim_h(fwx+ply12*S,fwx+(drawer_box_w-ply12)*S,fwy-30,f'front/back piece = {fmt_in(drawer_box_w-2*ply12)} wide',ext_y1=fwy,ext_y2=fwy,text_offset=-10)
dim_h(fwx,fwx+ply12*S,fwy-60,f'{fmt_in(ply12)} side',ext_y1=fwy,ext_y2=fwy,text_offset=-10)

# schedule
cx=1180; cy=1010
text(cx, cy, "D. Material schedule and checked dimensions", size=22, weight="bold")
lines=[
    f'3/4" plywood — lower box sides: 2 @ {fmt_in(lower_h)} x {fmt_in(lower_d)}',
    f'3/4" plywood — lower box top/bottom: 2 @ {fmt_in(inside_w)} x {fmt_in(lower_d)}',
    f'3/4" plywood — upper box sides: 2 @ {fmt_in(upper_h)} x {fmt_in(upper_d)}',
    f'3/4" plywood — upper box top/bottom: 2 @ {fmt_in(inside_w)} x {fmt_in(upper_d)}',
    f'3/4" plywood — upper cubby shelves: 2 @ {fmt_in(inside_w)} x {fmt_in(upper_d)}',
    f'3/4" plywood — drawer fronts (inset shown): 2 @ {fmt_in(drawer_front_w)} x {fmt_in(drawer_front_h)}',
    f'1/2" plywood — drawer box sides: 4 @ {fmt_in(drawer_box_d)} x {fmt_in(drawer_box_h)}',
    f'1/2" plywood — drawer box fronts/backs: 4 @ {fmt_in(drawer_box_w-2*ply12)} x {fmt_in(drawer_box_h)}',
    f'1/4" plywood — drawer bottoms (underside mount shown): 2 @ {fmt_in(drawer_box_w)} x {fmt_in(drawer_box_d)}',
    f'Slides — 2 pairs @ {fmt_in(drawer_box_d)} side-mount full extension',
]
text_multiline(cx,cy+36,lines,size=14,fill="#333")
notes2=[
    f'Inside width of carcass = {fmt_in(overall_w)} - 2 × {fmt_in(ply34)} = {fmt_in(inside_w)}',
    f'Drawer box width = {fmt_in(inside_w)} - 2 × {fmt_in(slide_side)} = {fmt_in(drawer_box_w)}',
    f'Lower interior height = {fmt_in(lower_h)} - 2 × {fmt_in(ply34)} = {fmt_in(lower_inside_h)}',
    f'Inset drawer front height = ({fmt_in(lower_inside_h)} - 3 × 1/8") / 2 = {fmt_in(drawer_front_h)}',
    f'Upper clear cubby height = ({fmt_in(upper_h)} - 4 × {fmt_in(ply34)}) / 3 = {fmt_in(cubby_clear_h)}',
]
text_multiline(cx,cy+225,notes2,size=14,fill="#333")

text(60, 1360, "Measured concept only — verify wall plumb/square, actual slide specs, and preferred face reveal before cutting finished drawer faces.", size=13, fill="#666")
add('</svg>')

svg_path="/mnt/data/entry_closet_tower_detailed_measured.svg"
with open(svg_path,"w",encoding="utf-8") as f: f.write("\n".join(svg))
print(svg_path, os.path.getsize(svg_path))
