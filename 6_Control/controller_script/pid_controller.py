# -----------
# User Instructions
#
# Implement a PD controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau_p and tau_d so that:
#
# steering = -tau_p * CTE - tau_d * diff_CTE
# where differential crosstrack error (diff_CTE)
# is given by CTE(t) - CTE(t-1)
#
#
# Only modify code at the bottom! Look for the TODO
# ------------

import random
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------
#
# this is the Robot class
#

class Robot(object):
    def __init__(self, length=20.0):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets a robot coordinate.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)

############## ADD / MODIFY CODE BELOW ####################
# ------------------------------------------------------------------------
#
# run - does a single control run

# P controller
def run_p(robot, tau, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    for i in range(n):
        cte = robot.y
        steer = -tau * cte
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
    return x_trajectory, y_trajectory

# PD controller
def run_pd(robot, tau_p, tau_d, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    cte = robot.y
    for i in range(n):
        cte_old = cte
        cte = robot.y
        diff_cte = cte - cte_old
        steer = (-tau_p * cte) - (tau_d * diff_cte)
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
    return x_trajectory, y_trajectory

# PID controller
def run_pdi(robot, tau_p, tau_d, tau_i, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    cte = robot.y
    int_cte = 0
    for i in range(n):
        cte_old = cte
        cte = robot.y
        diff_cte = cte - cte_old #differential
        int_cte += cte  #integral
        steer = (-tau_p * cte) - (tau_d * diff_cte) - (tau_i * int_cte)
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
    return x_trajectory, y_trajectory

# Twiddle algorithm to tune PID parameters based on error
def twiddle(tol=0.2):
    #initialize parameters with 0 and adjust them as per the cost function
    p = [0, 0, 0]
    dp = [1, 1, 1]
    robot = make_robot()
    x_trajectory, y_trajectory, best_err = run_pdi_err(robot, p)

    it = 0
    while sum(dp) > tol:
        print("Iteration {}, best error = {}".format(it, best_err))
        for i in range(len(p)):
            p[i] += dp[i]
            robot = make_robot()
            x_trajectory, y_trajectory, err = run_pdi_err(robot, p)

            if err < best_err:
                best_err = err
                dp[i] *= 1.1
            else:
                p[i] -= 2 * dp[i]
                robot = make_robot()
                x_trajectory, y_trajectory, err = run_pdi_err(robot, p)

                if err < best_err:
                    best_err = err
                    dp[i] *= 1.1
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9
        it += 1
    return p, err

def make_robot():
    """
    Resets the robot back to the initial position and drift.
    You'll want to call this after you call `run`.
    """
    robot = Robot()
    robot.set(0, 1, 0)
    robot.set_steering_drift(10 / 180 * np.pi)
    return robot

# NOTE: We use params instead of tau_p, tau_d, tau_i
# error (cost) function for PID controller
def run_pdi_err(robot, params, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    err = 0
    prev_cte = robot.y
    int_cte = 0
    for i in range(2 * n):
        cte = robot.y
        diff_cte = cte - prev_cte
        int_cte += cte
        prev_cte = cte
        steer = -params[0] * cte - params[1] * diff_cte - params[2] * int_cte
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        if i >= n:
            err += cte ** 2 # squared error
    return x_trajectory, y_trajectory, err / n

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

#twiddle calls the cost function which in turn runs 100 times to minimize errors
params, err = twiddle()
print("Final twiddle error = {}".format(err))
print("P=", params[0], " I=", params[2], " D=", params[1])

robot = make_robot()
x_trajectory, y_trajectory, err = run_pdi_err(robot, params)
n = len(x_trajectory)
ax1.plot(x_trajectory, y_trajectory, 'k', label='PID_err')
ax2.plot(x_trajectory, y_trajectory, 'k', label='PID_err')

robot_pdi = Robot()
robot_pdi.set(0, 1, 0)
pdi_x_trajectory, pdi_y_trajectory = run_pdi(robot_pdi, 0.2, 3.0, 0.008)
ax2.plot(pdi_x_trajectory, pdi_y_trajectory, 'c', label='PID')

robot_pd = Robot()
robot_pd.set(0, 1, 0)
pd_x_trajectory, pd_y_trajectory = run_pd(robot_pd, 0.2, 3.0)
ax2.plot(pd_x_trajectory, pd_y_trajectory, 'g', label='PD')

robot_p = Robot()
robot_p.set(0, 1, 0)
p_x_trajectory, p_y_trajectory = run_p(robot_p, 0.2)
ax2.plot(p_x_trajectory, p_y_trajectory, 'b', label='P')


ax1.plot(x_trajectory, np.zeros(n), 'r', label='reference')
ax2.plot(x_trajectory, np.zeros(n), 'r', label='reference')

ax1.set_xlabel('time')
ax1.set_ylabel('CTE')
ax2.set_xlabel('time')
ax2.set_ylabel('CTE')

plt.legend(loc="upper right")
plt.show()
