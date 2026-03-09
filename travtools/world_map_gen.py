import random
import base64

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

class SubMap:
    def __init__(self, parent_hex, level, rng):
        self.parent_hex = parent_hex
        self.level = level 
        self.rng = rng
        self.hexes = {} 
        self.generate_cluster()
        self.populate()

    def generate_cluster(self):
        for q in range(-5, 6):
            for r in range(-5, 6):
                if abs(q) <= 5 and abs(r) <= 5 and abs(q + r) <= 5:
                    self.hexes[(q, r)] = Hex(q, r, parent_hex=self.parent_hex)

    def populate(self):
        p_terrain = 'Clear'
        if self.parent_hex and self.parent_hex.terrain:
            if 'Ocean' in self.parent_hex.terrain: p_terrain = 'Ocean'
            elif 'Mountain' in self.parent_hex.terrain: p_terrain = 'Mountain'
            elif 'IceCap' in self.parent_hex.terrain: p_terrain = 'IceCap'
            else: p_terrain = list(self.parent_hex.terrain)[0]

        if p_terrain == 'Ocean':
            for h in self.hexes.values(): h.add('Ocean')
            if (0,0) in self.hexes: self.hexes[(0,0)].add('Ocean Depth')
        elif p_terrain == 'Mountain':
            for h in self.hexes.values(): h.add('Rough')
            for _ in range(5): self.rng.choice(list(self.hexes.values())).add('Mountain')
        elif p_terrain == 'IceCap':
            for h in self.hexes.values(): h.add('IceCap')
        else:
            for h in self.hexes.values(): h.add('Clear')
            for _ in range(3): self.rng.choice(list(self.hexes.values())).add('Rough')

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

    def subdivide_hex(self, triangle_id, x, y):
        target_tri = self.triangles[triangle_id]
        target_hex = target_tri.hexes.get((x, y))
        if target_hex:
            if not target_hex.sub_map:
                target_hex.sub_map = SubMap(target_hex, "Terrain", self.rng)
            return target_hex.sub_map
        return None