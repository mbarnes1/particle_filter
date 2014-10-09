import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import warnings
from scipy import ndimage
import math
from itertools import izip
from copy import deepcopy
__author__ = 'mbarnes1'
#from numpy.random import choice


class Map(object):
    """
    This is the object for the known map (of Wean Hall).
    It initializes using the provided map files.
    It allows queries of locations in this map.
    y are rows, starting at first line
    x are columns, starting at first column
    0 = occupied
    1 = unoccupied
    """
    def __init__(self, relative_path_to_map):
        """
        Initialize the map by loading the map path.
        Assumption: P=0 at unknown (-1 in map file) locations
        """
        # Initialize the map, given the relative path to the map file
        self._occupancy_grid_original = np.genfromtxt(relative_path_to_map, skip_header=7)
        self._occupancy_grid_original = np.flipud(self._occupancy_grid_original)
        self._occupancy_grid = deepcopy(self._occupancy_grid_original)
        self._occupancy_grid[self._occupancy_grid == -1] = 1.0
        self._occupancy_grid[0.3 < self._occupancy_grid] = 1.0
        self._resolution = 10.0  # 10cm resolution
        self._max_x = self._occupancy_grid.shape[0]*self._resolution
        self._max_y = self._occupancy_grid.shape[1]*self._resolution
        self._gaussian_occupancy_grid = ndimage.gaussian_filter(self._occupancy_grid, sigma=3.5)
        self._seed = []
        self._seed_index = 0

    def query(self, x, y):
        """
        Query an occupancy location in the map
        """
        if 0 <= y <= self._max_y and 0 <= x <= self._max_x:
            ind_x = int(x/self._resolution)
            ind_y = int(y/self._resolution)
            return self._occupancy_grid[ind_y, ind_x]
        else:
            #string = 'Query outside map: (' + str(x) + ', ' + str(y) + ')'
            #warnings.warn(string)
            return 0.7

    def query_gaussian(self, x, y):
        """
        Query an occupancy location in the map
        """
        if 0 <= y <= self._max_y and 0 <= x <= self._max_x:
            ind_x = int(x/self._resolution)
            ind_y = int(y/self._resolution)
            return self._gaussian_occupancy_grid[ind_y, ind_x]
        else:
            #string = 'Query outside map: (' + str(x) + ', ' + str(y) + ')'
            #warnings.warn(string)
            return 0.7

    def sample_seed(self, num_particles=10000):
        """
        Seeds the random point sampling for speed
        :param num_particles: Number of particles to start with
        """
        occupancy_vector = np.ravel(self._occupancy_grid_original)
        unoccupied_vector = (occupancy_vector == 1).astype(float)
        unoccupied_vector = unoccupied_vector/sum(unoccupied_vector)
        np.random.choice(range(0, len(occupancy_vector)), p=unoccupied_vector,
                                        replace=True)
        vector_indices = np.random.choice(range(0, len(occupancy_vector)), p=unoccupied_vector,
                                          replace=True, size=num_particles)
        self._seed = np.unravel_index(vector_indices, self._occupancy_grid.shape)
        self._seed_index = 0

    def sample(self):
        """
        Samples a single point from the map based on occupancy probabilities
        :return:
        x, y
        """
        try:
            x = self._resolution * self._seed[1][self._seed_index]
            y = self._resolution * self._seed[0][self._seed_index]
            self._seed_index += 1
        except IndexError:
            self.sample_seed(10000)
            x, y = self.sample()
        return x, y

    def display(self, particles, title='', ranges=[]):
        plt.imshow(self._occupancy_grid, cmap=cm.Greys_r)
        for particle in particles:
            plt.plot(particle.x/self._resolution, particle.y/self._resolution, 'r.')
        ax = plt.axes()
        for particle in particles:
            theta = particle.theta
            dx = 200*math.cos(theta)
            dy = 200*math.sin(theta)
            ax.arrow(particle.x/self._resolution,
                     particle.y/self._resolution,
                     dx/self._resolution,
                     dy/self._resolution,
                     head_width=8, head_length=10, fc='b', ec='b')
            if particle.debug:
                for angle, laser_reading in izip(range(-90, 91), ranges):
                    if angle % 5 == 0:
                        dtheta = angle*math.pi/180 + theta
                        x = particle.x + laser_reading*math.cos(dtheta)
                        y = particle.y + laser_reading*math.sin(dtheta)
                        plt.plot(x/self._resolution, y/self._resolution, 'g.')
            particle.debug = False
        #plt.axis([300, 450, 350, 450])
        plt.axis([0, self._occupancy_grid.shape[0], 0, self._occupancy_grid.shape[1]])
        plt.title(title)
        plt.show()

    def display_gaussian(self, particles, title=''):
        plt.imshow(self._gaussian_occupancy_grid, cmap=cm.Greys_r)
        for particle in particles:
            plt.plot(particle.x/self._resolution, particle.y/self._resolution, 'r.')
        plt.axis([0, self._gaussian_occupancy_grid.shape[0], 0, self._gaussian_occupancy_grid.shape[1]])
        plt.title(title)
        plt.show()