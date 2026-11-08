# Independent graphene TIM thickness series

## Question and frozen reference
Can a separately prepared 10 wt% batch reproduce the published effective joint resistance under comparable conditions? Use Sudhindra et al., DOI 10.3390/nano11071699, supplementary Table S1. Freeze k = 1.578 W/(m K), combined contacts = 10.20 mm² K/W, before viewing new outcomes. For installed thickness t in µm, predicted area-specific joint resistance in mm² K/W is t/1.578 + 10.20. Score observations at their actual thickness. Preserve the original predictions if a later exploratory fit changes the coefficients.

The Figure 3(b) markers digitized previously place the 10 wt% series at about 46–112 µm using the printed centimetre axis. The conclusion gives 5–35 µm. Record this discrepancy. Target thicknesses 50, 65, 80, 95 and 110 µm stay within the printed marker span.

## Condition record
- Assign a batch and series ID; record whether this is fresh preparation, a remount, or a different laboratory. State any author, thesis, or figure overlap for literature records.
- Record matrix identity, supplier, grade, viscosity and its reference temperature; filler identity, lot, lateral dimensions/thickness or distribution, loading as mass percent of total formulation, dispersion/mixing, solvent removal and storage history. Mark unavailable details explicitly.
- Reference uses steel tester surfaces, approximately 0.55 MPa, reported test temperature 80 °C, and 40 minutes at each thickness. Document steel finish, both surface roughness values and method, cleaning procedure, contact area, actual pressure, hot and cold surface temperatures, steady-state criterion and time. Preserve whether a temperature is hot-side, mean specimen, or a setpoint.
- Record installed thickness under load, its method and uncertainty; nominal shim thickness is a separate entry. Record heat rate and area or heat flux, surface temperature difference, and any fixture correction/calibration. Use area-specific joint resistance. Do not silently include bulk resistance of extra plates or layers.
- Proposed design: five thickness targets and three independent remounts at each. Randomize order, reapply material on remount, and record repeated readings within each mount separately. For a preparation reproducibility claim, repeat across independent batches. Include a matrix-only control if available.
- Before measuring, define equilibrium, instrument uncertainty, exclusion criteria, and a practical error tolerance with the laboratory. No numerical acceptance threshold is prescribed here.

## Analysis order
1. Preserve raw instrument files, correction procedure and mount-level uncertainties. Keep signed residuals as observed minus frozen prediction. Use the script for a preview of the prediction curve only.
2. Report per-thickness mean residual, between-remount scatter and overall signed bias and RMSE. Report batch-specific results if multiple batches are used. Record departures from the target conditions beside the comparison.
3. Fit slope and combined intercept independently afterward using timsim.fit. A constant offset motivates checking contacts and fixture correction; a thickness-dependent residual motivates checking bulk conductivity, thickness calibration or changing contacts. These are diagnostic possibilities, not unique causal assignments.
4. The Table S1 uncertainties are parameter standard errors. A prediction interval requires additional information such as slope/intercept covariance and new measurement uncertainty.

## Literature screen
Tian et al. (2013), DOI 10.1038/srep01710, Figure 3(c) is a candidate separate thickness-series fit. The authors report graphite nanoplatelets, multiple matrices, a LongWin steady-state through-plane tester, copper blocks, and thermal testing over 30–60 °C. The abstract/Methods and Figure 3(e) do not establish the formulation or pressure specific to panel 3(c). Check its legend, axis units and any area normalization before digitization. Keep the electrical-test pressure and temperature separate. Figure 3(c) numeric observations have not been extracted in this package.

Sudhindra's thesis Figure 3.2 identifies reuse of the original series; it is not an independent measurement source. Naghibi et al. (2020), DOI 10.1002/aelm.201901303, uses mineral oil and is a separate formulation comparator.

ASTM D5470 describes the impedance-versus-thickness interpretation: https://store.astm.org/standards/d5470 . Any formal conformity claim requires the laboratory's applicable method, instrumentation and procedures.
