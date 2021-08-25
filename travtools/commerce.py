import numpy as np
import travtools.converters as cnv
import travtools.system as sy
import travtools.dice as dd

# spec price
def spec_price(n, t):
    """
    Generate base cost of speculative cargo for a given set of trade codes n, with tech level t.
    """
    cost = 3000
    cost += cnv.ext_dec(t) * 100
    
    for i in range(len(n)):
        if n[i] == 'Ag':
            cost -= 1000
        if n[i] == 'As':
            cost -= 1000
        if n[i] == 'Ba':
            cost += 1000
        if n[i] == 'De':
            cost += 1000
        if n[i] == 'Fl':
            cost += 1000
        if n[i] == 'Hi':
            cost -= 1000
        if n[i] == 'Ic':
            cost += 0
        if n[i] == 'In':
            cost -= 1000
        if n[i] == 'Lo':
            cost += 1000
        if n[i] == 'Na':
            cost += 0
        if n[i] == 'Ni':
            cost += 1000
        if n[i] == 'Po':
            cost -= 1000
        if n[i] == 'Ri':
            cost += 1000
        if n[i] == 'Va':
            cost += 1000

    return cost

#trade
def trade_gds(n, skill = {'Steward':0, 'Admin':0, 'Streetwise':0, 'Liaison':0}, days = 7):
    """
    Generate trade goods for a given UWP. Using skills, skill, where skill is {Steward, Admin, Streetwise, Liaison} defaults = 0, for a given number of days default = 7.
    """
    
    pop = cnv.ext_dec(n[4])
    tech = n[8]
    trade = sy.fun_trade(n)
    trades = trade.split()

    admin = skill['Admin']
    street = skill['Streetwise']
    steward = skill['Steward']
    liaise = skill['Liaison']

    high = dd.flux() + pop + steward
    mid = dd.flux() + pop + admin
    low = dd.flux() + pop + street
    
    i = 0
    freight = ['None']*days
    cargo = [100]*days
    while i < days:
        freight[i] = dd.flux() + pop
        i += 1
    frt = ", ".join(map(str,freight))
    cgo = ", ".join(map(str,cargo))
    trd = "During the last {} days you find:\n".format(days)
    trd = trd + "* High Passengers: {}\n".format(high)
    trd = trd + "* Middle Passengers: {}\n".format(mid)
    trd = trd + "* Low Passengers: {}\n---\n".format(low)
    trd = trd + "* Freight (lots): {} \n".format(frt)
    trd = trd + "* Spec Cargo: {} \n".format(cgo)
    tc = " ".join(map(str, trades))
    cost = spec_price(trades, tech)
    crgo = "{} - {} Cr{}".format(tech, tc, cost)
    trd = trd + "* Spec Cargo Cost: {}".format(crgo)

    return trd