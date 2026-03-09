import sys
import os

# Add parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from travtools.world_map_gen import WorldMapGen

def test_world_gen():
    print("--- Testing World Map Generation Rules ---")
    
    # Test case 1: Agricultural World (Ag)
    print("\nTesting Ag world (A567500-8, Ag):")
    gen_ag = WorldMapGen("A567500-8", trade_codes=["Ag"])
    has_cropland = any('Cropland' in h.terrain for h in gen_ag.get_hexes())
    print(f"Has Cropland: {has_cropland}")
    
    # Test case 2: Vacuum World (Va)
    print("\nTesting Va world (A500000-8, Va):")
    gen_va = WorldMapGen("A500000-8", trade_codes=["Va"])
    has_crater = any('Crater' in h.terrain for h in gen_va.get_hexes())
    print(f"Has Crater: {has_crater}")
    
    # Test case 3: High Population (Hi)
    print("\nTesting Hi world (A867900-A, Hi):")
    gen_hi = WorldMapGen("A867900-A", trade_codes=["Hi"])
    has_arcology = any('Arcology' in h.terrain for h in gen_hi.get_hexes())
    print(f"Has Arcology: {has_arcology}")
    
    # Test case 4: Economic Extension (Resources)
    print("\nTesting Resources (R=5):")
    gen_res = WorldMapGen("A567500-8", economic_ext="(500+0)")
    res_count = sum(1 for h in gen_res.get_hexes() if 'Resource' in h.terrain)
    print(f"Resource Count: {res_count} (Expected: 5)")
    
    # Test case 5: Desert (De)
    print("\nTesting Desert (A567500-8, De, Hyd=0):")
    gen_de = WorldMapGen("A560000-8", trade_codes=["De"])
    has_desert = any('Desert' in h.terrain for h in gen_de.get_hexes())
    print(f"Has Desert: {has_desert}")

    # Test case 6: Ice Caps (Hyd=4 -> 2 rows)
    print("\nTesting Ice Caps (Hyd=4):")
    gen_ice = WorldMapGen("A564500-8")
    has_icecap = any('IceCap' in h.terrain for h in gen_ice.get_hexes())
    print(f"Has IceCap: {has_icecap}")

    print("\nVerification Finished!")

if __name__ == "__main__":
    test_world_gen()
