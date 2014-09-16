__author__ = 'mbarnes1'
from map import Map
import numpy as np
#from motion_model import MotionModel
#from sensor_model import SensorModel
from copy import deepcopy


class ParticleFilter(object):
    """
    This is the main particle filter object.
    """
    def __init__(self):
        self._map = Map('../data/map/wean.dat')
        self._number_particles = 100
        self._particles = list()
        for _ in range(0, self._number_particles):
            self._particles.append(Particle(self._map))
        #self._motion_model = MotionModel()
        #self._sensor_model = SensorModel()
        self._map.display(self._particles)

    def _update(self, line):
        """
        Update step.
        Reading is a single reading (i.e. line) from the log file
        Could be either an odometry or laser reading
        """
        measurement_type = line[0]  # O = odometry, L = laser scan
        measurements = np.fromstring(line[2:])
        if measurement_type == "O":
            x = measurements[0]
            y = measurements[1]
            theta = measurements[2]
            ts = measurements[3]
            for particle in self._particles:
                self._motion_model.update(particle, x, y, theta, ts)
        elif measurement_type == "L":
            ranges = measurements
            particle_probabilities = list()  # unnormalized sensor model probabilities of the particles
            for particle in self._particles:
                particle_probabilities.append(self._sensor_model.get_probability(particle, ranges))
            self._resample(particle_probabilities)
        else:
            raise Exception('Corrupted data log')

    def _resample(self, particle_probabilities):
        """
        Resamples the particles given unnormalized particle probabilites
        """
        indices = np.random.choice(range(0, self._number_particles), size=self._number_particles, replace=True,
                                   p=particle_probabilities)
        indices.sort()
        previous_index = -1
        new_particles = list()
        for index in indices:
            if index != previous_index:
                new_particles.append(self._particles[index])
            else:
                new_particles.append(deepcopy(self._particles[index]))
        self._particles = new_particles


class Particle(object):
    """
    An individual particle.
    Location initialized using the map occupancy probabilities.
    Orientation initialized randomly
    """
    def __init__(self, _map):
        self.x, self.y = _map.sample()  # global position
        self.theta = np.random.random()*2*np.pi  # global orientation, in radians


def main():
    particle_filter = ParticleFilter()

if __name__ == '__main__':
    main()
