"""
Armour generation module for Traveller 5.1 rules.
Provides data and calculations for custom and pre-made armour systems,
including mass, cost, armour values, and QREBS.
"""
import math
import travtools.data_loader as dl

# --- DATA LOADING ---
_data = dl.get_armour_data()
TYPES = _data.get("TYPES", {})
MODIFIERS = _data.get("MODIFIERS", {})
USERS = _data.get("USERS", {})
OPTIONS = _data.get("OPTIONS", [])
STANDARD_SUBSYSTEMS = _data.get("STANDARD_SUBSYSTEMS", {})
SUBSYSTEM_CATS = _data.get("SUBSYSTEM_CATS", {})
DRAWBACKS = _data.get("DRAWBACKS", {})

# --- CALCULATIONS ---

def calculate_custom_armor(type_key, desc_key, burden_key, stage_key, user_key, selected_options, drawbacks):
    """
    Calculates the final statistics for a custom armour configuration.
    
    Args:
        type_key (str): The base armour type key.
        desc_key (str): The descriptor modifier key.
        burden_key (str): The burden modifier key.
        stage_key (str): The stage modifier key.
        user_key (str): The user species/type key.
        selected_options (list): List of selected subsystem option IDs.
        drawbacks (dict): Mapping of option IDs to their associated drawback IDs.
        
    Returns:
        dict: A dictionary containing the final armour name, stats, mass, cost, etc.
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
