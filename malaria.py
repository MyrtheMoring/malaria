""" Lab 5 assignment:

Name: Arjen en Myrthe
Student ID: 11319119
Date: 11-03-2018
Course: Introduction Computational Science

"""

import numpy as np
import math
import random
import itertools

# def decimal_to_base_k(n, k):
#     """Converts a given decimal (i.e. base-10 integer) to a list containing the
#     base-k equivalant.
#     For example, for n=34 and k=3 this function should return [1, 0, 2, 1]."""
#
#     base = np.base_repr(n, k)
#     return (list(map(int, base)))
#
# def base_to_decimal(base, k):
#     """Converts a list containing a base-k number into a decimal.
#     (for convenience) """
#
#     n = 0
#     for i, x in enumerate(base):
#         n += x * k**(len(base)-i-1)
#     return n


class Grid:
    def __init__(self, mosq_count, width=100, height=100, population=0.5):
        self.population = population
        self.mosq_count = mosq_count
        self.humans = []
        self.mosquitoes = []
        self.width = width
        self.height = height
        self.human_deathcount = 0
        self.day = 1

        self.create_humans()
        self.create_mosquitoes(self.mosq_count)

    def create_humans(self):
        number_humans = int(self.width*self.height*self.population)
        positions_all = list(itertools.product(range(self.width), range(self.height)))
        positions = random.sample(positions_all, number_humans)
        for i in range(number_humans):
            self.humans.append(Humans(positions[i], 1))

    def create_mosquitoes(self, mosq_count):
        for i in range(mosq_count):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            pos = (x_pos, y_pos)
            self.mosquitoes.append(Mosquitoes(pos, True))

    def step(self):
        """ Steps per day """
        self.birth_mosquitoes()

        for mosq in self.mosquitoes:
            if mosq.check():
                (self.mosquitoes).remove(mosq)
                del(mosq)
            else:
                mosq.step(self.width, self.height)

        for hum in self.humans:
            if hum.check():
                (self.humans).remove(hum)
                del(hum)
                self.human_deathcount += 1
            else:
                hum.step()

        print('Day: %d' % self.day)
        print('Mosquitoes alive: %d' % len(self.mosquitoes))
        print('Humans alive: %d' % len(self.humans))
        print('Human deathcount: %d' % self.human_deathcount)
        print()

        self.day += 1

    def birth_mosquitoes(self):
        """ Create every day (step) new mosquitoes based on the number of mosquitoes.
        TODO: infected/not infected mosquitoes"""

        new_mosq = self.mosq_count * 8
        self.create_mosquitoes(new_mosq)

class Humans:
    def __init__(self, position, state=0):
        """
        States:
        - 0: susceptible
        - 1: infected
        - 2: immune
        - 3: dead
        """
        self.state = state
        self.position = (0,0)
        self.age = 0
        self.time_infected = 0

    def check(self):
        """
        Check if Human is going to die.
        Return True if dead.
        """
        if self.age > 29200 or self.time_infected > 30:
            return True

    def step(self):
        self.age += 1
        if self.state == 1:
            self.time_infected += 1

class Mosquitoes:
    def __init__(self, position, infected=False):
        self.position = position
        self.infected = infected
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

        self.position = (new_x,new_y)

    def check(self):
        """
        Check if Mosquito is going to die.
        Return True if dead.
        """
        if self.hungry > 3 or self.age > 14:
            return True

    def step(self, width, height):
        self.age += 1
        self.random_walk_Moore(width, height)
        if self.human != None:
            self.bite()

    def bite(self):
        """ Check if the mosquitoe is infected. """
        self.hungry = -3
        if self.infected:
            if self.human.state == 1:
                self.human.state = 4
            else:
                self.human.state = 1



if __name__ == '__main__':
    import collections
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from random import randint
    from collections import Counter

    malaria_grid = Grid(20)
    for i in range(50):
        malaria_grid.step()
