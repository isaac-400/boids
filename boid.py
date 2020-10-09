#Author: Isaac Feldman
#Date: 2/9/2020
#Purpose: Create an agent for a flock simulator. \
# This algorithm was first described by Craig Reynolds in his 1987 paper \
# "Flocks, herds, and schools: A distributed behavioral model"
from operator import mul
from random import uniform

from cs1lib import *
from math import sin, cos, sqrt, acos

class Boid:
### Basic Boid Operation Methods
    def __init__(self, x, y, v=uniform(1, 3), dir=uniform(0, 2*pi)):

        self.speed = v
        self.dir = dir
        self.v = [self.speed * sin(self.dir), self.speed * cos(self.dir)]
        self.pos = [x, y]



        self.width = 5
        self.height = 5

    def update(self, window_width, window_height, acceleration=[0, 0]):

        ##Enforce teleportation at window bounderies
        if self.pos[0] > window_width:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = window_width
        if self.pos[1] > window_height:
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = window_height

        ##Update the boid x and y

        self.pos = [self.pos[0] + self.v[0], self.pos[1] + self.v[1]]

        ##Update the speed of the boid

        self.v = [self.v[0] + acceleration[0], self.v[1] + acceleration[1]]
        self.v = self.limit_magnitude(self.v, 10, 0)

    def compute_acceleration(self, neighboring_list, separation_threshold, c, a, s):
        acceleration = [] # a vector in format [x, y]

        acceleration = map(sum, zip(map(mul, [a, a], self.align(neighboring_list)),
                                    map(mul, [c, c], self.cohere(neighboring_list)),
                                    map(mul, [s, s], self.separate(neighboring_list, separation_threshold))))

        return list(acceleration)

    def draw(self, r=1, g= 0.7, b=0, velocity_lines=False):
        set_fill_color(r, g, b)

        draw_circle(self.pos[0], self.pos[1], self.width) #Draw a circular boid

        if velocity_lines:
            set_stroke_color(1, 1, 1)                          #Draw the velocity pointer
            enable_stroke()
            draw_line(self.pos[0], self.pos[1], self.pos[0] + self.width * self.v[0], self.pos[1] + self.height * self.v[1])
            disable_stroke()

### Behavior Methods -- it might be a good idea to restructure this code into the flock class, but its pretty efficient to just leave it here

    def center(self, center): #returns an accelleration vector pointing from the boid to the center point
        if center == []:
            return [0, 0]
        direction_x = center[0] - self.pos[0]
        direction_y = center[1] - self.pos[1]

        return [direction_x, direction_y]

    def avoid(self, obstacle): #returns an accelleration vector pointing center point to the boid (i.e a vector pointing away from a given obstacle)
         return [-self.center(obstacle)[0], -self.center(obstacle)[1]]

    def align(self, flock): ##returns an accelleration vector parallel to the average direction vector of the nearby flock
        avg_dir = 0

        for boid in flock:
            avg_dir = avg_dir + boid.dir

        avg_dir = avg_dir / len(flock)

        result_vector = [sin(avg_dir), cos(avg_dir)]
        return result_vector

    def cohere(self, flock): #returns an accelleration vector pointing to the centerpoint of a flock around a boid

        avg_x = 0
        avg_y = 0

        for boid in flock:
            avg_x = avg_x + boid.pos[0]
            avg_y = avg_y + boid.pos[1]

        avg_x = avg_x / len(flock)
        avg_y = avg_y / len(flock)

        result_vector = [ avg_x - self.pos[0],  avg_y - self.pos[1]] #computes an average center in a flock
        return result_vector

    def separate(self, flock, threshold): #returns an accelleration vector pointing away from neighbors that are too close
        result = [0, 0]

        for boid in flock:
            distance = self.get_boid_distance(boid)

            if distance <= threshold:

                direction_x = -(boid.pos[0] - self.pos[0])
                direction_y = -(boid.pos[1] - self.pos[1])

                result[0] = result[0] + direction_x
                result[1] = result[1] + direction_y

        result = self.normalize(result)

        return result

### Utility Methods

    def get_boid_distance(self, boid):
        distance = sqrt( (self.pos[0] - boid.pos[0])**2 + (self.pos[1] - boid.pos[1])**2 )
        return distance

    def get_raw_distance(self, position_vector):
        if position_vector == []:
            return 0

        distance = sqrt((self.pos[0] - position_vector[0]) ** 2 + (self.pos[1] - position_vector[1]) ** 2)
        return distance

    def get_boid_angle(self, boid):

        self_mag = sqrt(self.v[0] ** 2 + self.v[1] ** 2)
        boid_mag = sqrt(boid.v[0] ** 2 + boid.v[1] ** 2)

        if self_mag == 0 or boid_mag == 0:
            return 0

        scalar_product = (self.v[0] * boid.v[0]) + (self.v[1] * boid.v[1])

        angle = acos(scalar_product/(self_mag*boid_mag))

        return angle

    def limit_magnitude(self, vector, max_magnitude, min_magnitude = 0): # the method here is pretty heavily inspired by Michael Dodsworth's implementation of boids on his github: https://github.com/mdodsworth/pyglet-boids/blob/master/boids/vector.py
        magnitude = sqrt((vector[0] ** 2 + (vector[1] ** 2)))

        if magnitude > max_magnitude:
            normalized_mag = max_magnitude / magnitude
            #print(normalized_mag)
        elif magnitude < min_magnitude:
            normalized_mag = min_magnitude / magnitude
            #print(normalized_mag)
        else:
            return vector

        return [vector[0] * normalized_mag, vector[1] * normalized_mag]

    def normalize(self, vector): # turn into unit vector

        if sqrt(vector[0] ** 2 + vector[1] ** 2) != 0: #catch any divide by zero errors
            mag = 1 / sqrt(vector[0] ** 2 + vector[1] ** 2)

        else:
            mag = 0

        return [mag * vector[0], mag * vector[1]]