import random


def is_close(a, b, tol=1e-5):
    return abs(a - b) < tol


def choose_random_concept(concepts):
    return random.choice(concepts)