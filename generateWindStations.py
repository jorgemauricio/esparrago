from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from numpy import meshgrid
import pandas as pd
import math

plt.figure(figsize=(24,12))

m = Basemap(projection='mill',llcrnrlat=25,urcrnrlat=33,llcrnrlon=-115,urcrnrlon=-107,resolution='c')

#%% read txt file
data = pd.read_csv('data/db_sonora.csv')

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
data = data.loc[data['longitud'] > -115.0]
data = data.loc[data['longitud'] < -107.0]

data = data.loc[data['latitud'] > 25.0]
data = data.loc[data['latitud'] < 33.0]

#%% calculate U
data['u'] = data.apply(lambda x: calculateU(x['velv'], x['dirv']), axis=1)

#%% calculate V
data['v'] = data.apply(lambda x: calculateV(x['velv'], x['dirv']), axis=1)

#%% get fecha columns as array
dates = np.array(data['fecha'])

#%% get all the uniques values from fecha
dates = np.unique(dates)

#%% loop 
for i in dates:
	plt.clf()
	dataTemp = data.loc[data['fecha'] == i]
	#%% read x, y, value
	lons = np.array(dataTemp['longitud'])
	lats = np.array(dataTemp['latitud'])
	u = np.array(dataTemp['u'])
	v = np.array(dataTemp['v'])
	speed = np.sqrt(u*u + v*v)

	x, y = m(lons, lats)

	m.fillcontinents(color='#cc9955', lake_color='aqua', zorder = 0)
	m.drawcoastlines(color = '0.15')

	m.quiver(x, y, u, v, speed, cmap=plt.cm.autumn)

	#%% tempTitle for png file
	tempTitleForPNG = 'maps/map_stations_{}.png'.format(i)
	plt.savefig(tempTitleForPNG,dpi=300)
	print('***** {}'.format(tempTitleForPNG))