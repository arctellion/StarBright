import numpy as np
import travtools.converters as cnv

# --- DATA DEFINITIONS ---
# Descriptions with values included for display
DESCRIPTIONS = {
    "quality": {0:"Very Bad (-5)", 1:"Bad (-4)", 2:"Poor (-3)", 3:"Lesser (-2)", 4:"Below Average (-1)", 5:"Average (0)", 6:"Better than same (+1)", 7:"Better than many (+2)", 8:"Very Good (+3)", 9: "Better than most (+4)", 10: "Excellent (+5)"},
    "period": {0:"Minutes", 1:"Hours", 2:"Days", 3:"Weeks", 4:"Months", 5:"Six Months", 6:"One Year", 7:"Two Years", 8:"Three Years", 9: "Four Years", 10: "Ten Years"},
    "reliability": {-5:"Very unreliable", -4:"More unreliable", -3:"Unreliable", -2:"Somewhat unreliable", -1:"Slightly unreliable", 0:"Reliability neutral", 1:"Better than some", 2:"Better than many", 3:"Reliable", 4:"More reliable", 5:"Very reliable"},
    "ease": {-5:"Very difficult to use (-5 EOU)", -4:"More difficult to use (-4 EOU)", -3:"Hard to use (-3 EOU)", -2:"Somewhat hard to use (-2 EOU)", -1:"Slightly difficult to use (-1 EOU)", 0:"Ease of use neutral (0 EOU)", 1:"Better than some (+1 EOU)", 2:"Better than many (+2 EOU)", 3:"Easy to use (+3 EOU)", 4:"Easier to use (+4 EOU)", 5:"Very easy to use (+5 EOU)"},
    "burden": {-5:"Very easy-to-carry (-5 kg)", -4:"Easier to carry (-4 kg)", -3:"Easy to carry/wear (-3 kg)", -2:"Better than many (-2 kg)", -1:"Better than some (-1 kg)", 0:"Burden neutral (0 kg)", 1:"Slightly unurgonomic (+1 kg)", 2:"Unwieldy (+2 kg)", 3:"Hard to carry (+3 kg)", 4:"More burdensome (+4 kg)", 5:"Very burdensome (+5 kg)"},
    "safety": {-5:"Very hazardous", -4:"More hazardous", -3:"Hazardous", -2:"Somewhat hazardous", -1:"Slightly hazardous", 0:"Safety neutral", 1:"Better than some", 2:"Better than many", 3:"Safe to use", 4:"Safer to use", 5:"Very safe"}
}

def generate_qrebs(seed=None, modifiers=None):
    """
    Generates structured QREBS data.
    
    Args:
        seed (int, optional): Seed for reproducibility.
        modifiers (dict, optional): Dictionary of modifiers e.g. {'b': 1, 'q': -2}.
                                    Keys: 'q', 'r', 'e', 'b', 's'.
    
    Returns:
        dict: {
            "code": str (e.g. "52364"),
            "values": dict (numeric values),
            "text": str (formatted description)
        }
    """
    if seed is not None:
        np.random.seed(1000 + seed)
        
    modifiers = modifiers or {}
    
    # Base Rolls - Using numpy for seeding support
    # Quality: 2D-2 (0 to 10)
    # np.random.randint(low, high, size) -> high is exclusive
    q_raw = np.sum(np.random.randint(1, 7, 2)) - 2
    
    # Flux: -5 to +5 (1d6 - 1d6)
    def flux_roll():
        return np.random.randint(1, 7) - np.random.randint(1, 7)

    r_raw = flux_roll()
    e_raw = flux_roll()
    b_raw = flux_roll()
    s_raw = flux_roll()
    
    # Apply Modifiers and Clamp
    # Quality: 0-10
    q = max(0, min(10, q_raw + modifiers.get('q', 0)))
    
    # PER T5.1: Safety is derived from Reliability? Or independent? 
    # Original script treated them all as independent flux rolls. We maintain that.
    
    # Flux Attributes: -5 to +5
    def clamp_flux(val): return max(-5, min(5, val))
    
    r = clamp_flux(r_raw + modifiers.get('r', 0))
    e = clamp_flux(e_raw + modifiers.get('e', 0))
    b = clamp_flux(b_raw + modifiers.get('b', 0))
    s = clamp_flux(s_raw + modifiers.get('s', 0))
    
    # Generate Hex Codes
    q_hex = cnv.ext_hex(q)
    r_hex = cnv.neg_ehex(r, "F")
    e_hex = cnv.neg_ehex(e, "F")
    b_hex = cnv.neg_ehex(b, "F")
    s_hex = cnv.neg_ehex(s, "F")
    
    code = f"{q_hex}{r_hex}{e_hex}{b_hex}{s_hex}"
    
    # Generate Description Text
    # Note: Period is derived from Quality in original script (per = {0:"Minutes"...})
    # We keep that logic: period index = q
    p_text = DESCRIPTIONS["period"].get(q, "Unknown")
    
    text = (
        f"Quality: {q_hex} ({DESCRIPTIONS['quality'].get(q, 'Unknown')})\n"
        f"Period: {p_text}\n"
        f"Reliability: {r_hex} ({DESCRIPTIONS['reliability'].get(r, 'Unknown')})\n"
        f"Ease of Use: {e_hex} ({DESCRIPTIONS['ease'].get(e, 'Unknown')})\n"
        f"Bulk / Burden: {b_hex} ({DESCRIPTIONS['burden'].get(b, 'Unknown')})\n"
        f"Safety: {s_hex} ({DESCRIPTIONS['safety'].get(s, 'Unknown')})"
    )
    
    return {
        "code": code,
        "values": {"q": q, "r": r, "e": e, "b": b, "s": s},
        "text": text,
        "formatted": f"QREBS for device:\n\n{text}"
    }

def qrebs(n, l=0):
    """
    Legacy compatibility wrapper.
    """
    res = generate_qrebs(seed=n)
    if l == 1:
        return res["formatted"] + "\n"
    else:
        return res["code"]

def decode_qrebs(code):
    """
    Decodes a 5-character QREBS string into its description.
    
    Args:
        code (str): The QREBS hex string (e.g. "52364").
        
    Returns:
        dict: {
            "valid": bool,
            "text": str (formatted description or error message)
        }
    """
    if not code or len(code) != 5:
        return {"valid": False, "text": "Invalid Code Length. Must be 5 characters."}
        
    try:
        def parse_quality(char):
            # 0-9, A-Z (similar to extended hex)
            if char.isdigit(): return int(char)
            # Map A=10, B=11 ...
            # Actually QREBS quality is usually 0-10.
            # Only 0-9 and A(10) are standard per the descriptions above?
            # Descriptions go up to 10 ("Excellent (+5)"). 
            # 10 is often represented as 'A'.
            if char.upper() == 'A': return 10
            if char.upper() == 'X': return 10 # Sometimes X is 10?
            # If not found, return value but clamp logic comes later?
            # Let's trust ext_dec for generic hex if needed, but QREBS is specific.
            return cnv.ext_dec(char)

        def parse_flux(char):
            # Parse reverse of neg_ehex
            # neg_ehex(F): -1->A, -2->B, -3->C, -4->D, -5->X
            # But wait, T5 rules or script rules?
            # Looking at neg_ehex source:
            # Fwd: -1->A, -5->X. 
            # So Backwards: A->-1, X->-5
            # Positive numbers likely stay numbers?
            # Let's define a map based on neg_ehex logic
            c = char.upper()
            if c == 'A': return -1
            if c == 'B': return -2
            if c == 'C': return -3
            if c == 'D': return -4
            if c == 'X': return -5
            if c.isdigit(): return int(c)
            # What about +1, +2? Usually '1', '2'.
            return 0 # Fallback

        if not code or len(code) != 5:
             return {"valid": False, "text": "Invalid Code Length. Must be 5 characters."}

        # Quality
        q = parse_quality(code[0])
        
        # Flux Values
        r = parse_flux(code[1])
        e = parse_flux(code[2])
        b = parse_flux(code[3])
        s = parse_flux(code[4])
        
        # Validation Limits
        # Quality 0-10 (technically can go higher/lower but description map has limits)
        if q not in DESCRIPTIONS["quality"]:
            # Maybe clamp it for description lookup?
            pass
            
        p_text = DESCRIPTIONS["period"].get(q, "Unknown")
        
        text = (
            f"Quality: {code[0]} ({DESCRIPTIONS['quality'].get(q, 'Unknown')})\n"
            f"Period: {p_text}\n"
            f"Reliability: {code[1]} ({DESCRIPTIONS['reliability'].get(r, 'Unknown')})\n"
            f"Ease of Use: {code[2]} ({DESCRIPTIONS['ease'].get(e, 'Unknown')})\n"
            f"Bulk / Burden: {code[3]} ({DESCRIPTIONS['burden'].get(b, 'Unknown')})\n"
            f"Safety: {code[4]} ({DESCRIPTIONS['safety'].get(s, 'Unknown')})"
        )
        
        return {"valid": True, "text": text}
        
    except Exception as e:
        return {"valid": False, "text": f"Error parsing code: {str(e)}"}