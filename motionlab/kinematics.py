"""Simple, dependency-free planar linkage kinematics.

Angles are in radians, link lengths in meters. No dynamics or torque model.
"""
from __future__ import annotations
import math
from typing import Sequence


def forward_kinematics(lengths: Sequence[float], angles: Sequence[float]) -> list[tuple[float, float]]:
    """Return joint endpoints for a serial planar chain with relative joint angles."""
    if not lengths or len(lengths) != len(angles):
        raise ValueError("provide equal nonempty sequences of lengths and angles")
    if any(not math.isfinite(v) or v <= 0 for v in lengths):
        raise ValueError("all link lengths must be positive and finite")
    if any(not math.isfinite(v) for v in angles):
        raise ValueError("angles must be finite")
    x = y = theta = 0.0
    points = [(x, y)]
    for length, angle in zip(lengths, angles):
        theta += angle
        x += length * math.cos(theta)
        y += length * math.sin(theta)
        points.append((x, y))
    return points


def path_length(points: Sequence[tuple[float, float]]) -> float:
    """Return total Euclidean distance along the given points."""
    if len(points) < 2:
        return 0.0
    if any(not all(math.isfinite(v) for v in point) for point in points):
        raise ValueError("points must be finite")
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def two_link_inverse(a: float, b: float, x: float, y: float, elbow_up: bool = False) -> tuple[float, float]:
    """Solve two-link planar inverse kinematics for a reachable target."""
    if not all(math.isfinite(v) for v in (a, b, x, y)) or a <= 0 or b <= 0:
        raise ValueError("link lengths must be positive and all values finite")
    c = (x*x + y*y - a*a - b*b) / (2*a*b)
    if c < -1 - 1e-12 or c > 1 + 1e-12:
        raise ValueError("target is outside the reachable workspace")
    c = max(-1.0, min(1.0, c))
    elbow = math.acos(c) * (-1 if elbow_up else 1)
    shoulder = math.atan2(y, x) - math.atan2(b*math.sin(elbow), a+b*math.cos(elbow))
    return shoulder, elbow
