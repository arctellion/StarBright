import numpy as np
import travtools.converters as cnv
import travtools.dice 

def fun_uwp(n):
  """
  Generates a UWP (Universal World Profile), based on Traveller 5.1 generation rules.

  Takes argument n, as a seed number to ensure that the generation process is repeatable for a given value of n.
  """

  #random seed set
  np.random.seed(1000 + n) # + 123456) add back in for sim
  # Starport
  starport = { 2: "A", 3: "A", 4:"A", 5:"B", 6:"B", 7:"C", 8:"C", 9:"D", 10:"E", 11:"E", 12:"X"}
  sprt = starport[dice.dice(2)]

  # Size 0-15
  sze = dice.dice(2) - 2
  if sze < 0:
    sze = 0
  elif sze == 10:
    sze = dice.die_roll() + 9

  # atmosphere 0-15
  atm = dice.flux() + sze
  if sze == 0:
    atm = 0
  if atm < 0:
    atm = 0
  elif atm > 15:
    atm = 15

  # Hydrographics 0-10
  hyd = dice.flux() + atm
  if sze < 2:
    hyd = 0
  elif (atm < 2 | atm > 9):
    hyd = hyd - 4
  if hyd < 0:
    hyd = 0
  elif hyd > 10:
    hyd = 10

  # Population 0-15
  pop = dice.dice(2) - 2
  if pop == 10:
    pop = dice.dice(2) + 3

  # Government 0-15
  gov = dice.flux() + pop
  if gov < 0:
    gov = 0
  elif gov > 15:
    gov = 15

  # Law level 0-18
  law = dice.flux() + gov
  if law < 0:
    law = 0
  elif law > 18:
    law = 18
  law = cnv.ext_hex(law)

  #Tech Level 0+
  tech = die_roll()
  #starport factor
  sprt_fct = { "A": 6, "B": 4, "C": 2, "D": 0, "E": 0, "X": -4}
  tech = tech + sprt_fct[sprt]
  #size factor
  sze_fct = { 0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,14: 0,15: 0}
  tech = tech + sze_fct[sze]
  #atmo factor
  atm_fct = {0: 1, 1: 1,  2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
  tech = tech + atm_fct[atm]
  #hydro factor
  hyd_fct = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0 ,5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 2}
  tech = tech + hyd_fct[hyd]
  #gov factor
  if (gov == 0 | gov == 5):
    tech = tech + 1
  elif (gov == 13):
    tech = tech - 2
  if tech < 0:
    tech = 0
  tech = cnv.ext_hex(tech)
  #output the data in std UWP format SpSzAtHyPoGoLa-Tc
  result = sprt + '%X%X%X%X%X' % (sze, atm, hyd, pop, gov) + law + '-' + tech
  return result

def fun_pbg(p):
  """
  Generate the Population Digit, Gas Giants & Asteroid Belts
  
  Arguments, p the UWP to process to get population digit.
  """
  
  p = cnv.ext_dec(p.str.slice(4,5))
  pop = 0
  if p == 0:
    pop = 0
  else:
    pop = dice.dice(2) - 3
    if pop < 1:
      pop = 1
  belt = dice.die_roll() - 3
  if belt < 0:
    belt = 0
  gas = round(dice.dice(2) / 2) - 2
  if gas < 0:
    gas = 0
  pbg = str(pop)+str(belt)+str(gas)
  return pbg

def fun_trade(n):
  """Generate Trade Classifications for a given UWP n"""
  siz <- ext_dec(n[1])
  atm <- ext_dec(n[2])
  hyd <- ext_dec(n[3])
  pop <- ext_dec(n[4])
  gov <- ext_dec(n[5])
  law <- ext_dec(n[6])
  print("UWP: ", n, "\nSize: ", siz, "| Atmo: ", atm, "| Hydro: ", hyd, "| Pop: ", pop, "| Gov: ", gov, "| Law: ", law, "\n")
  #Ag - Atm 5-9, Hyd 4-8, Pop 5-7
  #As - Siz 0, Atm 0, Hyd 0
  #Ba - Pop 0, Gov 0, Law 0
  #De - Atm 2-9, Hydro 0
  #Fl - Atm 10-12, Hydro 1-10
  #Hi - Pop 9-15
  #Ic - Atm 0,1, Hydro 1-10
  #In - Atm 0-4,7,9,10-12, Pop: 9-15
  #Lo - Pop 1-3
  #Na - Atm 0-3, Hydo 0-3, Pop: 6-15
  #Ni - Pop 4-6
  #Po - Atm 2-5, Hydro 0-3
  #Ri - Atm 6,8, Pop 6-8
  #Va - Atm 0

#Extended Profile {Ix} (Ex) [Cx]
#Importance (Ix)
#Starport Type A or B +1
#Starport D or worse -1
#Tech Level G or more +1
#Tech Level A or more +1
#Tech Level 8 or less -1
#Per Ag Hi In Ri +1
#If Pop 6 or less -1
#If Naval AND Scout Base +1
#If Way Station +1
#Important= +4 or greater.
#Unimportant= 0 or less.
#Economic (Ex)
#(RLI+E)
#R - Resources - 2D (if tech 8+, then +Gas Giants +Asteroid Belts) min 0
#L - Labour - Pop - 1 min 0 
#I - Infrastructure - Pop 0 = 0, Pop 1-3 = Ix, Pop 4-6 = 1D + Ix, Pop 7+ = 2D + Ix min 0
#E - Efficiency - Flux
#Cultrual (Cx)
#H - Pop + flux
#A - Pop + Ix
#S - flux + 5
#S - flux + TL
# if pop = 0, all = 0, if any less than 1, then = 1
def fun_ext(n):
  """
  Generates the Extended Profile for a planet {Ix}(Ex)[Cx].
  Importance (Ix)
  Economic (Ex) - (RLI+E)
  R - Resources, L - Labour, I - Infrastruture, E - Efficiency
  Cultural (Cx) - [HASS]
  H - Heterogeneity, A - Acceptance, S - Strangeness, S - Symbols
  """
  
  sport = n[0]
  tech = conv.ext_dec(n[-1])
  sprt_fac = {A: 1, B: 1, C: 0, D: -1, E: -1, X: -1}
  sx = sprt_fac[sport]
  tx = 0
  if (tech > 15):
    tx = tx + 1
  elif (tech > 10):
    tx = tx + 1
  elif (tech < 9):
    tx = tx - 1
  ix = sx + tx
  px = 0
  if (int(n[5],16) < 7):
    px = -1
