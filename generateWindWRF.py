from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from numpy import meshgrid
import pandas as pd
import math

plt.figure(figsize=(48,24))

m = Basemap(projection='mill',llcrnrlat=25,urcrnrlat=33,llcrnrlon=-115,urcrnrlon=-107,resolution='l')

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
#data = data.loc[data['Long'] > -115.0]
#data = data.loc[data['Long'] < -107.0]

#data = data.loc[data['Lat'] > 25.0]
#data = data.loc[data['Lat'] < 33.0]

#%% calculate U
data['u'] = data.apply(lambda x: calculateU(x['Winds (m/s)'], x['Windd (°)']), axis=1)

#%% calculate V
data['v'] = data.apply(lambda x: calculateV(x['Winds (m/s)'], x['Windd (°)']), axis=1)

#%% get hours
hours = np.array(data['Hour'])
hours = np.unique(hours)

#%% generate one by one maps
for i in hours:
	plt.clf()
	dataTemp = data.loc[data['Hour'] == i]
	#%% read x, y, value
	lons = np.array(dataTemp['Long'])
	lats = np.array(dataTemp['Lat'])
	u = np.array(dataTemp['u'])
	v = np.array(dataTemp['v'])
	speed = np.sqrt(u*u + v*v)

	x, y = m(lons, lats)

	m.fillcontinents(color='#cc9955', lake_color='aqua', zorder = 0)
	m.drawcoastlines(color = '0.15')

	m.quiver(x, y, u, v, speed, cmap=plt.cm.autumn)

	tempFileTitle = "maps/mapFromWRF_hour_{}.png".format(i)
	plt.savefig(tempFileTitle,dpi=300)
	print("***** {}".format(tempFileTitle))

