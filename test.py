import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import plotly.express as px
import pandas as pd
import networkx as nx
import scipy.spatial.distance as dis
from math import sqrt

class Points2D():
    def __init__(self,n=10, r=1, center=(0,0), mindist=0.2, maxtrials=10000 ) :
        self.success = False
        self.n = n
        self.r = r
        self.center=np.array(center)
        self.d = mindist
        self.points = np.ones((self.n,2))*10*r+self.center
        self.c = 0
        self.trials = 0
        self.maxtrials = maxtrials
        self.tx = "rad: {}, center: {}, min. dist: {} ".format(self.r, center, self.d)
        self.fill()

    def dist(self, p, x):
        if len(p.shape) >1:
            return np.sqrt(np.sum((p-x)**2, axis=1))
        else:
            return np.sqrt(np.sum((p-x)**2))

    def newpoint(self):
        x = (np.random.rand(2)-0.5)*2
        x = x*self.r-self.center
        if self.dist(self.center, x) < self.r:
            self.trials += 1
            if np.all(self.dist(self.points, x) > self.d):
                self.points[self.c,:] = x
                self.c += 1

    def fill(self):
        while self.trials < self.maxtrials and self.c < self.n:
            self.newpoint()
        self.points = self.points[self.dist(self.points,self.center) < self.r,:]
        if len(self.points) == self.n:
            self.success = True
        self.tx +="\n{} of {} found ({} trials)".format(len(self.points),self.n,self.trials)

    def __repr__(self):
        return self.tx

#center =(0,0,0)
#radius = 25
#mindist = 1
p  = Points(n=100,r=10, center=(0,0), mindist=1)
df = pd.DataFrame(p.points, columns=["x","y"])
print(df.head())
# coords = df.to_dict('index')
# print(coords)

# def dist(a,b):
#   d=[a[0]-b[0],a[1]-b[1],a[2]-b[2]]
#   return(sqrt(d[0]*d[0]+d[1]*d[1]+d[2]*d[2]))

# D={}
# for pt,pts in coords.items():
#   D[pt] = {}
#   for pt1, pts1 in coords.items():
#     D[pt][pt1] = dist(pts,pts1)
# for p1,v in D.items():
#   for p2, d in v.items():
#     print(p1, p2, d)

#print(p)
#print(df.head())
a = dis.cdist(p.points,p.points)
b = dis.pdist(p.points)
# translate df into dict for network
#pos = df.to_dict('index')
#print(pos)
print(a)

print(b)
#G = nx.from_numpy_matrix(a)
#plt.subplot(121)
#nx.draw(G)
#plt.savefig("path.png")
#G = nx.drawing.nx_agraph.to_agraph(G)

#G.node_attr.update(color="red", style="filled")
#G.edge_attr.update(color="blue", width="2.0")
#G.draw('out.png', format='png', prog='neato')

#network_plot_3D(G,0)

#fig = px.scatter_3d(df, x='x', y='y', z='z')
#fig.update_traces(marker=dict(size=2),
#                  selector=dict(mode='markers'))
#fig.show()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(x, y, z)
#plt.show()
