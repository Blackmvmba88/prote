"""Ideal quasistatic coupling model: excludes friction, inertia and contact."""
from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class StaticResult:
    input_torque_nm: float
    joint_torques_nm: tuple[float, ...]
    joint_displacements_rad: tuple[float, ...]
    input_work_j: float
    output_work_j: float


def evaluate_static_coupling(gains: Sequence[float], joint_torques_nm: Sequence[float],
                             input_displacement_rad: float) -> StaticResult:
    """Virtual work: input torque = sum(gain_i * output torque_i).

    Negative work is possible for loads assisting the input.
    This model does not predict actuator power, efficiency or stability.
    """
    if not gains or len(gains) != len(joint_torques_nm):
        raise ValueError("gains and joint torques must be nonempty and equal length")
    if not all(math.isfinite(v) for v in (*gains, *joint_torques_nm, input_displacement_rad)):
        raise ValueError("all values must be finite")
    torque = sum(g * t for g, t in zip(gains, joint_torques_nm))
    displacements = tuple(g * input_displacement_rad for g in gains)
    output_work = sum(t * d for t, d in zip(joint_torques_nm, displacements))
    return StaticResult(torque, tuple(joint_torques_nm), displacements,
                        torque * input_displacement_rad, output_work)
