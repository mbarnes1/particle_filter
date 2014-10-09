__author__ = 'mbarnes1'
import matplotlib
#matplotlib.use("Agg")
import numpy as np
from motion_model import MotionModel
from sensor_model import SensorModel
from copy import deepcopy
import math
import matplotlib.animation as manimation
import matplotlib.pyplot as plt
from map import Map
import matplotlib.cm as cm
from itertools import izip
import time


class ParticleFilter(object):
    """
    This is the main particle filter object.
    """
    def __init__(self, map_file='../data/map/wean.dat'):
        self.map = Map(map_file)
        #self.map.display_gaussian([], 'Gaussian Blurred Map')
        self._number_particles = 1000
        self.particles = list()
        self._particle_probabilities = []
        for _ in range(0, self._number_particles):
            print 'Initializing particle', _
            particle = Particle(self.map)
            #particle.x = 4080 + np.random.normal(scale=35)
            #particle.y = 3980 + np.random.normal(scale=15)
            #particle.theta = math.pi + 0.1 + np.random.normal(scale=.1)
            self.particles.append(particle)
            self._particle_probabilities.append(1)
        self._motion_model = MotionModel(0.001, 0.001, 0.1, 0.1)
        self._sensor_model = SensorModel(self.map)
        self._ranges = []

    def log(self, file_handle):
        line = list()
        for particle in self.particles:
            loc = str(particle.x) + ',' + str(particle.y)
            line.append(loc)
        file_handle.write(';'.join(line))
        file_handle.write('\n')

    def display(self):
        self.map.display(self.particles, ranges=self._ranges)

    def update(self, line):
        """
        Update step.
        Reading is a single reading (i.e. line) from the log file
        Could be either an odometry or laser reading
        """
        measurement_type = line[0]  # O = odometry, L = laser scan
        measurements = np.fromstring(line[2:], sep=' ')
        odometry = measurements[0:3]
        time_stamp = measurements[-1]  # last variable
        for particle in self.particles:
            self._motion_model.update(particle, odometry, time_stamp)
        if measurement_type == "L":
            odometry_laser = measurements[3:6]  # coordinates of the laser in standard odometry frame
            self._ranges = measurements[6:-1]  # exclude last variable, the time stamp
            self._particle_probabilities = list()  # unnormalized sensor model probabilities of the particles
            for particle in self.particles:
                self._particle_probabilities.append(self._sensor_model.get_probability(particle, self._ranges))
            argsorted_probabilities = np.argsort(-np.asarray(self._particle_probabilities))
            self.particles[argsorted_probabilities[0]].debug = True
            self.particles[argsorted_probabilities[1]].debug = True
            self.particles[argsorted_probabilities[2]].debug = True

    def _resample(self):
        """
        Resamples the particles given unnormalized particle probabilites
        """
        particle_probabilities = np.asarray(self._particle_probabilities)/sum(self._particle_probabilities)  # normalize
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
            previous_index = index
        self.particles = new_particles


class Particle(object):
    """
    An individual particle.
    Location initialized using the map occupancy probabilities.
    Orientation initialized randomly
    """
    def __init__(self, _map):
        #x = 0
        #y = 0
        #while not (3500 < y < 4500 and x < 4200):
        x, y = _map.sample()  # global position
        self.x = x
        self.y = y
        self.theta = np.random.random()*2*np.pi  # global orientation, in radians
        self.odometry = list()  # last odometry reading
        self.debug = False  # flag for plotting orientation and sensor readings
        self.debug_arrows = []
        self.debug_rays = []


def main():
    start = time.time()
    #FFMpegWriter = manimation.writers['ffmpeg']
    #metadata = dict(title='Particle Filter', artist='Matt Barnes')
    #writer = FFMpegWriter(fps=15, metadata=metadata)
    particle_filter = ParticleFilter()
    fig = plt.figure()
    p, = plt.plot([], [], 'r.')  # particles
    b, = plt.plot([], [], 'g.')  # beams from best particles
    a, = plt.plot([], [], 'b.')  # arrows
    #a, = plt.arrow([], [], [], [], head_width=8, head_length=10, fc='b', ec='b')
    #plt.axis([0, particle_filter.map._occupancy_grid.shape[0], 0, particle_filter.map._occupancy_grid.shape[1]])
    #plt.imshow(particle_filter.map._occupancy_grid_original, cmap=cm.Greys_r)
    #ax = plt.axes()
    ins = open('../data/log/robotdata5.log', 'r')
    out = open('../data/results/robotdata1.log', 'w')
    #for _ in range(0, 100):
    #    ins.next()  # skip first 25 time-steps
    out.write('x,y;x,y;x,y;etc.')
    max_lines = np.Inf
    #with writer.saving(fig, "writer_test.mp4", 100):
    for counter, measurement in enumerate(ins):
        print 'Time step', counter
        if measurement[0] == 'L':
            particle_filter.update(measurement)
            particle_filter.log(out)
            # x = []
            # y = []
            # bx = []
            # by = []
            # ax = []
            # ay = []
            # for particle in particle_filter.particles:
            #     x.append(particle.x/particle_filter.map._resolution)
            #     y.append(particle.y/particle_filter.map._resolution)
            #     #theta = particle.theta
            #     ax.append((particle.x + 200*math.cos(particle.theta))/particle_filter.map._resolution)
            #     ay.append((particle.y + 200*math.sin(particle.theta))/particle_filter.map._resolution)
            #     #dx = 200*math.cos(theta)
            #     #dy = 200*math.sin(theta)
            #     # ax.arrow(particle.x/particle_filter.map._resolution,
            #     #          particle.y/particle_filter.map._resolution,
            #     #          dx/particle_filter.map._resolution,
            #     #          dy/particle_filter.map._resolution,
            #     #          head_width=8, head_length=10, fc='b', ec='b')
            #     if particle.debug:
            #         particle.debug = False
            #         for angle, laser_reading in izip(range(-90, 91), particle_filter._ranges):
            #             if angle % 5 == 0:
            #                 dtheta = angle*math.pi/180 + particle.theta
            #                 bx.append((particle.x + laser_reading*math.cos(dtheta))/particle_filter.map._resolution)
            #                 by.append((particle.y + laser_reading*math.sin(dtheta))/particle_filter.map._resolution)
            # p.set_data(x, y)
            # b.set_data(bx, by)
            # a.set_data(ax, ay)
            # writer.grab_frame()
            #if counter > 150:
            #    particle_filter.display()
            particle_filter._resample()
        if counter >= max_lines:
            break
    ins.close()
    out.close()
    end = time.time()
    print end - start

if __name__ == '__main__':
    main()