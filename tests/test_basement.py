"""Consistency tests for the basement floor plan.

Run with:  uv run python -m unittest tests.test_basement
Or:        uv run python -m unittest discover
"""

import unittest

from basement_floor_plan.basement import build_plan
from basement_floor_plan.model import FloorPlan
from basement_floor_plan.validate import validate, validate_all


class BasementPlanConsistency(unittest.TestCase):
    def setUp(self):
        self.plan = build_plan()

    def test_no_errors(self):
        errors, _warnings = validate_all(self.plan)
        self.assertEqual(
            errors, [],
            "Basement plan has geometry errors:\n"
            + "\n".join("  • " + s for s in errors)
        )


class ValidatorCatchesBadPlans(unittest.TestCase):
    """Smoke tests: the validator should flag deliberately broken plans."""

    def _minimal(self):
        p = FloorPlan("test")
        p.pt("NW", 0, 0)
        p.pt("NE", 100, 0)
        p.pt("SE", 100, 100)
        p.pt("SW", 0, 100)
        for a, b in [("NW", "NE"), ("NE", "SE"), ("SW", "SE"), ("NW", "SW")]:
            p.wall(f"{a}-{b}", a, b)
        return p

    def test_duplicate_wall(self):
        p = self._minimal()
        p.wall("dup", "NW", "NE")
        self.assertTrue(any("duplicate" in s for s in validate(p)))

    def test_door_out_of_range(self):
        p = self._minimal()
        p.door("NW-NE", offset=80, width=30, swing="S")  # 80+30 > 100
        self.assertTrue(any("exceeds wall length" in s for s in validate(p)))

    def test_overlapping_doors(self):
        p = self._minimal()
        p.door("NW-NE", offset=10, width=30, swing="S")
        p.door("NW-NE", offset=20, width=30, swing="S")
        self.assertTrue(any("overlaps" in s for s in validate(p)))

    def test_door_swing_wrong_axis(self):
        p = self._minimal()
        p.door("NW-NE", offset=10, width=30, swing="E")  # horiz wall needs N/S
        self.assertTrue(any("must be N or S" in s for s in validate(p)))

    def test_unsplit_t_junction_is_not_an_error(self):
        # T-junctions are handled gracefully by the renderer (labels auto-split),
        # so they shouldn't trip the validator.
        p = self._minimal()
        p.pt("T", 50, 0)
        p.pt("Tbot", 50, 40)
        p.wall("stub", "T", "Tbot")  # T lies on NW-NE interior
        errors, warnings = validate_all(p)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_overlapping_walls(self):
        p = self._minimal()
        p.pt("mid", 50, 0)
        p.pt("past", 150, 0)
        p.wall("overlap", "mid", "past")  # covers x=50..100 of NW-NE
        issues = validate(p)
        self.assertTrue(any("overlap" in s for s in issues))

    def test_non_axis_aligned(self):
        p = self._minimal()
        p.pt("diag", 50, 50)
        p.wall("diag", "NW", "diag")
        self.assertTrue(any("not axis-aligned" in s for s in validate(p)))


if __name__ == "__main__":
    unittest.main()
