"""CLI entry point for the basement floor plan SVG generator."""

from pathlib import Path
import argparse

from .basement import build_plan
from .renderer import render, render_wall_labels, close_svg
from .furniture import draw_furniture
from .validate import validate_all


def _write(path, lines):
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved to {path}")


def cli():
    parser = argparse.ArgumentParser(description="Generate basement floor plan SVG")
    parser.add_argument("--furniture", action="store_true",
                        help="Include furniture in the SVG")
    parser.add_argument("--both", action="store_true",
                        help="Generate both furnished and unfurnished SVGs")
    args = parser.parse_args()

    plan = build_plan()

    errors, warnings = validate_all(plan)
    if warnings:
        print(f"[!] {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"[X] {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        raise SystemExit(1)

    structure = render(plan)       # ends with '</g>'
    wall_labels = render_wall_labels(plan)
    furn = draw_furniture()         # SVG lines (drawn inside the same <g>)
    out_dir = Path(__file__).resolve().parent

    # Inside the <g>, layer order: structure → (furniture) → wall labels.
    # Wall labels paint last so their letter-badges stay readable over
    # furniture fills.
    struct_open = structure[:-1]
    struct_close = [structure[-1]]
    bare = struct_open + wall_labels + struct_close + close_svg()
    full = struct_open + furn + wall_labels + struct_close + close_svg()

    if args.both:
        _write(out_dir / "basement_plan.svg", bare)
        _write(out_dir / "basement_plan_furnished.svg", full)
    elif args.furniture:
        _write(out_dir / "basement_plan_furnished.svg", full)
    else:
        _write(out_dir / "basement_plan.svg", bare)


if __name__ == "__main__":
    cli()
