import numpy as np
import travtools.converters as cnv
import travtools.dice as dd

def fun_uwp(n):
  """
  Generates a UWP (Universal World Profile), based on Traveller 5.1 generation rules.

  Takes argument n, as a seed number to ensure that the generation process is repeatable for a given value of n.
  """

  #random seed set
  np.random.seed(1000 + n) # + 123456) add back in for sim
  # Starport
  starport = { 2: "A", 3: "A", 4:"A", 5:"B", 6:"B", 7:"C", 8:"C", 9:"D", 10:"E", 11:"E", 12:"X"}
  sprt = starport[dd.dice(2)]

  # Size 0-15
  sze = dd.dice(2) - 2
  if sze < 0:
    sze = 0
  elif sze == 10:
    sze = dd.die_roll() + 9

  # atmosphere 0-15
  atm = dd.flux() + sze
  if sze == 0:
    atm = 0
  if atm < 0:
    atm = 0
  elif atm > 15:
    atm = 15

  # Hydrographics 0-10
  hyd = dd.flux() + atm
  if sze < 2:
    hyd = 0
  elif (atm < 2 | atm > 9):
    hyd = hyd - 4
  if hyd < 0:
    hyd = 0
  elif hyd > 10:
    hyd = 10

  # Population 0-15
  pop = dd.dice(2) - 2
  if pop == 10:
    pop = dd.dice(2) + 3

  # Government 0-15
  gov = dd.flux() + pop
  if gov < 0:
    gov = 0
  elif gov > 15:
    gov = 15

  # Law level 0-18
  law = dd.flux() + gov
  if law < 0:
    law = 0
  elif law > 18:
    law = 18
  law = cnv.ext_hex(law)

  #Tech Level 0+
  tech = dd.die_roll()
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

def fun_pbg(uwp):
  """
  Generate the Population Digit, Gas Giants & Asteroid Belts
  
  Arguments, uwp the UWP to process to get population digit.
  """
  
  p = cnv.ext_dec(str(uwp[4]))
  pop = 0
  if p == 0:
    pop = 0
  else:
    pop = dd.dice(2) - 3
    if pop < 1:
      pop = 1
  belt = dd.die_roll() - 3
  if belt < 0:
    belt = 0
  gas = round(dd.dice(2) / 2) - 2
  if gas < 0:
    gas = 0
  pbg = str(pop)+str(belt)+str(gas)
  return pbg

def fun_trade(n):
  """Generate Trade Classifications for a given UWP n"""
  siz = cnv.ext_dec(n[1])
  atm = cnv.ext_dec(n[2])
  hyd = cnv.ext_dec(n[3])
  pop = cnv.ext_dec(n[4])
  gov = cnv.ext_dec(n[5])
  law = cnv.ext_dec(n[6])
  tc = ""
  #print("UWP: ", n, "\nSize: ", siz, "| Atmo: ", atm, "| Hydro: ", hyd, "| Pop: ", pop, "| Gov: ", gov, "| Law: ", law, "\n")
  ## Planetary Trade Codes
  #As - Siz 0, Atm 0, Hyd 0
  if siz == 0 and atm == 0 and hyd == 0:
    tc += "As "
  #De - Atm 2-9, Hydro 0
  if atm in [2,3,4,5,6,7,8,9] and hyd == 0:
    tc += "De "
  #Fl - Atm 10-12, Hydro 1-10
  if atm in [10,11,12] and hyd in [1,2,3,4,5,6,7,8,9,10]:
    tc += "Fl "
  #Ga - siz 678, atm 568, hyd 567
  if siz in [6,7,8] and atm in [5,6,7,8] and hyd in [5,6,7]:
    tc += "Ga "
  #He - siz 3-12, atm 2479101112, Hydro 012
  if siz in [3,4,5,6,7,8,9,10,11,12] and atm in [2,4,7,9,10,11,12] and hyd in [0,1,2]:
    tc += "He "
  #Ic - Atm 0,1, Hydro 1-10
  if atm in [0,1] and hyd in [1,2,3,4,5,6,7,8,9,10]:
    tc += "Ic "
  #Oc- siz 10-15, atm 3456789 13 14 15, hydro 10
  if siz in [10,11,12,13,14,15] and atm in [3,4,5,6,7,8,9,13,14,15] and hyd == 10:
    tc += "Oc "
  #Va - Atm 0
  if atm == 0:
    tc += "Va "
  #Wa - siz 3456789, atm 3456789 13 14 15, hydro 10
  if siz in [3,4,5,6,7,8,9] and atm in [3,4,5,6,7,8,9,13,14,15] and hyd == 10:
    tc += "Wa "
  ##---##
  ## Population Trade Codes
  #Ba - Pop 0, Gov 0, Law 0
  if pop == 0 and gov == 0 and law == 0:
    tc += "Ba "
  #Lo - Pop 1-3
  if pop in [1,2,3]:
    tc += "Lo "
  #Ni - Pop 4-6
  if pop in [4,5,6]:
    tc += "Ni "
  #Ph - Pop 8
  if pop == 8:
    tc += "Ph "
  #Hi - Pop 9-15
  if pop in [9,10,11,12,13,14,15]:
    tc += "Hi "
  ##---##
  ## Economic Trade Codes
  #Pa - Atm 4-9, Hydro 4-8, Pop 4,8
  if atm in [4,5,6,7,8,9] and hyd in [4,5,6,7,8] and pop in [4,8]:
    tc += "Pa "
  #Ag - Atm 4-9, Hyd 4-8, Pop 5-7
  if atm in [4,5,6,7,8,9] and hyd in [4,5,6,7,8] and pop in [5,6,7]:
    tc += "Ag "
  #Na - Atm 0-3, Hydo 0-3, Pop: 6-15
  if atm in [0,1,2,3] and hyd in [0,1,2,3] and pop in [6,7,8,9,10,11,12,13,14,15]:
    tc += "Na "
  #Px - Atm 231011, hyd 1-5, pop 3-6, law 6789
  if atm in [2,3,10,11] and hyd in [1,2,3,4,5] and pop in [3,4,5,6] and law in [6,7,8,9]:
    tc += "Px "
  #Pi - atm 012479, pop 78
  if atm in [0,1,2,4,7,9] and pop in [7,8]:
    tc += "Pi "
  #In - Atm 012,4,7,9,10-12, Pop: 9-15
  if atm in [0,1,2,4,7,9,10,11,12] and pop in [9,10,11,12,13,14,15]:
    tc += "In "
  #Po - Atm 2-5, Hydro 0-3
  if atm in [2,3,4,5] and hyd in [0,1]:
    tc += "Po "
  #Pr - Atm 6,8, Pop 5,9
  if atm in [6,8] and pop in [5,9]:
    tc += "Pr "
  #Ri - Atm 6,8, Pop 6-8
  if atm in [6,8] and pop in [6,7,8]:
    tc += "Ri "
  ##---##
  ## Other Trade Codes
  #Re - pop 0-4. gov 6, law 0,4,5
  if pop in [0,1,2,3,4] and gov == 6 and law in [0,4,5]:
    tc += "Re "
  #Cy - Pop 5-10, gov 6, law 0-3
  if pop in [5,6,7,8,9,10] and gov == 6 and law in [0,1,2,3]:
    tc += "Cy "
  #Da - Pop 0-6
  if pop in [0,1,2,3,4,5,6]:
    tc += "Da "
  #Pz - pop 7-15
  if pop in [7,8,9,10,11,12,13, 14,15]:
    tc += "Pz "
  return tc.strip()
    
def fun_ext(uwp,pbg,bases,trade):
  """
  Generates the Extended Profile for a planet {Ix}(Ex)[Cx].
  
  Takes as variables, UWP, Pop-belt-gas giant, bases list, Trade Codes
  
  Importance (Ix)
  Economic (Ex) - (RLI+E)
  R - Resources, L - Labour, I - Infrastruture, E - Efficiency
  Cultural (Cx) - [HASS]
  H - Heterogeneity, A - Acceptance, S - Strangeness, S - Symbols
  """
  #Importance
  i = 0
  sport = str(uwp[0])
  bases = str(bases)
  tech = cnv.ext_dec(str(uwp[-1]))
  pop = cnv.ext_dec(str(uwp[4]))
  sprt_fac = {"A": 1, "B": 1, "C": 0, "D": -1, "E": -1, "X": -1}
  i += sprt_fac[sport]
  if (tech > 15):
    i += 1
  elif (tech > 9):
    i += 1
  elif (tech < 9):
    i -= 1
  if (pop < 7):
    i -= 1
  if (bases == "NS"):
    i += 1
  if "Ag" in trade:
    i += 1
  if "Hi" in trade:
    i += 1
  if "In" in trade:
    i += 1
  if "Ri" in trade:
    i += 1    
  if i > 5:
    i = 5
  if i < -3:
    i = -3
  ix = "{"
  if i > -1:
    ix += "+"+str(i)+"}"
  else:
    ix += str(i)+"}"
  ##Economic
  belt = int(str(pbg[1]))
  gas = int(str(pbg[2]))
  ex = ""
  r = dd.dice(2)
  if (tech > 7):
    r = r + belt + gas
  l = pop - 1
  if (l < 0):
    l = 0
  if (pop == 0):
    inf = 0
  elif (0 < pop < 4):
    inf = i
  elif (3 < pop < 7):
    inf = i + dd.die_roll()
  elif (pop > 6):
    inf = i + dd.dice(2)
  if inf < 0: 
    inf = 0
  e = dd.flux()
  ex = "("+str(cnv.ext_hex(r))+str(cnv.ext_hex(l))+str(cnv.ext_hex(inf))
  if (e >= 0):
    ex = ex + "+"+str(e)+")"
  else: 
    ex = ex + str(e) + ")"
  ##Cultural
  h = pop + dd.flux()
  a = pop + i
  s = dd.flux() + 5
  sy = dd.flux() + tech
  if (pop == 0):
    h = a = s = sy = 0
  if (h < 1):
    h = 1
  if (a < 1):
    a = 1
  if (s < 1):
    s = 1
  if (sy < 1): 
    sy = 1
  cx = "[" + str(cnv.ext_hex(h)) + str(cnv.ext_hex(a)) + str(cnv.ext_hex(s)) + str(cnv.ext_hex(sy)) + "]"
  return (ix + ex + cx)
    
def fun_bases(uwp):
  """
  Generate Navy & Scout Bases

  Navy - Sport Class 2d - A: 6 or less , B: 5 or less.
  Scout - Sport Class 2d - A: 4 or less, B: 5 or less, C: 6 or less, D: 7 or less.
  """
  base = ""
  sport = str(uwp[0])
  roll=dd.dice(2)
  nvy = {"A": 6, "B": 5, "C": 0, "D": 0, "E": 0, "X": 0}
  sct = {"A": 4, "B": 5, "C": 6, "D": 7, "E": 0, "X": 0}
  if (nvy[sport] > 0):
    if (roll <= nvy[sport]):
      base += "N"
  if (sct[sport] > 0):
    if (roll <= sct[sport]):
      base += "S"
  return base
