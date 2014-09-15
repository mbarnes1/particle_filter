__author__ = 'mbarnes1'
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
        #self._occupancy_grid = np.rot90(self._occupancy_grid)
        self._occupancy_grid[self._occupancy_grid == -1] = 0
        self._resolution = 10  # 10cm resolution
        #self.max_x = self._occupancy_grid.size[0]*self._resolution
        #self.max_y = self._occupancy_grid.size[1]*self._resolution

    def query(self, x, y):
        """
        Query a location.
        x is the horizontal axis
        y is the vertical axis
        origin is bottom left hand corner. Quadrant 1 is upper left hand corner
        """
        # Return occupancy of the (x, y) map location
        ind_x = round(x/self._resolution)
        ind_y = round(y/self._resolution)
        return self._occupancy_grid[ind_x, ind_y]

    def display(self):
        plt.imshow(self._occupancy_grid, cmap=cm.Greys_r)
        plt.xlabel('Y')
        plt.ylabel('X')
        plt.show()