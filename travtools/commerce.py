import numpy as np
import travtools.converters as cnv
import travtools.system as sy
import travtools.dice as dd

#trade
def trade_gds(n, skill = {"Steward":0, "Admin":0, "Streetwise":0, "Liaison":0}, broker = 0, days = 7):
    """
    Generate trade goods for a given UWP. Using skills, skill, where skill is {Steward, Admin, Streetwise, Liaison} defaults = 0, for given broker, default = 0, for a given number of days default = 7.
    """

    pop = cnv.ext_dec(n[4])
    trade = sy.fun_trade(n)

    admin = skill["Admin"]
    street = skill["Streetwise"]
    steward = skill["Steward"]
    liaise = skill["Liaison"]

    high = dd.flux() + pop + steward
    mid = dd.flux() + pop + admin
    low = dd.flux() + pop + street
    
    i = 0
    freight = []
    cargo = []
    while i < days:
        freight[i] = dd.flux() + pop
        cargo[i] = 100
        i += 1