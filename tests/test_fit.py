import unittest

from timsim.fit import fit_thickness_series


class ThicknessFitTests(unittest.TestCase):
    def test_recovers_hand_calculated_properties(self):
        fit = fit_thickness_series(
            thickness_m=[25e-6, 50e-6, 100e-6],
            resistance_m2k_w=[15e-6, 20e-6, 30e-6],
        )
        self.assertAlmostEqual(fit.conductivity_z_w_mk, 5.0)
        self.assertAlmostEqual(fit.combined_contact_m2k_w * 1e6, 10.0)
        for residual in fit.residuals_m2k_w:
            self.assertAlmostEqual(residual * 1e6, 0.0)

    def test_scatter_uses_all_measurements(self):
        # The middle point lies 3 mm²·K/W above the original line.
        fit = fit_thickness_series(
            thickness_m=[25e-6, 50e-6, 75e-6],
            resistance_m2k_w=[15e-6, 23e-6, 25e-6],
        )
        self.assertAlmostEqual(fit.conductivity_z_w_mk, 5.0)
        self.assertAlmostEqual(fit.combined_contact_m2k_w * 1e6, 11.0)
        self.assertEqual(len(fit.residuals_m2k_w), 3)
        for residual, expected in zip(fit.residuals_m2k_w, [-1, 2, -1]):
            self.assertAlmostEqual(residual * 1e6, expected)

    def test_negative_intercept_is_preserved(self):
        fit = fit_thickness_series(
            thickness_m=[50e-6, 100e-6],
            resistance_m2k_w=[5e-6, 15e-6],
        )
        self.assertAlmostEqual(fit.combined_contact_m2k_w * 1e6, -5.0)

    def test_invalid_series(self):
        cases = [
            ([25e-6], [15e-6]),
            ([25e-6, 50e-6], [15e-6]),
            ([25e-6, 25e-6], [15e-6, 20e-6]),
            ([25e-6, 50e-6], [20e-6, 15e-6]),
            ([25e-6, 50e-6], [15e-6, 15e-6]),
            ([25e-6, float("nan")], [15e-6, 20e-6]),
            ([25e-6, 50e-6], [15e-6, -1e-6]),
        ]
        for thickness, resistance in cases:
            with self.subTest(thickness=thickness, resistance=resistance):
                with self.assertRaises(ValueError):
                    fit_thickness_series(
                        thickness_m=thickness,
                        resistance_m2k_w=resistance,
                    )
