# Build flat-topped macro hexagons
# Since we know flat-topped (Point-At-Side) can be symmetric.
# Let's verify flat-topped with 6 vertical flat face, and 10 point-to-point.
import math

def build_shape(widths, r_offset=0):
    hexes = []
    for r, w in enumerate(widths):
        r_actual = r + r_offset
        start_q = int(math.floor(-r_actual / 2.0 - (w - 1) / 2.0 + 0.5))
        for i in range(w):
            hexes.append(((start_q + i) + r_actual/2.0, r_actual))
    return hexes

pas_widths = [6, 7, 8, 9, 10, 9, 8, 7, 6] # This is 70 hexes
pas_hexes = build_shape(pas_widths)
# Let's print the boundary of this.
print("Point-At-Side (70 hexes) layout edges:")
print("Left edge:", [min(x for x, y in pas_hexes if y == r) for r in range(9)])
print("Right edge:", [max(x for x, y in pas_hexes if y == r) for r in range(9)])

# Point-Up rotated from Point-At-Side!
# We found column heights of pas_widths:
cols = {}
for px, r in pas_hexes:
    px = round(px, 1)
    if px not in cols: cols[px] = []
    cols[px].append(r)

print("Rotated widths for Point-Up:")
col_widths = []
for k in sorted(cols.keys()):
    col_widths.append(len(cols[k]))
print(col_widths)
print("Sum:", sum(col_widths))
