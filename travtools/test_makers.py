import sys
import os

# Add parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from travtools.armourmaker import calculate_custom_armor, TYPES
    from travtools.gunmaker import calculate_weapon, CHART_3_TYPES
    import travtools.data_loader as dl
    
    print("--- Testing Data Loader ---")
    armour_data = dl.get_armour_data()
    gun_data = dl.get_gun_data()
    print(f"Armour data loaded: {len(armour_data.get('TYPES', {}))} types found.")
    print(f"Gun data loaded: {len(gun_data.get('CHART_3_TYPES', {}))} categories found.")
    
    print("\n--- Testing Armour Maker ---")
    # Basic Suit calculation
    result_armour = calculate_custom_armor("S", "", "", "", "", [], {})
    print(f"Basic Suit AR: {result_armour['stats']['ar']}")
    print(f"Basic Suit Cost: {result_armour['cost']}")
    
    print("\n--- Testing Gun Maker ---")
    # Basic Rifle calculation
    result_gun = calculate_weapon("Long Guns", "R", "", [], [], "M", "S", [])
    print(f"Basic Rifle TL: {result_gun['tl']}")
    print(f"Basic Rifle Cost: {result_gun['cost']}")
    
    print("\nVerification Successful!")
    
except Exception as e:
    print(f"\nVerification Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
