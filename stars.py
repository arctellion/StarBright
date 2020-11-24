import numpy as np
import pandas as pd
import travtools.stars as st
import travtools.system as sy
import plotly.express as px

p  = st.Points(n=5000,r=25, center=(0,0,0), mindist=1)
#print(p.points)
#print(p)

omega = pd.DataFrame(p.points, columns=["x","y","z"])
omega = omega.rename_axis('id').reset_index()
print(omega.head())


omega['uwp'] = omega['id'].apply(st.fun_uwp)
omega['pbg'] = omega['uwp'].apply(st.fun_pbg)

print(omega.head())

#fig = px.scatter_3d(df, x='x', y='y', z='z')
#fig.update_traces(marker=dict(size=2),
#                  selector=dict(mode='markers'))
#fig.show()
