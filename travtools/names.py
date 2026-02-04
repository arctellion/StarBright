"""
Name generation module for the StarBright project.
Utilizes Markov chains and pre-defined datasets to generate procedural 
character, planet, and object names.
"""
import random
import json
import os
import travtools.dice as dd
import travtools.converters as cnv

# --- DATA LOADING ---

DATA_FILE = os.path.join(os.path.dirname(__file__), "names_data.json")

def load_data():
    """Loads name data from JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback or empty struct if file is missing
        return {
            "male_first": [], "female_first": [], "neutral_first": [],
            "last_names": [], "planet_names": [], "planet_prefixes": [],
            "object_types": [], "brand_names": []
        }

NAME_DATA = load_data()

# --- MARKOV GENERATOR ---

class MarkovGenerator:
    """A character-level Markov chain generator for procedural names."""
    def __init__(self, data, order=2):
        self.order = order
        self.chain = {}
        self.starts = []
        if data:
            self._train(data)

    def _train(self, data):
        for item in data:
            if len(item) < self.order:
                continue
            self.starts.append(item[:self.order])
            for i in range(len(item) - self.order):
                state = item[i:i+self.order]
                next_char = item[i+self.order]
                if state not in self.chain:
                    self.chain[state] = []
                self.chain[state].append(next_char)
            
            # End of word state
            state = item[-(self.order):]
            if state not in self.chain:
                self.chain[state] = []
            self.chain[state].append(None)

    def generate(self, seed=None, min_length=3, max_length=12):
        if not self.starts:
            return "Unknown"
            
        if seed is not None:
            random.seed(seed)
            
        # Start with a random beginning
        res = random.choice(self.starts)
        
        for _ in range(max_length):
            state = res[-self.order:]
            next_chars = self.chain.get(state)
            
            if not next_chars:
                break
                
            next_char = random.choice(next_chars)
            
            if next_char is None:
                if len(res) >= min_length:
                    break
                else:
                    # Try again if too short, or just pick another if stuck
                    continue
            
            res += next_char
            if len(res) >= max_length:
                break
                
        return res.strip().capitalize()

# --- INITIALIZE GENERATORS ---

MALE_GEN = MarkovGenerator(NAME_DATA.get("male_first", []))
FEMALE_GEN = MarkovGenerator(NAME_DATA.get("female_first", []))
NEUTRAL_GEN = MarkovGenerator(NAME_DATA.get("neutral_first", []))
LAST_GEN = MarkovGenerator(NAME_DATA.get("last_names", []))
PLANET_GEN = MarkovGenerator(NAME_DATA.get("planet_names", []))
BRAND_GEN = MarkovGenerator(NAME_DATA.get("brand_names", []))

# --- GENERATION FUNCTIONS ---

def generate_character_name(gender="neutral", seed=None):
    """Generates a full character name using Markov chains."""
    if seed is not None:
        random.seed(seed)
    
    g = gender.lower()
    if g == "male":
        first = MALE_GEN.generate()
    elif g == "female":
        first = FEMALE_GEN.generate()
    else:
        first = NEUTRAL_GEN.generate()
    
    last = LAST_GEN.generate()
    return f"{first} {last}"

def get_uwp_numeric(uwp):
    """Converts a UWP string to a numeric string for seeding."""
    numeric_str = ""
    for char in uwp:
        if char == "-":
            continue
        if char.isdigit():
            numeric_str += char
        else:
            val = ord(char.upper()) - ord('A') + 1
            numeric_str += str(val)
    return numeric_str

def generate_planet_name(hex_location, uwp, seed=None):
    """Generates a planet name based on the specific seed logic."""
    uwp_num = get_uwp_numeric(uwp)
    # Ensure seed is stable regardless of global state if provided
    calc_seed = int(hex_location) + int(uwp_num)
    if seed: calc_seed += seed
    
    random.seed(calc_seed)
    
    # Optional prefix
    prefixes = NAME_DATA.get("planet_prefixes", [])
    if random.random() < 0.3 and prefixes:
        prefix = random.choice(prefixes)
        name = PLANET_GEN.generate()
        return f"{prefix} {name}"
    else:
        return PLANET_GEN.generate()

def generate_object_name(seed=None):
    """Generates an object or item name."""
    if seed is not None:
        random.seed(seed)
    
    brand = BRAND_GEN.generate()
    obj_types = NAME_DATA.get("object_types", [])
    obj_type = random.choice(obj_types) if obj_types else "Device"
    serial = random.randint(100, 999)
    return f"{brand}-{serial} {obj_type}"

if __name__ == "__main__":
    # Test generation
    print("--- Character Names ---")
    for _ in range(5):
        print(f"Male: {generate_character_name('male')}")
        print(f"Female: {generate_character_name('female')}")
        print(f"Neutral: {generate_character_name('neutral')}")
    
    print("\n--- Planet Names ---")
    uwp = "D100559-A"
    loc = "0304"
    for i in range(5):
        print(f"Planet {i}: {generate_planet_name(loc, uwp, seed=i)}")
        
    print("\n--- Object Names ---")
    for _ in range(5):
        print(f"Object: {generate_object_name()}")
