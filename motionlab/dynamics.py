"""Single-DOF reflected inertia model for fixed-ratio transmissions."""
from dataclasses import dataclass
import math


def _finite(values):
    return all(math.isfinite(v) for v in values)


@dataclass(frozen=True)
class CoupledDynamics:
    gains: tuple[float, ...]
    inertias_kg_m2: tuple[float, ...]
    viscous_nms_rad: tuple[float, ...]
    actuator_inertia_kg_m2: float = 0.0

    def __post_init__(self):
        n = len(self.gains)
        vals = (*self.gains, *self.inertias_kg_m2, *self.viscous_nms_rad, self.actuator_inertia_kg_m2)
        if n == 0 or len(self.inertias_kg_m2) != n or len(self.viscous_nms_rad) != n:
            raise ValueError('joint arrays must have equal nonzero length')
        if not _finite(vals) or any(v < 0 for v in (*self.inertias_kg_m2, *self.viscous_nms_rad, self.actuator_inertia_kg_m2)):
            raise ValueError('inertia and damping must be nonnegative finite values')
        if self.reflected_inertia <= 0:
            raise ValueError('effective inertia must be positive')

    @property
    def reflected_inertia(self):
        return self.actuator_inertia_kg_m2 + sum(i*g*g for i,g in zip(self.inertias_kg_m2,self.gains))

    @property
    def reflected_damping(self):
        return sum(b*g*g for b,g in zip(self.viscous_nms_rad,self.gains))

    def acceleration(self, velocity_rad_s: float, motor_torque_nm: float, load_torques_nm: tuple[float, ...]):
        if len(load_torques_nm) != len(self.gains) or not _finite((velocity_rad_s,motor_torque_nm,*load_torques_nm)):
            raise ValueError('invalid load, velocity or torque')
        opposing = sum(g*t for g,t in zip(self.gains,load_torques_nm))
        return (motor_torque_nm - opposing - self.reflected_damping*velocity_rad_s)/self.reflected_inertia

    def step(self, position_rad: float, velocity_rad_s: float, motor_torque_nm: float,
             load_torques_nm: tuple[float, ...], dt_s: float):
        """Semi-implicit Euler; not a safety-critical controller."""
        if not _finite((position_rad,dt_s)) or dt_s <= 0:
            raise ValueError('dt must be positive and finite; position must be finite')
        a = self.acceleration(velocity_rad_s,motor_torque_nm,load_torques_nm)
        v = velocity_rad_s + dt_s*a
        q = position_rad + dt_s*v
        if not _finite((q,v)):
            raise ValueError('integration overflow')
        return q,v
