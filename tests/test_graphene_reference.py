"""Guard unit conversion, the two-contact convention and source transcription."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('graphene_reference', ROOT / 'scripts/graphene_reference.py')
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
DATA = json.loads(reference.DATA_PATH.read_text(encoding='utf-8'))


class GrapheneReferenceTests(unittest.TestCase):
    def test_table_s1_transcription(self):
        expected = [
            (0, .176, .004, .681, .090), (2, .237, .100, .183, .330),
            (5, .330, .030, .149, .160), (10, 1.578, .110, .051, .020),
            (15, 1.748, .180, .011, .040), (18, 2.483, .200, .035, .020),
            (20, 2.645, .180, .075, .020), (30, 3.326, 1.200, .147, .100),
            (40, 4.221, 1.100, .234, .060),
        ]
        keys = ['loading_wt_pct', 'conductivity_w_mk', 'conductivity_se_w_mk',
                'rc_cm2k_w', 'rc_se_cm2k_w']
        self.assertEqual([tuple(row[key] for key in keys) for row in DATA['rows']], expected)

    def test_units_and_two_contacts(self):
        row = {'conductivity_w_mk': 2.0, 'rc_cm2k_w': .01}
        result = reference.reconstruct(row, 20, 10)
        self.assertAlmostEqual(result.bulk_m2k_w * 1e6, 10)
        self.assertAlmostEqual(result.contact_1_m2k_w * 1e6, 1)
        self.assertAlmostEqual(result.contact_2_m2k_w * 1e6, 1)
        self.assertAlmostEqual(result.total_m2k_w * 1e6, 12)
        self.assertAlmostEqual(result.delta_t_k, 1.2)

    def test_fifteen_percent_contact_intercept(self):
        row = next(row for row in DATA['rows'] if row['loading_wt_pct'] == 15)
        result = reference.reconstruct(row, 0, 10)
        self.assertAlmostEqual(result.total_m2k_w * 1e6, 2.2)
        self.assertEqual(row['rc_se_cm2k_w'], .040)
        self.assertGreater(row['rc_se_cm2k_w'], row['rc_cm2k_w'])

    def test_evidence_scope(self):
        self.assertEqual(DATA['evidence_type'], 'published_regression_estimates')
        self.assertEqual(DATA['contact_convention']['table_value'], 'single_interface_rc')
        self.assertEqual(DATA['material']['loading_basis'], 'mass_percent')

    def test_invalid_evaluation_inputs(self):
        row = DATA['rows'][0]
        for thickness, flux in [(-1, 10), (float('nan'), 10), (20, float('inf'))]:
            with self.subTest(thickness=thickness, flux=flux):
                with self.assertRaises(ValueError):
                    reference.reconstruct(row, thickness, flux)


if __name__ == '__main__':
    unittest.main()
