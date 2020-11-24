import numpy as np

def flux():
    """Rolls flux dice. 1d6 - 1d6, giving range -5 to +5"""

    result = 0
    result = die_roll() - die_roll()
    return result

def dice(n):
    """Rolls a number (n) of 6 sided dice and returns the total."""

    result = 0
    for i in range(n):
        result += die_roll()
    return result

def die_roll():
    """Rolls a d6"""

    result = 0
    result = np.random.randint(1, 7)
    return result