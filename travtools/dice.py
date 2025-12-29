import numpy as np
import random

def flux():
    """Rolls flux dice. 1d6 - 1d6, giving range -5 to +5.
    Returns total as int.
    """
    return die_roll() - die_roll()

def flux_detailed():
    """Rolls flux dice. 1d6 - 1d6.
    Returns (total, [d1, d2])
    """
    d1 = die_roll()
    d2 = die_roll()
    return d1 - d2, [d1, d2]

def dice(n):
    """Rolls a number (n) of 6 sided dice and returns total as int."""
    return sum([die_roll() for _ in range(n)])

def dice_detailed(n):
    """Rolls a number (n) of 6 sided dice and returns (total, [individual_rolls])."""
    rolls = [die_roll() for _ in range(n)]
    return sum(rolls), rolls

def die_roll():
    """Rolls a single d6."""
    return random.randint(1, 6)