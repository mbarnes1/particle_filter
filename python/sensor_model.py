from copy import copy
import math
import numpy as np
from itertools import izip
import matplotlib.pyplot as plt
__author__ = 'Matt Barnes'


class SensorModel(object):
    """
    This is the sensor model of the laser range finder.
    """
    def __init__(self, map):
        self._map = map  # pointer to the map, for querying
        self._zhit = 1.0
        self._zmax = 0.02
        self._zshort = 0.2
        self._zrand = 1.0
        normalizer = 1/(self._zhit + self._zmax + self._zshort + self._zrand)
        self._zhit *= normalizer
        self._zmax *= normalizer
        self._zshort *= normalizer
        self._zrand *= normalizer
        self._max_z = 2000 #8183
        self._sigmahit = 50
        self._lambdashort = 0.01

    def plot_model(self):
        zstar = 500.0
        x = range(0, self._max_z+1)
        p = []
        for _x in x:
            p.append(self._model(float(_x), zstar))
        plt.plot(x, p)
        plt.xlabel('z')
        plt.ylabel('p(z | z*)')
        plt.title('Sensor Model')
        plt.show()

    def get_probability(self, particle, ranges):
        """
        Returns the probability of seeing laser readings at current particle state
        :param particle: Current particle state
        :param ranges: Range readings from laser scanner. 1D array w/ 180 values, in cm. RIGHT TO LEFT, 180 DEGREES
        :return probability: The (log) probability
        """
        if self._map.query(particle.x, particle.y) > -0.1:
            laser_coordinates = _laser_state(particle)
            angles = np.arange(-90, 91)*np.pi/180
            probability = 1
            alpha = 0.75
            subsample = 10  # use only every tenth laser range reading
            for counter, (z, angle) in enumerate(izip(ranges, angles)):  # iterate through readings
                if counter % subsample == 0:
                    z += 40.0  # average wall thickness ~ 60
                    theta = particle.theta + angle
                    ray_x = laser_coordinates[0] + z*math.cos(theta)
                    ray_y = laser_coordinates[1] + z*math.sin(theta)
                    occupied_probability = 1-self._map.query_gaussian(ray_x, ray_y)
                    probability *= occupied_probability**alpha
                    """
                    #print 'Ray casting at angle', angle
                    z_star = self._ray_cast(laser_coordinates, angle)
                    #print 'Cast to', z_star, 'cm'
                    log_probability += math.log(self._model(z, z_star))
                    #print 'Measurement probability', probability
                    """
            return probability
        else:
            return 0

    def _model(self, z, zstar):
        """
        Returns the probability of beam reading z
        :param z: Beam reading, in cm
        :param zstar: Expected beam reading in cm, from ray casting
        :return p: Probability [0, 1]
        """
        phit = self._zhit*self._phit(z, zstar)
        pmax = self._zmax*self._pmax(z)
        pshort = self._zshort*self._pshort(z, zstar)
        prand = self._zrand*self._prand(z)
        prob = phit + pmax + pshort + prand
        return prob

    def _phit(self, z, zstar):
        """
        Model component of hitting target
        :param z: Reading, in cm
        :param zstar: Expected reading, from ray casting
        :return p: Probability of 'hit'
        """
        if z < self._max_z:
            N = 1.0/math.sqrt(2*math.pi*self._sigmahit**2)*math.e**(-0.5*(z-zstar)**2/self._sigmahit**2)
            eta = 0.5*(math.erf((self._max_z-zstar)/(self._sigmahit*math.sqrt(2))) + math.erf(zstar/(math.sqrt(2)*self._sigmahit)))
            return N*eta
        else:
            return 0

    def _pmax(self, z):
        """
        Probability of not hitting anything, and getting a max sensor value
        :param z: Reading
        :return prob:
        """
        if z == self._max_z:
            return 1.0
        else:
            return 0

    def _pshort(self, z, zstar):
        """
        Probability of hitting a unexpected obstacle in front of robot
        :param z: Reading
        :param zstar: Expected reading
        :return prob:
        """
        if z <= zstar:
            eta = 1.0/(1 - math.e**(-self._lambdashort*zstar))
            prob = eta*self._lambdashort*math.e**(-self._lambdashort*z)
            return prob
        else:
            return 0

    def _prand(self, z):
        """
        Probabiility of getting a random reading
        :param z: Reading
        :return prob:
        """
        if z < self._max_z:
            return 1.0/self._max_z
        else:
            return 0

    def _ray_cast(self, laser_state, ray_angle):
        """
        Returns the expected beam reading, in cm
        :param laser_state: Laser state as tuple (x, y, theta), global coordinates
        :param ray_angle: Ray angle from laser in standard odometry coordinates, radians
        :return zstar: Expected reading, in cm
        """
        threshold = 0.3
        sampling_interval = 7
        ray_angle += laser_state[2]  # ray angle, in global coordinates
        object_detected = 1
        ray_position = [copy(laser_state[0]), copy(laser_state[1])]
        ray_length = 0
        ray_in_bounds = True
        while (object_detected > threshold) and (ray_length < self._max_z) and ray_in_bounds:
            ray_position[0] += sampling_interval*math.cos(ray_angle)
            ray_position[1] += sampling_interval*math.sin(ray_angle)
            if ray_position[1] < -1005:
                print 'pause'
            object_detected = self._map.query(ray_position[0], ray_position[1])
            ray_length += sampling_interval
            if (ray_position[0] < 0) or (ray_position[1] < 0) or (ray_position[0] >= 8000) or (ray_position[1] >= 8000):
                ray_in_bounds = False
        if not ray_in_bounds:
            return self._max_z+10
        zstar = ray_length
        return zstar


def _laser_state(particle):
    """
    Given particle location, offset laser coordinates
    :param particle: Particle object
    :return state: Tuple (x, y, theta) in global coordinates
    """
    offset = 25  # laser is set 25cm forward (x-axis) of robot's center
    x = particle.x + offset*math.cos(particle.theta)
    y = particle.y + offset*math.sin(particle.theta)
    theta = particle.theta
    return (x, y, theta)