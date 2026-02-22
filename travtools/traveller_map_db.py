import sqlite3
import os

# Database path (relative to project root)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'traveller_map.db')

def get_milieux():
    """Returns a list of available milieux."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM MILIEU ORDER BY id ASC")
        milieux = [row[0] for row in cursor.fetchall()]
        conn.close()
        return milieux
    except Exception as e:
        print(f"Error fetching milieux from DB: {e}")
        return []

def get_sectors(milieu_name):
    """Returns sectors for a given milieu that have star systems."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = """
            SELECT DISTINCT S.name, S.abbreviation, S.x, S.y
            FROM SECTOR S
            JOIN MILIEU M ON S.milieu_id = M.id
            JOIN SUBSECTOR SS ON SS.sector_id = S.id
            JOIN WORLD W ON W.subsector_id = SS.id
            WHERE M.name = ? AND S.name IS NOT NULL
            ORDER BY S.name ASC
        """
        cursor.execute(query, (milieu_name,))
        sectors = []
        for row in cursor.fetchall():
            sectors.append({
                'name': row[0],
                'abbreviation': row[1],
                'x': row[2],
                'y': row[3]
            })
        conn.close()
        return sectors
    except Exception as e:
        print(f"Error fetching sectors from DB: {e}")
        return []

def get_sector_systems(milieu_name, sector_name):
    """
    Fetches all systems for a sector in a specific milieu.
    Maps database columns to internal StarBright system format.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Allow access by column name
        cursor = conn.cursor()
        
        query = """
            SELECT 
                W.*, 
                SS."index" as ss_index, 
                SS.name as ss_name,
                S.name as sector_name_db
            FROM WORLD W
            JOIN SUBSECTOR SS ON W.subsector_id = SS.id
            JOIN SECTOR S ON SS.sector_id = S.id
            JOIN MILIEU M ON S.milieu_id = M.id
            WHERE M.name = ? AND S.name = ?
        """
        cursor.execute(query, (milieu_name, sector_name))
        rows = cursor.fetchall()
        
        systems = []
        for row in rows:
            # Map DB columns to inner format
            # ext: {Ix}(Ex)[Cx]
            # DB has ix (integer), ex (string), cx (string)
            ix = row['ix'] if row['ix'] is not None else 0
            ix_str = f"{{ {ix} }}"
            ext = f"{ix_str}{row['ex'] or ''}{row['cx'] or ''}"
            
            system = {
                'name': row['name'] or 'Unknown',
                'coord': row['hex'],
                'uwp': row['uwp'],
                'pbg': row['pbg'],
                'bases': row['bases'] or '',
                'trade': row['remarks'] or '',
                'ext': ext,
                'stars': row['stars'] or '',
                'allegiance': row['allegiance'] or '',
                'subsector': row['ss_index'], # 'A', 'B', etc.
                'sector_name': sector_name,
                'raw_api_data': dict(row) # For detailed display
            }
            systems.append(system)
            
        conn.close()
        return systems
    except Exception as e:
        print(f"Error fetching sector systems from DB: {e}")
        return []

def get_sector_metadata(milieu_name, sector_name):
    """
    Fetches subsector names for a given sector.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = """
            SELECT SS."index", SS.name
            FROM SUBSECTOR SS
            JOIN SECTOR S ON SS.sector_id = S.id
            JOIN MILIEU M ON S.milieu_id = M.id
            WHERE M.name = ? AND S.name = ?
            ORDER BY SS."index" ASC
        """
        cursor.execute(query, (milieu_name, sector_name))
        metadata = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return metadata
    except Exception as e:
        print(f"Error fetching sector metadata from DB: {e}")
        return {}
