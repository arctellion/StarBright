import requests
import json
import travtools.converters as cnv
import io
import csv

def fetch_subsector_data(sector_name, subsector_name):
    """
    Fetches subsector data from Traveller Map API in JSON format.
    Keep this for backward compatibility or simple JSON lookups.
    """
    url = f"https://travellermap.com/api/sec?sector={sector_name}&subsector={subsector_name}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data from Traveller Map: {e}")
        return None

def fetch_sector_tab_data(milieu, sector_name):
    """
    Fetches full sector data in TabDelimited format for a specific milieu.
    The milieu parameter MUST include the 'M' prefix (e.g., M1105).
    """
    milieu_val = milieu if milieu.startswith('M') else f"M{milieu}"
    url = f"https://travellermap.com/api/sec?milieu={milieu_val}&sector={sector_name}&type=TabDelimited&sscoords=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching TabDelimited data: {e}")
        return None

def fetch_sector_metadata(milieu, sector_name):
    """
    Fetches metadata for a sector, containing subsector names.
    URL: https://travellermap.com/api/metadata?milieu=M1105&sector=Spinward%20Marches
    """
    milieu_val = milieu if milieu.startswith('M') else f"M{milieu}"
    url = f"https://travellermap.com/api/metadata?milieu={milieu_val}&sector={sector_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return None

def parse_tab_data(tab_text):
    """
    Parses TabDelimited response into a list of system dictionaries.
    """
    if not tab_text:
        return []
    
    systems = []
    # Use io.StringIO to treat the text as a file for csv.DictReader
    f = io.StringIO(tab_text.strip())
    # TabDelimited means delimiter is '\t'
    reader = csv.DictReader(f, delimiter='\t')
    
    for row in reader:
        # Map TabDelimited headers to internal format
        # Headers: Sector, SS, Hex, Name, UWP, Bases, Remarks, Zone, PBG, Allegiance, Stars, {Ix}, (Ex), [Cx], Nobility, W, RU
        
        # Extension: {Ix}(Ex)[Cx]
        ix = row.get('{Ix}', '{ 0 }')
        ex = row.get('(Ex)', '(000+0)')
        cx = row.get('[Cx]', '[0000]')
        ext = f"{ix}{ex}{cx}"
        
        system = {
            'name': row.get('Name', 'Unknown'),
            'coord': row.get('Hex', '0000'),
            'uwp': row.get('UWP', 'XXXXXXX-X'),
            'pbg': row.get('PBG', '000'),
            'bases': row.get('Bases', ''),
            'trade': row.get('Remarks', ''),
            'ext': ext,
            'stars': row.get('Stars', ''),
            'allegiance': row.get('Allegiance', ''),
            'subsector': row.get('SS', ''), # Useful for filtering
            'sector_name': row.get('Sector', ''),
            'raw_api_data': dict(row) # Future-proofing / Detailed display
        }
        systems.append(system)
    
    return systems

def map_api_to_system(api_world):
    """
    Converts a Traveller Map API world object (JSON format) to internal representation.
    """
    ix = api_world.get('Importance', 0)
    ix_str = f"{{ {ix} }}"
    
    ex_str = f"({cnv.ext_hex(api_world.get('Resources', 0))}{cnv.ext_hex(api_world.get('Labour', 0))}{cnv.ext_hex(api_world.get('Infrastructure', 0))}"
    eff = api_world.get('Efficiency', 0)
    if eff >= 0:
        ex_str += f"+{eff})"
    else:
        ex_str += f"{eff})"
        
    culture = api_world.get('Culture', 0)
    cx_str = f"[{culture:04d}]" # Placeholder/Simplified
    
    ext = ix_str + ex_str + cx_str

    return {
        'name': api_world.get('Name', 'Unknown'),
        'coord': api_world.get('Hex', '0000'),
        'uwp': api_world.get('UWP', 'XXXXXXX-X'),
        'pbg': api_world.get('PBG', '000'),
        'bases': api_world.get('Bases', ''),
        'trade': api_world.get('Remarks', ''),
        'ext': ext,
        'stars': api_world.get('Stars', ''),
        'allegiance': api_world.get('Allegiance', '')
    }
