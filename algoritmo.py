algoritmo.pyfrom mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from numpy import meshgrid
import pandas as pd
import math

plt.figure(figsize=(48,24))

m = Basemap(projection='mill',llcrnrlat=25,urcrnrlat=33,llcrnrlon=-115,urcrnrlon=-107,resolution='i')

#%% read txt file
data = pd.read_csv('data/2017-09-25.csv')

#%% calculate U and V vectors
def calculateU(windSpeed, windDirection):
	'''
	Generate U vector
	'''
	return windSpeed * math.cos(windDirection)

def calculateV(windSpeed, windDirection):
	'''
	Generate V vector
	'''
	return windSpeed * math.sin(windDirection)

#%% cut info
data = data.loc[data['Long'] > -115.0]
data = data.loc[data['Long'] < -107.0]

data = data.loc[data['Lat'] > 25.0]
data = data.loc[data['Lat'] < 33.0]

#%% calculate U
data['u'] = data.apply(lambda x: calculateU(x['Windpro'], x['WindDir']), axis=1)

#%% calculate V
data['v'] = data.apply(lambda x: calculateV(x['Windpro'], x['WindDir']), axis=1)

#%% read x, y, value
lons = np.array(data['Long'])
lats = np.array(data['Lat'])
u = np.array(data['u'])
v = np.array(data['v'])
speed = np.sqrt(u*u + v*v)

x, y = m(lons, lats)

xx = np.arange(0, len(x), 4)
yy = np.arange(0, len(y), 4)

uu = np.arange(0, len(u), 4)
vv = np.arange(0, len(v), 4)
#speed1 = np.arange(0, speed.shape[0], 4)

m.fillcontinents(color='#cc9955', lake_color='aqua', zorder = 0)
m.drawcoastlines(color = '0.15')

m.quiver(x, y, u, v, speed, cmap=plt.cm.autumn)

plt.savefig('test.png',dpi=300)