"""
Data loading utility for StarBright.
Handles loading datasets from JSON files.
"""
import json
import os

def load_json_data(filename):
    """
    Loads data from a JSON file in the same directory as this script.
    
    Args:
        filename (str): Name of the JSON file.
        
    Returns:
        dict: The loaded data or an empty dict on error.
    """
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return {}

def get_armour_data():
    """Returns the armour dataset."""
    return load_json_data("armour_data.json")

def get_gun_data():
    """Returns the gun dataset."""
    return load_json_data("gun_data.json")
