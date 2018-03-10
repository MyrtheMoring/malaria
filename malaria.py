""" Lab 5 assignment:

Name: Arjen Swarstenburg and Myrthe Moring
Student ID: 11060298, 11319119
Date: 11-03-2018
Course: Introduction Computational Science

Country: Sierra Leone
https://wwwnc.cdc.gov/travel/yellowbook/2018/infectious-diseases-related-to-travel/yellow-fever-malaria-information-by-country/sierra-leone
http://www.afro.who.int/sites/default/files/2017-05/mcsp.pdf
"""

import numpy as np
import math
import random
import itertools
import matplotlib.pyplot as plt

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)

    source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

class Grid:
    def __init__(self, mosq_count, width=100, height=100, population=0.5):
        self.population = population
        self.mosq_count = mosq_count
        # Grid containing the human_id's on the corresponding positions
        self.human_grid = np.zeros((width, height))
        self.humans = []
        self.mosquitoes = []
        self.width = width
        self.height = height
        self.human_deathcount = 0
        self.human_death_agecount = 0
        self.day = 1

        self.create_humans(int(self.width*self.height*self.population), 0.1)
        self.create_mosquitoes(self.mosq_count)

    def create_humans(self, number_humans, immune=0):
        immune_counter = 0
        """ The ratio of immune people. """
        immune_count = int(number_humans*immune)
        for i in range(number_humans):
            x_pos = random.randint(0, self.width - 1)
            y_pos = random.randint(0, self.height - 1)
            while self.human_grid[x_pos][y_pos] != 0:
                x_pos = random.randint(0, self.width - 1)
                y_pos = random.randint(0, self.height - 1)
            if immune != 0 and immune_counter < immune_count:
                immune_counter += 1
                hum = Humans((x_pos, y_pos), 2)
            else:
                hum = Humans((x_pos, y_pos), 0)
            self.humans.append(hum)
            self.human_grid[x_pos][y_pos] = hum.id

    def create_mosquitoes(self, mosq_count, infected=0):
        infected_counter = 0
        """ The ratio of infected mosquitoes. """
        infected_count = int(mosq_count*infected)
        for i in range(mosq_count):
            x_pos = random.randint(0, self.width - 1)
            y_pos = random.randint(0, self.height - 1)
            pos = (x_pos, y_pos)
            if infected != 0 and infected_counter < infected_count:
                infected_counter += 1
                self.mosquitoes.append(Mosquitoes(pos, True))
            else:
                self.mosquitoes.append(Mosquitoes(pos, False))

    def step(self):
        """ Steps per day.
        - first new mosquitoes are born
        - check which mosquitoe still alive
        - check which humans are going to die """
        self.birth_mosquitoes()

        for mosq in self.mosquitoes:
            if mosq.check():
                (self.mosquitoes).remove(mosq)
                del(mosq)
            else:
                mosq.step(self.human_grid, self.humans)

        humans_killed = []
        for hum in self.humans:
            if hum.check():
                humans_killed.append(hum)
            else:
                hum.step()

        for hum in humans_killed:
            self.kill_human(hum)
            self.create_humans(1)

        #self.print_statistics()
        self.day += 1

    def kill_human(self, human):
        self.human_agecount += human.age
        self.human_grid[human.position[0]][human.position[1]] = 0
        self.humans.remove(human)
        del(human)
        self.human_deathcount += 1

    def birth_mosquitoes(self):
        """ Create every day (step) new mosquitoes based on the number of mosquitoes.
        TODO: infected/not infected mosquitoes"""

        new_mosq = self.mosq_count * 2
        self.create_mosquitoes(new_mosq, 0.5)

    def print_statistics(self):
        print('Day: %d' % self.day)
        print('Mosquitoes alive: %d' % len(self.mosquitoes))
        print('Humans alive: %d' % len(self.humans))
        print('Human deathcount: %d' % self.human_deathcount)
        if self.human_deathcount != 0:
            print('Average human age when dying: %f years' % (float(self.human_death_agecount/self.human_deathcount)/365))
            cumulative_age = 0
            for hum in self.humans:
                cumulative_age += hum.age
            print('Average human age: %f years' % (float(cumulative_age/len(self.humans))/365))
        print()

class Humans:
    idcounter = 0

    def __init__(self, position, state=0):
        """
        States:
        - 0: susceptible
        - 1: infected
        - 2: immune
        - 3: dead
        """
        self.id = Humans.generate_id()
        self.state = state
        self.position = position
        self.age = 0
        self.time_infected = 0
        self.infections = 0

    @staticmethod
    def generate_id():
        Humans.idcounter += 1
        return Humans.idcounter

    def check(self):
        """
        Check if Human is going to die.
        Return True if dead:
            - if older than 80 years
            - if 50 days infected
            - if they are dead (just a check)
            - if 4 times infected (TODO: CHECK of dit zo is)
        """
        if self.age >= 29200 or self.state == 3:
            return True

        if (self.time_infected >= 50 or self.infections >= 4) and self.state != 2:
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

    def random_walk_Moore(self, grid):
        """ Random walk: check the grid borders. """
        width, height = grid.shape
        width -= 1
        height -= 1
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

    def human_check(self, grid, humans):
        hum_id = grid[self.position[0]][self.position[1]]
        if hum_id != 0:
            for hum in humans:
                if hum.id == hum_id:
                    self.human = hum
        else:
            self.human = None

    def check(self):
        """
        Check if Mosquito is going to die.
        Return True if dead.
        """
        if self.hungry > 3 or self.age >= 14:
            return True

    def step(self, grid, humans):
        """ The step function for the mosquitoes. """
        self.age += 1
        self.hungry += 1
        self.random_walk_Moore(grid)
        self.human_check(grid, humans)
        if self.human != None:
            if self.hungry >= 0:
                self.bite()

    def bite(self):
        """ Check if the mosquitoe is infected.
        If human is infected, """
        self.hungry = -3
        if self.infected:
            if self.human.state == 1:
                self.human.infections += 1
            if self.human.state == 0:
                self.human.state = 1
        else:
            if self.human.state == 1:
                self.infected = True

def main():
    if len(sys.argv) < 2:
        print("Usage: %s days_to_simulate" % sys.argv[0])
        return

    malaria_grid = Grid(20, population=0.1)
    number_mosquitoes = []
    number_humans = []
    days_simulating = int(sys.argv[1])
    printProgressBar(0, days_simulating, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i in range(days_simulating):
        number_mosquitoes.append(len(malaria_grid.mosquitoes))
        number_humans.append(len(malaria_grid.humans))
        malaria_grid.step()
        printProgressBar(i + 1, days_simulating, prefix = 'Progress:', suffix = 'Complete', length = 50)
    malaria_grid.print_statistics()

    #plt.plot(range(100), number_mosquitoes)
    #plt.xlabel("Days. ")
    #plt.ylabel("Number of mosquitoes. ")
    #plt.title("Number of mosquitoes per day. ")
    #plt.show()

if __name__ == '__main__':
    import collections
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    import sys
    from random import randint
    from collections import Counter
    main()
