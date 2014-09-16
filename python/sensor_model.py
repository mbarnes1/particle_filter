__author__ = 'Arun Srivatsan'


class SensorModel(object):
    """
    This is the sensor model of the laser range finder.
    """
    def __init__(self, map):
        self._map = map  # pointer to the map, for querying

    def get_probability(self, particle, ranges):
        """
        Returns the probability of seeing laser readings at current particle state
        :param particle: Current particle state
        :param ranges: Range readings from laser scanner. 1D array w/ 180 values, in cm. RIGHT TO LEFT, 180 DEGREES
        :return: Probability in range [0,1]
        """
        return 0.5