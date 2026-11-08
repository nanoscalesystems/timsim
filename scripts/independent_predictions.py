"""Print frozen Table S1 predictions for proposed thickness targets."""
from pathlib import Path
import json
from math import isclose

from timsim import calculate_joint

data_path = Path(__file__).resolve().parents[1] / "data/experiments/sudhindra2021_table_s1.json"


def main():
    data = json.loads(data_path.read_text(encoding="utf-8"))
    row = next(row for row in data["rows"] if row["loading_wt_pct"] == 10)
    k, rc = row["conductivity_w_mk"], row["rc_cm2k_w"]
    if (k, rc) != (1.578, 0.051):
        raise ValueError("Local Table S1 differs from the frozen study reference.")
    print("Predictions only | 10 wt% | installed thickness target (µm) | joint (mm² K/W)")
    for thickness_um in (50, 65, 80, 95, 110):
        joint = calculate_joint(thickness_m=thickness_um * 1e-6,
                                conductivity_z_w_mk=k,
                                contact_1_m2k_w=rc * 1e-4,
                                contact_2_m2k_w=rc * 1e-4,
                                heat_flux_w_m2=100_000)
        resistance = joint.total_m2k_w * 1e6
        assert isclose(resistance, thickness_um / k + 200 * rc)
        print(f"{thickness_um:3}  {resistance:.3f}")


if __name__ == "__main__":
    main()
