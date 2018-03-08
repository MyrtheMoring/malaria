""" Lab 4 assignment:

Name: Myrthe Moring
Student ID: 11319119
Date: 05-03-2018
Course: Introduction Computational Science

Rule 184 can be used as a simple model for traffic flow in a single lane of a
highway and forms the basis for many other cellular automata models of traffic
flow. Cars move forward only if there is open space in front of it.

Simple rule which achieves realistic complex features:
    – clusters of freely moving cars separated by
    stretches of open road when traffic is sparse;
    – waves of stop-and-go traffic when traffic is dense.
"""

import numpy as np
import math
import random
import itertools

def decimal_to_base_k(n, k):
    """Converts a given decimal (i.e. base-10 integer) to a list containing the
    base-k equivalant.
    For example, for n=34 and k=3 this function should return [1, 0, 2, 1]."""

    base = np.base_repr(n, k)
    return (list(map(int, base)))


def base_to_decimal(base, k):
    """Converts a list containing a base-k number into a decimal.
    (for convenience) """

    n = 0
    for i, x in enumerate(base):
        n += x * k**(len(base)-i-1)
    return n


class Grid:
    def __init__(self, mosq_count, width=100, height=100, population=0.5):
        self.population = population
        self.mosq_count = mosq_count
        self.humans = []
        self.mosquitoes = []
        self.width = width
        self.height = height

        self.create_humans()
        self.create_mosquitoes(self.mosq_count)

    def create_humans(self):
        number_humans = int(self.width*self.height*self.population)
        positions_all = list(itertools.product(range(self.width), range(self.height)))
        positions = random.sample(positions_all, number_humans)
        for i in range(number_humans):
            self.humans.append(Humans(positions[i]))

    def create_mosquitoes(self, mosq_count):
        for i in range(mosq_count):
            x_pos = random.randint(0, self.width-1)
            y_pos = random.randint(0, self.height-1)
            pos = (x_pos, y_pos)
            self.mosquitoes.append(Mosquitoes(pos))

    def step(self):
        """ Steps per day """
        self.birth_mosquitoes()

        for mosq in self.mosquitoes:
            if mosq.mosquitoe_check() == False:
                (self.mosquitoes).remove(mosq)
                del(mosq)
            mosq.step_mosquitoe(self.width, self.height)

    def birth_mosquitoes(self):
        """ Create every day (step) new mosquitoes based on the number of mosquitoes.
        TODO: infected/not infected mosquitoes"""
        new_mosq = self.mosq_count * 8
        self.create_mosquitoes(new_mosq)

class Humans:
    def __init__(self, position):
        """
        States:
        - 0: susceptible
        - 1: infected
        - 2: immune
        - 3: dead
        """
        self.state = 0
        self.position = (0,0)

class Mosquitoes:
    def __init__(self, position):
        self.position = position
        self.infected = False
        # ophogen van hungry tot 3 (dan dood)
        self.hungry = 0
        self.human = None
        self.age = 0

    def random_walk_Moore(self, width, height):
        change_pos = (random.randint(-1,1), random.randint(-1,1))
        while change_pos == (0,0):
            change_pos = (random.randint(-1,1), random.randint(-1,1))

        new_x = self.position[0] + change_pos[0]
        while (new_x < 0 or new_x > width):
            new_x = self.position[0] + random.randint(-1,1)

        new_y = self.position[1] + change_pos[1]
        while (new_y < 0 or new_y > height):
            new_y = self.position[1] + random.randint(-1,1)
            print(self.position[1])

        new_pos = (self.position[0] + new_x,self.position[1] + new_y)
        self.position = new_pos

    def mosquitoe_check(self):
        if self.hungry > 3 or self.age > 5:
            return False

    def step_mosquitoe(self, width, height):
        self.age += 1
        self.random_walk_Moore(width, height)


if __name__ == '__main__':
    import collections
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from random import randint
    from collections import Counter

    malaria_grid = Grid(20)

    malaria_grid.step()
    # malaria_grid.step()
