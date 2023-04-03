import numpy as np
import time
#import pandas as pd
#import travtools.stars as st
import travtools.system as sy
import travtools.qrebs as qr
import travtools.commerce as cm
import travtools.gunmaker as gm
#import plotly.express as px
#import plotly
#import re

##qrebs generation
# i=1
# while i <= 100:
#     qrb = qr.qrebs(i)
#     print(qrb)
#     i = i + 1
# print("\n====\n")

#Starbright Crew:
# Steward - Prof Afan - 1; 
# Admin - ?? - 2; Sir Otto - 1; Prof Afan - 1;
# Streetwise - Sir Otto - 1
# Liaison - Sir Otto - 2; Aruk - 1;  ?? - 1;

g=cm.trade_gds("A110877-E",{'Steward':1, 'Admin':2, 'Streetwise':1, 'Liaison':2}, 2)
print(g)

g = cm.sell_price("B - Ri Cr5,100","B787AA9-E",8,4)
print("Sell Price:  Cr{:,}".format(g))

#gm.gunmaker()
## system generation test for a million systems
#idx=range(1,1000000)
#cols=['uwp']
#omega = pd.DataFrame(index=idx, columns=cols)
#omega = omega.rename_axis('id').reset_index()
#omega['uwp'] = np.vectorize(sy.fun_uwp)(omega['id'])
#omega.to_csv('stars.csv')

#collab subsector Planet: A573331-C 813 Lo  {+1}(B21+2)[445A]
