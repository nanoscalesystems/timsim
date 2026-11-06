# Graphene reference, step 1

Sudhindra, S., Kargar, F., and Balandin, A. A. (2021), Noncured Graphene Thermal Interface Materials for High-Power Electronics: Minimizing the Thermal Contact Resistance. Nanomaterials 11(7), 1699. https://doi.org/10.3390/nano11071699

## Evidence and scope

The JSON transcribes all nine rows and both standard-error columns from supplementary Table S1, page 2. The table reports properties extracted by the authors' linear regressions. The script reconstructs joint resistance from those properties using the existing timsim.calculate_joint API. It performs no new regression on experimental observations. The original point coordinates, replicate measurements, and parameter covariance have not been supplied in Table S1. Figure 3 digitization or author-provided raw data remains the next step.

The material is noncuring silicone oil (PDMS) with graphene/few-layer-graphene filler. Loading is mass percent. The reported test conditions are 0.55 MPa (approximately 80 psi), 80 C, and 40 minutes per thickness. The paper identifies steel tester surfaces for the Figure 3 series and states the heat-source temperature was held constant. The reported 80 C must not be interpreted as a uniform temperature throughout the specimen.

## Contact convention and units

The main paper's Equation 2 and discussion of Figure 5 define the Figure 3 intercept as 2 RC. Figure 5 plots RC after division by two. Its numerical points agree with the Table S1 contact column. Consequently the imported table value is treated as a single-interface estimate. The SI prose refers generally to extracting contact resistance from intercepts, so this interpretation relies on cross-checking the main paper as well as Table S1.

- 1 cm² K/W = 100 mm² K/W = 0.0001 m² K/W.
- 1 W/cm² = 10,000 W/m².
- In display units, R_joint [mm² K/W] = thickness [um] / k [W/(m K)] + 200 RC [cm² K/W].
- The two contacts use the paper's equal-contact representation. Individual top and bottom values were not independently measured.

At 15 wt%, RC = 0.011 cm² K/W gives 1.1 mm² K/W per interface, or 2.2 mm² K/W combined. The published standard error is 0.040 cm² K/W per-interface estimate. The combined-contact standard error is therefore 8.0 mm² K/W, since the sum is twice the same inferred parameter. Independent-error root-sum-square treatment would be inappropriate.

All standard errors are retained as reported. Large standard errors, including values exceeding central contact estimates, must be shown when presenting the evidence. A negative lower error-bar endpoint expresses regression uncertainty and must not be presented as a physically negative contact resistance. The script displays central estimates and does not claim a statistically established best loading. Raw data and slope/intercept covariance would be needed for a defensible joint uncertainty analysis.

## Illustrative evaluation

The default script evaluates 20 um and 10 W/cm² across all tabulated loadings. These are illustrative evaluation inputs. Each formulation's actual measured thickness range remains to be extracted from Figure 3. At 20 um, the 15 wt% central estimate gives 13.642 mm² K/W total and 1.364 K across the joint. At 40 wt%, the higher conductivity lowers bulk resistance, while the larger contact term yields 51.538 mm² K/W total and 5.154 K. These are reconstructions from published fit parameters under the model assumptions, and must be labeled that way in the website.

The current model contains no phase-change or graphene effective-medium physics. It takes experimental effective conductivity and contacts as inputs. Do not reinterpret this oil-based dataset as a PCM formulation. Do not interpolate loading or extrapolate pressure, temperature, or surface finish automatically.

## Table S2

The copper-plate roughness series is a different fixture. Table S2 labels its response RC,tot + Roil. The main paper's Equation 4 includes contacts between steel, oil, copper and TIM, plus layer resistances. The Table S2 values cannot be inserted as either single TIM contact without separating those contributions. It is intentionally deferred to a fixture-aware model.

## Applying the files

Copy the archive contents into ~/work/timsim, activate its virtual environment, and run:

```bash
python scripts/graphene_reference.py
python -m unittest discover -s tests -v
```

Five additional tests cover source transcription, contact convention, unit conversions, preservation of large standard errors, and invalid evaluation inputs. The full suite should contain fourteen tests if the original nine remain present.

No wheel rebuild is needed for this data/script step. To change the evaluation inputs:

```bash
python scripts/graphene_reference.py --thickness-um 30 --heat-flux-w-cm2 10
```

Before website integration, review this transcription locally and reproduce at least one measured thickness series. Future UI should distinguish published fitted parameters, digitized observations, and model-generated curves.
