import unittest
from motionlab.mechanics import evaluate_static_coupling


class StaticCouplingTests(unittest.TestCase):
    def test_torque_and_work(self):
        result = evaluate_static_coupling((1., 0.5), (2., 4.), 0.2)
        self.assertAlmostEqual(result.input_torque_nm, 4.)
        self.assertAlmostEqual(result.input_work_j, 0.8)
        self.assertAlmostEqual(result.output_work_j, 0.8)

    def test_opposing_torques(self):
        result = evaluate_static_coupling((1., -1.), (3., 3.), 0.5)
        self.assertAlmostEqual(result.input_torque_nm, 0.)
        self.assertAlmostEqual(result.output_work_j, 0.)

    def test_assisting_load(self):
        result = evaluate_static_coupling((1.,), (-2.,), 0.5)
        self.assertLess(result.input_work_j, 0.)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            evaluate_static_coupling((1.,), (2., 3.), 0.2)

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            evaluate_static_coupling((1.,), (float('nan'),), 0.2)

    def test_empty(self):
        with self.assertRaises(ValueError):
            evaluate_static_coupling((), (), 0.2)


if __name__ == '__main__':
    unittest.main()
