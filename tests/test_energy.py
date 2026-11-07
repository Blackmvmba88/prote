import unittest
from motionlab.dynamics import CoupledDynamics
from motionlab.energy import bounded_step, simulate


class EnergyTests(unittest.TestCase):
    def setUp(self):
        self.m = CoupledDynamics((1., 0.5), (2., 4.), (0.2, 0.4), 1.)

    def test_positive_torque_clamp(self):
        s = bounded_step(self.m, 0., 0., 100., 8., (0., 0.), 0.01)
        self.assertEqual(s.applied_torque_nm, 8.)

    def test_negative_torque_clamp(self):
        s = bounded_step(self.m, 0., 0., -100., 8., (0., 0.), 0.01)
        self.assertEqual(s.applied_torque_nm, -8.)

    def test_unclamped_torque(self):
        s = bounded_step(self.m, 0., 0., 3., 8., (0., 0.), 0.01)
        self.assertEqual(s.applied_torque_nm, 3.)

    def test_zero_velocity_no_work(self):
        s = bounded_step(self.m, 0., 0., 0., 8., (0., 0.), 0.01)
        self.assertEqual(s.motor_work_j, 0.)
        self.assertEqual(s.kinetic_energy_j, 0.)

    def test_energy_residual_without_damping(self):
        m = CoupledDynamics((1.,), (2.,), (0.,))
        s = bounded_step(m, 0., 0., 2., 3., (0.,), 0.1)
        self.assertAlmostEqual(s.balance_residual_j, 0., places=12)

    def test_dissipation_nonnegative(self):
        s = bounded_step(self.m, 0., 1., 0., 8., (0., 0.), 0.01)
        self.assertGreaterEqual(s.dissipated_j, 0.)

    def test_constant_load_opposes(self):
        free = bounded_step(self.m, 0., 0., 8., 8., (0., 0.), 0.01)
        loaded = bounded_step(self.m, 0., 0., 8., 8., (2., 4.), 0.01)
        self.assertLess(loaded.velocity_rad_s, free.velocity_rad_s)

    def test_sequence_length(self):
        self.assertEqual(len(simulate(self.m, (1., 2., 3.), 5., (0., 0.), 0.01)), 3)

    def test_invalid_bound(self):
        with self.assertRaises(ValueError):
            bounded_step(self.m, 0., 0., 1., 0., (0., 0.), 0.01)

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            bounded_step(self.m, 0., 0., float('nan'), 8., (0., 0.), 0.01)


if __name__ == '__main__':
    unittest.main()
