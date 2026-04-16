"""CLI entry point for the basement floor plan SVG generator."""

from pathlib import Path
import argparse

from .helpers import svg_preamble
from .structure import draw_structure
from .furniture import draw_furniture


def main():
    svg = svg_preamble()
    svg += draw_structure()
    furn = draw_furniture()
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
        bare = svg + ['</g>', '</svg>']
        p1 = out_dir / "basement_plan.svg"
        p1.write_text("\n".join(bare), encoding="utf-8")
        print(f"Saved to {p1}")
        # Furnished
        full = svg + furn + ['</g>', '</svg>']
        p2 = out_dir / "basement_plan_furnished.svg"
        p2.write_text("\n".join(full), encoding="utf-8")
        print(f"Saved to {p2}")
    elif args.furniture:
        full = svg + furn + ['</g>', '</svg>']
        p = out_dir / "basement_plan_furnished.svg"
        p.write_text("\n".join(full), encoding="utf-8")
        print(f"Saved to {p}")
    else:
        bare = svg + ['</g>', '</svg>']
        p = out_dir / "basement_plan.svg"
        p.write_text("\n".join(bare), encoding="utf-8")
        print(f"Saved to {p}")


if __name__ == "__main__":
    cli()
