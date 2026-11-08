# timsim

**How much of the temperature drop across a thermal interface comes from the material itself, and how much comes from its contacts?** `timsim` is an open-source Python library from NanoScale.Systems for answering that question. It models steady heat flow through an installed thermal interface material (TIM), such as the layer between a chip and a heat spreader.

The calculator works with any TIM for which you can supply an effective through-plane conductivity and two surface contact resistances. Graphene-filled silicone oil is the first published material system included with the project.

[Launch the browser simulator](https://nanoscale-systems-webapp.systemsnanoscale.workers.dev/research/timsim/simulator/) Â· [Project overview](https://nanoscale-systems-webapp.systemsnanoscale.workers.dev/research/timsim/)

## What you can calculate

- **Joint resistance and temperature drop.** Supply the installed thickness, through-plane conductivity, contact resistance at each surface, and heat flux. The result gives the bulk and contact contributions separately, along with the total resistance and temperature drop across the joint.
- **Properties from a thickness series.** Fit measured area-specific joint resistance against installed thickness for a single formulation under consistent test conditions. The reciprocal of the fitted slope gives the effective through-plane conductivity. The intercept estimates the two contact resistances combined.

The model assumes steady, one-dimensional heat flow and constant properties at the chosen operating condition:

```text
area-specific joint resistance = contact 1 + thickness / conductivity + contact 2
temperature drop across joint  = heat flux Ã— area-specific joint resistance
```

In the Python API, thickness is in metres, conductivity in W/(mÂ·K), area-specific resistance in mÂ²Â·K/W, and heat flux in W/mÂ². The calculated temperature drop is the difference between the two sides of the TIM joint. Estimating absolute chip temperature also requires the surrounding thermal path and a boundary temperature.

## Install locally

From the repository root, using Python 3.10 or later:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The editable installation lets you run the examples against your local source. The calculator and thickness-series fitter use Pythonâ€™s standard library.

## Quick example

Consider an illustrative 50 Âµm bond line with a through-plane conductivity of 5 W/(mÂ·K). The two contacts contribute 3 and 7 mmÂ²Â·K/W, and the applied heat flux is 10 W/cmÂ².

```python
from timsim import calculate_joint

joint = calculate_joint(
    thickness_m=50e-6,
    conductivity_z_w_mk=5.0,
    contact_1_m2k_w=3e-6,
    contact_2_m2k_w=7e-6,
    heat_flux_w_m2=100_000,
)

print(f"Bulk resistance:  {joint.bulk_m2k_w * 1e6:.1f} mmÂ²Â·K/W")
print(f"Joint resistance: {joint.total_m2k_w * 1e6:.1f} mmÂ²Â·K/W")
print(f"Temperature drop: {joint.delta_t_k:.1f} K")
```

The layer contributes **10.0 mmÂ²Â·K/W** and the two contacts together contribute another **10.0 mmÂ²Â·K/W**. The total is **20.0 mmÂ²Â·K/W**, giving a **2.0 K** drop. In this example, doubling the conductivity halves the layer contribution and reduces the total drop to **1.5 K**.

## Experimental evidence: graphene thermal interfaces

`timsim` includes published data for noncuring graphene and few-layer graphene dispersed in silicone oil. Sudhindra, Kargar and Balandin tested the materials against steel surfaces at approximately 0.55 MPa and a reported test temperature of 80 Â°C. The reconstruction scripts use effective properties measured for those formulations and test conditions.

- [Table S1 reconstruction](docs/graphene-reference.md) uses the authorsâ€™ fitted conductivity and contact resistance for nine filler loadings, including the unfilled silicone-oil reference. The dataset preserves the reported standard errors. Table S1 gives a single-interface contact estimate, so the joint calculation uses twice that value.
- [Figure 3 reproduction](docs/graphene-digitization.md) fits four digitized measurements for the 10 wt% formulation. The fit gives **1.587 W/(mÂ·K)** through-plane conductivity and **10.03 mmÂ²Â·K/W** combined contact resistance. Table S1 gives **1.578 W/(mÂ·K)** and **10.20 mmÂ²Â·K/W**, respectively.

The Figure 3 thickness axis places these four observations at approximately **46â€“112 Âµm**. The paperâ€™s conclusion cites **5â€“35 Âµm**. The reproduction follows the printed axis and documents the discrepancy. Evaluating this formulation at 20 Âµm therefore extrapolates below the four observed thicknesses.

To reproduce the comparisons and run the tests:

```bash
python scripts/graphene_reference.py
python scripts/graphene_digitized_fit.py
python -m unittest discover -s tests -v
```

[Original paper and supplementary information](https://doi.org/10.3390/nano11071699)

## License

[Apache License 2.0](LICENSE)
