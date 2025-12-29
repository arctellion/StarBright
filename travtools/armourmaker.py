import math

# --- DATASETS ---

TYPES = {
    # SYSTEMS
    "D": { "name": "Dress", "type": "System", "category": "System", "tl": 10, "mass": 40, "cost": 40000, "ar": 9, "ca": 6, "fl": 6, "ra": 6, "so": 6, "ps": 1, "ins": 6, "seal": 6, "qrebs": {}, "skill": "BattleDress", "eval": {"str": "x10", "dex": -2, "end": -1} },
    "A": { "name": "Armor", "type": "System", "category": "System", "tl": 8, "mass": 30, "cost": 20000, "ar": 7, "ca": 3, "fl": 3, "ra": 3, "so": 3, "ps": 1, "ins": 3, "seal": 3, "qrebs": {}, "skill": "BattleDress", "eval": {"str": "x10", "dex": -2, "end": -2} },
    "S": { "name": "Suit", "type": "System", "category": "System", "tl": 5, "mass": 10, "cost": 1000, "ar": 2, "ca": 1, "fl": 1, "ra": 1, "so": 1, "ps": 1, "ins": 1, "seal": 1, "qrebs": {}, "skill": "Vacc Suit", "eval": {"str": "x1", "dex": -2, "end": -3} },
    "U": { "name": "Unit", "type": "System", "category": "System", "tl": 9, "mass": 200, "cost": 60000, "ar": 4, "ca": 2, "fl": 2, "ra": 2, "so": 2, "ps": 1, "ins": 2, "seal": 2, "qrebs": {}, "skill": "Driver: Legged", "eval": {"str": "x10", "dex": -2, "end": 0} },
    
    # ITEMS - BODY
    "J": { "name": "Jack", "type": "Item", "category": "Body", "tl": 1, "mass": 1, "cost": 50, "ar": 5, "ca": 1, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "Ma": { "name": "Mail", "type": "Item", "category": "Body", "tl": 4, "mass": 3, "cost": 400, "ar": 6, "ca": 2, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "M": { "name": "Mesh", "type": "Item", "category": "Body", "tl": 7, "mass": 2, "cost": 150, "ar": 10, "ca": 1, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "K": { "name": "Cloth", "type": "Item", "category": "Body", "tl": 8, "mass": 2, "cost": 250, "ar": 14, "ca": 1, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "Q": { "name": "Quilt", "type": "Item", "category": "Body", "tl": 9, "mass": 1, "cost": 600, "ar": 18, "ca": 1, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "P": { "name": "Plate", "type": "Item", "category": "Body", "tl": 6, "mass": 4, "cost": 900, "ar": 22, "ca": 1, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {"b": 2}, "comment": "B=+2" },
    "Abl": { "name": "Ablat", "type": "Item", "category": "Body", "tl": 9, "mass": 2, "cost": 375, "ar": 12, "ca": 3, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 8, "seal": 0, "qrebs": {"b": 3}, "comment": "2x vs K" },
    "R": { "name": "Reflec", "type": "Item", "category": "Body", "tl": 10, "mass": 1, "cost": 100, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {}, "comment": "Deflects Laser" },
    "C": { "name": "Coat", "type": "Item", "category": "Body", "tl": 1, "mass": 1, "cost": 100, "ar": 2, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "hC": { "name": "Heavy Coat", "type": "Item", "category": "Body", "tl": 2, "mass": 2, "cost": 200, "ar": 3, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    
    # ITEMS - HEAD
    "Sh": { "name": "Shield", "type": "Item", "category": "Head", "tl": 2, "mass": 3, "cost": 100, "ar": 12, "ca": 3, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "aSh": { "name": "Adv. Shield", "type": "Item", "category": "Head", "tl": 8, "mass": 2, "cost": 400, "ar": 14, "ca": 2, "fl": 0, "ra": 8, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "H": { "name": "Mil Helmet", "type": "Item", "category": "Head", "tl": 4, "mass": 1, "cost": 100, "ar": 8, "ca": 0, "fl": 0, "ra": 0, "so": 5, "ps": 0, "ins": 0, "seal": 0, "qrebs": {"b": 1} },
    "Hp": { "name": "Full Helmet", "type": "Item", "category": "Head", "tl": 8, "mass": 1, "cost": 300, "ar": 10, "ca": 5, "fl": 12, "ra": 5, "so": 5, "ps": 0, "ins": 5, "seal": 0, "qrebs": {"b": 2} },
    "Hc": { "name": "Crew Helmet", "type": "Item", "category": "Head", "tl": 8, "mass": 1, "cost": 300, "ar": 6, "ca": 6, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 5, "qrebs": {"b": 1} },
    "eP": { "name": "Ear Protectors", "type": "Item", "category": "Head", "tl": 4, "mass": 0, "cost": 100, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 12, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "Gog": { "name": "Flash Goggles", "type": "Item", "category": "Head", "tl": 8, "mass": 0, "cost": 200, "ar": 0, "ca": 0, "fl": 12, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "Sun": { "name": "Sunglasses", "type": "Item", "category": "Head", "tl": 4, "mass": 0, "cost": 100, "ar": 0, "ca": 0, "fl": 6, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "qrebs": {} },
    "Psi": { "name": "Psi Shield", "type": "Item", "category": "Head", "tl": 12, "mass": 1, "cost": 3000, "ar": 3, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 15, "ins": 0, "seal": 0, "qrebs": {} },
    
    # ITEMS - BREATHER
    "F": { "name": "Filter", "type": "Item", "category": "Breather", "tl": 3, "mass": 1, "cost": 10, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 3, "qrebs": {} },
    "B": { "name": "Breather", "type": "Item", "category": "Breather", "tl": 7, "mass": 2, "cost": 200, "ar": 0, "ca": 4, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 6, "qrebs": {} },
    "Comb": { "name": "Combination", "type": "Item", "category": "Breather", "tl": 5, "mass": 1, "cost": 150, "ar": 0, "ca": 4, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 12, "qrebs": {} },
    "Resp": { "name": "Respirator", "type": "Item", "category": "Breather", "tl": 5, "mass": 1, "cost": 100, "ar": 0, "ca": 4, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 12, "qrebs": {} },
    "aT": { "name": "Air Tanks", "type": "Item", "category": "Breather", "tl": 5, "mass": 4, "cost": 500, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 12, "qrebs": {} },
    "rB": { "name": "ReBreather", "type": "Item", "category": "Breather", "tl": 10, "mass": 1, "cost": 200, "ar": 0, "ca": 10, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 12, "qrebs": {} },
    "G": { "name": "Gill", "type": "Item", "category": "Breather", "tl": 11, "mass": 4, "cost": 4000, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 18, "qrebs": {} },
}

MODIFIERS = {
    "descriptor": {
        "": { "tl": 0, "mass": 1, "cost": 1, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "abbrev": "" },
        "Carrier": { "tl": 1, "mass": 2, "cost": 3, "ar": "x1", "ca": "x1", "fl": "x1", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x1", "seal": "x1", "abbrev": "<>" },
        "Assault": { "tl": 4, "mass": 1.5, "cost": 3, "ar": "x2", "ca": "x2", "fl": "x2", "ra": "x2", "so": "x2", "ps": "x2", "ins": "x2", "seal": "x2", "abbrev": "A" },
        "Battle": { "tl": 3, "mass": 2.5, "cost": 5, "ar": "x5", "ca": "x5", "fl": "x5", "ra": "x5", "so": "x5", "ps": "x5", "ins": "x5", "seal": "x5", "abbrev": "B" },
        "Boarding": { "tl": 3, "mass": 1.2, "cost": 4, "ar": "x4", "ca": "x1", "fl": "x4", "ra": "x1", "so": "x2", "ps": "x1", "ins": "x1", "seal": "x3", "abbrev": "Bd" },
        "Combat": { "tl": 3, "mass": 2, "cost": 4, "ar": "x4", "ca": "x4", "fl": "x4", "ra": "x4", "so": "x4", "ps": "x4", "ins": "x4", "seal": "x4", "abbrev": "C" },
        "Drop": { "tl": 2, "mass": 3, "cost": 3, "ar": "x8", "ca": "x1", "fl": "x8", "ra": "x1", "so": "x8", "ps": "x1", "ins": "x1", "seal": "x8", "abbrev": "Dr" },
        "Environ": { "tl": 2, "mass": 0.5, "cost": 1.5, "ar": "x4", "ca": "x4", "fl": "x4", "ra": "x1", "so": "x4", "ps": "x1", "ins": "x20", "seal": "x10", "abbrev": "Env" },
        "Exploration": { "tl": 1, "mass": 1, "cost": 7, "ar": "x5", "ca": "x1", "fl": "x1", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x8", "seal": "x8", "abbrev": "Ex" },
        "Hazmat": { "tl": 0, "mass": 1.3, "cost": 9, "ar": "x2", "ca": "x6", "fl": "x6", "ra": "x6", "so": "x6", "ps": "x1", "ins": "x12", "seal": "x12", "abbrev": "Hz" },
        "Hostile": { "tl": 1, "mass": 1.2, "cost": 8, "ar": "x8", "ca": "x1", "fl": "x1", "ra": "x8", "so": "x1", "ps": "x1", "ins": "x8", "seal": "x12", "abbrev": "HE" },
        "Hot": { "tl": 1, "mass": 0.3, "cost": 0.6, "ar": "x2", "ca": "x7", "fl": "x5", "ra": "x5", "so": "x5", "ps": "x1", "ins": "x5", "seal": "x5", "abbrev": "H" },
        "Cold": { "tl": 2, "mass": 0.2, "cost": 0.2, "ar": "x1", "ca": "x1", "fl": "x1", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x6", "seal": "x1", "abbrev": "C" },
        "Police": { "tl": 0, "mass": 0.6, "cost": 1.7, "ar": "x3", "ca": "x1", "fl": "x5", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x1", "seal": "x2", "abbrev": "P" },
        "Prospector": { "tl": 2, "mass": 2, "cost": 6, "ar": "x2", "ca": "x2", "fl": "x1", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x3", "seal": "x5", "abbrev": "Pr" },
        "Labor": { "tl": -1, "mass": 0.7, "cost": 4, "ar": "x1", "ca": "x1", "fl": "x1", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x6", "seal": "x6", "abbrev": "L" },
        "Sapper": { "tl": 2, "mass": 1.2, "cost": 7, "ar": "x5", "ca": "x6", "fl": "x6", "ra": "x1", "so": "x6", "ps": "x1", "ins": "x8", "seal": "x8", "abbrev": "S" },
        "Vacc": { "tl": 4, "mass": 1, "cost": 10, "ar": "x5", "ca": "x5", "fl": "x0", "ra": "x1", "so": "x1", "ps": "x1", "ins": "x5", "seal": "x5", "abbrev": "V" },
        "Protected": { "tl": 2, "mass": 2, "cost": 7, "ar": "x2", "ca": "x2", "fl": "x2", "ra": "x2", "so": "x2", "ps": "x1", "ins": "x3", "seal": "x4", "abbrev": "Pr" },
        "CombatEnviron": { "tl": 7, "mass": 2.5, "cost": 6, "ar": "x7", "ca": "x4", "fl": "x5", "ra": "x5", "so": "x5", "ps": "x1", "ins": "x5", "seal": "x5", "abbrev": "CE" }
    },
    "burden": {
        "": { "tl": 0, "mass": 1, "cost": 1, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "b": 0, "abbrev": "" },
        "Disposable": { "tl": 3, "mass": 0.9, "cost": 0.5, "ar": -5, "ca": -5, "fl": -5, "ra": -5, "so": -5, "ps": 0, "ins": 5, "seal": -5, "b": -5, "abbrev": "D" },
        "Heavy": { "tl": 1, "mass": 1.3, "cost": 2, "ar": 8, "ca": 10, "fl": 10, "ra": 10, "so": 10, "ps": 0, "ins": 15, "seal": 10, "b": 1, "abbrev": "H" },
        "Light": { "tl": 0, "mass": 0.7, "cost": 1.1, "ar": -3, "ca": -3, "fl": -3, "ra": -3, "so": -3, "ps": 0, "ins": 5, "seal": -3, "b": 0, "abbrev": "L" },
        "Medium": { "tl": 0, "mass": 1, "cost": 1, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 10, "seal": 0, "b": 0, "abbrev": "M" },
        "Vlight": { "tl": 1, "mass": 0.6, "cost": 2, "ar": -5, "ca": -5, "fl": -5, "ra": -5, "so": -5, "ps": 0, "ins": -2, "seal": -5, "b": 0, "abbrev": "Vl" },
        "Oversize": { "tl": 1, "mass": 8, "cost": 10, "ar": 12, "ca": 8, "fl": 8, "ra": 8, "so": 8, "ps": 0, "ins": 8, "seal": 8, "b": 0, "abbrev": "OS" },
        "Titan": { "tl": 3, "mass": 27, "cost": 30, "ar": 16, "ca": 8, "fl": 8, "ra": 8, "so": 8, "ps": 0, "ins": 8, "seal": 8, "b": 0, "abbrev": "T" }
    },
    "stage": {
        "": { "tl": 0, "mass": 1, "cost": 1, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "b": 0, "abbrev": "" },
        "Experimental": { "tl": -2, "mass": 2, "cost": 4, "ar": -8, "ca": -8, "fl": -8, "ra": -8, "so": -8, "ps": 0, "ins": -8, "seal": -8, "b": 0, "abbrev": "X" },
        "Prototype": { "tl": -1, "mass": 1.9, "cost": 3, "ar": -4, "ca": -4, "fl": -4, "ra": -4, "so": -4, "ps": 0, "ins": -4, "seal": -4, "b": 0, "abbrev": "P" },
        "Early": { "tl": -1, "mass": 1.7, "cost": 1.2, "ar": -2, "ca": -2, "fl": -2, "ra": -2, "so": -2, "ps": 0, "ins": -2, "seal": -2, "b": 0, "abbrev": "E" },
        "Basic": { "tl": 0, "mass": 1.3, "cost": 0.7, "ar": -5, "ca": -5, "fl": -5, "ra": -5, "so": -5, "ps": 0, "ins": -5, "seal": -5, "b": 0, "abbrev": "B" },
        "Standard": { "tl": 1, "mass": 1, "cost": 1, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "b": 0, "abbrev": "St" },
        "Improved": { "tl": 1, "mass": 1, "cost": 1.1, "ar": 6, "ca": 6, "fl": 6, "ra": 6, "so": 6, "ps": 0, "ins": 18, "seal": 6, "b": 0, "abbrev": "Im" },
        "Modified": { "tl": 2, "mass": 0.9, "cost": 1.2, "ar": 3, "ca": 3, "fl": 3, "ra": 3, "so": 3, "ps": 0, "ins": 9, "seal": 3, "b": 0, "abbrev": "Mod" },
        "Advanced": { "tl": 3, "mass": 0.8, "cost": 2, "ar": 10, "ca": 10, "fl": 10, "ra": 10, "so": 10, "ps": 3, "ins": 30, "seal": 10, "b": 0, "abbrev": "A" },
        "Alternate": { "tl": 1, "mass": 1.1, "cost": 1.1, "ar": 5, "ca": 5, "fl": 5, "ra": 5, "so": 5, "ps": 0, "ins": 15, "seal": 5, "b": 0, "abbrev": "Alt" },
        "Obsolete": { "tl": 4, "mass": 0.7, "cost": 0.5, "ar": 3, "ca": 3, "fl": 3, "ra": 3, "so": 3, "ps": 0, "ins": 9, "seal": 3, "b": 0, "abbrev": "Ob" },
        "Remote": { "tl": 2, "mass": 1.5, "cost": 4, "ar": 0, "ca": 0, "fl": 0, "ra": 0, "so": 0, "ps": 0, "ins": 0, "seal": 0, "b": 0, "abbrev": "Re" },
        "Ultimate": { "tl": 5, "mass": 1, "cost": 10, "ar": 20, "ca": 20, "fl": 20, "ra": 20, "so": 20, "ps": 5, "ins": 50, "seal": 20, "b": 0, "abbrev": "Ul" }
    }
}

USERS = {
    "": { "tl": 0, "abbrev": "M", "name": "Man" },
    "Universal": { "tl": 0, "abbrev": "U", "name": "Universal" },
    "Aslan": { "tl": 1, "abbrev": "A", "name": "Aslan" },
    "Hiver": { "tl": 1, "abbrev": "H", "name": "Hiver" },
    "Vargr": { "tl": 0, "abbrev": "V", "name": "Vargr" },
    "K'kree": { "tl": 0, "abbrev": "K", "name": "K'kree" },
    "Vegan": { "tl": 2, "abbrev": "V", "name": "Vegan" },
    "Droyne": { "tl": 0, "abbrev": "D", "name": "Droyne" },
    "Other": { "tl": 0, "abbrev": "O", "name": "Other" }
}

OPTIONS = [
    { "id": "comms_a", "name": "Comms: Standard", "desc": "Range=5", "type": "comm" },
    { "id": "comms_b", "name": "Comms: Grid", "desc": "Range=6", "type": "comm" },
    { "id": "comms_c", "name": "Comms: Battlefield", "desc": "Range=6", "type": "comm" },
    { "id": "comms_d", "name": "Comms: Command", "desc": "Range=8", "type": "comm" },
    { "id": "comms_e", "name": "Comms: LOS", "desc": "Range=6, Secure", "type": "comm" },
    { "id": "comms_f", "name": "Comms: LR-LOS", "desc": "Range=10, Secure", "type": "comm" },
    { "id": "sensor_g", "name": "Relay Option", "desc": "Auto relay", "type": "sensor" },
    { "id": "sensor_h", "name": "Sensors: Basic", "desc": "Speed/Dir/Status", "type": "sensor" },
    { "id": "sensor_i", "name": "Sensors: Additional", "desc": "Sophisticated instr.", "type": "sensor" },
    { "id": "sensor_j", "name": "Sensors: Direct", "desc": "See/Hear External", "type": "sensor" },
    { "id": "sensor_k", "name": "Sensors: Enhanced 1", "desc": "+08 to 2 senses", "type": "sensor" },
    { "id": "sensor_l", "name": "Sensors: Enhanced 2", "desc": "+08 to 2 senses", "type": "sensor" },
    { "id": "sensor_m", "name": "Sensors: Enhanced 3", "desc": "+08 to 2 senses", "type": "sensor" },
    { "id": "ctrl_n", "name": "Controls: Self", "desc": "Suits only", "type": "ctrl" },
    { "id": "ctrl_p", "name": "Controls: Feedback", "desc": "Transparent operation", "type": "ctrl" },
    { "id": "ctrl_q", "name": "Controls: Manual", "desc": "Hand/Foot/etc", "type": "ctrl" },
    { "id": "ctrl_r", "name": "Controls: Wafer", "desc": "Jack required", "type": "ctrl" },
    { "id": "ctrl_s", "name": "AutoPilot", "desc": "Self-operation", "type": "ctrl" },
    { "id": "other_t", "name": "Fine Control", "desc": "C2 +3", "type": "other", "effect": { "dex": 3 } },
    { "id": "other_u", "name": "Reflec", "desc": "+2 Vis, Laser Deflect", "type": "other" },
    { "id": "other_v", "name": "Spot Armor", "desc": "", "type": "other" },
    { "id": "other_w", "name": "PsiShield", "desc": "", "type": "other", "effect": { "ps": 1 } },
    { "id": "other_x", "name": "Stealthy", "desc": "-Vis Mod", "type": "other" },
    { "id": "power_0", "name": "Power: None", "desc": "Standard", "type": "pwr" },
    { "id": "power_1", "name": "Power: Day", "desc": "~1 day LS", "type": "pwr" },
    { "id": "power_3", "name": "Power: Days", "desc": "~2-3 day LS", "type": "pwr" },
    { "id": "power_7", "name": "Power: Week", "desc": "~1 week LS", "type": "pwr" },
    { "id": "power_9", "name": "Power: Extended", "desc": ">1 week LS", "type": "pwr" },
    { "id": "other_y", "name": "Stamina", "desc": "C3 = Stamina", "type": "other", "effect": { "stamina": True } }
]

STANDARD_SUBSYSTEMS = {
    "D": ["comms_c", "sensor_h", "ctrl_q", "power_7"],
    "A": ["comms_c", "sensor_h", "ctrl_q", "power_3"],
    "S": ["comms_b", "sensor_h", "ctrl_s", "power_1"],
    "U": ["comms_a", "sensor_h", "ctrl_s", "power_3"]
}

SUBSYSTEM_CATS = {
    "comms": ["comms_a", "comms_b", "comms_c", "comms_d", "comms_e", "comms_f", "sensor_g"],
    "sensors": ["sensor_h", "sensor_i", "sensor_j", "sensor_k", "sensor_l", "sensor_m"],
    "controls": ["ctrl_n", "ctrl_p", "ctrl_q", "ctrl_r", "ctrl_s"],
    "power": ["power_0", "power_1", "power_3", "power_7", "power_9"],
    "other": ["other_t", "other_u", "other_v", "other_w", "other_x", "other_y"]
}

DRAWBACKS = {
    1: [
        { "id": "1-1", "name": "Cramped", "desc": "C3 -1", "effect": { "end": -1 } },
        { "id": "1-2", "name": "Irritating Interior Noise", "desc": "Hearing -2", "effect": {} },
        { "id": "1-3", "name": "Bad Taste in Drinks", "desc": "Complaints", "effect": {} },
        { "id": "1-4", "name": "Interior Runs Cold", "desc": "Cold-1/Round", "effect": {} },
        { "id": "1-5", "name": "Interior Runs Hot", "desc": "Hot-1/Round", "effect": {} },
        { "id": "1-6", "name": "Poor Quality Diversion", "desc": "Complaints", "effect": {} }
    ],
    2: [
        { "id": "2-1", "name": "Vibration", "desc": "C3 -1", "effect": { "end": -1 } },
        { "id": "2-2", "name": "Heavy Vibration", "desc": "C3 -2", "effect": { "end": -2 } },
        { "id": "2-3", "name": "Waste Heat Plume", "desc": "Mod +4 IR", "effect": {} },
        { "id": "2-4", "name": "Externally Loud", "desc": "Bang-2/Round", "effect": {} },
        { "id": "2-5", "name": "Hard To Use", "desc": "qrebs B -2", "effect": { "qrebsB": -2 } },
        { "id": "2-6", "name": "Poorly Planned Interior", "desc": "qrebs S -2", "effect": { "qrebsS": -2 } }
    ],
    3: [
        { "id": "3-1", "name": "Faulty Manipulator Joints", "desc": "C2 Half", "effect": { "dexHalf": True } },
        { "id": "3-2", "name": "Faulty Limb Joints", "desc": "Str Half", "effect": { "strHalf": True } },
        { "id": "3-3", "name": "Poor Manipulator Design", "desc": "C2 = Agility", "effect": { "dexIsAgi": True } },
        { "id": "3-4", "name": "Highly Visible Shape", "desc": "Vis +2", "effect": {} },
        { "id": "3-5", "name": "Mag Flashes", "desc": "Mag Int 5", "effect": {} },
        { "id": "3-6", "name": "Contaminated Life Support", "desc": "Infection -1", "effect": {} }
    ],
    4: [
        { "id": "4-1", "name": "Strange Internal Harmonics", "desc": "San Check Daily", "effect": {} },
        { "id": "4-2", "name": "Unsteady", "desc": "Check Stability/Hour", "effect": {} },
        { "id": "4-3", "name": "Rapid System Fatigue", "desc": "C3 = Vigor", "effect": { "stamina": True } },
        { "id": "4-4", "name": "Distracting Feedback", "desc": "Skill/Int Halved", "effect": {} },
        { "id": "4-5", "name": "Randomly Locks", "desc": "Locks 2D=12", "effect": {} },
        { "id": "4-6", "name": "Hangar Queen", "desc": "Reliability Check Daily", "effect": {} }
    ]
}

# --- CALCULATIONS ---

def calculate_custom_armor(type_key, desc_key, burden_key, stage_key, user_key, selected_options, drawbacks):
    """
    selected_options: list of option IDs
    drawbacks: dict mapping option ID to drawback ID
    """
    base_data = TYPES[type_key]
    desc_data = MODIFIERS["descriptor"].get(desc_key, MODIFIERS["descriptor"][""])
    burden_data = MODIFIERS["burden"].get(burden_key, MODIFIERS["burden"][""])
    stage_data = MODIFIERS["stage"].get(stage_key, MODIFIERS["stage"][""])
    user_data = USERS.get(user_key, USERS[""])
    
    standards = STANDARD_SUBSYSTEMS.get(type_key, [])
    
    # 1. TL
    tl = base_data["tl"] + desc_data["tl"] + burden_data["tl"] + stage_data["tl"] + user_data["tl"]
    
    # 2. Mass & Cost
    mass = base_data["mass"] * desc_data["mass"] * burden_data["mass"] * stage_data["mass"]
    cost = base_data["cost"] * desc_data["cost"] * burden_data["cost"] * stage_data["cost"]
    
    # 3. Armor Values
    stats_keys = ['ar', 'ca', 'fl', 'ra', 'so', 'ps', 'ins', 'seal']
    final_stats = {}
    for stat in stats_keys:
        val = base_data[stat]
        d_mod = desc_data[stat]
        if isinstance(d_mod, str) and d_mod.startswith('x'):
            val = val * float(d_mod[1:])
        else:
            val = val + float(d_mod)
        val += burden_data[stat]
        val += stage_data[stat]
        final_stats[stat] = math.floor(val)
        
    # 4. QREBS
    b_mod = base_data.get("qrebs", {}).get("b", 0)
    b_mod += burden_data.get("b", 0)
    b_mod += stage_data.get("b", 0)
    
    all_drawbacks = [d for sublist in DRAWBACKS.values() for d in sublist]
    for opt_id in selected_options:
        if opt_id not in standards:
            db_id = drawbacks.get(opt_id)
            if db_id:
                db_data = next((d for d in all_drawbacks if d["id"] == db_id), None)
                if db_data and "qrebsB" in db_data.get("effect", {}):
                    b_mod += db_data["effect"]["qrebsB"]
                    
    qrebs_str = f"B={b_mod}" if b_mod != 0 else "50000"
    
    # 5. Name Construction
    long_parts = []
    if stage_key: long_parts.append(stage_key)
    if burden_key: long_parts.append(burden_key)
    if desc_key: long_parts.append(desc_key)
    long_parts.append(base_data["name"])
    if user_key and user_data["name"] != "Man": long_parts.append(user_data["name"])
    long_name = " ".join(long_parts) + f"-{tl}"
    
    model_parts = []
    if stage_key: model_parts.append(f"({stage_data['abbrev']})")
    if burden_key: model_parts.append(f"({burden_data['abbrev']})")
    if desc_key: model_parts.append(desc_data['abbrev'])
    model_parts.append(type_key)
    if user_key: model_parts.append(user_data['abbrev'])
    model = "".join(model_parts) + f"-{tl}"
    
    # 6. Evaluation
    eval_stats = { "str": 0, "dex": 0, "end": 0, "strMult": 1, "stamina": False }
    if "eval" in base_data:
        if isinstance(base_data["eval"]["str"], str) and base_data["eval"]["str"].startswith('x'):
            eval_stats["strMult"] = float(base_data["eval"]["str"][1:])
        else:
            eval_stats["str"] = base_data["eval"]["str"]
        eval_stats["dex"] = base_data["eval"].get("dex", 0)
        eval_stats["end"] = base_data["eval"].get("end", 0)
        
    if burden_key == 'Oversize': eval_stats["strMult"] = 100
    if burden_key == 'Titan': eval_stats["strMult"] = 1000
    
    for opt_id in selected_options:
        opt_data = next((o for o in OPTIONS if o["id"] == opt_id), None)
        if opt_data and "effect" in opt_data:
            if "dex" in opt_data["effect"]: eval_stats["dex"] += opt_data["effect"]["dex"]
            if "stamina" in opt_data["effect"]: eval_stats["stamina"] = True
            
        if opt_id not in standards:
            db_id = drawbacks.get(opt_id)
            if db_id:
                db_data = next((d for d in all_drawbacks if d["id"] == db_id), None)
                if db_data and "effect" in db_data:
                    if "end" in db_data["effect"]: eval_stats["end"] += db_data["effect"]["end"]
                    if "strHalf" in db_data["effect"]: eval_stats["strMult"] /= 2
                    if "stamina" in db_data["effect"]: eval_stats["stamina"] = True
                    
    return {
        "long_name": long_name,
        "model": model,
        "tl": tl,
        "mass": mass,
        "cost": cost,
        "stats": final_stats,
        "qrebs": qrebs_str,
        "eval": eval_stats,
        "skill": base_data.get("skill", "N/A"),
        "standards": [next(o["name"] for o in OPTIONS if o["id"] == sid) for sid in selected_options if sid in standards],
        "extras": [next(o["name"] for o in OPTIONS if o["id"] == sid) for sid in selected_options if sid not in standards],
        "drawbacks": [next(d["name"] for d in all_drawbacks if d["id"] == drawbacks.get(sid)) for sid in selected_options if sid not in standards and drawbacks.get(sid)]
    }

def calculate_premade_armor(body_key, head_key, breather_key):
    keys = [body_key, head_key, breather_key]
    selected = [TYPES[k] for k in keys if k and k in TYPES]
    
    if not selected:
        return None
        
    tl = max(item["tl"] for item in selected)
    mass = sum(item["mass"] for item in selected)
    cost = sum(item["cost"] for item in selected)
    
    stats_keys = ['ar', 'ca', 'fl', 'ra', 'so', 'ps', 'ins', 'seal']
    final_stats = { k: sum(item.get(k, 0) for item in selected) for k in stats_keys }
    
    names = [item["name"] for item in selected]
    long_name = ", ".join(names) + f"-{tl}"
    
    return {
        "long_name": long_name,
        "model": "Composite",
        "tl": tl,
        "mass": mass,
        "cost": cost,
        "stats": final_stats,
        "qrebs": "50000",
        "eval": { "str": 0, "dex": 0, "end": 0, "strMult": 1, "stamina": False },
        "skill": "N/A",
        "notes": ", ".join(names)
    }
