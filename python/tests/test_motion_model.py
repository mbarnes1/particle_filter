import unittest
import sys
import numpy as np
sys.path.append('../')
from particlefilter import Particle
import matplotlib.pyplot as plt
from map import Map
from motion_model import MotionModel
__author__ = 'mbarnes1'


class MyTestCase(unittest.TestCase):
    def setUp(self):
        map = Map('../../data/map/wean.dat')
        self.particles = list()
        for _ in range(0, 100):
            particle = Particle(map)
            particle.x = 0
            particle.y = 0
            particle.theta = 0
            particle.odometry = [0, 0, 0]
            self.particles.append(particle)
        self.particle = particle

    def test_distribution(self):
        motion_model = MotionModel(1, 1, 1, 1)
        odometry = [0, 0, 0]
        p, = plt.plot([], [], 'r.')
        for _ in range(0, 100):
            odometry[0] += 0.05
            x = list()
            y = list()
            for particle in self.particles:
                motion_model.update(particle, odometry, 0)
                x.append(particle.x)
                y.append(particle.y)
            plt.plot(x, y, 'r.')
            plt.xlim(-5, 5)
            plt.ylim(-5, 5)
            plt.show()
    #
    # def test_zero_variance(self):
    #     motion_model = MotionModel(0, 0, 0, 0)
    #     ins = open('../../data/log/robotdata1.log')
    #     for line in ins:
    #         measurements = np.fromstring(line[2:], sep=' ')
    #         odometry = measurements[0:3]
    #         time_stamp = measurements[-1]  # last variable
    #         motion_model.update(self.particle, odometry, time_stamp)
    #         print self.particles.x, self.particle.y, self.particle.theta
