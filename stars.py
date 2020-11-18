from utils import *
import numpy as np
import scipy.spatial.distance as sc

# nums = np.random.randint(x0, x1, size = (n,3))
# # for nearest neighbours and min/max dist apart maybe BallTree or KDTree? or some Nearest NEighbour calculation.
# print(nums)
# dis = sc.cdist(nums,nums)
# print(dist)
def rand_sep(n, x0, x1, y0, y1, z0, z1, d, seed = 256, test = 1000):
  np.random.seed(seed)
  for i in range(1,test):
    x = np.random.randint(x0, x1, n)
    y = np.random.randint(y0, y1, n)
    z = np.random.randint(z0, z1, n)
    points = np.column_stack((x,y,z))
    #if (min(dist(nums)) >= d || max(dist(nums)) <= 6) {
    if (min(sc.pdist(points)) < d):
      return(points)
  return("FAIL") #failed

test = rand_sep(5000, 0, 100, 0, 100, 0, 100, 1)
dist = sc.pdist(test)
dmatrx =  sc.squareform(dist)
np.savetxt("test.csv", test, delimiter=",")
np.savetxt("dist.csv", dist, delimiter=",")
np.savetxt("dmatrx.csv", dmatrx, delimiter=",")
#print(test)
#print(dist)
#print(min(dist), max(dist))