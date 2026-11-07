"""Example of shared-actuator angular coupling search."""
from motionlab.synthesis import search_couplings

if __name__ == '__main__':
    commands = (0., 0.25, 0.5, 0.75, 1.)
    targets = tuple((u, -0.5*u, 0.5*u) for u in commands)
    best, rmse = search_couplings(commands, targets)
    print({'gains': best.gains, 'offsets': best.offsets, 'rmse_rad': rmse})
