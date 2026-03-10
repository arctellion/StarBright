import random
import base64
import math

# --- ICONS (Base64 SVGs) ---
ICON_MOUNTAIN = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M16 6 L28 26 L4 26 Z" fill="#5D4037" stroke="#3E2723" stroke-width="1"/></svg>').decode('utf-8')
ICON_OCEAN = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M4 18 Q10 12 16 18 T28 18" stroke="#90CAF9" fill="none" stroke-width="2"/></svg>').decode('utf-8')
ICON_CITY = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="6" y="6" width="20" height="20" fill="#B0BEC5" stroke="#546E7A" stroke-width="1"/></svg>').decode('utf-8')
ICON_STARPORT = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><polygon points="16,2 19,12 30,12 21,19 24,30 16,23 8,30 11,19 2,12 13,12" fill="#FFFFFF" stroke="#000" stroke-width="0.5"/></svg>').decode('utf-8')
ICON_RUINS = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M8 26 V18 H12 V22 H20 V18 H24 V26 Z" fill="#94a3b8" stroke="#475569" stroke-width="1"/></svg>').decode('utf-8')
ICON_CRATER = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><ellipse cx="16" cy="16" rx="10" ry="6" fill="none" stroke="#71717a" stroke-width="1"/></svg>').decode('utf-8')
ICON_CROPLAND = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M4 24 L8 8 M12 24 L16 8 M20 24 L24 8" stroke="#a3e635" stroke-width="2"/></svg>').decode('utf-8')
ICON_TOWN = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M8 26 V16 L16 10 L24 16 V26 Z" fill="#94a3b8" stroke="#475569" stroke-width="1"/></svg>').decode('utf-8')
ICON_ARCOLOGY = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M16 4 L28 28 H4 Z M16 10 L22 22 H10 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="1"/></svg>').decode('utf-8')
ICON_PENAL = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M8 8 H24 V24 H8 Z M12 8 V24 M16 8 V24 M20 8 V24" fill="none" stroke="#ef4444" stroke-width="1"/></svg>').decode('utf-8')

class Hex:
    def __init__(self, x, y, triangle_id=None, parent_hex=None):
        self.x = x
        self.y = y
        self.triangle_id = triangle_id
        self.parent_hex = parent_hex
        self.terrain = set()
        self.is_land = True
        self.sub_map = None 

    def add(self, terrain_type):
        self.terrain.add(terrain_type)
        if terrain_type in ['Ocean', 'Ocean Depth', 'Abyss', 'Sea']:
            self.is_land = False
        elif terrain_type in ['Islands', 'Shore']:
            self.is_land = True

    def has(self, terrain_type):
        return terrain_type in self.terrain

class Triangle:
    def __init__(self, tid, size, orientation):
        self.id = tid
        self.size = size
        # 1 = Point Up (North/South Poles)
        # 0 = Point Down (Equator)
        self.orientation = orientation
        self.hexes = {}
        self.is_ocean = False

# Standard T5 Regional Map Layout (75 hexes)
# Mapping (q, r) -> (color, number) based on T5 rules / image
# (0,0) is center, q axial, r diagonal-down.
WORLD_HEX_LAYOUT = [
    # Top Row
    (0, -5, 'Black', 36),
    # Row 2
    (-1, -4, 'Black', 41), (0, -4, 'Black', 63), (1, -5, 'Black', 35),
    # Row 3
    (-2, -3, 'Black', 42), (-1, -3, 'White', 31), (0, -3, 'White', 26), (1, -4, 'Black', 62), (2, -5, 'Black', 34), (3, -6, 'White', 66),
    # Row 4
    (-3, -2, 'Black', 43), (-2, -2, 'White', 25), (-1, -2, 'White', 24), (0, -2, 'Black', 64), (1, -3, 'White', 16), (2, -4, 'White', 64), (3, -5, 'Black', 61), (4, -6, 'White', 65), (5, -7, 'Black', 33),
    # Row 5 (12 hexes)
    (-4, -1, 'Black', 11), (-3, -1, 'Black', 44), (-2, -1, 'White', 32), (-1, -1, 'White', 23), (0, -1, 'White', 22), (1, -2, 'Black', 65), (2, -3, 'White', 11), (3, -4, 'White', 12), (4, -5, 'White', 15), (5, -6, 'White', 63), (6, -7, 'White', 61), (7, -8, 'Black', 32),
    # Row 6 (Center, 13 hexes)
    (-5, 0, 'Black', 12), (-4, 0, 'Black', 45), (-3, 0, 'White', 33), (-2, 0, 'White', 34), (-1, 0, 'White', 35), (0, 0, 'Black', 66), (1, -1, 'None', 0), (2, -2, 'White', 14), (3, -3, 'White', 56), (4, -4, 'White', 61), (5, -5, 'White', 55), (6, -6, 'Black', 31), (7, -7, 'White', 56),
    # Row 7 (12 hexes)
    (-5, 1, 'Black', 13), (-4, 1, 'Black', 46), (-3, 1, 'White', 36), (-2, 1, 'White', 41), (-1, 1, 'White', 42), (0, 1, 'Black', 51), (1, 0, 'White', 43), (2, -1, 'White', 44), (3, -2, 'White', 53), (4, -3, 'White', 54), (5, -4, 'White', 52), (6, -5, 'Black', 56),
    # Row 8 (9 hexes)
    (-5, 2, 'Black', 14), (-4, 2, 'Black', 51), (-3, 2, 'White', 16), (-2, 2, 'Black', 16), (-1, 2, 'White', 45), (0, 2, 'White', 46), (1, 1, 'Black', 52), (2, 0, 'White', 51), (3, -1, 'Black', 26), 
    # Row 9 (6 hexes)
    (-5, 3, 'Black', 15), (-4, 3, 'Black', 52), (-3, 3, 'Black', 53), (-2, 3, 'Black', 54), (-1, 3, 'None', 0), (0, 2, 'Black', 25),
    # Row 10 (3 hexes)
    (-4, 4, 'Black', 21), (-3, 4, 'Black', 53), (-2, 4, 'Black', 23),
    # Bottom Row
    (-3, 5, 'Black', 22)
]
# Adjust logic to fill to 75 if needed, but this is the primary structure.

class SubMap:
    def __init__(self, parent_hex, level, rng):
        self.parent_hex = parent_hex
        self.level = level 
        self.rng = rng
        self.hexes = {} 
        self.generate_layout()
        self.populate()

    def generate_layout(self):
        # 75-hex T5 Regional Map layout
        # (q, r, color, number)
        # Transcribed from the provided image
        # Left: World Hex (Regional) - 75 hexes
        # Staggered axial coordinates (q, r) where q is column, r is row-diagonal
        # Transcription from left diagram (row by row):
        layout_world = [
            (0, -5, 'Black', 36),
            (-1, -4, 'Black', 41), (0, -4, 'Black', 63), (1, -5, 'Black', 35),
            (-2, -3, 'Black', 42), (-1, -3, 'White', 31), (0, -3, 'White', 26), (1, -4, 'Black', 62), (2, -5, 'Black', 34), (3, -6, 'White', 66),
            (-3, -2, 'Black', 43), (-2, -2, 'White', 25), (-1, -2, 'White', 24), (0, -2, 'Black', 64), (1, -3, 'White', 16), (2, -4, 'White', 64), (3, -5, 'Black', 61), (4, -6, 'White', 65), (5, -7, 'Black', 33),
            (-4, -1, 'Black', 11), (-3, -1, 'Black', 44), (-2, -1, 'White', 32), (-1, -1, 'White', 23), (0, -1, 'White', 21), (1, -2, 'Black', 65), (2, -3, 'White', 11), (3, -4, 'White', 12), (4, -5, 'White', 15), (5, -6, 'White', 63), (6, -7, 'White', 61), (7, -8, 'Black', 32),
            (-5, 0, 'Black', 12), (-4, 0, 'Black', 45), (-3, 0, 'White', 33), (-2, 0, 'White', 34), (-1, 0, 'White', 35), (0, 0, 'Black', 66), (1, -1, 'White', 16), (2, -2, 'White', 14), (3, -3, 'White', 56), (4, -4, 'White', 61), (5, -5, 'White', 55), (6, -6, 'Black', 31), (7, -7, 'White', 56),
            (-5, 1, 'Black', 13), (-4, 1, 'Black', 46), (-3, 1, 'White', 36), (-2, 1, 'White', 41), (-1, 1, 'White', 42), (0, 1, 'Black', 51), (1, 0, 'White', 43), (2, -1, 'White', 44), (3, -2, 'White', 53), (4, -3, 'White', 54), (5, -4, 'White', 52), (6, -5, 'Black', 56),
            (-5, 2, 'Black', 14), (-4, 2, 'Black', 51), (-3, 2, 'White', 16), (-2, 2, 'Black', 16), (-1, 2, 'White', 45), (0, 2, 'White', 46), (1, 1, 'Black', 52), (2, 0, 'White', 51), (3, -1, 'Black', 26), 
            (-5, 3, 'Black', 15), (-4, 3, 'Black', 52), (-3, 3, 'Black', 53), (-2, 3, 'Black', 54), (-1, 3, 'Black', 25), (0, 3, 'Black', 24),
            (-4, 4, 'Black', 21), (-3, 4, 'Black', 53), (-2, 4, 'Black', 23),
            (-3, 5, 'Black', 22)
        ]
        
        # Middle: Terrain Hex (Vdistant) - 75 hexes
        # Column-based numbering (transcribed from middle diagram)
        layout_terrain = [
            (0, -5, 'Black', 36),
            (-1, -4, 'Black', 41), (0, -4, 'Black', 63), (1, -5, 'Black', 35),
            (-2, -3, 'Black', 42), (-1, -3, 'White', 16), (0, -3, 'White', 42), (1, -4, 'Black', 64), (2, -5, 'Black', 62), (3, -6, 'White', 66),
            (-3, -2, 'Black', 43), (-2, -2, 'White', 44), (-1, -2, 'White', 21), (0, -2, 'White', 15), (1, -3, 'White', 14), (2, -4, 'White', 63), (3, -5, 'Black', 61), (4, -6, 'White', 34),
            (-4, -1, 'Black', 11), (-3, -1, 'Black', 12), (-2, -1, 'White', 24), (-1, -1, 'White', 22), (0, -1, 'White', 13), (1, -2, 'Black', 65), (2, -3, 'White', 64), (3, -4, 'White', 65), (4, -5, 'White', 66), (5, -7, 'Black', 33),
            (-5, 0, 'Black', 12), (-4, 0, 'Black', 45), (-3, 0, 'White', 26), (-2, 0, 'White', 25), (-1, 0, 'White', 23), (0, 0, 'White', 12), (1, -1, 'White', 11), (2, -2, 'White', 66), (3, -3, 'White', 63), (4, -4, 'White', 61), (5, -5, 'White', 33),
            (-5, 1, 'Black', 14), (-4, 1, 'Black', 46), (-3, 1, 'White', 31), (-2, 1, 'White', 32), (-1, 1, 'White', 45), (0, 1, 'White', 66), (1, 0, 'White', 63), (2, -1, 'White', 61), (3, -2, 'Black', 32),
            (-5, 2, 'Black', 15), (-4, 2, 'Black', 51), (-3, 2, 'White', 33), (-2, 2, 'White', 44), (-1, 2, 'White', 46), (0, 2, 'White', 54), (1, 1, 'White', 55), (2, 0, 'White', 62), (3, -1, 'Black', 31),
            (-5, 3, 'Black', 16), (-4, 3, 'White', 34), (-3, 3, 'White', 35), (-2, 3, 'White', 43), (-1, 3, 'White', 51), (0, 3, 'White', 53), (1, 2, 'White', 56), (2, 1, 'Black', 26),
            (-5, 4, 'Black', 52), (-4, 4, 'White', 36), (-3, 4, 'White', 42), (-2, 4, 'White', 52), (-1, 4, 'White', 56), (0, 4, 'Black', 31),
            (-4, 5, 'Black', 21), (-3, 5, 'Black', 53), (-2, 5, 'Black', 41), (-1, 5, 'Black', 54), (0, 5, 'Black', 55), (1, 4, 'Black', 26),
            (-3, 6, 'Black', 22), (-2, 6, 'Black', 23), (-1, 6, 'Black', 24), (0, 6, 'Black', 25)
        ]

        # Right: Local Hex (Distant) - 37 hexes
        # Transcribed from right diagram (mirroring regional layout shape but smaller)
        layout_local = [
            (0, -3, 'Black', 36),
            (-1, -2, 'Black', 41), (0, -2, 'Black', 63), (1, -3, 'Black', 35),
            (-2, -1, 'Black', 42), (-1, -1, 'White', 31), (0, -1, 'White', 26), (1, -2, 'Black', 62), (2, -3, 'Black', 34), (3, -4, 'White', 66),
            (-3, 0, 'Black', 43), (-2, 0, 'White', 25), (-1, 0, 'White', 24), (0, 0, 'Black', 65), (1, -1, 'White', 16), (2, -2, 'White', 64), (3, -3, 'Black', 61), (4, -4, 'White', 65), (5, -5, 'Black', 33),
            (-3, 1, 'Black', 44), (-2, 1, 'White', 32), (-1, 1, 'White', 23), (0, 1, 'Black', 66), (1, 0, 'White', 11), (2, -1, 'White', 12), (3, -2, 'White', 15), (4, -3, 'White', 63),
            (-3, 2, 'Black', 45), (-2, 2, 'White', 33), (-1, 2, 'White', 34), (0, 2, 'White', 35), (1, 1, 'White', 14), (2, 0, 'White', 56), (3, -1, 'White', 61),
            (-2, 3, 'Black', 46), (-1, 3, 'White', 36), (0, 3, 'White', 41), (1, 2, 'White', 42), (2, 1, 'White', 55),
            (-2, 4, 'Black', 51), (-1, 4, 'White', 43), (0, 4, 'White', 44), (1, 3, 'White', 53),
            (-1, 5, 'Black', 52), (0, 5, 'White', 51), (1, 4, 'Black', 26),
            (-1, 6, 'Black', 53), (0, 6, 'Black', 25),
            (0, 7, 'Black', 21)
        ]

        if self.level == "Terrain":
            layout_data = layout_terrain
        elif self.level == "Local":
            layout_local_actual = layout_local # Or a variant if they are identical
            layout_data = layout_local_actual
        else: # World Hex (Regional)
            layout_data = layout_world

        
        self.hexes = {}
        for q, r, color, num in layout_data:
            h = Hex(q, r, parent_hex=self.parent_hex)
            h.color = color
            h.number = num
            self.hexes[(q, r)] = h

    def get_next_level(self):
        levels = ["World", "Terrain", "Local"]
        try:
            return levels[levels.index(self.level) + 1]
        except (ValueError, IndexError):
            return None

    def populate(self):
        # 1. Table-based population from worldhex.rules.md
        if not self.parent_hex: return
        parent_terrain = list(self.parent_hex.terrain)
        
        # Consistent mapping based on worldmap.rules.md and T5 conventions
        rules = {
            'Ocean': {31: 'Ocean', 32: 'Islands', 11: 'Reef'},
            'Mountain': {21: 'Mountain', 11: 'Rough'},
            'IceCap': {36: 'IceCap', 44: 'Ice Field'},
            'Desert': {22: 'Desert', 21: 'Mesa'},
            'City': {51: 'City', 55: 'Town', 24: 'Cropland'},
            'Ruins': {26: 'Ruins', 11: 'Rough'},
            'Starport': {56: 'Starport', 51: 'City'},
            'Crater': {74: 'Crater', 11: 'Rough'},
            'Frozen Lands': {43: 'Frozen Lands', 44: 'Ice Field'},
            'Baked Lands': {41: 'Baked Lands', 22: 'Desert'},
            'Cropland': {24: 'Cropland', 23: 'Rural'},
        }

        # Determine base terrain (the most "fundamental" one)
        # Priority: Ocean > IceCap > Desert > Clear
        base_fill = 'Clear'
        for t in ['Ocean', 'IceCap', 'Desert', 'Frozen Lands', 'Baked Lands']:
            if t in parent_terrain:
                base_fill = t
                break
        
        for h in self.hexes.values():
            h.add(base_fill)

        # Apply specific overrides for each terrain type found on parent
        for pt in parent_terrain:
            rule = rules.get(pt)
            if rule:
                for h in self.hexes.values():
                    # Apply if there's a specific instruction for this hex number
                    # or if the color matches a generic pattern (simplified)
                    t_over = rule.get(h.number)
                    if t_over:
                        h.add(t_over)
                    
                    # Special color-based distributions for certain terrains
                    if pt == 'City' and h.color == 'White' and self.rng.random() < 0.2:
                        h.add('Rural')
                    if pt == 'Ocean' and h.color == 'Black' and self.rng.random() < 0.1:
                        h.add('Ocean Depth')

        # Handle Shore lines specifically (interpolation)
        if 'Shore' in parent_terrain:
            for h in self.hexes.values():
                # Simple spatial gradient for shorelines
                if h.y < 0: h.add('Ocean')
                elif h.y == 0: h.add('Shore')
                else: h.add('Clear')

class WorldMapGen:
    def __init__(self, uwp, trade_codes=None, economic_ext=None, seed=None):
        self.uwp = uwp
        self.size = self.parse_hex(uwp[1])
        self.atmos = self.parse_hex(uwp[2])
        self.hydro = self.parse_hex(uwp[3])
        self.pop = self.parse_hex(uwp[4])
        self.tech = self.parse_hex(uwp[8])
        
        self.trade_codes = trade_codes if trade_codes else []
        self.economic_ext = economic_ext if economic_ext else "(000+0)"
        self.seed_val = seed if seed is not None else sum(ord(c) for c in uwp)
        self.rng = random.Random(self.seed_val)
        
        self.triangles = []
        self.generate_grid()
        self.generate_terrain_pdf_rules()

    def parse_hex(self, char):
        if '0' <= char <= '9': return int(char)
        return ord(char.upper()) - ord('A') + 10

    def generate_grid(self):
        """Generates 20 triangles in a 5-10-5 Icosahedral layout."""
        for tid in range(20):
            # Define Rows and Orientations
            if tid < 5: 
                orientation = 1  # North: All Point Up
            elif tid < 15:
                # Equator: Alternating Down/Up starting with Down (0)
                # This ensures the flat top of Eq Tri 0 mates with North Tri 0.
                orientation = 0 if (tid - 5) % 2 == 0 else 1
            else:
                orientation = 0  # South: All Point Down

            t = Triangle(tid, self.size, orientation)
            
            if orientation == 1: # Point Up
                for y in range(self.size):
                    for x in range(y + 1):
                        t.hexes[(x, y)] = Hex(x, y, tid)
            else: # Point Down
                for y in range(self.size):
                    width = self.size - y
                    for x in range(width):
                        t.hexes[(x, y)] = Hex(x, y, tid)
            
            self.triangles.append(t)

    def get_hexes(self):
        for t in self.triangles:
            for h in t.hexes.values():
                yield h

    def get_neighbors(self, h):
        x, y, tid = h.x, h.y, h.triangle_id
        t = self.triangles[tid]
        neighbors = []
        if t.orientation == 1: offsets = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)] 
        else: offsets = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if (nx, ny) in t.hexes:
                neighbors.append(t.hexes[(nx, ny)])
        return neighbors

    def generate_terrain_pdf_rules(self):
        # 2. Resources (R from Ex)
        try: res_val = self.parse_hex(self.economic_ext[1])
        except: res_val = 0
        for _ in range(res_val):
            t = self.rng.choice(self.triangles)
            h = self.rng.choice(list(t.hexes.values()))
            h.add('Resource')

        # 3. Mountains
        for t in self.triangles:
            num_mtns = self.rng.randint(1, 6)
            candidates = list(t.hexes.values())
            self.rng.shuffle(candidates)
            for i in range(min(num_mtns, len(candidates))):
                candidates[i].add('Mountain')

        # 4 & 5. Chasms and Precipices
        for _ in range(self.size):
            t_c = self.rng.choice(self.triangles)
            for _ in range(self.rng.randint(1, 6)):
                self.rng.choice(list(t_c.hexes.values())).add('Chasm')
            t_p = self.rng.choice(self.triangles)
            self.rng.choice(list(t_p.hexes.values())).add('Precipice')

        # 6. Die-Back (Ruins)
        if 'Di' in self.trade_codes:
            for t in self.triangles:
                num_ruins = self.rng.randint(1, 6)
                for _ in range(num_ruins):
                    self.rng.choice(list(t.hexes.values())).add('Ruins')

        # 7. Vacuum Plain (Craters)
        if 'Va' in self.trade_codes:
            for t in self.triangles:
                num_craters = self.rng.randint(1, 6)
                for _ in range(num_craters):
                    self.rng.choice(list(t.hexes.values())).add('Crater')

        # 9. Oceans
        num_ocean_triangles = min(20, self.hydro * 2)
        ocean_triangle_ids = self.rng.sample(range(20), num_ocean_triangles)
        land_triangle_ids = [i for i in range(20) if i not in ocean_triangle_ids]

        for tid in ocean_triangle_ids:
            t = self.triangles[tid]
            t.is_ocean = True
            for h in t.hexes.values():
                h.add('Ocean')
        
        # 8. Desert Fill (after ocean selection)
        if 'De' in self.trade_codes:
            for h in self.get_hexes():
                if not h.terrain:
                    h.add('Desert')

        # 10. Seas
        num_seas = min(len(land_triangle_ids), self.hydro)
        sea_triangles = self.rng.sample(land_triangle_ids, num_seas)
        for tid in sea_triangles:
            t = self.triangles[tid]
            h = self.rng.choice(list(t.hexes.values()))
            h.add('Sea')

        # 11. Islands
        for tid in ocean_triangle_ids:
            t = self.triangles[tid]
            for h in t.hexes.values():
                if h.has('Mountain'):
                    h.terrain.discard('Mountain')
                    h.add('Islands')

        # Shore lines
        for h in self.get_hexes():
            if h.is_land:
                neighbors = self.get_neighbors(h)
                for n in neighbors:
                    if n.has('Ocean') or n.has('Sea'):
                        h.add('Shore')
                        break

        # 12. Ice-Caps. (Hyd/2 rows top and bottom)
        rows = self.hydro // 2
        if rows > 0:
            for tid in range(5): # North
                t = self.triangles[tid]
                for h in t.hexes.values():
                    if h.y < rows:
                        if h.has('Ocean'): h.add('Ice Field')
                        else: h.add('IceCap')
            for tid in range(15, 20): # South
                t = self.triangles[tid]
                for h in t.hexes.values():
                    if h.y >= (self.size - rows):
                        if h.has('Ocean'): h.add('Ice Field')
                        else: h.add('IceCap')

        # 13. Ic - More Ice Cap
        if 'Ic' in self.trade_codes:
            extra = self.rng.randint(1, 6)
            for tid in range(5):
                for h in self.triangles[tid].hexes.values():
                    if h.y < (rows + extra):
                        if h.has('Ocean'): h.add('Ice Field')
                        else: h.add('IceCap')
            for tid in range(15, 20):
                for h in self.triangles[tid].hexes.values():
                    if h.y >= (self.size - rows - extra):
                        if h.has('Ocean'): h.add('Ice Field')
                        else: h.add('IceCap')

        # 14 & 15. Fr / Tu
        if 'Fr' in self.trade_codes or 'Tu' in self.trade_codes:
            for h in self.get_hexes():
                if h.has('Ocean'): h.add('Ice Field')
                elif h.is_land and not h.has('IceCap'): h.add('Frozen Lands')

        # 16 & 17. Ag / Fa
        if 'Ag' in self.trade_codes or 'Fa' in self.trade_codes:
            num = self.rng.randint(2, 12) if 'Ag' in self.trade_codes else self.rng.randint(1, 6)
            for t in self.triangles:
                if not t.is_ocean:
                    for _ in range(num):
                        land_hexes = [h for h in t.hexes.values() if h.is_land]
                        if land_hexes: self.rng.choice(land_hexes).add('Cropland')

        # 18-21. Pop features
        if self.pop > 0:
            if 'Lo' in self.trade_codes or 'Ni' in self.trade_codes:
                land = [h for h in self.get_hexes() if h.is_land]
                if land: self.rng.choice(land).add('Town')
            else:
                cities_to_place = self.pop
                continents = [t for t in self.triangles if not t.is_ocean]
                self.rng.shuffle(continents)
                for t in continents:
                    if cities_to_place <= 0: break
                    land_hexes = [h for h in t.hexes.values() if h.is_land]
                    if land_hexes:
                        self.rng.choice(land_hexes).add('City')
                        cities_to_place -= 1
                if 'Hi' in self.trade_codes:
                    for _ in range(self.pop // 2):
                        land = [h for h in self.get_hexes() if h.is_land]
                        if land: self.rng.choice(land).add('Arcology')

        # 22. Rural
        cities = [h for h in self.get_hexes() if h.has('City') or h.has('Arcology')]
        for city in cities:
            for h in self.get_hexes():
                if h.is_land and not h.has('City') and not h.has('Arcology'):
                    dist = abs(h.x - city.x) + abs(h.y - city.y) 
                    if dist <= self.pop: h.add('Rural')

        # 23. Starport
        if cities: self.rng.choice(cities).add('Starport')
        else:
            land = [h for h in self.get_hexes() if h.is_land]
            if land: self.rng.choice(land).add('Starport')

        # 26. Penal
        if 'Pe' in self.trade_codes:
            for t in self.triangles:
                for _ in range(self.pop):
                    land = [h for h in t.hexes.values() if h.is_land]
                    if land: self.rng.choice(land).add('Penal')

        # 27. Wasteland
        if self.tech > 5:
            t = self.rng.choice(self.triangles)
            num_waste = self.rng.randint(1, 6)
            for _ in range(num_waste):
                self.rng.choice(list(t.hexes.values())).add('Wasteland')

        # 28 & 29. Exotic & Noble
        t_e = self.rng.choice(self.triangles)
        self.rng.choice(list(t_e.hexes.values())).add('Exotic')
        t_n = self.rng.choice(self.triangles)
        self.rng.choice(list(t_n.hexes.values())).add('Noble Lands')

        # 30. Clear
        for h in self.get_hexes():
            if not h.terrain:
                h.add('Clear')

    def get_map_json(self):
        output = []
        for t in self.triangles:
            tri = {'id': t.id, 'orientation': t.orientation, 'hexes': []}
            for h in t.hexes.values():
                h_data = {'x': h.x, 'y': h.y, 'terrain': list(h.terrain)}
                tri['hexes'].append(h_data)
            output.append(tri)
        return output

    def subdivide_hex(self, triangle_id, x, y, terrain_x=None, terrain_y=None):
        """Recursively subdivide from World -> Terrain -> Local."""
        target_tri = self.triangles[triangle_id]
        target_hex = target_tri.hexes.get((x, y))
        
        if not target_hex:
            return None
            
        # Level 1: World -> Terrain
        if not target_hex.sub_map:
            target_hex.sub_map = SubMap(target_hex, "Terrain", self.rng)
            
        if terrain_x is None or terrain_y is None:
            return target_hex.sub_map
            
        # Level 2: Terrain -> Local
        terrain_hex = target_hex.sub_map.hexes.get((terrain_x, terrain_y))
        if terrain_hex:
            if not terrain_hex.sub_map:
                terrain_hex.sub_map = SubMap(terrain_hex, "Local", self.rng)
            return terrain_hex.sub_map
            
        return None