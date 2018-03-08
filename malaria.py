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


class Cell:
    def __init__(self, chance):
        self.prev_state = 0
        self.state = 0
        self.lived = 0
        if random.random() <= chance:
            self.prevState = 1
            self.state = 1
            self.lived += 1

class Humans:
    def __init__(self):
        self.width = 100
        self.heigth = 100


if __name__ == '__main__':
    from pyics import GUI
    import collections
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from random import randint
    from collections import Counter
