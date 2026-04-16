"""Declarative floor plan model.

All geometry is in inches relative to an interior origin. The renderer is
responsible for converting to pixels and drawing SVG.

Locked vs loose (unlocked):
- Every measurement carries `locked: bool` (default True).
- Locked = intentional / verified — treat this value as authoritative.
- Loose = an estimate / placeholder — this value should absorb changes
  when a neighboring locked value is adjusted.
- Visually: loose walls render dashed orange, loose dimensions render
  italic orange so it's obvious which numbers aren't confirmed.

This file defines dataclasses and the FloorPlan builder. No pixel math here.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Point:
    name: str
    x: float                 # inches
    y: float                 # inches
    locked: bool = True      # False = estimated position


@dataclass
class Wall:
    name: str
    p1: str                  # point name
    p2: str                  # point name
    locked: bool = True      # False = estimated (rendered dashed orange)


@dataclass
class Door:
    wall: str
    offset: float            # inches from p1 along wall
    width: float = 30
    hinge: str = "start"     # "start" or "end"
    swing: str = "N"         # "N" / "S" / "E" / "W"
    leaves: int = 1          # 1 = single, 2 = double
    locked: bool = True


@dataclass
class Window:
    wall: str
    offset: float
    width: float
    locked: bool = True


@dataclass
class Opening:
    """Open passage (no door, no window) — just a gap in the wall."""
    wall: str
    offset: float
    width: float
    locked: bool = True


@dataclass
class Room:
    name: str
    bounds: list             # ordered point names (polygon)
    label: Optional[str] = None
    label_style: str = "room"
    label_pos: Optional[tuple] = None  # override (x, y) in inches


@dataclass
class Stairs:
    x: float
    y: float
    w: float
    h: float
    steps: int = 7
    direction: str = "up"


@dataclass
class Fixture:
    kind: str                # "toilet" | "sink" | "shower" | "rect" | "fireplace"
    x: float
    y: float
    w: float
    h: float
    label: str = ""


@dataclass
class Dimension:
    p1: str
    p2: str
    offset: float            # inches perpendicular offset from measured line
    axis: str = "h"          # "h" (measures x-distance) or "v" (measures y-distance)
    locked: bool = True


@dataclass
class Label:
    text: str
    x: float
    y: float
    style: str = "small"
    anchor: str = "middle"
    wall_label: bool = False


class FloorPlan:
    """Declarative floor plan. Add points, walls, features, rooms, labels."""

    def __init__(self, name: str = "Floor Plan"):
        self.name = name
        self.points: dict[str, Point] = {}
        self.walls: dict[str, Wall] = {}
        self.doors: list[Door] = []
        self.windows: list[Window] = []
        self.openings: list[Opening] = []
        self.rooms: list[Room] = []
        self.stairs: list[Stairs] = []
        self.fixtures: list[Fixture] = []
        self.dimensions: list[Dimension] = []
        self.labels: list[Label] = []

    # ----- Points -----

    def pt(self, name, x=None, y=None, *, anchor=None, dx=0, dy=0, locked=True):
        """Add a named point. Either absolute (x, y) or offset (anchor, dx, dy)."""
        if anchor is not None:
            a = self.points[anchor]
            x = a.x + dx
            y = a.y + dy
        if x is None or y is None:
            raise ValueError(f"Point '{name}' needs (x,y) or (anchor, dx, dy)")
        self.points[name] = Point(name, float(x), float(y), locked)
        return self

    # ----- Walls -----

    def wall(self, name, p1, p2, *, locked=True):
        """Add a wall segment between two named points."""
        if p1 not in self.points:
            raise ValueError(f"Wall '{name}': unknown point '{p1}'")
        if p2 not in self.points:
            raise ValueError(f"Wall '{name}': unknown point '{p2}'")
        # A wall is only fully locked if both its endpoints are locked too.
        p1_locked = self.points[p1].locked
        p2_locked = self.points[p2].locked
        self.walls[name] = Wall(name, p1, p2, locked and p1_locked and p2_locked)
        return self

    # ----- Features -----

    def door(self, wall, offset, width=30, *,
             hinge="start", swing="N", leaves=1, locked=True):
        self.doors.append(Door(wall, offset, width, hinge, swing, leaves, locked))
        return self

    def window(self, wall, offset, width, *, locked=True):
        self.windows.append(Window(wall, offset, width, locked))
        return self

    def opening(self, wall, offset, width, *, locked=True):
        self.openings.append(Opening(wall, offset, width, locked))
        return self

    # ----- Rooms / stairs / fixtures -----

    def room(self, name, bounds=None, *, label=None, label_style="room", label_pos=None):
        self.rooms.append(Room(name, bounds or [], label, label_style, label_pos))
        return self

    def add_stairs(self, x, y, w, h, *, steps=7, direction="up"):
        self.stairs.append(Stairs(x, y, w, h, steps, direction))
        return self

    def fixture(self, kind, x, y, w, h, label=""):
        self.fixtures.append(Fixture(kind, x, y, w, h, label))
        return self

    # ----- Dimensions / labels -----

    def dim(self, p1, p2, offset, *, axis="h", locked=True):
        self.dimensions.append(Dimension(p1, p2, offset, axis, locked))
        return self

    def label(self, text, x, y, *, style="small", anchor="middle", wall_label=False):
        self.labels.append(Label(text, x, y, style, anchor, wall_label))
        return self

    # ----- Queries -----

    def features_on(self, wall_name):
        """Yield (kind, feature) for every door/window/opening on a wall."""
        for d in self.doors:
            if d.wall == wall_name:
                yield ("door", d)
        for w in self.windows:
            if w.wall == wall_name:
                yield ("window", w)
        for o in self.openings:
            if o.wall == wall_name:
                yield ("opening", o)
