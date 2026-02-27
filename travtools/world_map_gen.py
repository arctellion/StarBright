import random
import base64

# --- ICONS (Base64 SVGs) ---
ICON_MOUNTAIN = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M16 6 L28 26 L4 26 Z" fill="#5D4037" stroke="#3E2723" stroke-width="1"/></svg>').decode('utf-8')
ICON_OCEAN = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M4 18 Q10 12 16 18 T28 18" stroke="#90CAF9" fill="none" stroke-width="2"/></svg>').decode('utf-8')
ICON_CITY = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="6" y="6" width="20" height="20" fill="#B0BEC5" stroke="#546E7A" stroke-width="1"/></svg>').decode('utf-8')
ICON_STARPORT = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><polygon points="16,2 19,12 30,12 21,19 24,30 16,23 8,30 11,19 2,12 13,12" fill="#FFFFFF" stroke="#000" stroke-width="0.5"/></svg>').decode('utf-8')

class Hex:
    def __init__(self, x, y, triangle_id=None, parent_hex=None):
        self.x = x
        self.y = y
        self.triangle_id = triangle_id
        self.parent_hex = parent_hex
        self.terrain = set()
        self.is_land = False
        self.sub_map = None 

    def add(self, terrain_type):
        self.terrain.add(terrain_type)
        if terrain_type in ['Ocean', 'Ocean Depth', 'Abyss']:
            self.is_land = False
        else:
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
    def __init__(self, uwp, trade_codes=None, seed=None):
        self.uwp = uwp
        self.size = self.parse_hex(uwp[1])
        self.hydro = self.parse_hex(uwp[3])
        self.atmos = self.parse_hex(uwp[2])
        self.pop = self.parse_hex(uwp[4])
        
        self.trade_codes = trade_codes if trade_codes else []
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
        for t in self.triangles:
            h = self.rng.choice(list(t.hexes.values()))
            h.add('Resource')

        for t in self.triangles:
            num_mtns = self.rng.randint(1, 6)
            candidates = list(t.hexes.values())
            self.rng.shuffle(candidates)
            for i in range(min(num_mtns, len(candidates))):
                candidates[i].add('Mountain')

        num_ocean_triangles = min(20, self.hydro * 2)
        ocean_triangle_ids = self.rng.sample(range(20), num_ocean_triangles)
        land_triangle_ids = [i for i in range(20) if i not in ocean_triangle_ids]

        for tid in ocean_triangle_ids:
            t = self.triangles[tid]
            for h in t.hexes.values():
                h.add('Ocean')
                h.is_land = False
        
        num_seas = min(len(land_triangle_ids), self.hydro)
        sea_triangles = self.rng.sample(land_triangle_ids, num_seas)
        for tid in sea_triangles:
            t = self.triangles[tid]
            h = self.rng.choice(list(t.hexes.values()))
            h.add('Ocean')
            h.is_land = False

        for tid in ocean_triangle_ids:
            t = self.triangles[tid]
            for h in t.hexes.values():
                if h.has('Mountain'):
                    h.terrain.discard('Mountain')
                    h.add('Islands')
                    h.is_land = True

        for t in self.triangles:
            for h in t.hexes.values():
                if h.is_land:
                    neighbors = self.get_neighbors(h)
                    for n in neighbors:
                        if n.has('Ocean'):
                            h.add('Shore')
                            break

        for tid in list(range(0, 5)) + list(range(15, 20)):
            t = self.triangles[tid]
            for h in t.hexes.values():
                if h.has('Ocean'): h.add('Ice Field')
                else: h.add('IceCap')

        placed_cities = 0
        if self.pop > 0:
            self.rng.shuffle(land_triangle_ids)
            for tid in land_triangle_ids:
                if placed_cities >= self.pop: break
                t = self.triangles[tid]
                candidates = [h for h in t.hexes.values() if h.is_land]
                if candidates:
                    self.rng.choice(candidates).add('City')
                    placed_cities += 1

        cities = [h for h in self.get_hexes() if h.has('City')]
        if cities:
            self.rng.choice(cities).add('Starport')
        elif self.pop > 0:
            land = [h for h in self.get_hexes() if h.is_land]
            if land: self.rng.choice(land).add('Starport')

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