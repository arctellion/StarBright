# Chart 3: Category & Type
CHART_3_TYPES = {
    "Artillery": {
        "G": { "name": "Gun", "tl": 6, "range": 4, "mass": 9, "qrebs": "+1", "h1": "*", "d1": "2", "cost": 5000, "desc": "Artillery Gun" },
        "Ga": { "name": "Gatling", "tl": 7, "range": 4, "mass": 40, "qrebs": "+2", "h1": "*", "d1": "3", "cost": 8000, "desc": "Gatling" },
        "C": { "name": "Cannon", "tl": 6, "range": 6, "mass": 200, "qrebs": "+4", "h1": "*", "d1": "4", "cost": 10000, "desc": "Cannon" },
        "aC": { "name": "AutoCannon", "tl": 8, "range": 6, "mass": 300, "qrebs": "+4", "h1": "*", "d1": "5", "cost": 30000, "desc": "AutoCannon" }
    },
    "Long Guns": {
        "R": { "name": "Rifle", "tl": 5, "range": 5, "mass": 4, "qrebs": "0", "h1": "Bullet", "d1": "2", "cost": 500, "desc": "Rifle" },
        "C": { "name": "Carbine", "tl": 5, "range": 4, "mass": 3, "qrebs": "-", "h1": "Bullet", "d1": "1", "cost": 400, "desc": "Carbine" }
    },
    "Handguns": {
        "P": { "name": "Pistol", "tl": 5, "range": 2, "mass": 1.1, "qrebs": "0", "h1": "Bullet", "d1": "1", "cost": 150, "desc": "Pistol" },
        "Re": { "name": "Revolver", "tl": 4, "range": 2, "mass": 1.25, "qrebs": "0", "h1": "Bullet", "d1": "1", "cost": 100, "desc": "Revolver" }
    },
    "Shotguns": {
        "S": { "name": "Shotgun", "tl": 4, "range": 2, "mass": 4, "qrebs": "0", "h1": "Frag", "d1": "2", "cost": 300, "desc": "Shotgun" }
    },
    "Machineguns": {
        "Mg": { "name": "Machinegun", "tl": 6, "range": 5, "mass": 8, "qrebs": "+1", "h1": "Bullet", "d1": "4", "cost": 3000, "desc": "Machinegun" }
    },
    "Projectors": {
        "Pj": { "name": "Projector", "tl": 9, "range": 0, "mass": 1, "qrebs": "0", "h1": "*", "d1": "1", "cost": 300, "desc": "Projector" }
    },
    "Designators": {
        "D": { "name": "Designator", "tl": 7, "range": 5, "mass": 10, "qrebs": "+1", "h1": "*", "d1": "1", "cost": 2000, "desc": "Designator" }
    },
    "Launchers": {
        "L": { "name": "Launcher", "tl": 6, "range": 3, "mass": 10, "qrebs": "+1", "h1": "*", "d1": "1", "cost": 1000, "desc": "Launcher" },
        "mL": { "name": "Multi-Launcher", "tl": 8, "range": 5, "mass": 8, "qrebs": "+1", "h1": "*", "d1": "1", "cost": 3000, "desc": "Multi-Launcher" }
    }
}

# Chart 4: Descriptors
CHART_4_DESCRIPTORS = {
    "Artillery": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "aF": { "name": "Anti-Flyer", "tl": 4, "range": 6, "mass": 6.0, "qrebs": 0, "h2": "Frag", "d2": "1", "h3": "Blast", "d3": "3", "cost": 3.0 },
        "aT": { "name": "Anti-Tank", "tl": 5, "range": 8, "mass": 8.0, "qrebs": 0, "h2": "Pen", "d2": "3", "h3": "Blast", "d3": "3", "cost": 2.0 },
        "A": { "name": "Assault", "tl": 2, "range": 4, "mass": 0.8, "qrebs": 0, "h2": "Bang", "d2": "1", "h3": "Blast", "d3": "2", "cost": 1.5 },
        "F": { "name": "Fusion", "tl": 7, "range": 4, "mass": 2.3, "qrebs": 0, "h2": "Pen", "d2": "4", "h3": "Burn", "d3": "4", "cost": 6.0 },
        "G": { "name": "Gauss", "tl": 7, "range": 4, "mass": 0.9, "qrebs": 0, "h2": "Bullet", "d2": "3", "h3": "", "d3": "", "cost": 2.0 },
        "P": { "name": "Plasma", "tl": 5, "range": 4, "mass": 2.5, "qrebs": 0, "h2": "Pen", "d2": "3", "h3": "Burn", "d3": "3", "cost": 2.0 }
    },
    "Long Guns": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "Ac": { "name": "Accelerator", "tl": 4, "range": 0, "mass": 0.6, "qrebs": 0, "h2": "Bullet", "d2": "2", "h3": "", "d3": "", "cost": 3.0 },
        "A": { "name": "Assault", "tl": 2, "range": 4, "mass": 0.8, "qrebs": 0, "h2": "Blast", "d2": "2", "h3": "Bang", "d3": "1", "cost": 1.5 },
        "B": { "name": "Battle", "tl": 1, "range": 5, "mass": 1.0, "qrebs": "+1", "h2": "Bullet", "d2": "1", "h3": "", "d3": "", "cost": 0.8 },
        "C": { "name": "Combat", "tl": 2, "range": 3, "mass": 0.9, "qrebs": 0, "h2": "Frag", "d2": "2", "h3": "", "d3": "", "cost": 1.5 },
        "D": { "name": "Dart", "tl": 1, "range": 4, "mass": 0.6, "qrebs": 0, "h2": "Tranq", "d2": "1-2-3", "h3": "", "d3": "", "cost": 0.9 },
        "PD": { "name": "Poison Dart", "tl": 1, "range": 4, "mass": 1.0, "qrebs": 0, "h2": "Poison", "d2": "1-2-3", "h3": "", "d3": "", "cost": 0.9 },
        "G": { "name": "Gauss", "tl": 7, "range": 4, "mass": 0.9, "qrebs": 0, "h2": "Bullet", "d2": "3", "h3": "", "d3": "", "cost": 2.0 },
        "H": { "name": "Hunting", "tl": 0, "range": 3, "mass": 0.9, "qrebs": "-1", "h2": "Bullet", "d2": "1", "h3": "", "d3": "", "cost": 1.2 },
        "L": { "name": "Laser", "tl": 5, "range": 0, "mass": 1.2, "qrebs": 0, "h2": "Burn", "d2": "2", "h3": "Pen", "d3": "2", "cost": 6.0 },
        "Sp": { "name": "Splat", "tl": 2, "range": 4, "mass": 1.3, "qrebs": "+1", "h2": "Bullet", "d2": "1", "h3": "", "d3": "", "cost": 2.4 },
        "S": { "name": "Survival", "tl": 0, "range": 2, "mass": 0.5, "qrebs": 0, "h2": "Bullet", "d2": "1", "h3": "", "d3": "", "cost": 1.2 }
    },
    "Handguns": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "Ac": { "name": "Accelerator", "tl": 4, "range": 0, "mass": 0.6, "qrebs": 0, "h2": "Bullet", "d2": "2", "h3": "", "d3": "", "cost": 3.0 },
        "G": { "name": "Gauss", "tl": 7, "range": 4, "mass": 0.9, "qrebs": 0, "h2": "Bullet", "d2": "3", "h3": "", "d3": "", "cost": 2.0 },
        "L": { "name": "Laser", "tl": 5, "range": 0, "mass": 1.2, "qrebs": 0, "h2": "Burn", "d2": "2", "h3": "Pen", "d3": "2", "cost": 2.0 },
        "M": { "name": "Machine", "tl": 2, "range": 0, "mass": 1.2, "qrebs": 0, "h2": "Bullet", "d2": "2", "h3": "", "d3": "", "cost": 1.5 }
    },
    "Shotguns": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "A": { "name": "Assault", "tl": 2, "range": 4, "mass": 0.8, "qrebs": 0, "h2": "Bang", "d2": "1", "h3": "Blast", "d3": "2", "cost": 2.0 },
        "H": { "name": "Hunting", "tl": 0, "range": 3, "mass": 0.9, "qrebs": 0, "h2": "Bullet", "d2": "1", "h3": "", "d3": "", "cost": 1.2 }
    },
    "Machineguns": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "aF": { "name": "Anti-Flyer", "tl": 4, "range": 6, "mass": 6.0, "qrebs": 0, "h2": "Frag", "d2": "1", "h3": "Blast", "d3": "3", "cost": 3.0 },
        "A": { "name": "Assault", "tl": 2, "range": 4, "mass": 0.8, "qrebs": 0, "h2": "Bang", "d2": "1", "h3": "Blast", "d3": "2", "cost": 1.5 },
        "S": { "name": "Sub", "tl": -1, "range": 3, "mass": 0.3, "qrebs": 0, "h2": "Bullet", "d2": "-1", "h3": "", "d3": "", "cost": 0.9 }
    },
    "Projectors": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "A": { "name": "Acid", "tl": 0, "range": 3, "mass": 1.0, "qrebs": "+1", "h2": "Corrode", "d2": "2", "h3": "Pen", "d3": "1-2-3", "cost": 3.0 },
        "H": { "name": "Fire", "tl": 0, "range": 1, "mass": 0.9, "qrebs": 0, "h2": "Burn", "d2": "1-2-3", "h3": "Pen", "d3": "1-2-3", "cost": 2.0 },
        "P": { "name": "Poison Gas", "tl": 0, "range": 2, "mass": 1.0, "qrebs": 0, "h2": "Gas", "d2": "1-2-3", "h3": "Poison", "d3": "1-2-3", "cost": 3.0 },
        "S": { "name": "Stench", "tl": 3, "range": 2, "mass": 0.4, "qrebs": 0, "h2": "Stench", "d2": "1-2-3", "h3": "", "d3": "", "cost": 1.2 },
        "Emp": { "name": "EMP", "tl": 1, "range": 3, "mass": 1.0, "qrebs": 0, "h2": "EMP", "d2": "1-2-3", "h3": "", "d3": "", "cost": 4.0 },
        "F": { "name": "Flash", "tl": -1, "range": 2, "mass": 0.5, "qrebs": 0, "h2": "Flash", "d2": "1-2-3", "h3": "", "d3": "", "cost": 1.5 },
        "C": { "name": "Freeze", "tl": 1, "range": 3, "mass": 1.0, "qrebs": "+1", "h2": "Cold", "d2": "1-2-3", "h3": "", "d3": "", "cost": 3.0 },
        "G": { "name": "Grav", "tl": 5, "range": 2, "mass": 3.0, "qrebs": 0, "h2": "Grav", "d2": "1-2-3", "h3": "", "d3": "", "cost": 20.0 },
        "L": { "name": "Laser", "tl": 5, "range": 0, "mass": 1.2, "qrebs": 0, "h2": "Burn", "d2": "1-2-3", "h3": "Pen", "d3": "1-2-3", "cost": 6.0 },
        "M": { "name": "Mag", "tl": 4, "range": 1, "mass": 2.0, "qrebs": 0, "h2": "EMP", "d2": "1-2-3", "h3": "Mag", "d3": "1-2-3", "cost": 15.0 },
        "Psi": { "name": "Psi Amp", "tl": 4, "range": 2, "mass": 1.0, "qrebs": 0, "h2": "Psi", "d2": "1-2-3", "h3": "", "d3": "", "cost": 9.0 },
        "R": { "name": "Rad", "tl": 1, "range": 4, "mass": 1.0, "qrebs": "+2", "h2": "Rad", "d2": "1-2-3", "h3": "", "d3": "", "cost": 8.0 },
        "Sh": { "name": "Shock", "tl": 0, "range": 2, "mass": 0.5, "qrebs": 0, "h2": "Elec", "d2": "1-2-3", "h3": "Pain", "d3": "1-2-3", "cost": 2.0 },
        "Sonic": { "name": "Sonic", "tl": 3, "range": 2, "mass": 0.6, "qrebs": 0, "h2": "Sound", "d2": "1-2-3", "h3": "Bang", "d3": "1-2-3", "cost": 1.1 }
    },
    "Designators": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "A": { "name": "Acid", "tl": 0, "range": 3, "mass": 1.0, "qrebs": "+1", "h2": "Corrode", "d2": "2", "h3": "Pen", "d3": "1-2-3", "cost": 3.0 },
        "H": { "name": "Fire", "tl": 0, "range": 1, "mass": 0.9, "qrebs": 0, "h2": "Burn", "d2": "1-2-3", "h3": "Pen", "d3": "1-2-3", "cost": 2.0 },
        "P": { "name": "Poison Gas", "tl": 0, "range": 2, "mass": 1.0, "qrebs": 0, "h2": "Gas", "d2": "1-2-3", "h3": "Poison", "d3": "1-2-3", "cost": 3.0 },
        "S": { "name": "Stench", "tl": 3, "range": 2, "mass": 0.4, "qrebs": 0, "h2": "Stench", "d2": "1-2-3", "h3": "", "d3": "", "cost": 1.2 },
        "Emp": { "name": "EMP", "tl": 1, "range": 3, "mass": 1.0, "qrebs": 0, "h2": "EMP", "d2": "1-2-3", "h3": "", "d3": "", "cost": 4.0 },
        "F": { "name": "Flash", "tl": -1, "range": 2, "mass": 0.5, "qrebs": 0, "h2": "Flash", "d2": "1-2-3", "h3": "", "d3": "", "cost": 1.5 },
        "C": { "name": "Freeze", "tl": 1, "range": 3, "mass": 1.0, "qrebs": "+1", "h2": "Cold", "d2": "1-2-3", "h3": "", "d3": "", "cost": 3.0 },
        "G": { "name": "Grav", "tl": 5, "range": 2, "mass": 3.0, "qrebs": 0, "h2": "Grav", "d2": "1-2-3", "h3": "", "d3": "", "cost": 20.0 },
        "L": { "name": "Laser", "tl": 5, "range": 0, "mass": 1.2, "qrebs": 0, "h2": "Burn", "d2": "1-2-3", "h3": "Pen", "d3": "1-2-3", "cost": 6.0 },
        "M": { "name": "Mag", "tl": 4, "range": 1, "mass": 2.0, "qrebs": 0, "h2": "EMP", "d2": "1-2-3", "h3": "Mag", "d3": "1-2-3", "cost": 15.0 },
        "Psi": { "name": "Psi Amp", "tl": 4, "range": 2, "mass": 1.0, "qrebs": 0, "h2": "Psi", "d2": "1-2-3", "h3": "", "d3": "", "cost": 9.0 },
        "R": { "name": "Rad", "tl": 1, "range": 4, "mass": 1.0, "qrebs": "+2", "h2": "Rad", "d2": "1-2-3", "h3": "", "d3": "", "cost": 8.0 },
        "Sh": { "name": "Shock", "tl": 0, "range": 2, "mass": 0.5, "qrebs": 0, "h2": "Elec", "d2": "1-2-3", "h3": "Pain", "d3": "1-2-3", "cost": 2.0 },
        "Sonic": { "name": "Sonic", "tl": 3, "range": 2, "mass": 0.6, "qrebs": 0, "h2": "Sound", "d2": "1-2-3", "h3": "Bang", "d3": "1-2-3", "cost": 1.1 }
    },
    "Launchers": {
        "": { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 },
        "aF": { "name": "AF Missile", "tl": 4, "range": 7, "mass": 4.0, "qrebs": 0, "h2": "Frag", "d2": "2", "h3": "Blast", "d3": "3", "cost": 3.0 },
        "aT": { "name": "AT Missile", "tl": 3, "range": 4, "mass": 1.0, "qrebs": "+1", "h2": "Frag", "d2": "2", "h3": "Pen", "d3": "3", "cost": 2.0 },
        "Gr": { "name": "Grenade", "tl": 1, "range": 4, "mass": 0.8, "qrebs": 0, "h2": "Frag", "d2": "2", "h3": "Blast", "d3": "2", "cost": 1.0 },
        "M": { "name": "Missile", "tl": 1, "range": 6, "mass": 2.2, "qrebs": 0, "h2": "Frag", "d2": "2", "h3": "Pen", "d3": "2", "cost": 5.0 },
        "RAM": { "name": "RAM Grenade", "tl": 2, "range": 6, "mass": 1.0, "qrebs": 0, "h2": "Frag", "d2": "2", "h3": "Blast", "d3": "2", "cost": 3.0 },
        "R": { "name": "Rocket", "tl": -1, "range": 5, "mass": 3.0, "qrebs": 0, "h2": "Frag", "d2": "2", "h3": "Pen", "d3": "2", "cost": 1.0 }
    }
}

# Chart 5: Burden
CHART_5_BURDEN = {
    "aD": { "name": "Anti-Designator", "tl": 3, "range": 1, "mass": 3.0, "qrebs": 3, "d2Mod": 1, "cost": 3.0 },
    "B": { "name": "Body", "tl": 2, "range": 1, "mass": 0.5, "qrebs": -4, "d2Mod": -1, "cost": 3.0 },
    "D": { "name": "Disposable", "tl": 3, "range": 0, "mass": 0.9, "qrebs": -1, "d2Mod": 0, "cost": 0.5 },
    "H": { "name": "Heavy", "tl": 0, "range": 1, "mass": 1.3, "qrebs": 3, "d2Mod": 1, "cost": 2.0 },
    "Lt": { "name": "Light", "tl": 0, "range": -1, "mass": 0.7, "qrebs": -1, "d2Mod": -1, "cost": 1.1 },
    "M": { "name": "Magnum", "tl": 1, "range": 1, "mass": 1.1, "qrebs": 1, "d2Mod": 1, "cost": 1.1 },
    "Med": { "name": "Medium", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "d2Mod": 0, "cost": 1.0 },
    "R": { "name": "Recoilless", "tl": 1, "range": 1, "mass": 1.2, "qrebs": 0, "d2Mod": 1, "cost": 3.0 },
    "Sn": { "name": "Snub", "tl": 1, "range": 2, "mass": 0.7, "qrebs": -3, "d2Mod": 1, "cost": 1.5 },
    "Vh": { "name": "Vheavy", "tl": 0, "range": 5, "mass": 4.0, "qrebs": 4, "d2Mod": 5, "cost": 5.0 },
    "Vl": { "name": "Vlight", "tl": 1, "range": -2, "mass": 0.6, "qrebs": -2, "d2Mod": -1, "cost": 2.0 },
    "Vrf": { "name": "VRF", "tl": 2, "range": 0, "mass": 14.0, "qrebs": 5, "d2Mod": 1, "cost": 9.0 }
}

# Chart 5: Stage
CHART_5_STAGE = {
    "A": { "name": "Advanced", "tl": 3, "range": 0, "mass": 0.8, "qrebs": -3, "d2Mod": 2, "d3Mod": 0, "cost": 2.0 },
    "Alt": { "name": "Alternate", "tl": 0, "range": 1, "mass": 1.1, "qrebs": 0, "d2Mod": 0, "d3Mod": 0, "cost": 1.1 },
    "B": { "name": "Basic", "tl": 0, "range": 0, "mass": 1.3, "qrebs": 1, "d2Mod": 0, "d3Mod": 0, "cost": 0.7 },
    "E": { "name": "Early", "tl": -1, "range": -1, "mass": 1.7, "qrebs": 1, "d2Mod": 0, "d3Mod": 0, "cost": 1.2 },
    "Exp": { "name": "Experimental", "tl": -3, "range": -1, "mass": 2.0, "qrebs": 3, "d2Mod": 0, "d3Mod": 0, "cost": 4.0 },
    "Im": { "name": "Improved", "tl": 1, "range": 1, "mass": 1.0, "qrebs": -1, "d2Mod": 1, "d3Mod": 0, "cost": 1.1 },
    "Mod": { "name": "Modified", "tl": 2, "range": 0, "mass": 0.9, "qrebs": 0, "d2Mod": 0, "d3Mod": 0, "cost": 1.2 },
    "P": { "name": "Prototype", "tl": -2, "range": -1, "mass": 1.9, "qrebs": 2, "d2Mod": 0, "d3Mod": 0, "cost": 3.0 },
    "Pr": { "name": "Precision", "tl": 6, "range": 3, "mass": 4.0, "qrebs": 2, "d2Mod": 0, "d3Mod": 0, "cost": 5.0 },
    "R": { "name": "Remote", "tl": 1, "range": 0, "mass": 1.0, "qrebs": 0, "d2Mod": 0, "d3Mod": 0, "cost": 7.0 },
    "Sn": { "name": "Sniper", "tl": 1, "range": 1, "mass": 1.1, "qrebs": 1, "d2Mod": 0, "d3Mod": 0, "cost": 2.0 },
    "St": { "name": "Standard", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "d2Mod": 0, "d3Mod": 0, "cost": 1.0 },
    "T": { "name": "Target", "tl": 0, "range": 0, "mass": 1.1, "qrebs": 1, "d2Mod": 0, "d3Mod": 0, "cost": 1.5 },
    "Ul": { "name": "Ultimate", "tl": 4, "range": 4, "mass": 0.7, "qrebs": -4, "d2Mod": 2, "d3Mod": 0, "cost": 1.4 }
}

# Chart 5: User
CHART_5_USER = {
    "M": { "name": "Man", "mass": 1.0, "qrebs": 0, "code": "M" },
    "U": { "name": "Universal", "mass": 1.1, "qrebs": 1, "code": "U" },
    "V": { "name": "Vargr", "mass": 1.0, "qrebs": 0, "code": "V" },
    "K": { "name": "K’kree", "mass": 1.3, "qrebs": 2, "code": "K" },
    "H": { "name": "Hiver (Grasper)", "mass": 1.0, "qrebs": -1, "code": "H" },
    "A": { "name": "Aslan (Paw)", "mass": 1.0, "qrebs": -1, "code": "A" },
    "G": { "name": "Gripper", "mass": 1.0, "qrebs": -2, "code": "G" },
    "T": { "name": "Vegan (Tentacle)", "mass": 1.0, "qrebs": -2, "code": "T" },
    "S": { "name": "Socket", "mass": 1.0, "qrebs": -2, "code": "S" }
}

# Chart 7: Installable Options
CHART_7_OPTIONS = {
    "a": "Low Signature Visual (Camouflaged)",
    "b": "Low Signature Metal (Plastic)",
    "c": "Quiet (Silenced)",
    "d": "Folding Stock (Close Quarters)",
    "e": "Stable Platform (Gyro)",
    "f": "Flash Suppressor",
    "g": "Hot Environment Adapted",
    "h": "Corrosion Environment Adapted",
    "i": "Cold Environment Adapted",
    "j": "Magnification Sights (+1 Range)"
}

def calculate_weapon(category, type_code, desc_code, burden_codes, stage_codes, user_code, portability_mode, selected_options):
    type_data = CHART_3_TYPES[category][type_code]
    desc_data = CHART_4_DESCRIPTORS[category].get(desc_code, { "name": "", "tl": 0, "range": 0, "mass": 1.0, "qrebs": 0, "h2": "", "d2": "", "h3": "", "d3": "", "cost": 1.0 })
    user_data = CHART_5_USER.get(user_code, CHART_5_USER["M"])

    # 1. TL
    tl = type_data["tl"] + desc_data["tl"]
    for code in burden_codes: tl += CHART_5_BURDEN[code]["tl"]
    for code in stage_codes: tl += CHART_5_STAGE[code]["tl"]

    # 2. Range
    range_val = desc_data["range"] if desc_data["range"] != 0 else type_data["range"]
    for code in burden_codes: range_val += CHART_5_BURDEN[code]["range"]
    for code in stage_codes: range_val += CHART_5_STAGE[code]["range"]
    if range_val < 0: range_val = 0

    # 3. Mass
    mass = type_data["mass"] * desc_data["mass"] * user_data["mass"]
    for code in burden_codes: mass *= CHART_5_BURDEN[code]["mass"]
    for code in stage_codes: mass *= CHART_5_STAGE[code]["mass"]

    # 4. Cost
    cost = type_data["cost"] * desc_data["cost"]
    for code in burden_codes: cost *= CHART_5_BURDEN[code]["cost"]
    for code in stage_codes: cost *= CHART_5_STAGE[code]["cost"]

    # 5. QREBS
    b_val = 0
    if isinstance(desc_data.get("qrebs"), int): b_val += desc_data["qrebs"]
    elif isinstance(desc_data.get("qrebs"), str): 
        try: b_val += int(desc_data["qrebs"].replace('+',''))
        except: pass
        
    for code in burden_codes: b_val += CHART_5_BURDEN[code]["qrebs"]
    for code in stage_codes: b_val += CHART_5_STAGE[code]["qrebs"]
    
    qrebs = "50000"
    if b_val != 0:
        qrebs = f"B{'+' if b_val > 0 else ''}{b_val}"

    # 6. Effects
    effect_map = {}
    def add_to_map(etype, dice):
        if not etype or etype == "*" or etype == "": return
        try:
            new_num = int(dice)
            if etype in effect_map and isinstance(effect_map[etype], int):
                effect_map[etype] += new_num
            else:
                effect_map[etype] = new_num
        except:
            effect_map[etype] = dice

    add_to_map(type_data["h1"], type_data["d1"])
    
    d2_mod = sum(CHART_5_BURDEN[c].get("d2Mod", 0) for c in burden_codes) + sum(CHART_5_STAGE[c].get("d2Mod", 0) for c in stage_codes)
    d3_mod = sum(CHART_5_STAGE[c].get("d3Mod", 0) for c in stage_codes)

    if desc_data.get("h2"):
        d2_val = desc_data.get("d2", "0")
        try:
            d2_val = str(int(d2_val) + d2_mod)
        except: pass
        add_to_map(desc_data["h2"], d2_val)

    if desc_data.get("h3"):
        d3_val = desc_data.get("d3", "0")
        try:
            d3_val = str(int(d3_val) + d3_mod)
        except: pass
        add_to_map(desc_data["h3"], d3_val)

    # 7. Portability
    portability = portability_mode
    if portability == "auto":
        if mass < 20: portability = ""
        elif mass < 200: portability = "Crewed"
        elif mass < 500: portability = "Turret"
        elif mass < 1000: portability = "Vehicle Mount"
        else: portability = "Fixed"

    # 8. Names
    parts = []
    for c in stage_codes: parts.append(CHART_5_STAGE[c]["name"])
    for c in burden_codes: parts.append(CHART_5_BURDEN[c]["name"])
    if desc_data["name"]: parts.append(desc_data["name"])
    parts.append(type_data["name"])
    if user_data["name"] != "Man": parts.append(user_data["name"])
    if portability: parts.append(portability)
    parts.append(f"TL {tl}")
    long_name = " ".join(filter(None, parts))

    model_parts = stage_codes + burden_codes + ([desc_code] if desc_code else []) + [type_code]
    model = "".join(model_parts) + f"-{tl}"

    # 9. Controls
    controls = {"off": True, "single": False, "burst": False, "full": False, "p123": False, "override": False}

    # 1-2-3 Group (Fusion, Plasma, Laser, Poison Dart, or any Projector/Designator)
    # Fusion: F, Plasma: P, Laser: L, Poison Dart: PD
    is_p123 = (category in ["Projectors", "Designators"]) or (desc_code in ["F", "P", "L", "PD"])

    if is_p123:
        controls["p123"] = True
    else:
        controls["single"] = True
        
        # Burst Capable: Accelerator (Ac), Assault (A), Gauss (G)
        # Types: Gatling (Ga), Autocannon (aC), Multi-Launcher (mL)
        if desc_code in ["Ac", "A", "G"] or type_code in ["Ga", "aC", "mL"]:
            controls["burst"] = True
            
        # Full Auto Capable: Anti-Flyer (aF), Assault (A), Gauss (G), Splat (Sp), Machine (M), Sub (S)
        if desc_code in ["aF", "A", "G", "Sp", "M", "S"]:
            controls["full"] = True

    return {
        "model": model,
        "long_name": long_name,
        "tl": tl,
        "range": range_val,
        "mass": mass,
        "cost": cost,
        "qrebs": qrebs,
        "effects": effect_map,
        "controls": controls,
        "options": [CHART_7_OPTIONS[o] for o in selected_options]
    }
