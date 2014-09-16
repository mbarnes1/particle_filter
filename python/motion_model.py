__author__ = 'Arun Srivatsan'


class MotionModel(object):
    """
    This is them motion model of the robot
    """
    def __init__(self):
        self.temp = []

    def update(self, particle, x, y, theta, ts):
        """
        Updates a particle's position using the motion model
        :param particle: Particle object
        :param x: Odometry update in local robot coordinates (forward)
        :param y: Odometry update in local robot coordinates (right)
        :param theta: Odometry update in local robot coordinates (clockwise)
        :param ts: Timestamp
        :return: Nothing. Updates the particle values in place.
        """