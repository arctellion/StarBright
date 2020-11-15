import random

def flux():
    """Rolls flux dice. 1d6 - 1d6, giving range -5 to +5"""

    result = 0
    result = die_roll(1) - die_roll(1)
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
    result = random.randint(1, 6)
    return result

def ext_hex(n):
    """Converts decimal into extended Hexadecimal"""
    
    result = ""
    if n < 16 {
        result = "%X" % n
    elif n == 16:
        result = "G"
    elif n == 17:
        result = "H"
    elif n == 18:
        result = "J"
    elif n == 19:
        return "K")
    elif n == 20:
        result = "L"
    return result


def ext_dec(n):
    """Converts an extended hex string back into integers.""""

    result = 0
    try: 
        result = int(n, 16)
    except:
        if n == "G":
            result = 16
        elif n == "H":
            result = 17
        elif  n == "J":
            result = 18
        elif n == "K":
            result = 19
        elif n == "L":
            result = 20
    
    return result

starport = { 2: "A", 3: "A", 4:"A", 5:"B", 6:"B", 7:"C", 8:"C", 9:"D", 10:"E", 11:"E", 12:"X"}

fun_uwp(n):
  #random seed set
  random.seed(1000 + n)
  # Starport
  sprt <- starport[dice(2)]
  # Size 0-15
  sze <- dice(2) - 2
  if sze < 0:
    sze = 0
  elif sze == 10:
    sze = die_roll() + 9
  # atmosphere 0-15
  atm = flux() + sze
  if sze == 0:
    atm = 0
  if atm < 0:
    atm = 0
  elif atm > 15:
    atm <- 15

  # Hydrographics 0-10
  hyd = dice.flux() + atm
  if sze < 2:
    hyd = 0
  elif (atm < 2 || atm > 9):
    hyd = hyd - 4
  if hyd < 0:
    hyd = 0
  elif hyd > 10:
    hyd = 10

  # Population 0-15
  pop = dice.sum(2) - 2
  if pop == 10:
    pop = dice.sum(2) + 3

  # Government 0-15
  gov = flux() + pop
  if gov < 0:
    gov = 0
  elif gov > 15:
    gov = 15

  # Law level 0-18
  law <- flux() + gov
  if law < 0:
    law = 0
  elif law > 18:
    law = 18
  law = ext_hex(law)

  #Tech Level 0+
  tech = dice_roll()
  #starport factor
  sprt_fct = { "A": 6, "B": 4, "C": 2, "D": 0, "E": 0, "X": -4}
  tech = tech + sprt_fct[sprt]
  #size factor
  sze_fct = { 0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,14: 0,15: 0}
  tech = tech + sze_fct()
  #atmo factor
  atm_fct = {0: 1, 1: 1,  2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
  tech = tech + atm_fct[atm]
  #hydro factor
  hyd_fct = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0 ,5: 0, 6: 0. 7: 0, 8: 0, 9: 1, 10: 2}
  tech = tech + hyd_fct[hyd]
  #gov factor
  if (gov == 0 || gov == 5):
    tech = tech + 1
  elif (gov == 13):
    tech <- tech - 2



































































































    
  #print(tech)
  if(identical(tech, numeric(0))) { 
    tech <- 1
  }
  if (tech < 0){
    tech <- 0
  }
  return (sprintf("%s%X%X%X%X%X%s-%s", sprt, sze, atm, hyd, pop, gov, law, ext.hex(tech)))
}