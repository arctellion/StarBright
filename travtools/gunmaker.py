import pandas as pd
import numpy as np

cat = { 
    ## [code,type,tl,range,mass,B,H1,D1,v1,cr]
    #artillery
    1:  ['G', 'Gun',            6, 4,   9.0,  1, '*',      2, 2,  5000],
    2:  ['Ga','Gattling',       7, 4,  40.0,  2, '*',      3, 2,  8000],
    3:  ['C', 'Cannon',         6, 6, 200.0,  4, '*',      4, 2, 10000],
    4:  ['aC','Autocannon',     8, 6, 300.0,  4, '*',      5, 3, 30000],
    #longguns
    5:  ['R', 'Rifle',          5, 5,   4.0,  0, 'Bullet', 2, 2,   500],
    6:  ['Ca','Carbine',        5, 4,   3.0, -1, 'Bullet', 1, 1,   400],
    #Handguns
    7:  ['P', 'Pistol',         5, 2,   1.1,  0, 'Bullet', 1, 1,   150],
    8:  ['R', 'Revolver',       4, 2,   1.25, 0, 'Bullet', 1, 1,   100],
    #Other weapons
    9:  ['S', 'Shotgun',        4, 2,   4.0,  0, 'Frag',   2, 2,   300],
    10: ['Mg','Machinegun',     6, 5,   8.0,  1, 'Bullet', 4, 4,  3000],
    11: ['Pj','Projector',      9, 0,   1.0,  0, '*',      1, 1,   300],
    12: ['D', 'Designator',     7, 5,  10.0,  1, '*',      1, 0,  2000],
    #Launchers
    13: ['L', 'Launcher',       6, 3,  10.0,  1, '*',      1, 0,  1000],
    14: ['mL','Multi-Launcher', 8, 5,   8.0,  1, '*',      1, 0,  3000]
}
artillery = {
    1: ['aF', 'Anti-Flyer', 4,6,6.0,0,'Frag',  1,'Blast',3,4,3.0],
    2: ['aT', 'Anti-Tank',  0,5,8.0,0,'Pen',   3,'Blast',3,6,2.0],
    3: ['A',  'Assault',    2,4,0.8,0,'Bang',  1,'Blast',2,3,1.5],
    4: ['F',  'Fusion',     7,4,2.3,0,'Pen',   4,'Burn', 4,8,6.0],
    5: ['G',  'Gauss',      7,4,0.9,0,'Bullet',3,'',     0,3,2.0],
    6: ['P',  'Plasma',     5,4,2.5,0,'Pen',   3,'Burn', 3,6,2.0]
}
longgun = {
    0:  ['',  'blank',      0,0,1.0, 0,'',      0,      '',    0,0,1.0],
    1:  ['Ac','Accelerator',4,0,0.6, 0,'Bullet',2,      '',    0,2,3.0],
    2:  ['A', 'Assault',    2,4,0.8, 0,'Blast', 2,      'Bang',1,3,1.5],
    3:  ['B', 'Battle',     1,5,1.0, 1,'Bullet',1,      '',    0,1,0.8],
    4:  ['C', 'Combat',     2,3,0.9, 0,'Frag',  2,      '',    0,2,1.5],
    5:  ['D', 'Dart',       1,4,0.6, 0,'Tranq', '1-2-3','',    0,1,0.9],
    6:  ['P', 'Poison Dart',1,4,1.0, 0,'Poison','1-2-3','',    0,1,0.9],
    7:  ['G', 'Gauss',      7,0,0.9, 0,'Bullet',3,      '',    0,3,2.0],
    8:  ['H', 'Hunting',    0,3,0.9,-1,'Bullet',1,      '',    0,1,1.2],
    9:  ['L', 'Laser',      5,0,1.2, 0,'Burn',  2,      'Pen', 2,4,6.0],
    10: ['Sp','Splat',      2,4,1.3, 1,'Bullet',1,      '',    0,1,2.4],
    11: ['S', 'Survival',   0,2,0.5, 0,'Bullet',1,      '',    0,1,1.2]
}
handgun ={
    0: ['',  'blank',      0,0,1.0,0,'',      0,'',   0,0,1.0],
    1: ['Ac','Accelerator',4,0,0.6,0,'Bullet',2,'',   0,2,3.0],
    2: ['L', 'Laser',      5,0,1.2,0,'Burn',  2,'Pen',2,4,6.0],
    3: ['M', 'Machine',    0,2,1.2,0,'Bullet',2,'',   0,0,1.5],
    4: ['G', 'Gauss',      8,+3,0.6,0,'Bullet',3,'',   0,3,4.0]
}
shot = {
    0: ['', 'blank',  0,0,1.0,0,'',      0,'',     0,0,1.0],
    1: ['A','Assault',2,4,0.8,0,'Bang',  1,'Blast',2,3,2.0],
    2: ['H','Hunting',0,3,0.9,0,'Bullet',1,'',     0,1,1.2]
}
mg = {
    0: ['',  'blank',     0,0,1.0,0,'',       0,'',     0, 0,1.0],
    1: ['aF','Anti-Flyer',4,6,6.0,0,'Frag',   1,'Blast',3, 4,3.0],
    2: ['A', 'Assault',   2,4,0.8,0,'Bang',   1,'Blast',2, 3,2.0],
    3: ['S', 'Sub',      -1,3,0.3,0,'Bullet',-1,'',     0,-1,0.9]
}
spray = {
    0: ['A','Acid',      0,3,1.0,1,'Corrode',     2, 'Pen',   '1-2-3',      4,3.0],
    1: ['H','Fire',      0,1,0.9,0,'Burn',   '1-2-3','Pen',   '1-2-3','2-4-6',2.0],
    2: ['P','Poison Gas',0,2,1.0,0,'Gas',    '1-2-3','Poison','1-2-3','2-4-6',3.0],
    3: ['S','Stench',    3,2,0.4,0,'Stench', '1-2-3','',            0,'1-2-3',1.2]
}
exotic = {
    0: ['Emp','EMP',     1,3,1.0,0,'EMP',  '1-2-3','',         0,       1, 4.0],
    1: ['F','Flash',    -1,2,0.5,0,'Flash','1-2-3','',         0,       2, 1.5],
    2: ['C','Freeze',    1,3,1.0,1,'Cold', '1-2-3','',         0,       2, 3.0],
    3: ['G','Grav',      5,2,3.0,0,'Grav', '1-2-3','',         0,       3,20.0],
    4: ['L','Laser',     5,0,1.2,0,'Burn', '1-2-3','Pen', '1-2-3','2-4-6', 6.0],
    5: ['M','Mag',       4,1,2.0,0,'EMP',  '1-2-3','Mag', '1-2-3','2-4-6',15.0],
    6: ['Psi','Psi Amp', 4,2,1.0,0,'Psi',  '1-2-3','',          0,'1-2-3', 9.0],
    7: ['R','Rad',       1,4,1.0,2,'Rad',  '1-2-3','',          0,'1-2-3', 8.0],
    8: ['Sh','Shock',    0,2,0.5,0,'Elec', '1-2-3','Pain','1-2-3','2-4-6', 2.0],
    9: ['S','Sonic',     3,2,0.6,0,'Sound','1-2-3','Bang','1-2-3','2-4-6', 1.1]
}
launcher = {
    0: ['aF', 'AF Missile', 4,7,4.0,0,'Frag',2,'Blast',3,5,3.0],
    1: ['aT', 'AT Missile', 3,4,1.0,1,'Frag',2,'Pen',  3,5,2.0],
    2: ['Gr', 'Grenade',    1,4,0.8,0,'Frag',2,'Blast',2,4,1.0],
    3: ['M',  'Missile',    1,6,2.2,0,'Frag',2,'Pen',  2,4,5.0],
    4: ['RAM','RAM Grenade',2,6,1.0,0,'Frag',2,'Blast',2,4,3.0],
    5: ['R',  'Rocket',     1,5,3.0,0,'Frag',2,'Pen',  2,4,1.0]
}

burden = {
    0: ['',   'blank',          0, 0, 1.0, 0,'',0, 0,'',                    0,1.0],
    1: ['aD', 'Anti-Designator',3,+1, 3.0, 3,'',0, 1,'Not Pitols, Shotguns',0,3.0],
    2: ['B',  'Body',           2, 1, 0.5,-4,'',0,-1,'Only Pistols',        0,3.0],
    3: ['D',  'Disposable',     3, 0, 0.9,-1,'Q= -2',0, 0,'',               0,0.5],
    4: ['H',  'Heavy',          0, 1, 1.3, 3,'',0, 1,'Not Lasers',          0,2.0],
    5: ['Lt', 'Light',          0,-1, 0.7,-1,'',0,-1,'Not Lasers',          0,1.1],
    6: ['M',  'Magnum',         1, 1, 1.1, 1,'',0, 1,'Only Pistols',        0,1.1],
    7: ['M',  'Medium',         0, 0, 1.0, 0,'',0, 0,'Not Pistols',         0,1.0],
    8: ['R',  'Recoilless',     1, 1, 1.2, 0,'',0, 1,'',                    0,3.0],
    9: ['Sn', 'Snub',           1, 2, 0.7,-3,'',0, 1,'',                    0,1.5],
    10:['Vh', 'Very Heavy',     0, 5, 4.0, 4,'',0, 5,'',                    0,5.0],
    11:['Vl', 'Very Light',     1,-2, 0.6,-2,'',0,-1,'',                    0,2.0],
    12:['VrF','VRF',            2, 0,14.0, 5,'',0, 1,'Only Guns and MGs',   0,9.0]
}
stage = {

}
user = {

}
portability = {

}

def gunmaker():
    gun = ""
    print("ID | Code | Descriptor")
    for key in cat:
        print("{:^3}|{:^6}| {:<}".format(key,cat[key][0],cat[key][1]))
    
    while True:
        try:
            choose = int(input("Choose Weapon Type [1-14]:"))
        except ValueError:
            print("Invalid input!")
            continue
        if choose <= 0 or choose >14:
            print("Please choose from between 1 and 14.")
            continue
        else:
            break
    print(cat[choose])
    return gun