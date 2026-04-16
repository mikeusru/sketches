from pathlib import Path


def main():
    # Canvas + scale
    W, H = 980, 1290
    left, top = 50, 50
    outer_w, outer_h = 735, 1190

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
    y_bath_top = 596
    y_bath_mid = 711

    # Foyer/hall top horizontal
    y_foyer_top = 559

    # Mechanical room / rec room
    y_mech_top = 697
    y_mech_bottom = 807   # approx 110 px -> about 4 ft-ish
    x_mech_left = 392
    x_mech_right = x_right  # user said outside width more like 12', basically full right bay

    # Door opening from hall into mech on LEFT side wall, not bottom
    mech_door_y1 = 725
    mech_door_y2 = 775

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
.dim{font:13px Arial,sans-serif;fill:#333}
.guide{stroke:#aaa;stroke-width:1.5;fill:none;stroke-dasharray:5 4}
]]></style>
</defs>''')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f6f6f6"/>')

    # Outer shell
    A(f'<rect x="{left}" y="{top}" width="{outer_w}" height="{outer_h}" class="wall"/>')

    # Window notches (same rough look)
    for x1, x2, y in [(134, 246, y_top), (358, 456, y_bottom)]:
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#f6f6f6" stroke-width="20"/>')
        A(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#999" stroke-width="2"/>')
    for y1, y2 in [(162, 207), (408, 462), (910, 954)]:
        A(f'<line x1="{x_right}" y1="{y1}" x2="{x_right}" y2="{y2}" stroke="#f6f6f6" stroke-width="20"/>')
        A(f'<line x1="{x_right}" y1="{y1}" x2="{x_right}" y2="{y2}" stroke="#999" stroke-width="2"/>')

    # Main center partition / hall guide
    A(f'<line x1="{x_center}" y1="{y_top}" x2="{x_center}" y2="{y_foyer_top}" class="wall"/>')
    A(f'<line x1="{x_center-50}" y1="{y_top}" x2="{x_center-50}" y2="{y_bottom}" class="thin" opacity="0.55"/>')
    A(f'<line x1="{x_center-2}" y1="{y_top}" x2="{x_center-2}" y2="{y_bottom}" class="thin" opacity="0.55"/>')

    # Left side bath/storage block with separation wall
    A(f'<line x1="{x_left}" y1="{y_bath_top}" x2="{x_storage_right}" y2="{y_bath_top}" class="wall"/>')
    A(f'<line x1="{x_left}" y1="{y_bath_mid}" x2="{x_storage_right}" y2="{y_bath_mid}" class="wall"/>')
    A(f'<line x1="{x_storage_right}" y1="{y_bath_top}" x2="{x_storage_right}" y2="{y_bottom}" class="wall"/>')

    # Separate wall between bathroom and storage closet
    A(f'<line x1="{x_left}" y1="{y_bath_mid}" x2="{x_storage_right}" y2="{y_bath_mid}" class="wall"/>')

    # Small hall bath divider and fixtures (rough)
    A(f'<line x1="{x_left+40}" y1="{y_bath_top-37}" x2="{x_left+40}" y2="{y_bath_mid}" class="thin"/>')
    A(f'<line x1="{x_left}" y1="{y_bath_top-37}" x2="{x_left+85}" y2="{y_bath_top-37}" class="wall"/>')

    # Foyer top wall
    A(f'<line x1="{x_left}" y1="{y_foyer_top}" x2="274" y2="{y_foyer_top}" class="wall"/>')
    A(f'<line x1="344" y1="{y_foyer_top}" x2="462" y2="{y_foyer_top}" class="wall"/>')

    # Mechanical room walls
    A(f'<line x1="{x_mech_left}" y1="{y_mech_top}" x2="{x_mech_right}" y2="{y_mech_top}" class="wall"/>')
    # left wall with door opening from left side
    A(f'<line x1="{x_mech_left}" y1="{y_mech_top}" x2="{x_mech_left}" y2="{mech_door_y1}" class="wall"/>')
    A(f'<line x1="{x_mech_left}" y1="{mech_door_y2}" x2="{x_mech_left}" y2="{y_mech_bottom}" class="wall"/>')
    A(f'<line x1="{x_mech_left}" y1="{y_mech_bottom}" x2="{x_mech_right}" y2="{y_mech_bottom}" class="wall"/>')

    # little hall stub wall left of mech like in original
    A(f'<line x1="411" y1="{y_mech_top}" x2="411" y2="756" class="wall"/>')
    A(f'<line x1="411" y1="730" x2="459" y2="730" class="wall"/>')

    # Stairs block
    stairs_x, stairs_y, stairs_w, stairs_h = 504, 571, 182, 126
    A(f'<rect x="{stairs_x}" y="{stairs_y}" width="{stairs_w}" height="{stairs_h}" fill="none" class="thin"/>')
    for i in range(1, 7):
        x = stairs_x + i * 26
        A(f'<line x1="{x}" y1="{stairs_y}" x2="{x}" y2="{stairs_y+stairs_h}" class="thin"/>')
    A(f'<line x1="{stairs_x}" y1="{stairs_y+63}" x2="{stairs_x+stairs_w}" y2="{stairs_y+63}" class="thin"/>')

    # Doors
    # storage closet door from rec room
    A(f'<line x1="{x_storage_right}" y1="1085" x2="{x_storage_right}" y2="1145" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {x_storage_right} 1085 A 60 60 0 0 1 {x_storage_right-60} 1145" class="door"/>')

    # bath door
    A(f'<line x1="{x_storage_right}" y1="760" x2="{x_storage_right}" y2="820" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M {x_storage_right} 760 A 60 60 0 0 1 {x_storage_right+60} 820" class="door"/>')

    # hall/laundry-ish doors from top zone
    A(f'<line x1="132" y1="560" x2="192" y2="560" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 132 560 A 60 60 0 0 0 192 620" class="door"/>')
    A(f'<line x1="284" y1="560" x2="344" y2="560" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 344 560 A 60 60 0 0 0 284 620" class="door"/>')

    # exterior/bottom entry-ish door
    A(f'<line x1="190" y1="{y_bottom}" x2="250" y2="{y_bottom}" stroke="#f6f6f6" stroke-width="20"/>')
    A(f'<path d="M 190 {y_bottom} A 60 60 0 0 0 250 {y_bottom-60}" class="door"/>')

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
    A('<text x="102" y="885" class="room2">Storage</text>')
    A('<text x="88" y="913" class="room2">Closet</text>')
    A('<text x="116" y="675" class="small">Bathroom</text>')
    A('<text x="543" y="760" class="small">MECHANICAL ROOM</text>')
    A('<text x="455" y="920" class="room">Rec Room</text>')

    # Simple bathroom fixtures
    A('<rect x="61" y="825" width="63" height="103" fill="none" class="thin"/>')
    A('<ellipse cx="82" cy="660" rx="16" ry="24" class="thin"/>')
    A('<ellipse cx="82" cy="704" rx="16" ry="24" class="thin"/>')
    A('<rect x="114" y="650" width="32" height="20" class="thin"/>')
    A('<rect x="114" y="694" width="32" height="20" class="thin"/>')
    A('<circle cx="130" cy="660" r="6" class="thin"/>')
    A('<circle cx="130" cy="704" r="6" class="thin"/>')

    # Dimension callouts
    A('<text x="197" y="250" class="dim">12\' 2 1/4"</text>')
    A('<text x="588" y="250" class="dim">14\' 1 1/2"</text>')
    A('<text x="603" y="840" class="dim">12\' mech width (approx)</text>')
    A('<text x="470" y="798" class="dim">bottom wall to mech bottom ≈ 13\'</text>')
    A('<text x="68" y="965" class="dim">Storage width ≈ 4\'8"</text>')

    # Notes
    A('<text x="810" y="1010" class="note">Updated per your notes:</text>')
    A('<text x="810" y="1032" class="note">• mech room width ≈ 12\'</text>')
    A('<text x="810" y="1054" class="note">• mech door opens from left side</text>')
    A('<text x="810" y="1076" class="note">• bath separated from storage closet</text>')
    A('<text x="810" y="1098" class="note">• separate storage door from rec room</text>')
    A('</svg>')

    out = Path(__file__).resolve().parent / "basement_plan.svg"
    out.write_text("\n".join(svg), encoding="utf-8")
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
