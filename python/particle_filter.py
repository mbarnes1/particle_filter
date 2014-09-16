__author__ = 'mbarnes1'
from map import Map
import numpy as np
from motion_model import MotionModel
from sensor_model import SensorModel
from copy import deepcopy


class ParticleFilter(object):
    """
    This is the main particle filter object.
    """
    def __init__(self):
        self.map = Map('../data/map/wean.dat')
        self._number_particles = 10
        self.particles = list()
        for _ in range(0, self._number_particles):
            self.particles.append(Particle(self.map))
        self._motion_model = MotionModel()
        self._sensor_model = SensorModel(self.map)

    def display(self):
        self.map.display(self.particles)

    def update(self, line):
        """
        Update step.
        Reading is a single reading (i.e. line) from the log file
        Could be either an odometry or laser reading
        """
        measurement_type = line[0]  # O = odometry, L = laser scan
        measurements = np.fromstring(line[2:], sep=' ')
        x = measurements[0]
        y = measurements[1]
        theta = measurements[2]
        time_stamp = measurements[-1]  # last variable
        for particle in self.particles:
            self._motion_model.update(particle, x, y, theta, time_stamp)
        if measurement_type == "L":
            ranges = measurements[3:-1]  # exclude last variable, the time stamp
            particle_probabilities = list()  # unnormalized sensor model probabilities of the particles
            for particle in self.particles:
                particle_probabilities.append(self._sensor_model.get_probability(particle, ranges))
            self._resample(particle_probabilities)

    def _resample(self, particle_probabilities):
        """
        Resamples the particles given unnormalized particle probabilites
        """
        particle_probabilities = np.asarray(particle_probabilities)/sum(particle_probabilities)  # normalize
        indices = np.random.choice(range(0, self._number_particles), size=self._number_particles, replace=True,
                                   p=particle_probabilities)
        indices.sort()
        previous_index = -1
        new_particles = list()
        for index in indices:
            if index != previous_index:
                new_particles.append(self.particles[index])
            else:
                new_particles.append(deepcopy(self.particles[index]))
        self.particles = new_particles


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
    ins = open('../data/log/robotdata1.log')
    for measurement in ins:
        particle_filter.update(measurement)
        particle_filter.display()

if __name__ == '__main__':
    main()