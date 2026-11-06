import math
import unittest
from motionlab.synthesis import Candidate, score, search_couplings


class SynthesisTests(unittest.TestCase):
    def test_pose(self):
        self.assertEqual(Candidate((1., -0.5), (0., 0.2)).pose(2.), (2., -0.8))

    def test_exact_coupling(self):
        commands = (0., 0.5, 1.)
        targets = ((0., 0.), (0.5, -0.25), (1., -0.5))
        candidate, error = search_couplings(commands, targets)
        self.assertEqual(candidate.gains, (1., -0.5))
        self.assertAlmostEqual(error, 0.)

    def test_nonzero_error(self):
        self.assertAlmostEqual(score(Candidate((0.,), (0.,)), (0., 1.), ((0.,), (1.,))), math.sqrt(0.5))

    def test_search_budget(self):
        with self.assertRaises(ValueError):
            search_couplings((0.,), ((0.,) * 5,), limit=100)

    def test_bad_dimensions(self):
        with self.assertRaises(ValueError):
            score(Candidate((1.,), (0.,)), (0.,), ((0., 0.),))

    def test_bad_data(self):
        with self.assertRaises(ValueError):
            search_couplings((float('nan'),), ((0.,),))

    def test_bad_command(self):
        with self.assertRaises(ValueError):
            Candidate((1.,), (0.,)).pose(float('inf'))

    def test_empty(self):
        with self.assertRaises(ValueError):
            search_couplings((), ())


if __name__ == '__main__':
    unittest.main()
