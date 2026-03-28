import random


def should_explore(epsilon=0.15):
    return random.random() < epsilon