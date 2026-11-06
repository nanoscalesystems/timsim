"""Reconstruct joint resistances from published Table S1 regression estimates."""
import argparse
import json
import math
from pathlib import Path

from timsim import calculate_joint

DATA_PATH = Path(__file__).resolve().parents[1] / 'data/experiments/sudhindra2021_table_s1.json'


def reconstruct(row, thickness_um, heat_flux_w_cm2):
    """Use the table's single-interface RC for both sides of the joint."""
    for name, value in [('thickness_um', thickness_um), ('heat_flux_w_cm2', heat_flux_w_cm2)]:
        if not math.isfinite(value):
            raise ValueError(f'{name} must be finite')
    if thickness_um < 0:
        raise ValueError('thickness_um must be nonnegative')
    # 1 cm² K/W = 1e-4 m² K/W; 1 W/cm² = 1e4 W/m².
    return calculate_joint(
        thickness_m=thickness_um * 1e-6,
        conductivity_z_w_mk=row['conductivity_w_mk'],
        contact_1_m2k_w=row['rc_cm2k_w'] * 1e-4,
        contact_2_m2k_w=row['rc_cm2k_w'] * 1e-4,
        heat_flux_w_m2=heat_flux_w_cm2 * 1e4,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--thickness-um', type=float, default=20.0)
    parser.add_argument('--heat-flux-w-cm2', type=float, default=10.0)
    args = parser.parse_args()
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    print('Table S1 published fit reconstruction; raw-data refitting pending.')
    print('Reference conditions: reported 80 C, 0.55 MPa, steel contact surfaces.')
    print(f'Illustrative evaluation: {args.thickness_um:g} um; {args.heat_flux_w_cm2:g} W/cm2.')
    print('Individual measured thickness ranges remain to be extracted from Figure 3.')
    print('wt%      k       bulk     contacts      total      drop')
    print('       W/mK       ------- mm2 K/W -------           K')
    for row in data['rows']:
        try:
            result = reconstruct(row, args.thickness_um, args.heat_flux_w_cm2)
        except ValueError as error:
            parser.error(str(error))
        print(f"{row['loading_wt_pct']:3g}  {row['conductivity_w_mk']:7.3f}"
              f'  {result.bulk_m2k_w * 1e6:9.3f}'
              f'  {(result.contact_1_m2k_w + result.contact_2_m2k_w) * 1e6:9.3f}'
              f'  {result.total_m2k_w * 1e6:9.3f}  {result.delta_t_k:8.3f}')
    print('Source standard errors are retained in the JSON. This table uses central estimates.')
    print('No ranking uncertainty is inferred; fitted-parameter covariance is unavailable.')


if __name__ == '__main__':
    main()
