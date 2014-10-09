__author__ = 'mbarnes1'
import sys
sys.path.append('../')
from sensor_model import SensorModel, _laser_state
from map import Map
from particlefilter import Particle
import unittest
import math

map = Map('../../data/map/synthetic_wall.txt')
map.sample_seed(1000)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sensor_model = SensorModel(map)
        self.particle = Particle(map)
        self.particle.x = 250
        self.particle.y = 250
        self.particle.theta = 0

    def test_plot(self):
        self.sensor_model.plot_model()

    def test_laser_state(self):
        (x, y, theta) = _laser_state(self.particle)
        self.assertEqual(x, 275)
        self.assertEqual(y, 250)
        self.assertEqual(theta, 0)
        self.particle.theta = -math.pi/2
        (x, y, theta) = _laser_state(self.particle)
        self.assertEqual(x, 250)
        self.assertEqual(y, 225)
        self.assertEqual(theta, -math.pi/2)

    def test_ray_cast(self):
        laser_state = _laser_state(self.particle)
        right = self.sensor_model._ray_cast(laser_state, -math.pi/2)
        self.assertAlmostEqual(right, 250, places=0)  # should hit edge of map
        straight = self.sensor_model._ray_cast(laser_state, 0)
        self.assertAlmostEqual(straight, 225, places=0)  # should hit wall in front, minus 25 for laser offset
        left = self.sensor_model._ray_cast(laser_state, math.pi/2)
        self.assertAlmostEqual(left, 750, places=0)  # should hit edge of map on left
        left_diagonal = self.sensor_model._ray_cast(laser_state, math.pi/4)
        self.assertAlmostEqual(left_diagonal, 225/math.cos(math.pi/4), places=0)  # should hit wall off to left

    def test__get_probability(self):
        log_probabilities = []
        particle = Particle(map)
        particle.x = 250
        particle.y = 500
        particle.theta = 0
        for _ in range(0, 10):
            x = 200 + 10*_
            ranges = []
            for i in range(-90, 91):
                side = abs(500.0/(math.sin(i*math.pi/180)+0.000001))
                wall = abs((500.0-x-25)/(math.cos(i*math.pi/180)+0.0000001))
                ranges.append(min(side, wall))
            log_probabilities.append(self.sensor_model.get_probability(particle, ranges))
        most_likely_reading = max(enumerate(log_probabilities), key=lambda x: x[1])[0]
        self.assertEqual(most_likely_reading, 5)



