"""Deterministic, kinematic-only exploration of coupled joint mechanisms."""
from dataclasses import dataclass
import itertools
import math


@dataclass(frozen=True)
class Candidate:
    """Joint angle = gain * shared actuator command + offset (radians)."""
    gains: tuple[float, ...]
    offsets: tuple[float, ...]

    def pose(self, command: float) -> tuple[float, ...]:
        if not math.isfinite(command):
            raise ValueError("command must be finite")
        return tuple(g * command + o for g, o in zip(self.gains, self.offsets))


def score(candidate: Candidate, commands: tuple[float, ...], targets: tuple[tuple[float, ...], ...]) -> float:
    """Root mean square angular tracking error, in radians."""
    if not commands or len(commands) != len(targets):
        raise ValueError("commands and targets must have matching nonzero lengths")
    n = len(candidate.gains)
    if n == 0 or len(candidate.offsets) != n or any(len(t) != n for t in targets):
        raise ValueError("joint dimensions do not match")
    values = (*candidate.gains, *candidate.offsets, *commands, *(v for t in targets for v in t))
    if any(not math.isfinite(v) for v in values):
        raise ValueError("all inputs must be finite")
    errors = [(p - t)**2 for u, target in zip(commands, targets) for p, t in zip(candidate.pose(u), target)]
    return math.sqrt(sum(errors) / len(errors))


def search_couplings(commands: tuple[float, ...], targets: tuple[tuple[float, ...], ...],
                     gain_options: tuple[float, ...] = (-1., -0.5, 0., 0.5, 1.),
                     offset_options: tuple[float, ...] = (0.,), limit: int = 100_000
                     ) -> tuple[Candidate, float]:
    """Exhaustive search for shared-input fixed-ratio couplings."""
    if not targets or not targets[0]:
        raise ValueError("targets must contain joints")
    n = len(targets[0])
    if not gain_options or not offset_options or limit < 1:
        raise ValueError("invalid search options")
    if any(not math.isfinite(v) for v in (*gain_options, *offset_options)):
        raise ValueError("search options must be finite")
    if (len(gain_options) * len(offset_options)) ** n > limit:
        raise ValueError("search space exceeds limit")
    best = None
    best_error = math.inf
    for pairs in itertools.product(itertools.product(gain_options, offset_options), repeat=n):
        gains, offsets = zip(*pairs)
        candidate = Candidate(tuple(gains), tuple(offsets))
        error = score(candidate, commands, targets)
        if error < best_error:
            best, best_error = candidate, error
    return best, best_error
