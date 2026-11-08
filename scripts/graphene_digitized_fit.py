"""Reproduce the 10 wt% Figure 3(b) fit and compare it with Table S1."""
import json
from itertools import product
from pathlib import Path

from timsim.fit import fit_thickness_series

DATA = Path(__file__).resolve().parents[1] / "data/experiments"


def axis_value(pixel, ticks, values):
    fraction = (pixel - ticks[0]) / (ticks[1] - ticks[0])
    return values[0] + fraction * (values[1] - values[0])


def coordinates(data, centers):
    thickness = [axis_value(x, data["x_ticks_px"], data["x_ticks_cm"]) * 0.01
                 for x, _ in centers]
    resistance = [axis_value(y, data["y_ticks_px"], data["y_ticks_cm2k_w"]) * 1e-4
                  for _, y in centers]
    return thickness, resistance


def fit(data, centers):
    thickness, resistance = coordinates(data, centers)
    return fit_thickness_series(thickness_m=thickness, resistance_m2k_w=resistance)


def sensitivity(data):
    centers = data["marker_centers_px"]
    delta = data["sensitivity_offset_px"]
    for offsets in product((-delta, delta), repeat=2 * len(centers)):
        shifted = [(x + offsets[2*i], y + offsets[2*i+1]) for i, (x, y) in enumerate(centers)]
        yield fit(data, shifted)


def main():
    data = json.loads((DATA / "sudhindra2021_fig3b_10wt.json").read_text())
    s1 = json.loads((DATA / "sudhindra2021_table_s1.json").read_text())
    row = next(row for row in s1["rows"] if row["loading_wt_pct"] == data["loading_wt_pct"])
    centers = data["marker_centers_px"]
    thickness, resistance = coordinates(data, centers)
    result = fit(data, centers)
    print("10 wt% graphene; Figure 3(b), printed cm axis")
    print("Thickness (um)   Observed   Fitted   Residual (all resistances in mm2 K/W)")
    for x, y, residual in zip(thickness, resistance, result.residuals_m2k_w):
        print(f"{x*1e6:14.3f} {y*1e6:10.3f} {(y-residual)*1e6:8.3f} {residual*1e6:10.3f}")
    print(f"Conductivity: {result.conductivity_z_w_mk:.6f} vs S1 {row['conductivity_w_mk']:.3f} W/(m K)")
    print(f"Combined contacts: {result.combined_contact_m2k_w*1e6:.6f} vs S1 {200*row['rc_cm2k_w']:.3f} mm2 K/W")
    trials = list(sensitivity(data))
    ks = [r.conductivity_z_w_mk for r in trials]
    contacts = [r.combined_contact_m2k_w*1e6 for r in trials]
    print(f"Marker sensitivity (+/-2 px, axes fixed): k {min(ks):.4f} to {max(ks):.4f}; combined contacts {min(contacts):.4f} to {max(contacts):.4f}")


if __name__ == "__main__":
    main()
