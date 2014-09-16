__author__ = 'mbarnes1'
#from numpy.random import choice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class Map(object):
    """
    This is the object for the known map (of Wean Hall).
    It initializes using the provided map files.
    It allows queries of locations in this map.
    x are rows, starting at first line
    y are columns, starting at first column
    """
    def __init__(self, relative_path_to_map):
        """
        Initialize the map by loading the map path.
        Assumption: P=0 at unknown (-1 in map file) locations
        """
        # Initialize the map, given the relative path to the map file
        self._occupancy_grid = np.genfromtxt(relative_path_to_map, skip_header=7)
        self._occupancy_grid[self._occupancy_grid == -1] = 0
        self._resolution = 10  # 10cm resolution
        self._occupancy_vector = self._occupancy_grid.ravel()
        self._normalized_occupancy_vector = self._occupancy_vector/sum(self._occupancy_vector)
        self._max_x = self._occupancy_grid.shape[0]*self._resolution
        self._max_y = self._occupancy_grid.shape[1]*self._resolution

    def query(self, x, y):
        """
        Query an occupancy location in the map
        """
        # Return occupancy of the (x, y) map location
        ind_x = round(x/self._resolution)
        ind_y = round(y/self._resolution)
        return self._occupancy_grid[ind_x, ind_y]

    def sample(self):
        """
        Samples a single point from the map based on occupancy probabilities
        :return:
        x, y
        """
        vector_index = np.random.choice(range(0, len(self._occupancy_vector)), p=self._normalized_occupancy_vector,
                                        replace=True)
        array_index = np.unravel_index(vector_index, self._occupancy_grid.shape)
        return array_index[0], array_index[1]

    def display(self, particles):
        plt.imshow(self._occupancy_grid, cmap=cm.Greys_r)
        for particle in particles:
            plt.plot(particle.y, particle.x, 'r.')
        plt.axis([0, self._occupancy_grid.shape[0], 0, self._occupancy_grid.shape[1]])
        plt.show()