import json
import runpy
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
script = runpy.run_path(str(ROOT / "scripts/graphene_digitized_fit.py"))
data = json.loads((ROOT / "data/experiments/sudhindra2021_fig3b_10wt.json").read_text())


class DigitizationTests(unittest.TestCase):
    def test_axis_units_and_direction(self):
        x, y = script["coordinates"](data, [(123, 466), (658, 35)])
        self.assertEqual(x[0], 0)
        self.assertEqual(y[0], 0)
        self.assertAlmostEqual(x[1] * 1e6, 250)
        self.assertAlmostEqual(y[1] * 1e6, 120)

    def test_observed_thickness_range(self):
        x, _ = script["coordinates"](data, data["marker_centers_px"])
        self.assertEqual(len(x), 4)
        self.assertAlmostEqual(min(x)*1e6, 45.7944, places=3)
        self.assertAlmostEqual(max(x)*1e6, 111.6822, places=3)

    def test_reference_fit_and_contact_units(self):
        fit = script["fit"](data, data["marker_centers_px"])
        self.assertAlmostEqual(fit.conductivity_z_w_mk, 1.586778, places=5)
        self.assertAlmostEqual(fit.combined_contact_m2k_w*1e6, 10.025723, places=5)
        self.assertAlmostEqual(sum(fit.residuals_m2k_w)*1e6, 0)

    def test_sensitivity_corners(self):
        results = list(script["sensitivity"](data))
        self.assertEqual(len(results), 256)
        ks = [r.conductivity_z_w_mk for r in results]
        self.assertAlmostEqual(min(ks), 1.4886, places=4)
        self.assertAlmostEqual(max(ks), 1.6931, places=4)
