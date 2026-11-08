import json
import unittest
from pathlib import Path

from timsim.fit import fit_thickness_series

SOURCE = Path(__file__).resolve().parents[1] / "data/experiments/tian2013_fig3c.json"


class TianThicknessTests(unittest.TestCase):
    def test_marker_calibration(self):
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
        axis = data["calibration"]
        self.assertEqual(len(data["observations"]), 4)
        for row in data["observations"]:
            x, y = row["marker_center_pdf_pt"]
            left, right = axis["x_pdf_pt"]
            bottom, top = axis["y_pdf_pt"]
            # Use the labeled 100 and 300 µm ticks; the left frame is not zero.
            self.assertAlmostEqual(100 + 200*(x-left)/(right-left), row["thickness_um"], places=5)
            self.assertAlmostEqual(5*(y-bottom)/(top-bottom), row["resistance_cm2k_w"], places=6)

    def test_si_conversion_and_intercept(self):
        rows = json.loads(SOURCE.read_text(encoding="utf-8"))["observations"]
        fit = fit_thickness_series(thickness_m=[r["thickness_um"]*1e-6 for r in rows],
                                   resistance_m2k_w=[r["resistance_cm2k_w"]*1e-4 for r in rows])
        self.assertAlmostEqual(fit.conductivity_z_w_mk, 0.672599, places=5)
        self.assertAlmostEqual(fit.combined_contact_m2k_w*1e6, 12.98378, places=4)
