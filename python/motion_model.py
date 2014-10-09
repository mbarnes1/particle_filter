import math
import numpy as np
__author__ = 'Matt Barnes'


class MotionModel(object):
    """
    This is them motion model of the robot
    """
    def __init__(self, alpha1, alpha2, alpha3, alpha4):
        """
        :param alpha1:
        :param alpha2:
        :param alpha3:
        :param alpha4:
        """
        self.temp = []
        self._alpha1 = alpha1
        self._alpha2 = alpha2
        self._alpha3 = alpha3
        self._alpha4 = alpha4

    def update(self, particle, odometry, ts):
        """
        Updates a particle's position using the motion model
        :param particle: Particle object
        :param odometry: Odometry reading of form [x, y, theta] in odometry coordinates
        :param ts: Timestamp
        :return: Nothing. Updates the particle values in place.
        """
        if not particle.odometry:  # first reading?
            particle.odometry = list(odometry)
        u_t = [particle.odometry, odometry]  # old odometry, new odoemtry
        x_new = self._sample_motion_model_odometry(u_t, [particle.x, particle.y, particle.theta])
        particle.odometry = list(odometry)
        particle.x = x_new[0]
        particle.y = x_new[1]
        particle.theta = x_new[2]

    def _sample_motion_model_odometry(self, u_t, x_t0):
        """
        Samples from the motion model
        :param u_t: Pseudo-control input, in the form of odometry update. Of the form:
                    u_t[0] = [xbar, ybar, thetabeta] (odometry at time t-1)
                    u_t[1] = [xbar', ybar', thetabar'] (odometry at time t)
        :param x_t0: State at time t-1. Of form [x y theta]
        :return x_t1: Sample drawn from motion model. Of form [x' y' theta']
        """
        delta_rot_1 = math.atan2(u_t[1][1] - u_t[0][1], u_t[1][0] - u_t[0][0]) - u_t[0][2]
        delta_trans = math.sqrt((u_t[0][0] - u_t[1][0])**2 + (u_t[0][1] - u_t[1][1])**2)
        delta_rot_2 = u_t[1][2] - u_t[0][2] - delta_rot_1

        var1 = self._alpha1*delta_rot_1**2 + self._alpha2*delta_trans**2
        var2 = self._alpha3*delta_trans**2 + self._alpha4*delta_rot_1**2 + self._alpha4*delta_rot_2**2
        var3 = self._alpha1*delta_rot_2**2 + self._alpha2*delta_trans**2

        rand1 = np.random.normal(0, math.sqrt(var1)) if var1 else 0
        rand2 = np.random.normal(0, math.sqrt(var2)) if var2 else 0
        rand3 = np.random.normal(0, math.sqrt(var3)) if var3 else 0

        delta_rot_1_hat = delta_rot_1 - rand1
        delta_trans_hat = delta_trans - rand2
        delta_rot_2_hat = delta_rot_2 - rand3

        x_prime = x_t0[0] + delta_trans_hat*math.cos(x_t0[2] + delta_rot_1_hat)
        y_prime = x_t0[1] + delta_trans_hat*math.sin(x_t0[2] + delta_rot_1_hat)
        theta_prime = x_t0[2] + delta_rot_1_hat + delta_rot_2_hat

        x_t1 = [x_prime, y_prime, theta_prime]
        return x_t1