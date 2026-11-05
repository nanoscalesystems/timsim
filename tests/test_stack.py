import math
import unittest

from timsim import calculate_joint


class JointResistanceTests(unittest.TestCase):
    def setUp(self):
        self.inputs = {
            "thickness_m": 50e-6,
            "conductivity_z_w_mk": 5.0,
            "contact_1_m2k_w": 3e-6,
            "contact_2_m2k_w": 7e-6,
            "heat_flux_w_m2": 100_000.0,
        }

    def test_hand_calculation(self):
        result = calculate_joint(**self.inputs)
        self.assertAlmostEqual(result.bulk_m2k_w * 1e6, 10.0)
        self.assertAlmostEqual(result.contact_1_m2k_w * 1e6, 3.0)
        self.assertAlmostEqual(result.contact_2_m2k_w * 1e6, 7.0)
        self.assertAlmostEqual(result.total_m2k_w * 1e6, 20.0)
        self.assertAlmostEqual(result.delta_t_k, 2.0)

    def test_bulk_only(self):
        self.inputs.update(contact_1_m2k_w=0.0, contact_2_m2k_w=0.0)
        result = calculate_joint(**self.inputs)
        self.assertEqual(result.total_m2k_w, result.bulk_m2k_w)

    def test_zero_thickness_leaves_contacts(self):
        self.inputs["thickness_m"] = 0.0
        result = calculate_joint(**self.inputs)
        self.assertEqual(result.bulk_m2k_w, 0.0)
        self.assertAlmostEqual(result.total_m2k_w * 1e6, 10.0)

    def test_zero_and_reverse_heat_flux(self):
        for flux, expected_drop in [(0.0, 0.0), (-100_000.0, -2.0)]:
            with self.subTest(flux=flux):
                self.inputs["heat_flux_w_m2"] = flux
                result = calculate_joint(**self.inputs)
                self.assertAlmostEqual(result.delta_t_k, expected_drop)
                self.assertAlmostEqual(result.total_m2k_w * 1e6, 20.0)

    def test_invalid_inputs(self):
        invalid_values = [
            ("thickness_m", -1e-6),
            ("conductivity_z_w_mk", 0.0),
            ("conductivity_z_w_mk", -1.0),
            ("contact_1_m2k_w", -1e-6),
            ("contact_2_m2k_w", -1e-6),
        ]
        for field in self.inputs:
            for value in (math.nan, math.inf, -math.inf):
                invalid_values.append((field, value))

        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                inputs = self.inputs.copy()
                inputs[field] = value
                with self.assertRaises(ValueError):
                    calculate_joint(**inputs)
