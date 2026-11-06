import unittest
from motionlab.dynamics import CoupledDynamics

class DynamicsTests(unittest.TestCase):
    def setUp(self):
        self.m = CoupledDynamics((1.,0.5),(2.,4.),(0.2,0.4),1.)
    def test_reflected_inertia(self):
        self.assertAlmostEqual(self.m.reflected_inertia,4.)
    def test_reflected_damping(self):
        self.assertAlmostEqual(self.m.reflected_damping,0.3)
    def test_acceleration(self):
        self.assertAlmostEqual(self.m.acceleration(0.,8.,(2.,4.)),1.)
    def test_damping(self):
        self.assertAlmostEqual(self.m.acceleration(2.,0.,(0.,0.)),-0.15)
    def test_step(self):
        q,v=self.m.step(0.,0.,8.,(2.,4.),0.1)
        self.assertAlmostEqual(v,0.1)
        self.assertAlmostEqual(q,0.01)
    def test_zero_inertia(self):
        with self.assertRaises(ValueError): CoupledDynamics((1.,),(0.,),(0.,))
    def test_negative_inertia(self):
        with self.assertRaises(ValueError): CoupledDynamics((1.,),(-1.,),(0.,))
    def test_bad_loads(self):
        with self.assertRaises(ValueError): self.m.acceleration(0.,1.,(0.,))
    def test_bad_step(self):
        with self.assertRaises(ValueError): self.m.step(0.,0.,1.,(0.,0.),0.)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): self.m.acceleration(float('nan'),1.,(0.,0.))

if __name__=='__main__': unittest.main()
