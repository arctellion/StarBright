import numpy as np
import pandas as pd
import travtools.travtools as tt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

omega = tt.fun_stars(500, 1, [10,10,10])
omega = pd.DataFrame(omega, columns=["x","y","z"])
omega = omega.rename_axis('id').reset_index()
omega['uwp'] = omega['id'].apply(tt.fun_uwp)
print(omega.head())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(omega['x'], omega['y'], omega['z'])
plt.show()

# sample run for uwp distribution
sim = pd.DataFrame(np.arange(1,1000000,1), columns=['id'])
sim['uwp'] = sim['id'].apply(tt.fun_uwp)
print(sim.tail())
prt = sim['uwp'].str.slice(0,1).value_counts().sort_index()
sze = sim['uwp'].str.slice(1,2).value_counts().sort_index()
atm = sim['uwp'].str.slice(2,3).value_counts().sort_index()
hyd = sim['uwp'].str.slice(3,4).value_counts().sort_index()
pop = sim['uwp'].str.slice(4,5).value_counts().sort_index()
gov = sim['uwp'].str.slice(5,6).value_counts().sort_index()
law = sim['uwp'].str.slice(6,7).value_counts().sort_index()
tech = sim['uwp'].str.slice(8,9).value_counts().sort_index()
print(prt, sze, atm, hyd, pop, gov, law, tech)