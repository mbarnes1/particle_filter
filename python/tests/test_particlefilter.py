__author__ = 'mbarnes1'
import unittest
import sys
sys.path.append('../')
from particlefilter import ParticleFilter


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.particle_filter = ParticleFilter('../../data/map/synthetic_small.dat')

    def test_init(self):
        for particle in self.particle_filter.particles:
            self.assertEqual(self.particle_filter.map.query(particle.x, particle.y), 1.0)
        self.particle_filter.map.display(self.particle_filter.particles)