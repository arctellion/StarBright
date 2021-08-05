import numpy as np
#import pandas as pd
#import travtools.stars as st
#import travtools.system as sy
import travtools.qrebs as qr
#import plotly.express as px
#import plotly
#import re

##qrebs generation
i=1
while i <= 10:
    qrb = qr.qrebs(i)
    print(qrb)
    i = i + 1

## system generation test for a million systems
#idx=range(1,1000000)
#cols=['uwp']
#omega = pd.DataFrame(index=idx, columns=cols)
#omega = omega.rename_axis('id').reset_index()
#omega['uwp'] = np.vectorize(sy.fun_uwp)(omega['id'])
#omega.to_csv('stars.csv')
