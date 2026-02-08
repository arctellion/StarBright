"""
Vehicle generation module for Traveller 5.1 rules.
Ported from omni_vehicle_maker (o_vehicle_common.js and omni_maker.js).
Handles calculations for Ground, Flyer, Watercraft, and Military vehicles.
"""
import math
import re
import travtools.data_loader as dl

# --- DATA LOADING ---
_data = dl.get_vehicle_data()
KEYS = _data.get("keys", [])
GROUND = _data.get("ground", [])
GR_MISSION = _data.get("gr_mission", [])
GR_MOTIVE = _data.get("gr_motive", [])
FLYERS = _data.get("flyers", [])
F_MISSION = _data.get("f_mission", [])
F_MOTIVE = _data.get("f_motive", [])
WATERCRAFT = _data.get("watercraft", [])
W_MISSION = _data.get("w_mission", [])
W_MOTIVE = _data.get("w_motive", [])
MILITARY = _data.get("military", [])
M_MISSION = _data.get("m_mission", [])
M_MOTIVE = _data.get("m_motive", [])
BULK = _data.get("vehicle_bulk", [])
STAGE = _data.get("vehicle_stage", [])
OPT = _data.get("vehicle_opt", [])
ENDURANCE = _data.get("vehicle_endurance", [])
DESCRIPTORS = _data.get("vehicle_descriptors", [])

def compose(elements):
    """
    Core calculation logic ported from JS 'compose' function.
    Processes a list of element data (lists of values corresponding to KEYS)
    and applies sigil-based modifications.
    """
    if not elements:
        return None
    
    # Start with a copy of the first element (the base craft)
    # We use a dictionary for easier field access by key
    out = {KEYS[i]: elements[0][i] for i in range(len(KEYS))}
    
    for i in range(1, len(elements)):
        item_raw = elements[i]
        for j in range(len(KEYS)):
            key = KEYS[j]
            val_to_apply = item_raw[j]
            
            # Convert to string for regex matching
            f1 = str(val_to_apply)
            
            # Logic from JS el.match( /^[^\(\-\$=x\+\^\_\/]/ ) ) f1 = '+' + f1;
            # If it doesn't start with a sigil, assume it's an additive number
            if not re.match(r'^[(\-$=x+^_/]', f1):
                f1 = '+' + f1
            
            # match sigil and value
            # JS: var field = f1.match( /^([\(\-=x\+\^\_\/]|\$speed x)\s*(.*)$/ );
            match = re.match(r'^([(\-=x+^_/]|(?:\$speed x))\s*(.*)$', f1)
            if not match:
                continue
                
            sigil = match.group(1)
            val_str = match.group(2)
            
            if sigil == '(':
                # Ignore string context
                continue
            elif sigil == '=':
                # Override
                out[key] = val_str
            elif sigil == 'x':
                # Multiply
                try:
                    out[key] = float(out[key]) * float(val_str)
                    out[key] = round(out[key], 2)
                except (ValueError, TypeError):
                    pass
            elif sigil == '/':
                # Divide
                try:
                    if float(val_str) != 0:
                        out[key] = float(out[key]) / float(val_str)
                        out[key] = round(out[key], 2)
                except (ValueError, TypeError):
                    pass
            elif sigil == '-':
                # Subtract number
                try:
                    out[key] = float(out[key]) - float(val_str)
                except (ValueError, TypeError):
                    pass
            elif sigil == '^':
                # Max
                try:
                    out[key] = max(float(val_str), float(out[key]))
                except (ValueError, TypeError):
                    pass
            elif sigil == '_':
                # Min
                try:
                    out[key] = min(float(val_str), float(out[key]))
                except (ValueError, TypeError):
                    pass
            elif sigil == '$speed x':
                # Multiply by current speed rating
                try:
                    speed_val = float(out.get('spd', 0))
                    bonus = speed_val * float(val_str)
                    out[key] = float(out[key]) + bonus
                except (ValueError, TypeError):
                    pass
            elif val_str.isalpha() or (val_str and not val_str[0].isdigit() and val_str[0] not in '+-'):
                 # Concat to front of string (JS: val.match( /\D/ ))
                 out[key] = val_str + str(out[key])
            else:
                # Default: Add number
                try:
                    out[key] = float(out[key]) + float(val_str)
                except (ValueError, TypeError):
                    pass
                    
    return out

def calculate_vehicle(category, base_idx, mission_idx, motive_idx, bulk_idx, stage_idx, desc_idx, opt_idxs, end_idx):
    """
    Orchestrates the calculation for a vehicle.
    """
    elements = []
    
    # 1. Base Craft
    if category == "ground":
        elements.append(GROUND[base_idx])
        elements.append(GR_MISSION[mission_idx])
        elements.append(GR_MOTIVE[motive_idx])
    elif category == "flyer":
        elements.append(FLYERS[base_idx])
        elements.append(F_MISSION[mission_idx])
        elements.append(F_MOTIVE[motive_idx])
    elif category == "watercraft":
        elements.append(WATERCRAFT[base_idx])
        elements.append(W_MISSION[mission_idx])
        elements.append(W_MOTIVE[motive_idx])
    elif category == "military":
        elements.append(MILITARY[base_idx])
        elements.append(M_MISSION[mission_idx])
        elements.append(M_MOTIVE[motive_idx])
        
    # 2. Add standardized modifiers
    elements.append(BULK[bulk_idx])
    elements.append(STAGE[stage_idx])
    elements.append(DESCRIPTORS[desc_idx])
    
    # 3. Dynamic options
    for o_idx in opt_idxs:
        elements.append(OPT[o_idx])
        
    # 4. Endurance
    elements.append(ENDURANCE[end_idx])
    
    # Perform calculation
    result = compose(elements)
    
    # Final cleanup (ensure numbers are clean)
    for k in result:
        if isinstance(result[k], float):
            if result[k] == int(result[k]):
                result[k] = int(result[k])
            else:
                result[k] = round(result[k], 2)
                
    return result
