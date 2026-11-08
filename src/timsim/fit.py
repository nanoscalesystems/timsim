"""Fit area-specific joint resistance against installed TIM thickness."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import fsum, isfinite


@dataclass(frozen=True)
class ThicknessFit:
    conductivity_z_w_mk: float
    combined_contact_m2k_w: float
    residuals_m2k_w: tuple[float, ...]


def fit_thickness_series(
    *,
    thickness_m: Sequence[float],
    resistance_m2k_w: Sequence[float],
) -> ThicknessFit:
    """Fit R = thickness / conductivity + combined contact resistance.

    Uses ordinary least squares with equal weight for each observation.
    Residuals are observed minus fitted resistance, in input order.
    """
    if len(thickness_m) != len(resistance_m2k_w):
        raise ValueError("each thickness needs one resistance measurement")
    if len(thickness_m) < 2:
        raise ValueError("at least two measurements are required")

    for value in thickness_m:
        if not isfinite(value) or value < 0:
            raise ValueError("thickness must be finite and nonnegative")
    for value in resistance_m2k_w:
        if not isfinite(value) or value < 0:
            raise ValueError("resistance must be finite and nonnegative")

    if min(thickness_m) == max(thickness_m):
        raise ValueError("at least two distinct thicknesses are required")

    count = len(thickness_m)
    mean_t = fsum(thickness_m) / count
    mean_r = fsum(resistance_m2k_w) / count

    offsets_t = [t - mean_t for t in thickness_m]
    offsets_r = [r - mean_r for r in resistance_m2k_w]
    slope = (
        fsum(dt * dr for dt, dr in zip(offsets_t, offsets_r))
        / fsum(dt * dt for dt in offsets_t)
    )
    if slope <= 0:
        raise ValueError("the fitted slope must be positive to infer conductivity")

    intercept = mean_r - slope * mean_t
    residuals = tuple(
        dr - slope * dt for dt, dr in zip(offsets_t, offsets_r)
    )
    return ThicknessFit(
        conductivity_z_w_mk=1.0 / slope,
        combined_contact_m2k_w=intercept,
        residuals_m2k_w=residuals,
    )
