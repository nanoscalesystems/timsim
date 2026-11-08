# Tian Figure 3(c)

Tian, Itkis, Bekyarova and Haddon (2013), Scientific Reports 3, 1710.
https://doi.org/10.1038/srep01710

The four black vector squares in Figure 3(c), PDF page 4, provide thickness and through-plane resistance observations. Their centers were extracted from the rectangle bounding boxes in the supplied PDF. The dataset records the PDF hash, coordinates, calibration and converted observations. Thickness uses the printed 100 and 300 µm tick locations; the ordinate uses the 0 and 5 °C·cm²/W ticks. Interpolate linearly between ticks. The plotted red line was excluded. Retained digits support reproduction of the graphic only; instrument precision and replicate uncertainties are unavailable.

The ordinate is already area-specific. Convert µm to m with 1e-6 and °C·cm²/W to m²·K/W with 1e-4. The script calls timsim.fit.fit_thickness_series with equal weight per marker. The reciprocal of the slope gives apparent through-plane conductivity; the intercept estimates the sum of contacts under the series model. Individual contacts were not independently determined.

The thermal methods identify a 30–60 °C test range and copper meter blocks. Matrix identity, loading, applied pressure and point-specific temperature are unresolved for this panel. The pressure used in the electrical experiment cannot be carried over. This series supplies a separate example for fitting. It cannot validate the frozen Sudhindra 10 wt% reference or serve as a named material preset.

Run python scripts/tian_thickness_fit.py and python -m unittest discover -s tests -v from the timsim repo with its virtual environment active.
