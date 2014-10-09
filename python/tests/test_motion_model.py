import unittest
import sys
import numpy as np
sys.path.append('../')
from particlefilter import Particle
import matplotlib.pyplot as plt
from map import Map
import math
from motion_model import MotionModel
__author__ = 'mbarnes1'


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.map = Map('../../data/map/synthetic_small.dat')
        self.map.sample_seed(100)
        self.particles = list()
        for _ in range(0, 100):
            particle = Particle(self.map)
            particle.x = 0
            particle.y = 40
            particle.theta = 0
            particle.odometry = [0, 0, 0]
            self.particles.append(particle)
        self.particle = particle

    def test_straight_right(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        for _ in range(0, 100):
            odometry[0] += 1
            motion_model.update(self.particle, odometry, 0)
        self.assertEqual(self.particle.x, 100)
        self.assertEqual(self.particle.y, 40)
        self.assertEqual(self.particle.theta, 0)

    def test_straight_up(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        self.particle.x = 40
        self.particle.y = 0
        self.particle.theta = math.pi/2
        for _ in range(0, 100):
            odometry[0] += 1
            motion_model.update(self.particle, odometry, 0)
        self.assertEqual(self.particle.x, 40)
        self.assertEqual(self.particle.y, 100)
        self.assertEqual(self.particle.theta, math.pi/2)

    def test_sidestep_right(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        self.particle.x = 0
        self.particle.y = 40
        self.particle.theta = math.pi/2
        for _ in range(0, 100):
            odometry[1] -= 1
            motion_model.update(self.particle, odometry, 0)
        self.assertEqual(self.particle.x, 100)
        self.assertEqual(self.particle.y, 40)
        self.assertEqual(self.particle.theta, math.pi/2)

    def test_turn_left(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        self.particle.x = 0
        self.particle.y = 40
        self.particle.theta = 0
        for _ in range(0, 10):
            odometry[2] += math.pi/20
            motion_model.update(self.particle, odometry, 0)
        self.assertEqual(self.particle.x, 0)
        self.assertEqual(self.particle.y, 40)
        self.assertEqual(self.particle.theta, math.pi/2)

    def test_turn_right(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        self.particle.x = 0
        self.particle.y = 40
        self.particle.theta = 0
        for _ in range(0, 10):
            odometry[2] -= math.pi/20
            motion_model.update(self.particle, odometry, 0)
        self.assertEqual(self.particle.x, 0)
        self.assertEqual(self.particle.y, 40)
        self.assertEqual(self.particle.theta, -math.pi/2)

    def test_forward_back(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        self.particle.x = 0
        self.particle.y = 40
        self.particle.theta = 0
        for _ in range(0, 10):
            odometry[0] += 1
            motion_model.update(self.particle, odometry, 0)
        for _ in range(0, 10):
            odometry[2] += math.pi/10
            motion_model.update(self.particle, odometry, 0)
        for _ in range(0, 10):
            odometry[0] += 1
            motion_model.update(self.particle, odometry, 0)
        self.assertEqual(self.particle.x, 0)
        self.assertEqual(self.particle.y, 40)
        self.assertEqual(self.particle.theta, math.pi)

    def test_circle(self):
        motion_model = MotionModel(0, 0, 0, 0)
        odometry = [0, 0, 0]
        self.particle.x = 0
        self.particle.y = 40
        self.particle.theta = math.pi/2
        for _ in range(0, 4):
            odometry[0] += 10*math.sqrt(2)/2
            odometry[1] -= 10*(1-math.sqrt(2)/2)
            odometry[2] -= math.pi/4
            motion_model.update(self.particle, odometry, 0)
            #self.map.display([self.particle], title='Zero Variance Upper Circle')
        self.assertAlmostEqual(self.particle.x, 20)
        self.assertEqual(self.particle.y, 40)
        self.assertEqual(self.particle.theta, -math.pi/2)

    def test_distribution_line(self):
        motion_model = MotionModel(0.1, 0.1, 0.1, 0.1)
        odometry = [0, 0, 0]
        p, = plt.plot([], [], 'r.')
        for _ in range(0, 3):
            odometry[0] += 1
            x = list()
            y = list()
            for particle in self.particles:
                motion_model.update(particle, odometry, 0)
                x.append(particle.x)
                y.append(particle.y)
            self.map.display(self.particles, title='Line w/ motion model')

    def test_distribution_circle(self):
        motion_model = MotionModel(0.01, 0.01, 0.01, 0.01)
        odometry = [0, 0, 0]
        for particle in self.particles:
            particle.x = 0
            particle.y = 40
            particle.theta = math.pi/2
        for _ in range(0, 4):
            odometry[0] += 10*math.sqrt(2)/2
            odometry[1] -= 10*(1-math.sqrt(2)/2)
            odometry[2] -= math.pi/4
            for particle in self.particles:
                motion_model.update(particle, odometry, 0)
            self.map.display(self.particles, title='Upper Circle w/ Motion Model')
