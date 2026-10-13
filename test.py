import numpy as np
from stable_baselines3 import A2C

track_length = 6.1 # m

theta = 7 * np.pi / 8 # rad
theta_d = 0 # rad/s
# define the center of the track to be x=0
cart_x = 0 # m
cart_x_d = 0 # m/s
cart_x_dd = 0 # m/s^2

g = 9.8 # m/s
L = 1 # m
dt = 1 / 60 # s

def env(theta, theta_d, cart_x, cart_x_d, cart_x_dd, g, l, dt):
    # angle update
    theta_dd = 1.5 * (g * np.sin(theta) - cart_x_dd * np.cos(theta)) / l # rad/s^2
    theta_d += theta_dd * dt
    theta += theta_d * dt
    # cart update
    cart_x_d += cart_x_dd * dt
    cart_x += cart_x_d * dt

    while theta > np.pi * 2:
        theta -= np.pi * 2
    while theta < 0:
        theta += np.pi * 2
    return theta, theta_d, cart_x, cart_x_d

def reward_func(theta, terminated):
    reward = -np.abs(cart_x) # maximizing reward means minimizing the distance to the center of the track (bringing cart_x as close to zero as possible)
    if theta < 0.20944 or theta > 6.07375:
        reward += 1
    if terminated:
        reward -= 10
    return reward
    

# this takes about 15 seconds to run on my machine. If each time step represents dt amount of time, this bit of code
# simulates dt * 5,184,000 = 24 hours of time. In other words, every second of real time represents 1.6 hrs of simulated time
for i in range(5184000):
    theta, theta_d, cart_x, cart_x_d = env(theta, theta_d, cart_x, cart_x_d, cart_x_dd, g, L, dt)

    # prints the first few seconds and last few seconds of oscillation. It's stable!
    printing = False
    if i < 180 and printing:
        print(theta - np.pi)
    if i == 190 and printing:
        print("----------------------------------------------------------")
    if i > 5184000 - 180 and printing:
        print(theta - np.pi)
print("done!")

