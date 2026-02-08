"""
Weapon generation module for Traveller 5.1 rules.
Provides data and calculations for designing and customizing firearms, artillery, 
projectors, and launchers, including mass, cost, damage effects, and firing controls.
"""
import travtools.data_loader as dl

# --- DATA LOADING ---
_data = dl.get_gun_data()
CHART_3_TYPES = _data.get("CHART_3_TYPES", {})
CHART_4_DESCRIPTORS = _data.get("CHART_4_DESCRIPTORS", {})
CHART_5_BURDEN = _data.get("CHART_5_BURDEN", {})
CHART_5_STAGE = _data.get("CHART_5_STAGE", {})
CHART_5_USER = _data.get("CHART_5_USER", {})
CHART_7_OPTIONS = _data.get("CHART_7_OPTIONS", {})
CHART_8_CONTROLS = _data.get("CHART_8_CONTROLS", {})

def calculate_weapon(category, type_code, desc_code, burden_codes, stage_codes, user_code, portability_mode, selected_options):
    """
    Calculates the final statistics for a custom weapon design.
    
    Args:
        category (str): The weapon category (e.g., 'Long Guns', 'Handguns').
        type_code (str): The specific weapon type code.
        desc_code (str): The descriptor modifier code.
        burden_codes (list): List of burden modifier codes.
        stage_codes (list): List of stage modifier codes.
        user_code (str): The user/species modifier code.
        portability_mode (str): Portability setting ('auto' or specific mode).
        selected_options (list): List of selected installable option codes.
        
    Returns:
        dict: A dictionary containing the final weapon name, stats, mass, cost, effects, and controls.
    """
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
    
    # Options Cost: Each option adds 10% of the base cost
    if selected_options:
        cost += (cost * 0.10) * len(selected_options)

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

    
    # Determine Base Key
    base_key = ""
    if category == "Artillery": base_key = "Base_Artillery"
    elif category == "Long Guns": base_key = "Base_Rifle_Carbine"
    elif category == "Handguns": base_key = "Base_Pistol_Revolver"
    elif category == "Shotguns": base_key = "Base_Shotgun"
    elif category == "Machineguns": base_key = "Base_Machinegun"
    elif category in ["Projectors", "Designators"]: base_key = "Base_Projector_Designator"
    elif category == "Launchers": base_key = "Base_Artillery" # HTML Parity: Launchers use Artillery base

    # Controls (Refer to global CHART_8_CONTROLS derived from external data)
    controls = CHART_8_CONTROLS.get(base_key, { "off": False, "single": False, "burst": False, "full": False, "p123": False, "override": False }).copy()

    # Apply Descriptor Logic (Exact HTML Parity)
    if desc_code:
        # Assault (A) or Combat (C) -> Desc_Assault
        if desc_code == "A" or desc_code == "C":
            controls = merge_controls(controls, CHART_8_CONTROLS["Desc_Assault"])
        
        # Plasma (P) or Fusion (F) -> Desc_Plasma_Fusion
        if desc_code == "P" or desc_code == "F":
             controls = merge_controls(controls, CHART_8_CONTROLS["Desc_Plasma_Fusion"])

        # Laser (L) -> Desc_Laser
        if desc_code == "L":
             controls = merge_controls(controls, CHART_8_CONTROLS["Desc_Laser"])
        
        # Gauss (G) -> Special
        if desc_code == "G":
            if category in ["Artillery", "Long Guns", "Machineguns"]:
                controls["burst"] = True
                controls["full"] = True
            else:
                controls["p123"] = True
        
        # Machine (M) -> Full
        if desc_code == "M":
            controls["full"] = True
            
        # Splat (Sp) -> Full
        if desc_code == "Sp":
            controls["full"] = True
            
        # Sub (S) -> Full (only Machineguns)
        if desc_code == "S" and category == "Machineguns":
            controls["full"] = True

    return {
        "model": model,
        "long_name": long_name,
        "tl": tl,
        "range": range_val,
        "mass": mass,
        "cost": cost,
        "qrebs": qrebs,
        "qrebs_mod": b_val,
        "base_qrebs": type_data.get("qrebs", ""),
        "effects": effect_map,
        "controls": controls,
        "options": [CHART_7_OPTIONS[o] for o in selected_options]
    }
