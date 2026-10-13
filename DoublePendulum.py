import pygame
import numpy as np
pygame.init()

# this is a simulation (and maybe later a framework for developing a deep RL agent to balance it) of a double pendulum
# on a cart that moves arbitrarily (either from user input or agent input). A double pendulum is a pendulum which 
# is attached to the end of another pendulum. The pendulum which is attached to the cart will be known as pendulum 1, while
# the other pendulum will be known as pendulum 2.

# ------------------------------------------------ necessary game settings ------------------------------------------------------

game_name = "double pendulum" # the name of the window that pops up
WIDTH = 1400 # pixels
HEIGHT = 600 # pixels
FRAME = 0
FRAME_RATE = 60 # frames / second
background_color = (0, 0, 0) # rgb color; each value ranges from 0-225 inclusive

# ----------------------------------------------------- game logic --------------------------------------------------------------

dt = 1 / FRAME_RATE
# track and cart variables
track_width = WIDTH - 60
track_y = HEIGHT / 2
cart_x = WIDTH / 2
cart_x_d = 0
cart_x_dd = 0
cart_size = 40

# pendulum variables: let 1 m be defined as the length of the 1st pendulum
L1 = 220 # pendulum 1 length
L2 = 220 # pendulum 2 length
theta1 = np.pi / 8 # pendulum angle as measured clockwise from the vertical upwards direction (radians)
theta_d1 = 0 # pendulum angular speed in rad/sec
theta2 = np.pi / 16
theta_d2 = 0
g = 9.8 * 220 # pixels / s^2
mouse_p = (0, 0)

# any variable you want to update should be declared global in the function
def main_loop(FRAME): # the current frame number is passed to the main loop if you so choose to use it
    global theta1, theta_d1, theta2, theta_d2, cart_x_dd, cart_x_d, cart_x
    k = 400
    f = 30
    cart_x_dd = - k * (cart_x - mouse_p[0]) - (f * cart_x_d) # the mouse position determines the position of the cart
    cart_x_d += cart_x_dd * dt
    cart_x += cart_x_d * dt
    
    #print(str(track_width * w * w * np.sin(w * FRAME * dt)) + " " + str(cart_x_d) + " " + str(cart_x))
    theta, theta_d = environment(cart_x_dd, theta, theta_d, L, g, dt)
    while theta > 2 * np.pi:
        theta -= 2 * np.pi
    while theta < 0:
        theta += 2 * np.pi
    
# given the current state (theta1, theta)
def environment(x_dd, angle, angle_d, l, gravity, dt): # outputs the updated angle
    angle_dd = 1.5 * (gravity * np.sin(angle) - x_dd * np.cos(angle)) / l # rad/s^2
    theta_d = angle_d + angle_dd * dt
    return angle + theta_d * dt, theta_d

def paint_loop(screen):
    pygame.draw.rect(screen, (255, 255, 255), ((WIDTH - track_width) / 2, track_y - 1, track_width, 2)) # track
    pygame.draw.line(screen, (255, 255, 255), (cart_x, track_y), (cart_x + (L * np.sin(theta)), track_y - (L * np.cos(theta)))) # pendulum rod
    cart_color = (180, 0, 0) # red
    if (theta < np.pi / 2 or theta > 3 * np.pi / 2) and np.abs(theta_d) < 1:
        cart_color = (0, 180, 0) # green
    cart_color = (255, 255, 255) # remove this line to display green/red for good/bad state
    pygame.draw.rect(screen, cart_color, (cart_x - (cart_size / 2), track_y - (cart_size / 2), cart_size, cart_size)) # cart

def input_loop(keys, mouse, mouse_pos):
    global mouse_p, theta, theta_d, cart_x_d, cart_x_dd
    mouse_p = mouse_pos
    if keys[pygame.K_SPACE] == True:
        theta, theta_d, cart_x_d, cart_x_dd = np.pi, 0, 0, 0

# -------------------------------------------------- background functionality -------------------------------------------------

# below makes the code function. It is not necessary to fully understand how it works
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()
run = True
while run:
    # fill the background with the background color
    screen.fill(background_color)

    main_loop(FRAME) # the current frame is passed to the main loop if you so choose to use it
    paint_loop(screen) # screen gets passed so that the print_loop function can draw on the screen
    input_loop(pygame.key.get_pressed(), pygame.mouse.get_pressed(), pygame.mouse.get_pos()) # a list of all inputs
    # the mouse_pressed input is a tuple containing: (left_click, middle_click, right_click)

    # increment the frame number. This is to keep track of what frame the game is on
    FRAME += 1
    clock.tick(FRAME_RATE) # keeps the game running at a max speed of 'FRAME_RATE' frames/second (might be slower if computations are heavy)
    # this makes sure everything is closed properly when the window is closed
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()