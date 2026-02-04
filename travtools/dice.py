"""
Dice rolling utility for Traveller games.
Provides functions for standard d6 rolls, flux rolls, and parsing roll strings.
"""
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

def roll_string(s):
    """
    Parses and rolls a string like '2d6+3' or '1d6'.
    Returns (total, [individual_rolls], modifier)
    """
    import re
    s = s.lower().replace(" ", "")
    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", s)
    if not match:
        raise ValueError("Invalid dice format. Use XdY+Z")
    
    num_dice = int(match.group(1))
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    return total, rolls, modifier