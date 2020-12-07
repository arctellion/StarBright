import numpy as np
import pandas as pd
import travtools.stars as st
import travtools.system as sy
import plotly.express as px
import plotly
import re

p  = st.Points(n=5000,r=25, center=(0,0,0), mindist=1)
p2d = st.Points2D(n=2000, r=100, center=(0,0), mindist=1)
#3d world view
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
#2d world view
omega2d = pd.DataFrame(p2d.points, columns=["x","y"])
omega2d = omega2d.rename_axis('id').reset_index
omega2d['uwp'] = omega2d['id'].apply(sy.fun_uwp)
omega2d['pbg'] = omega2d['uwp'].apply(sy.fun_pbg)
omega2d['base'] = omega2d['uwp'].apply(sy.fun_bases)
omega2d['ixexcx'] = np.vectorize(sy.fun_ext)(omega2d['uwp'],omwga2d['pbg'],omeag2d['base'])
print(omega2d.head())
#
def split_ix(d):
  return(int(re.search("[+-]?\d",d)[0]))

omega['ix'] = np.vectorize(split_ix)(omega['IxExCx'])
omega2d['ix'] = np.vectorize(split_ix)(omega2d['ixexcx'])
print(omega.head())
print(omega2d.head())

fig = px.scatter_3d(omega, x='x', y='y', z='z', color = 'ix')  
fig.update_traces(marker=dict(size=2),
                  selector=dict(mode='markers'))
plotly.offline.plot(fig, filename = 'stars.html', auto_open=False)

fig2d = px.scatter(omega2d, x='x',y='y',color='ix')
fig2d.update_traces(marker=dict(size=2),
                    selector=dict(mode='markers'))
plotly.offline.plot(fig2d, filename='stars2d.html', auto_open=False)