__author__ = 'mbarnes1'
import unittest
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
sys.path.append('../')
from map import Map
from particlefilter import Particle

map = Map('../../data/map/synthetic_small.dat')
map.sample_seed(1000)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print 'Setting up'

    def test_query(self):
        self.assertEqual(map.query(0, 0), 1)
        self.assertEqual(map.query(0, 40), 1)
        self.assertEqual(map.query(0, 90), 0)
        self.assertEqual(map.query(50, 0), 0)
        self.assertEqual(map.query(50, 50), 1)
        self.assertEqual(map.query(50, 90), 0)
        self.assertEqual(map.query(90, 0), 0)
        self.assertEqual(map.query(90, 50), 1)
        self.assertEqual(map.query(90, 90), 0)

    def test_display(self):
        particles = []
        for _ in range(0, 5):
            particle = Particle(map)
            particle.x = 0
            particle.y = _*10
            particles.append(particle)
        for _ in range(0, 10):
            particle = Particle(map)
            particle.x = _*10
            particle.y = 50
            particles.append(particle)
        map.display(particles, title='Particles Manually Set in White Space')

    def test_gaussian(self):
        plt.imshow(map._gaussian_occupancy_grid, cmap=cm.Greys_r)
        plt.axis([0, map._gaussian_occupancy_grid.shape[0], 0, map._gaussian_occupancy_grid.shape[1]])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Gaussian Blurred Image')
        plt.show()

    def test_sample(self):
        for _ in range(0, 100):
            x, y = map.sample()
            p = map.query(x, y)
            self.assertTrue(p > 0.0)

