"""
Created on Thu May 18 09:31:15 2017

@author: jaeyoon
"""

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
verts= [(0.,0.),(0.,1.),(1.,1.),(1.,0.),(0.,0.),]


codef= [Path.MOVETO, Path.LINETO, Path.LINETO,Path.LINETO,Path.CLOSEPOLY,]
path = Path(verts,codef)


fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor = (0.5,0.88,0.1), lw = 2)
ax.add_patch(patch)
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
plt.show()





verts1= [(0.,0.),(0.,1.),(1.,1.),(1.,0.),]
np.shape(verts1)

import matplotlib.patches as Polygon
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111)
patch = Polygon.Polygon(verts,facecolor = 'orange', lw = 2)
ax.add_patch(patch)
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
plt.show()

import shapefile
import fiona
shp = fiona.open(r'C:\Users\jaeyoon\GoogleDrive\BusinessAnalysis\chapter12\Chicago_Boundaries_Community_Areas_current.shx',  encoding = '949')
sf = shapefile.Reader(r'C:\Users\jaeyoon\GoogleDrive\BusinessAnalysis\chapter12\2016_us_election\county_shapefiles\cb_2014_us_county_500k.shx')
shp[0]
shp[0].keys()

coord = shp[1]['geometry']
info = shp[1]['properties']



shapes[3].points


  
verts = coord['coordinates'][0]
fig = plt.figure()
ax = fig.add_subplot(111)
patch = Polygon.Polygon(verts,facecolor = 'r', lw = 2)
ax.add_patch(patch)
plt.autoscale()
plt.show()



fig = plt.figure()
ax = plt.gca()
cooef2 = shp[0]['geometry']['coordinates']
for x in cooef2:
    poly = Polygon.Polygon(x[0], ec= 'k')
    ax.add_patch(poly)
plt.autoscale()
plt.show()



#전체 그림 완빵에 끝내기

fig = plt.figure()
fig.set_size_inches((10,10))
ax = plt.gca()
for x in range(len(shp)):
    coord = shp[x]['geometry'] 
    info = shp[x]['properties']
    if coord['type'] == 'Polygon':       
        verts = coord['coordinates'][0]
        patch = Polygon.Polygon(verts,facecolor = 'r', ec ='k')
        ax.add_patch(patch)
    elif coord['type'] == 'MultiPolygon':
        cooef2 = shp[0]['geometry']['coordinates']
        for x in cooef2:
            poly = Polygon.Polygon(x[0], ec= 'k', facecolor = 'r')
            ax.add_patch(poly)
plt.autoscale()
plt.axis('off')
plt.show()      



from matplotlib import cm
seoul = [x for x in shp if x['properties']['SIG_CD'][:2] == '11']
import pandas as pd

pop = pd.read_csv(r'C:\Users\jaeyoon\GoogleDrive\BusinessAnalysis\chapter12\OctagonExcel.csv',encoding = 'utf-8')

#자치구 - 인구 매칭
pop2 = pop.set_index('자치구')
gu_names = [x['properties']['SIG_KOR_NM'] for x  in seoul]
pop2 = pop2.loc[gu_names]
c = cm.Blues(pop2['인구']/pop2['인구'].max())


#서울 구별 인구수 비례 색깔 입히는 사전 만들기
seoul[0]['properties']['SIG_KOR_NM']
[ seoul[x]['geometry']['type'] for x  in range(len(seoul))]
colors = cm.Blues(pop['인구']/pop['인구'].max())
seoulcolor = {}
i = 0 
for x in pop['자치구']:
    seoulcolor[x] = colors[i]
    i +=1
  

from matplotlib.collections import PathCollection
import numpy as np
    
    
cols = []
#서울 구별 인구수 반영 그림 그리기
fig = plt.figure()
ax = plt.gca()
for x in range(len(seoul)):
    coord = seoul[x]['geometry']
    verts = coord['coordinates'][0]
    patch = Polygon.Polygon(verts, facecolor = seoulcolor[seoul[x]['properties']['SIG_KOR_NM']] , ec = 'k')
    cols.append(patch)
    ax.add_patch(patch)
plt.autoscale()
plt.axis('off')
p =PathCollection(cols, cmap = cm.Blues )
p.set_array(np.array(colors))
ax.add_collection(p)
ax.autoscale_view()
plt.colorbar(p)
plt.show()


#Draw Heat Map

dx, dy = 0.15, 0.05

y, x = np.mgrid[slice(-3,3+dy,dy),slice(-3,3+dx,dx)]
z = (1-x/2. +x**5 + y**3) * np.exp(-x**2 - y**2)
z = z[:-1,:-1]
z_min, z_max = -np.abs(z).max(), np.abs(z).max()

plt.pcolor(x,y,z, cmap = 'RdBu', vmin = z_min, vmax = z_max)
plt.title('pcolor')
plt.axis([x.min(), x.max(), y.min(), y.max()])
plt.colorbar()
plt.show()

data = np.random.rand(100,2)
temp = np.histogram2d(data[:,0], data[:,1])

X,Y = np.meshgrid(temp[1], temp[2])
Z = temp[0]
plt.pcolor(X,Y,Z, cmap = 'terrain')
