"""Steady, one-dimensional heat conduction across an installed TIM joint."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class JointResult:
    """Area-specific resistances and the temperature drop across the joint."""

    bulk_m2k_w: float
    contact_1_m2k_w: float
    contact_2_m2k_w: float
    total_m2k_w: float
    delta_t_k: float


def calculate_joint(
    *,
    thickness_m: float,
    conductivity_z_w_mk: float,
    contact_1_m2k_w: float,
    contact_2_m2k_w: float,
    heat_flux_w_m2: float,
) -> JointResult:
    """Calculate the joint resistance and signed temperature drop in SI units."""
    inputs = {
        "thickness_m": thickness_m,
        "conductivity_z_w_mk": conductivity_z_w_mk,
        "contact_1_m2k_w": contact_1_m2k_w,
        "contact_2_m2k_w": contact_2_m2k_w,
        "heat_flux_w_m2": heat_flux_w_m2,
    }
    for name, value in inputs.items():
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")

    if thickness_m < 0:
        raise ValueError("thickness_m must be nonnegative")
    if conductivity_z_w_mk <= 0:
        raise ValueError("conductivity_z_w_mk must be positive")
    if contact_1_m2k_w < 0 or contact_2_m2k_w < 0:
        raise ValueError("contact resistances must be nonnegative")

    bulk = thickness_m / conductivity_z_w_mk
    total = contact_1_m2k_w + bulk + contact_2_m2k_w
    delta_t = heat_flux_w_m2 * total

    if not isfinite(total) or not isfinite(delta_t):
        raise ValueError("inputs exceed the finite range of the calculation")

    return JointResult(
        bulk_m2k_w=bulk,
        contact_1_m2k_w=contact_1_m2k_w,
        contact_2_m2k_w=contact_2_m2k_w,
        total_m2k_w=total,
        delta_t_k=delta_t,
    )
