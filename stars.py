#from utils import *
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

r = 2

# Generate 100 points (3-tuples) between 0 and 10
points = np.random.randint(0,100,[1000,3])

# Pairwise distances between points
distances = euclidean_distances(points)

# "Remove" distance to itself by setting to a distance of r+1 (to discard it later)
distances += np.identity(len(distances)) * (r+1)

# Retrieve the distance to the closest point
min_dist = np.min(distances,axis=1)

# Filter your set of points
filtered_points = points[min_dist>r]

print(filtered_points)