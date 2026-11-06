"""Bounded actuator and energy bookkeeping for the idealized coupled model.

The model uses a single input coordinate, fixed transmission gains, constant
inertia and viscous damping. It is not a motor, hydraulic or prosthetic model.
"""
from dataclasses import dataclass
import math
from .dynamics import CoupledDynamics


@dataclass(frozen=True)
class EnergySample:
    position_rad: float
    velocity_rad_s: float
    applied_torque_nm: float
    motor_work_j: float
    load_work_j: float
    dissipated_j: float
    kinetic_energy_j: float
    balance_residual_j: float


def bounded_step(model: CoupledDynamics, position_rad: float, velocity_rad_s: float,
                 requested_torque_nm: float, max_torque_nm: float,
                 load_torques_nm: tuple[float, ...], dt_s: float) -> EnergySample:
    """One midpoint-work energy-accounted semi-implicit Euler step.

    Work terms use midpoint velocity and are signed except dissipation.
    Residual captures numerical integration error, not hidden physical loss.
    """
    if not all(math.isfinite(x) for x in (position_rad, velocity_rad_s, requested_torque_nm,
                                          max_torque_nm, dt_s)):
        raise ValueError("inputs must be finite")
    if max_torque_nm <= 0 or dt_s <= 0:
        raise ValueError("torque bound and time step must be positive")
    applied = max(-max_torque_nm, min(max_torque_nm, requested_torque_nm))
    q, v = model.step(position_rad, velocity_rad_s, applied, load_torques_nm, dt_s)
    mean_v = (velocity_rad_s + v) / 2
    displacement = mean_v * dt_s
    load_torque = sum(g * t for g, t in zip(model.gains, load_torques_nm))
    motor_work = applied * displacement
    load_work = load_torque * displacement
    dissipation = model.reflected_damping * mean_v * mean_v * dt_s
    kinetic_start = 0.5 * model.reflected_inertia * velocity_rad_s**2
    kinetic_end = 0.5 * model.reflected_inertia * v**2
    residual = motor_work - load_work - dissipation - (kinetic_end - kinetic_start)
    return EnergySample(q, v, applied, motor_work, load_work, dissipation,
                        kinetic_end, residual)


def simulate(model: CoupledDynamics, commands_nm: tuple[float, ...], max_torque_nm: float,
             loads_nm: tuple[float, ...], dt_s: float) -> tuple[EnergySample, ...]:
    """Simulate a prescribed command sequence with constant joint loads."""
    q = v = 0.0
    samples = []
    for command in commands_nm:
        sample = bounded_step(model, q, v, command, max_torque_nm, loads_nm, dt_s)
        samples.append(sample)
        q, v = sample.position_rad, sample.velocity_rad_s
    return tuple(samples)
