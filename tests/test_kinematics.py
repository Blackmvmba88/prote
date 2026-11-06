import math
import unittest
from motionlab.kinematics import forward_kinematics, path_length, two_link_inverse


class TestKinematics(unittest.TestCase):
    def test_straight_chain(self):
        pts = forward_kinematics([1, 2], [0, 0])
        self.assertAlmostEqual(pts[-1][0], 3)
        self.assertAlmostEqual(pts[-1][1], 0)

    def test_relative_angles(self):
        pts = forward_kinematics([1, 1], [math.pi/2, -math.pi/2])
        self.assertAlmostEqual(pts[-1][0], 1)
        self.assertAlmostEqual(pts[-1][1], 1)

    def test_input_validation(self):
        for lengths, angles in [([], []), ([1], []), ([0], [0]), ([float('nan')], [0]), ([1], [float('inf')])]:
            with self.assertRaises(ValueError):
                forward_kinematics(lengths, angles)

    def test_path_length(self):
        self.assertAlmostEqual(path_length([(0, 0), (3, 4), (6, 8)]), 10)

    def test_ik_roundtrip(self):
        for elbow_up in [False, True]:
            angles = two_link_inverse(1, 1, 1, 1, elbow_up)
            endpoint = forward_kinematics([1, 1], angles)[-1]
            self.assertAlmostEqual(endpoint[0], 1)
            self.assertAlmostEqual(endpoint[1], 1)

    def test_unreachable(self):
        with self.assertRaises(ValueError):
            two_link_inverse(1, 1, 5, 0)

    def test_ik_invalid(self):
        with self.assertRaises(ValueError):
            two_link_inverse(0, 1, 1, 0)


if __name__ == '__main__':
    unittest.main()
