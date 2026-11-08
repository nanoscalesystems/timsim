"""Fit Tian et al. Figure 3(c) with the existing timsim fitter."""
import json
from pathlib import Path

from timsim.fit import fit_thickness_series

SOURCE = Path(__file__).resolve().parents[1] / "data/experiments/tian2013_fig3c.json"


def main():
    observations = json.loads(SOURCE.read_text(encoding="utf-8"))["observations"]
    fit = fit_thickness_series(
        thickness_m=[row["thickness_um"] * 1e-6 for row in observations],
        resistance_m2k_w=[row["resistance_cm2k_w"] * 1e-4 for row in observations],
    )
    print("Tian Figure 3(c): graphite nanoplatelet TIM; panel formulation unspecified.")
    print("Thickness (µm)   Observed    Fitted    Residual (resistance in mm² K/W)")
    for row, residual in zip(observations, fit.residuals_m2k_w):
        observed = row["resistance_cm2k_w"] * 100
        print(f"{row['thickness_um']:14.2f} {observed:10.2f} "
              f"{observed - residual * 1e6:9.2f} {residual * 1e6:10.2f}")
    print(f"Apparent through-plane conductivity: {fit.conductivity_z_w_mk:.4f} W/(m K)")
    print(f"Combined-contact intercept: {fit.combined_contact_m2k_w * 1e6:.2f} mm² K/W")


if __name__ == "__main__":
    main()
