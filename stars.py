import numpy as np
import pandas as pd
import travtools as tt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

p  = tt.stars.Points(n=5000,r=25, center=(0,0,0), mindist=1)
#print(p.points)
#print(p)

df = pd.DataFrame(p.points, columns=["x","y","z"])
print(df.head())

fig = px.scatter_3d(df, x='x', y='y', z='z')
fig.update_traces(marker=dict(size=2),
                  selector=dict(mode='markers'))
fig.show()
