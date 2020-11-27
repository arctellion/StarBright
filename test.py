import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import plotly.express as px
import pandas as pd
import networkx as nx

class Points():
    def __init__(self,n=10, r=1, center=(0,0,0), mindist=0.2, maxtrials=10000 ) :
        self.success = False
        self.n = n
        self.r = r
        self.center=np.array(center)
        self.d = mindist
        self.points = np.ones((self.n,3))*10*r+self.center
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
        x = (np.random.rand(3)-0.5)*2
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

p  = Points(n=50,r=10, center=(0,0,0), mindist=1)
print(p.points)
#print(p)
df = pd.DataFrame(p.points, columns=["x","y","z"])
print(df.head())
# translate df into dict for network
pos = df.dict

G = nx.random_geometric_graph(50,4,pos=pos)

pos = nx.get_node_attributes(G, 'pos')
n = G.number_of_nodes()
edge_max = max([G.degree(i) for i in range(n)])
colors = [plt.cm.plasma(G.degree(i)/edge_max) for i in range(n)] 
# 3D network plot
with plt.style.context(('ggplot')):

    fig = plt.figure(figsize=(10,7))
    ax = Axes3D(fig)

    # Loop on the pos dictionary to extract the x,y,z coordinates of each node
    for key, value in pos.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]

        # Scatter plot
        ax.scatter(xi, yi, zi, c=colors[key], s=20+20*G.degree(key), edgecolors='k', alpha=0.7)

    # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
    # Those two points are the extrema of the line to be plotted
    for i,j in enumerate(G.edges()):
        x = np.array((pos[j[0]][0], pos[j[1]][0]))
        y = np.array((pos[j[0]][1], pos[j[1]][1]))
        z = np.array((pos[j[0]][2], pos[j[1]][2]))

    # Plot the connecting lines
        ax.plot(x, y, z, c='black', alpha=0.5)

# Set the initial view
ax.view_init(30, angle)
# Hide the axes
ax.set_axis_off()
plt.show()
#fig = px.scatter_3d(df, x='x', y='y', z='z')
#fig.update_traces(marker=dict(size=2),
#                  selector=dict(mode='markers'))
#fig.show()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(x, y, z)
#plt.show()
