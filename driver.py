#Author: Isaac Feldman
#Date: 2/9/2020
#Purpose: A driver to test some code for some boids!

#Instructions: Click to add a new boid to the flock, the boids should try to avoid the mouse!

from boid import Boid
from flock import Flock
from cs1lib import *
from random import uniform


WIDTH = 600
HEIGHT = 600

mouse = []

clicked = False

f = Flock(50, 50, WIDTH, HEIGHT)

def main():
    global clicked
    set_clear_color(0,0,0)
    clear()
    #Cohesion | Alignment | Separation
    f.update(0.15, 3, 5, 25, mouse, 10)
    f.draw(1, 1, 1, True) #True: draw velocity vectors (drawing these takes a lot of resources so be careful)

    if clicked:
        f.add_boid(Boid(mouse[0], mouse[1], uniform(1, 3), uniform(0, 2*pi)))
        clicked = False

def move(mx, my):
    global mouse
    mouse = [mx, my]

def click(mx, my):
    global clicked
    clicked = True


start_graphics(main, width=WIDTH, height=HEIGHT, mouse_move=move, mouse_press=click)