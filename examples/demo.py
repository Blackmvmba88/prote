"""Demonstrate a reachable 2-link pose, no external packages required."""
from motionlab import forward_kinematics, two_link_inverse

if __name__ == '__main__':
    angles = two_link_inverse(0.30, 0.25, 0.40, 0.20)
    joints = forward_kinematics([0.30, 0.25], angles)
    print({'angles_rad': [round(x, 5) for x in angles], 'joints_m': joints})
