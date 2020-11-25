import numpy as np
import pandas as pd
import travtools.stars as st
import travtools.system as sy
import plotly.express as px
import plotly

p  = st.Points(n=5000,r=25, center=(0,0,0), mindist=1)
#print(p.points)
#print(p)

omega = pd.DataFrame(p.points, columns=["x","y","z"])
omega = omega.rename_axis('id').reset_index()
print(omega.head())
omega['uwp'] = omega['id'].apply(sy.fun_uwp)
print(omega.dtypes)
omega['pbg'] = omega['uwp'].apply(sy.fun_pbg)
print(omega.head())
omega['base'] = omega['uwp'].apply(sy.fun_bases)
print(omega.head())
omega['IxExCx'] = np.vectorize(sy.fun_ext)(omega['uwp'],omega['pbg'],omega['base'])
print(omega.head())

fig = px.scatter_3d()
fig = px.scatter_3d(omega, x='x', y='y', z='z')
fig.update_traces(marker=dict(size=2),
                  selector=dict(mode='markers'))
plotly.offline.plot(fig, filename = 'stars.html', auto_open=False)