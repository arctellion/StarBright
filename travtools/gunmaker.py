import pandas as pd
import numpy as np

cat = { 
    ## [code,type,tl,range,mass,B,H1,D1,v1,cr]
    #artillery
    1: ['G', 'Gun', 6, 4, 9.0, 1, '*', 2, 2, 5000],
    2: ['Ga', 'Gattling', 7, 4, 40.0, 2, '*', 3, 2, 8000],
    3: ['C', 'Cannon', 6, 6, 200.0, 4, '*', 4, 2, 10000],
    4: ['aC', 'Autocannon', 8, 6, 300.0, 4, '*', 5, 3, 30000],
    #longguns
    5: ['R', 'Rifle', 5, 5, 4.0, 0, 'Bullet', 2, 2, 500],
    6: ['Ca', 'Carbine', 5, 4, 3.0, -1, 'Bullet', 1, 1, 400],
    #Handguns
    7: ['P', 'Pistol', 5, 3, 1.1, 0, 'Bullet', 1, 1, 150],
    8: ['R', 'Revolver', 4, 2, 1.25, 0, 'Bullet', 1, 1, 100],
    #Other weapons
    9: ['S', 'Shotgun', 4, 2, 4.0, 0, 'Frag', 2, 2, 300]
}

def gunmaker():
    gun = ""
    return gun