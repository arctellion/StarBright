import numpy as np
import pandas as pd
import travtools.travtools as tt

# def rand_sep(n, x0, x1, y0, y1, z0, z1, d, seed = 256, test = 1000):
#   np.random.seed(seed)
#   for i in range(1,test):
#     x = np.random.randint(x0, x1, n)
#     y = np.random.randint(y0, y1, n)
#     z = np.random.randint(z0, z1, n)
#     points = np.column_stack((x,y,z))
#     #if (min(dist(nums)) >= d || max(dist(nums)) <= 6) {
#     if (min(sc.pdist(points)) < d):
#       return(points)
#   return("FAIL") #failed

omega = tt.rand_sep(500, -5, 5, -5, 5, -5, 5, 1,500)
omega = pd.DataFrame(omega, columns=["x","y","z"])

# sample run for uwp distribution
sim = pd.DataFrame(np.arange(1,100,1), columns=['id'])
sim['uwp'] = sim['id'].apply(tt.fun_uwp)
sim.head()