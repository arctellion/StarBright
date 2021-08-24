import numpy as np
import travtools.converters as cnv
import travtools.system as sy
import travtools.dice as dd

#trade
def trade_gds(n, skill = {'Steward':0, 'Admin':0, 'Streetwise':0, 'Liaison':0}, broker = 0, days = 7):
    """
    Generate trade goods for a given UWP. Using skills, skill, where skill is {Steward, Admin, Streetwise, Liaison} defaults = 0, for given broker, default = 0, for a given number of days default = 7.
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
    
    trd = "During the last " + str(days) + " you find:\n"
    trd = trd + "* High Passengers: " + str(high) + "\n"
    trd = trd + "* Middle Passengers: " + str(mid) + "\n"
    trd = trd + "* Low Passengers: " + str(low) + "\n---\n"
    trd = trd + "\n* Freight (lots): ".join(map(str,freight)) + "\n"
    trd = trd + "\n* Spec Cargo: ".join(map(str, cargo)) + "\n"
    #trd = trd + "\n".join(map(str, trades))

    return trd