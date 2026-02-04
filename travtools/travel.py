"""
Travel time calculation module for interplanetary travel.
Uses simplified physics formulas for Traveller gameplay.
"""
import math as m

def calculate_travel_time(a_dia, p_dia, s_spd):
    """
    Calculates estimated travel time in hours.
    Formula: sqrt( (2*d) / a ) simplified for Traveller play.
    """
    try:
        # Time in hours: sqrt( (a_dia * p_dia) / (s_spd * 32400) )
        # 32400 is a constant factor for G to m/h^2 conversion or similar heuristic used in the original app.py
        time = m.sqrt((a_dia * p_dia) / (s_spd * 32400))
        hr = int(time)
        mins = int((time - hr) * 60)
        return hr, mins
    except Exception:
        return None, None
