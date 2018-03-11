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
from pyics import Model

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

class CASim(Model):
    def __init__(self):
        Model.__init__(self)

        self.t = 0
        self.rule_set = []
        self.config = None

        self.make_param('r', 1)
        self.make_param('k', 2)
        self.make_param('width', 50)
        self.make_param('height', 50)
        self.make_param('rule', 30, setter=self.setter_rule)

    def setter_rule(self, val):
        """Setter for the rule parameter, clipping its value between 0 and the
        maximum possible rule number."""

        rule_set_size = self.k ** (2 * self.r + 1)
        max_rule_number = self.k ** rule_set_size
        return max(0, min(val, max_rule_number - 1))

    def build_rule_set(self):
        """Sets the rule set for the current rule.
        A rule set is a list with the new state for every old configuration.

        For example, for rule=34, k=3, r=1 this function should set rule_set to
        [0, ..., 0, 1, 0, 2, 1] (length 27). This means that for example
        [2, 2, 2] -> 0 and [0, 0, 1] -> 2."""

        base = decimal_to_base_k(self.rule, self.k)
        nzeros = self.k ** (2*self.r +1) - len(base)
        self.rule_set = [0 for i in range(nzeros)] + base

    def check_rule(self, inp):
        """Returns the new state based on the input states.

        The input state will be an array of 2r+1 items between 0 and k, the
        neighbourhood which the state of the new cell depends on."""

        return self.rule_set[int(len(self.rule_set)-base_to_decimal(inp,
        self.k)-1)]

    def setup_initial_row(self):
        """Returns an array of length `width' with the initial state for each of
        the cells in the first row. Values should be between 0 and k."""

        return np.random.random_integers(0, self.k-1, self.width)

    def setup_initial_array(self, n):
        """Returns an matrix of n initial rows's with the first two rows set as
        basecases. """

        return np.random.randint((self.k), size=(n, self.width))

    def initial_row_dens(self, d, width=0):
        """Returns an array of length width based on the density of cars (1s).
        """

        if d > 1:
            print("The density cannot be greater than zero. ")
            return False

        if width == 0:
            w = self.width
        else:
            w = width

        initial_row = [0] * int(w)
        for i in range(int(d*w)):
            initial_row[i] = 1
        np.random.shuffle(initial_row)
        return initial_row

    def reset(self):
        """Initializes the configuration of the cells and converts the entered
        rule number to a rule set."""

        self.t = 0
        self.config = np.zeros([self.height, self.width])
        self.config[0, :] = self.setup_initial_row()
        self.build_rule_set()

    def draw(self, title=""):
        """Draws the current state of the grid."""

        import matplotlib
        import matplotlib.pyplot as plt

        plt.cla()
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.imshow(self.config, interpolation='none', vmin=0, vmax=self.k - 1,
                cmap=matplotlib.cm.binary)
        plt.axis('image')
        plt.title(title)
        plt.show()

    def step(self):
        """Performs a single step of the simulation by advancing time (and thus
        row) and applying the rule to determine the state of the cells."""

        self.t += 1
        if self.t >= self.height:
            return True

        for patch in range(self.width):
            # We want the items r to the left and to the right of this patch,
            # while wrapping around (e.g. index -1 is the last item on the row).
            # Since slices do not support this, we create an array with the
            # indices we want and use that to index our grid.
            indices = [i % self.width
                    for i in range(patch - self.r, patch + self.r + 1)]
            values = self.config[self.t - 1, indices]
            self.config[self.t, patch] = self.check_rule(values)
        return self.config

    def states(self, rule, width, height, density = 0, initial_state=[]):
        """Performs a single step of the simulation by advancing time (and thus
        row) and applying the rule to determine the state of the cells."""

        self.width, self.height, self.rule = width, height, rule
        self.reset()

        if density > 0:
            self.config[0, :] = self.initial_row_dens(density)
        if len(initial_state) > 0:
            self.config[0, :] = initial_state
        state_transition = []
        for i in range(self.height):
            state = self.step()
            if state is True:
                break
            else:
                str_state = ''.join(map(str, state[i].astype(int)))
                state_transition.append(str_state)

        return state_transition

    def densities(self, states):
        """Returns given the transition states the densities."""

        cars_dict, cars = {}, []
        for s in state_transition:
            cars_dict[s] = list(s).count('1')
            cars.append(list(s).count('1'))

        car_dens = [float(x/sim.width) for x in cars]
        return cars_dict, car_dens

    def car_flow(self, initial_state, N, T):
        """" Number of ones that cross the system boundary on the rigth-hand
        side per unit time. Look how often the last cell changes from a 1 to a 0.
        This represents a measurement that we can compute on a (simulated)
        experiment. """

        transition_states = self.states(184, N, T, 0, initial_state)
        change = 0
        for i in range(1, T-1):
            if (int(transition_states[i-1][-1]) -
            int(transition_states[i][-1])) == -1:
                change += 1
        return change/T

    def plot_car_flow(self, densities, N, T, R, title="", show=True):
        """" This function plots the densties against the car flow. """

        average_flows = []
        for d in densities:
            flows = []
            for i in range(R):
                initial_state = self.initial_row_dens(d, N)
                flow = self.car_flow(initial_state, N, T)
                flows.append(flow)
            flows = np.array(flows)
            average_flow = np.mean(flows)
            average_flows.append(average_flow)
        if show is True:
            plt.plot(densities, average_flows)
            plt.xlabel("Densitity")
            plt.ylabel("Car flow")
            plt.title(title)
            plt.show()
        return densities, average_flows

    def transition_position(self, car_flow, densities):
        """" This function takes the ”car flow versus density” data points and
        returns the critical density = an automatically estimated ’position’
        of the phase transition. """

        import operator

        index_flow, max_flow = max(enumerate(car_flow),
        key=operator.itemgetter(1))
        max_dens = densities[index_flow]
        return (max_flow, max_dens)

if __name__ == '__main__':
    from pyics import GUI
    import collections
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from random import randint
    from collections import Counter

    """" Setup the cellular automata: """
    sim = CASim()

    """ Q1: ECA rule 184 is known as the ’traffic rule’. Implement it; use
    periodic boundary conditions. """

    state_transition = sim.states(184, 50, 50)
    cars_dict, car_dens = sim.densities(state_transition)
    cars = range(len(car_dens))
    plt.plot(cars, car_dens)
    plt.title("Bottleneck-free congestion")
    plt.xlabel("Number of cars")
    plt.ylabel("Density")
    plt.show()

    """Q2: Show the evolution of a CA of size N = 50 cells for 50 time steps for
    the ’car’ densities 0.4 and 0.9. """

    states_f = sim.states(184, 50, 50, 0.4)
    cars_dict_f, car_dens_f = sim.densities(states_f)
    sim.draw("Evolution with N = 50, T = 50 and density = 0.4. ")

    states_n = sim.states(184, 50, 50, 0.9)
    cars_dict_n, car_dens_n = sim.densities(states_n)
    sim.draw("Evolution with N = 50, T = 50 and density = 0.9. ")

    """"Q4: Write a function which calculates a ’car flow’ value for a given
    initial state for the CA. Plot this car flow as function of the initial
    density of cars. For each density value there are multiple initial states
    generated and the average of the car flow for each initial state is plotted.
    """

    """ Density values in the range [0.0, 1.0] """
    densities = np.arange(0.0, 1.0, 0.02)
    densities, average_flows = sim.plot_car_flow(densities, 50, 1000, 10, "Average car flow per density value. T = 1000, N = 50, R = 10. ")
    (f,d) = sim.transition_position(average_flows, densities)

    """" Q5: Now plot the same graph but for a very low T (e.g., T = 5) and
    a very low number of initial conditions R per density value (e.g., R = 3).
    """

    sim.plot_car_flow(densities, 50, 5, 3, 'Average car flow per density value. T = 5, N = 50, R = 3.')

    """"Q6: Implement a function which takes the ”car flow versus density” data
    points of exercise 4 as input and returns an automatically estimated
    ’position’ (density value) of the phase transition as output
    (termed ’critical density’, a scalar).
    """
    c = 0
    probs = []
    real_d = 0.5
    correct = []
    Ts = range(1, 50, 5)
    Ds = []
    for t in Ts:
        dens, car_flow = sim.plot_car_flow(densities, 50, t, 10, show=False)
        (f,d) = sim.transition_position(car_flow, dens)
        Ds.append(d)
        if d >= (real_d-0.05) and d <= (real_d+0.05):
            c += 1
            correct.append((t,d))
        prob = c/10
        probs.append(prob)

    plt.plot(Ts, probs)
    plt.scatter(*zip(*correct))
    plt.title("Probability correct of the density based on the time T.")
    plt.xlabel("T")
    plt.ylabel("Probability correct of density")
    plt.legend(['The scattered points are the right estimated densities. '])
    plt.show()
