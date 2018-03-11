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
    def __init__(self, mosq_perc, width=25, height=34, population=0.5):
        """ Parameters:
        - mosq_perc = percentage of mosquitoes relative to humans
        - width, height of the grid based on the country Sierra Leone
        - population = percentage of human population based on the grid
        - humans = list of humans on the Grid
        - mosquitoes = list of mosquitoes on the Grid
        - human_deathcount = number of died humans
        - human_death_agecount =
        - day = counter per day """

        # Grid containing the human_id's on the corresponding positions
        self.human_grid = np.zeros((width, height))
        self.width = width
        self.height = height

        self.population = int(self.width*self.height*population)
        self.mosq_count = int(mosq_perc*self.population)
        self.day = 1

        self.humans = []
        self.mosquitoes = []
        self.create_humans(self.population, 0.1)
        self.create_mosquitoes(self.mosq_count)

        self.human_deathcount = 0
        self.human_death_agecount = 0

    def create_humans(self, number_humans, immune=0):
        immune_counter = 0
        """ The ratio of immune people. """
        immune_count = int(number_humans*immune)
        age = 0

        """ A seventh of the people in Sierra Leone lives in the capital
        city Freetown located in the North West of the country.
        The x coordinates can be between 0 and 10 percent of the width.
        The y coordinates can be between 40 percent and 50 percent of the
        height.These values are based on real data (GoogleMaps and Wikipedia).
        https://en.wikipedia.org/wiki/Sierra_Leone
        """

        capital_city_humans = int(number_humans/7)
        country_humans = number_humans - capital_city_humans

        age_0 = int(number_humans*0.4)
        width_freetown = int(self.width*0.1)
        height_freetown_1 = int(self.height*0.4)
        height_freetown_2 = int(self.height*0.5)

        for i in range(number_humans):
            """ 40 percent of the people are between 0-14 years old. """
            if i > age_0:
                age = 1
            if i < capital_city_humans:
                x_pos = random.randint(0, width_freetown)
                y_pos = random.randint(height_freetown_1, height_freetown_2)
            else:
                x_pos = random.randint(0, self.width - 1)
                y_pos = random.randint(0, self.height - 1)
            while self.human_grid[x_pos][y_pos] != 0:
                x_pos = random.randint(0, self.width - 1)
                y_pos = random.randint(0, self.height - 1)

            if immune != 0 and immune_counter < immune_count:
                immune_counter += 1
                hum = Humans((x_pos, y_pos), 2, 0)
            else:
                hum = Humans((x_pos, y_pos), 0, 0)
            self.humans.append(hum)
            self.human_grid[x_pos][y_pos] = hum.id

    def ages(self, number_humans):
        """ Create the age structure in Sierra Leone: approximately 40 percent
        of the people are between the 0 and 14 and 60 percent is between the 15
        and 64 years old. """

        ages = np.zeros(number_humans)
        age1 = int(number_humans*0.6)
        for i in range(age_1):
            ages[i] = 1
        return ages

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

        # self.print_statistics()
        self.day += 1

    def kill_human(self, human):
        self.human_death_agecount += human.age
        self.human_grid[human.position[0]][human.position[1]] = 0
        self.humans.remove(human)
        del(human)
        self.human_deathcount += 1

    def birth_mosquitoes(self):
        """ Create every day (step) new mosquitoes based on the number of mosquitoes.
        TODO: infected/not infected mosquitoes"""

        new_mosq = self.mosq_count * 1
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

    def __init__(self, position, state=0, age=0):
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
        # age is 0 or 1
        self.age = age
        self.time_infected = 0
        self.infections = 0

        self.set_age(age)

    @staticmethod
    def generate_id():
        Humans.idcounter += 1
        return Humans.idcounter

    def set_age(self, age):
        """ Set the age of the humans. If the binary variable age is 0, the age
        is between to 0-14 years (in days). Else, the age is between the 15-64 years
        (in days). """
        if age == 0:
            self.age = random.randint(0, 5113)
        else:
            self.age = random.randint(5113, 23375)

    def check(self):
        """
        Check if Human is going to die.
        Return True if dead:
            - if older than 80 years
            - if 50 days infected
            - if they are dead (just a check)
            - if 10 times infected
        """
        if self.age >= 29200 or self.state == 3:
            return True

        if (self.time_infected >= 50 or self.infections >= 10) and self.state != 2:
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

def plot_death_mosq(days, frac_mos, frac_pop):
    malaria_grid = Grid(frac_mos, population=frac_pop)

    """ Plot deaths and mosquitoes per day. """
    number_mosquitoes = []
    deaths = []
    for i in range(days):
        deaths.append(malaria_grid.human_deathcount)
        number_mosquitoes.append(len(malaria_grid.mosquitoes))
        malaria_grid.step()

    plt.plot(range(days), number_mosquitoes)
    plt.plot(range(days), deaths)
    plt.xlabel("Days. ")
    plt.ylabel("Mosquitoes/deaths. ")
    plt.title("Number of mosquitoes and death of humans per day. ")
    plt.show()


def main():
    if len(sys.argv) < 2:
        print("Usage: %s days_to_simulate" % days)
        return

    days = int(sys.argv[1])
    days_simulating = int(sys.argv[1])
    # malaria_grid = Grid(0.5, population=0.5)
    # printProgressBar(0, days_simulating, prefix = 'Progress:', suffix = 'Complete', length = 50)
    #
    # # Statistics
    # for i in range(days_simulating):
    #     malaria_grid.step()
    #     printProgressBar(i + 1, days_simulating, prefix = 'Progress:', suffix = 'Complete', length = 50)
    # malaria_grid.print_statistics()

    mosquitoe_fract = 0.4
    population_fract = 0.4

    plot_death_mosq(days_simulating, mosquitoe_fract, population_fract)


            # mean_infections, std_infections = [], []
            # for i in range(days_simulating):
            #     infections = []
            #     for human in malaria_grid.humans:
            #         infections.append(human.infections)
            #     mean_infections.append(np.mean(np.array(infections)))
            #     std_infections.append(np.std(infections))
            #     malaria_grid.step()
            #
            # plt.plot(range(days), mean_infections)
            # plt.show()

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
