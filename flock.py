#Author: Isaac Feldman
#Date: 2/9/2020
#Purpose: define a class to manage many boid objects

from boid import Boid
from cs1lib import *
from math import fabs
from random import uniform

VIEW_ANGLE = pi

class Flock:
    def __init__(self, num_boids, neighborhood_threshold, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.crowd = []
        self.threshold = neighborhood_threshold
        self.pop = num_boids

        for i in range(self.pop): #add boids of random position, speed, and direction
            self.crowd.append(Boid(uniform(0, self.window_width), uniform(0, self.window_height), uniform(1, 5), uniform(0, 2 * pi)))

    def add_boid(self, boid): #add a boid, increase the population count
        self.crowd.append(boid)
        self.pop = self.pop + 1

    def update(self, c, a, s, seperation_threshold, obstacle_position = [], obstacle_weight = 1):

        pass

        # for agent in self.crowd: #Select a boid
        #
        #     neighborhood = Flock(0, self.threshold, self.window_width, self.window_height) #Define an empty subflock
        #     acceleration = [0,0]
        #
        #     for member in self.crowd: #Select a boid
        #
        #         if agent.get_boid_distance(member) <= self.threshold  and agent != member and agent.get_boid_angle(member) <= VIEW_ANGLE: #If a boid in close enough, not the agent, and visible to the agent add it to the neighborhood
        #             neighborhood.add_boid(member)
        #             #set_fill_color(1, 1, 1, 0.2)
        #             #draw_circle(agent.pos[0], agent.pos[1], self.threshold)
        #
        #     ##Handle the radius of effect of any obstacles
        #     if 0 < fabs(agent.get_raw_distance(obstacle_position)) < 100:
        #         obstacle_weight = 10
        #     else:
        #         obstacle_weight = 0
        #     if neighborhood.pop != 0: #This is an efficiency improvement: if a boid has no neighbors, don't call its methods that involve neighbors
        #         ## This magical line combines all the forces affecting the current boid
        #         acceleration = [ c * agent.cohere(neighborhood)[0] + a * agent.align(neighborhood)[0] + s * agent.separate(neighborhood, seperation_threshold)[0], c * agent.cohere(neighborhood)[1] + a * agent.align(neighborhood)[1] + s*  agent.separate(neighborhood, seperation_threshold)[1]]
        #
        #     ##Add in the obstacles and update the boid
        #     acceleration = [acceleration[0] + obstacle_weight * agent.avoid(obstacle_position)[0], acceleration[1] + obstacle_weight * agent.avoid(obstacle_position)[1]]
        #     agent.update(self.window_width, self.window_height, acceleration)


    def draw(self, r, g, b, velocity_lines): #Draw the boids
        for boid in self.crowd:
            boid.draw(r, g, b, velocity_lines)