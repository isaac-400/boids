#Author: Isaac Feldman
#Date: 2/9/2020
#Purpose: A driver to test some code for some boids!

#Instructions: Click to add a new boid to the flock, the boids should try to avoid the mouse!

from boid import Boid
from cs1lib import *
from random import uniform
from quadtree import Quadtree

WIDTH = 800
HEIGHT = 600
NEIGHBORHOOD_THRESHOLD = 100
SEPARATION_THRESHOLD = 25
C, A, S = 0.15, 3, 5
mouse = [WIDTH/2, HEIGHT/2]


clicked = False


b = []

def main():
    global clicked
    set_clear_color(0,0,0)
    clear()

    update_boids()
    draw()

    if clicked:
        add(mouse[0], mouse[1])
        clicked = False

def move(mx, my):
    global mouse
    mouse = [mx, my]

def click(mx, my):
    global clicked
    clicked = True


def add(x, y):
    b.append(Boid(x, y,))

def draw():
    for boid in b:
        boid.draw(0, 0, 1, False)

def update_boids():

    tree = Quadtree(b[0], 0, 0, WIDTH, HEIGHT)
    for i in range(1, len(b)):
        tree.insert(b[i])

    for boid in b:
        accel = [0, 0]
        possible_close_boids = tree.findInCircle(boid.pos[0], boid.pos[1], NEIGHBORHOOD_THRESHOLD)
        if len(possible_close_boids) > 1:
            accel = boid.compute_acceleration(possible_close_boids, SEPARATION_THRESHOLD, C, A, S)
        if Quadtree.pointInCircle(tree, boid.pos[0], boid.pos[1], mouse[0], mouse[1], NEIGHBORHOOD_THRESHOLD):
            accel = list(map(sum, zip(accel, boid.avoid(mouse))))
        boid.update(WIDTH, HEIGHT, accel)

for _ in range(50):
    add(uniform(0, WIDTH), uniform(0, HEIGHT))

start_graphics(main, width=WIDTH, height=HEIGHT, mouse_move=move, mouse_press=click, framerate=50)