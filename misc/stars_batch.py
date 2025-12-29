import numpy as np
import pandas as pd
import stars as st
import travtools.system as sy
import plotly.express as px
import plotly
import re

p  = st.Points(n=5000,r=25, center=(0,0,0), mindist=1)
p2d = st.Points2D(n=2000, r=100, center=(0,0), mindist=1)
#3d world view
omega = pd.DataFrame(p.points, columns=["x","y","z"])
omega = omega.rename_axis('id').reset_index()
omega['uwp'] = np.vectorize(sy.fun_uwp)(omega['id'])
omega['pbg'] = np.vectorize(sy.fun_pbg)(omega['uwp'])
omega['base'] = np.vectorize(sy.fun_bases)(omega['uwp'])
omega['trade'] = np.vectorize(sy.fun_trade)(omega['uwp'])
omega['IxExCx'] = np.vectorize(sy.fun_ext)(omega['uwp'],omega['pbg'],omega['base'],omega['trade'])
print(omega.head())
#2d world view
omega2d = pd.DataFrame(p2d.points, columns=["x","y"])
omega2d = omega2d.rename_axis('id').reset_index()
omega2d['uwp'] = np.vectorize(sy.fun_uwp)(omega2d['id'])
omega2d['pbg'] = np.vectorize(sy.fun_pbg)(omega2d['uwp'])
omega2d['base'] = np.vectorize(sy.fun_bases)(omega2d['uwp'])
omega2d['trade'] = np.vectorize(sy.fun_trade)(omega2d['uwp'])
omega2d['ixexcx'] = np.vectorize(sy.fun_ext)(omega2d['uwp'],omega2d['pbg'],omega2d['base'],omega2d['trade'])
print(omega2d.head())
#
def split_ix(d):
  return(int(re.search("[+-]?\d",d)[0]))

omega['ix'] = np.vectorize(split_ix)(omega['IxExCx'])
omega2d['ix'] = np.vectorize(split_ix)(omega2d['ixexcx'])
print(omega.head())
print(omega2d.head())
## output csv of star data
omega.to_csv('stars.csv')
omega2d.to_csv('stars2d.csv')
## output interactive graphs of star data
fig = px.scatter_3d(omega, x='x', y='y', z='z', color = 'ix')  
fig.update_traces(marker=dict(size=2),
                  selector=dict(mode='markers'))
plotly.offline.plot(fig, filename = 'stars.html', auto_open=False)

fig2d = px.scatter(omega2d, x='x',y='y',color='ix')
fig2d.update_traces(marker=dict(size=2),
                    selector=dict(mode='markers'))
plotly.offline.plot(fig2d, filename='stars2d.html', auto_open=False)