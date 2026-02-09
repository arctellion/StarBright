import sys
import os

# Add parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import travtools.traveller_map_api as tmap

def test_mapping():
    print("--- Testing Traveller Map API Mapping ---")
    
    # Mock API world data
    mock_world = {
        "Name": "Regina",
        "Hex": "1910",
        "UWP": "A788899-C",
        "PBG": "703",
        "Bases": "NS",
        "Remarks": "Ri Pa Ph An Cp (Amindii)2 Varg0 Asla0 Sa Ht",
        "Importance": 4,
        "Resources": 13, # D
        "Labour": 7,      # 7
        "Infrastructure": 14, # E
        "Efficiency": 5,
        "Culture": 12 # C
    }
    
    mapped = tmap.map_api_to_system(mock_world)
    
    print(f"Name: {mapped['name']} (Expected: Regina)")
    print(f"Coord: {mapped['coord']} (Expected: 1910)")
    print(f"UWP: {mapped['uwp']} (Expected: A788899-C)")
    print(f"PBG: {mapped['pbg']} (Expected: 703)")
    print(f"Bases: {mapped['bases']} (Expected: NS)")
    print(f"Trade: {mapped['trade']} (Expected: Ri Pa Ph ...)")
    print(f"Ext: {mapped['ext']}")
    
    # Check extension parts
    # { 4 }(D7E+5)[0012]
    assert "{ 4 }" in mapped['ext']
    assert "(D7E+5)" in mapped['ext']
    
    print("\nMapping Verification Successful!")

def test_metadata_fetching():
    print("\n--- Testing Traveller Map Metadata Fetching ---")
    meta = tmap.fetch_sector_metadata("1105", "Spinward Marches")
    assert meta is not None
    assert "Subsectors" in meta
    
    # Subsector C should be Regina
    regina = next((ss for ss in meta["Subsectors"] if ss["Index"] == "C"), None)
    assert regina is not None
    print(f"Subsector C: {regina['Name']} (Expected: Regina)")
    assert regina["Name"] == "Regina"
    
    print("Metadata Fetching Verification Successful!")

def test_tab_parsing():
    print("\n--- Testing Traveller Map TabDelimited Parsing ---")
    
    mock_tab = (
        "Sector\tSS\tHex\tName\tUWP\tBases\tRemarks\tZone\tPBG\tAllegiance\tStars\t{Ix}\t(Ex)\t[Cx]\tNobility\tW\tRU\n"
        "Spinward Marches\tA\t1910\tRegina\tA788899-C\tNS\tRi Pa Ph\t\t703\tIm\tG2V\t{ 4 }\t(D7E+5)\t[6b22]\t\t\t\n"
    )
    
    systems = tmap.parse_tab_data(mock_tab)
    
    assert len(systems) == 1
    s = systems[0]
    
    print(f"Name: {s['name']} (Expected: Regina)")
    assert s['name'] == "Regina"
    assert s['coord'] == "1910"
    assert s['subsector'] == "A"
    assert s['ext'] == "{ 4 }(D7E+5)[6b22]"
    
    print("TabDelimited Parsing Verification Successful!")

if __name__ == "__main__":
    try:
        test_mapping()
        test_metadata_fetching()
        test_tab_parsing()
    except Exception as e:
        print(f"\nVerification Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
