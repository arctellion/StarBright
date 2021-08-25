import numpy as np
#import pandas as pd
#import travtools.stars as st
#import travtools.system as sy
import travtools.qrebs as qr
import travtools.commerce as cm
#import plotly.express as px
#import plotly
#import re

##qrebs generation
i=1
while i <= 10:
    qrb = qr.qrebs(i)
    print(qrb)
    i = i + 1
print("\n====\n")

#Starbrigh Crew:
# Steward - Prof Afan - 1; 
# Admin - ?? - 2; Sir Otto - 1; Prof Afan - 1;
# Streetwise - Sir Otto - 1
# Liaison - Sir Otto - 2; Aruk - 1;  ?? - 1;

g=cm.trade_gds("A2009AB-E",{'Steward':1, 'Admin':2, 'Streetwise':1, 'Liaison':2}, 7)
print(g)
## system generation test for a million systems
#idx=range(1,1000000)
#cols=['uwp']
#omega = pd.DataFrame(index=idx, columns=cols)
#omega = omega.rename_axis('id').reset_index()
#omega['uwp'] = np.vectorize(sy.fun_uwp)(omega['id'])
#omega.to_csv('stars.csv')
