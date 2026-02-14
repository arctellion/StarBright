import random

class Hex:
    def __init__(self, x, y, triangle_id):
        self.x = x
        self.y = y
        self.triangle_id = triangle_id
        self.terrain = set()
        self.is_land = False

    def add(self, terrain_type):
        self.terrain.add(terrain_type)

    def has(self, terrain_type):
        return terrain_type in self.terrain

    def __repr__(self):
        return f"Hex({self.x},{self.y},T{self.triangle_id})"

class Triangle:
    def __init__(self, tid, size, up_or_down, large_or_small):
        self.id = tid
        self.size = size
        self.up_or_down = up_or_down
        self.large_or_small = large_or_small
        self.hexes = {}

class WorldMapGen:
    def __init__(self, uwp, seed=None):
        self.uwp = uwp
        self.size = self.parse_hex(uwp[1])
        self.hydro = self.parse_hex(uwp[3])
        self.atmos = self.parse_hex(uwp[2])
        
        self.seed_val = seed if seed is not None else sum(ord(c) for c in uwp)
        self.rng = random.Random(self.seed_val)
        
        self.triangles = []
        self.generate_grid()

    def parse_hex(self, char):
        if '0' <= char <= '9': return int(char)
        return ord(char.upper()) - ord('A') + 10

    def generate_grid(self):
        for tid in range(20):
            vert_pos = tid % 4
            if vert_pos == 0:
                t = Triangle(tid, self.size, 0, 0) # SMALL UP
            elif vert_pos == 1:
                t = Triangle(tid, self.size, 1, 1) # LARGE DOWN
            elif vert_pos == 2:
                t = Triangle(tid, self.size, 0, 1) # LARGE UP
            else:
                t = Triangle(tid, self.size, 1, 0) # SMALL DOWN
            
            hex_per_side = self.size if t.large_or_small == 1 else self.size - 1
            
            if hex_per_side > 0:
                if t.up_or_down == 0:
                    for y in range(hex_per_side):
                        for x in range(y + 1):
                            t.hexes[(x, y)] = Hex(x, y, tid)
                else:
                    for y in range(hex_per_side):
                        for x in range(hex_per_side - y):
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
        
        if t.up_or_down == 0:
            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]
        else:
            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
            
        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if (nx, ny) in t.hexes:
                neighbors.append(t.hexes[(nx, ny)])
        return neighbors

    def generate_terrain(self):
        for h in self.get_hexes():
            h.add('Clear')
            h.is_land = True

        # Ice Caps (Pole triangles)
        for tid in range(20):
            if tid % 4 == 0: # North
                for h in self.triangles[tid].hexes.values():
                    if self.rng.random() < 0.8: h.add('IceCap')
            if tid % 4 == 3: # South
                for h in self.triangles[tid].hexes.values():
                    if self.rng.random() < 0.8: h.add('IceCap')

        total_hexes = sum(len(t.hexes) for t in self.triangles)
        num_ocean_hexes = int(total_hexes * (self.hydro / 10.0))
        
        # Grow Oceans from random points in the belt trianlges (vert_pos 1 and 2)
        ocean_seeds = [h for tid in range(20) if tid % 4 in [1, 2] for h in self.triangles[tid].hexes.values()]
        self.grow_blobs('Ocean', num_ocean_hexes, land_only=False, seeds=ocean_seeds)

        # Mountains
        num_mountains = self.rng.randint(self.size * 2, self.size * 4 + 1)
        self.grow_blobs('Mountain', num_mountains * 4, land_only=True)

    def grow_blobs(self, terrain_type, target_count, land_only=False, seeds=None):
        all_hexes = list(self.get_hexes())
        current_count = sum(1 for h in all_hexes if h.has(terrain_type))
        if current_count >= target_count:
            return

        potential = []
        if seeds is None: seeds = all_hexes
        
        # Initial clumping
        num_seeds = max(2, target_count // 20)
        chosen_seeds = self.rng.sample(seeds, min(len(seeds), num_seeds))
        for s in chosen_seeds:
            if land_only and not s.is_land: continue
            if s.has('IceCap') and terrain_type != 'IceCap': continue
            s.add(terrain_type)
            if terrain_type == 'Ocean': s.is_land = False
            potential.extend(self.get_neighbors(s))

        while current_count < target_count and potential:
            h = self.rng.choice(potential)
            potential.remove(h)
            if h.has(terrain_type): continue
            if land_only and not h.is_land: continue
            if h.has('IceCap') and terrain_type != 'IceCap': continue
            
            h.add(terrain_type)
            if terrain_type == 'Ocean': h.is_land = False
            current_count += 1
            
            for n in self.get_neighbors(h):
                if not n.has(terrain_type):
                    potential.append(n)

    def get_map_json(self):
        output = []
        for t in self.triangles:
            tri = {
                'id': t.id, 
                'up_or_down': t.up_or_down, 
                'large_or_small': t.large_or_small,
                'hexes': []
            }
            for h in t.hexes.values():
                tri['hexes'].append({
                    'x': h.x,
                    'y': h.y,
                    'terrain': list(h.terrain)
                })
            output.append(tri)
        return output
