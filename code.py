#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  code.py
#  
#  Copyright 2026 haoyin <haoyin@YINHAO>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta
import glob
import datetime as dt
from datetime import datetime, timedelta
import scipy.stats as stats
import scipy.optimize as opt
import statsmodels.stats.stattools as st
import pingouin as pg
from scipy.stats import linregress
from datetime import datetime, timedelta
from netCDF4 import Dataset
from matplotlib import cm
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import random
from scipy.stats import norm
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error,mean_absolute_error
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def colormap_res11():
	cdict=['#3281C4','#52A7DD','#87CDF1','#B6E2ED','#DDF0F4','#FAF3D0','#F7D162','#F6A31F','#ED5D19','#E12A12']
	return matplotlib.colors.ListedColormap(cdict,'indexed')

def colormap_res111():
	cdict=['#52A7DD','#87CDF1','#B6E2ED','#DDF0F4','#FAF3D0','#F7D162','#F6A31F','#ED5D19']
	return matplotlib.colors.ListedColormap(cdict,'indexed')
		
def colormap_res1():
	cdict=['#1950A2','#3281C4','#52A7DD','#87CDF1','#B6E2ED','#DDF0F4','#FAF3D0','#F7D162','#F6A31F','#ED5D19','#E12A12','#C01922']
	return matplotlib.colors.ListedColormap(cdict,'indexed')

def colormap1():
	cdict=['#11346E','#1B5AA9','#4298D3','#72BEEA','#ABDCEB','#DCF0F4',
	'#F9F1BE','#F7C24B','#F0851B','#E83C17','#C41B1F','#9B1E23']
	return matplotlib.colors.ListedColormap(cdict,'indexed')
	
def phenology():
	data=pd.read_csv(r'./data/phenology.csv')
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')

	lon=np.array(data['lon'])
	lat=np.array(data['lat'])    
	Date_Mid_Greenup_Phase_1=np.array(data['Date_Mid_Greenup_Phase_1'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1,s=5,vmin=60,vmax=160,cmap=colormap_res11(),transform=ccrs.PlateCarree())	
	ax.set_extent([-180, 180,18, 90], crs=ccrs.PlateCarree())

	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(60,170,10))
	cb.ax.tick_params(labelsize=12)
	cb.set_label('SOS (Day of year)',fontdict={'family':'arial','weight':'normal','size':16,})
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])  
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True 
	plt.savefig('./figure/sos.pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
					  linewidth=1, color='gray', alpha=0.5, linestyle='--')
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30)) 
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True

	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')

	lon=np.array(data['lon'])
	lat=np.array(data['lat'])    
	Date_Mid_Greenup_Phase_1=np.array(data['Date_Mid_Senescence_Phase_1'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1,s=5,vmin=220,vmax=320,cmap=colormap_res11(),transform=ccrs.PlateCarree())	
	ax.set_extent([-180, 180,18, 90], crs=ccrs.PlateCarree())

	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(220,330,10))
	cb.ax.tick_params(labelsize=12)
	cb.set_label('EOS (Day of year)',fontdict={'family':'arial','weight':'normal','size':16,})
	plt.savefig('./figure/eos.pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
	
	fig = plt.figure()
	lon=np.array(data['lon'])
	lat=np.array(data['lat'])    
	Date_Mid_Greenup_Phase_1=np.array(data['EVI2_Onset_Greenness_Maximum_1'])
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
					  linewidth=1, color='gray', alpha=0.5, linestyle='--')
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30)) 
	gl.ylocator = mticker.FixedLocator([20,50,80])   
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True

	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1=np.array(data['EVI2_Onset_Greenness_Maximum_1'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1,s=5,vmin=0,vmax=0.8,cmap=colormap_res11(),transform=ccrs.PlateCarree())	
	ax.set_extent([-180, 180,18, 90], crs=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks([0,0.2,0.4,0.6,0.8])
	cb.ax.tick_params(labelsize=16)
	cb.set_label('EVI$_{max}$',fontdict={'family':'arial','weight':'normal','size':16,})
	plt.savefig('./figure/evimax.pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)
	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	
	gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
					  linewidth=1, color='gray', alpha=0.5, linestyle='--')
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30)) 
	gl.ylocator = mticker.FixedLocator([20,50,80]) 
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True 

	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	lon=np.array(data['lon'])
	lat=np.array(data['lat'])    
	Date_Mid_Greenup_Phase_1=np.array(data['EVI2_Growing_Season_Area_1'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1,s=5,vmin=0,vmax=80,cmap=colormap_res11(),transform=ccrs.PlateCarree())		
	ax.set_extent([-180, 180,18, 90], crs=ccrs.PlateCarree())

	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(0,88,8))
	cb.ax.tick_params(labelsize=12)
	cb.set_label('EVI$_{area}$',fontdict={'family':'arial','weight':'normal','size':16,})
	plt.savefig('./figure/eviarea.pdf', dpi=300, bbox_inches='tight', pad_inches=0.1)

def latitude_plot():
	data=pd.read_csv('./data/latitude_sos.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('SOS', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([80,130,180])
	ax.set_xticklabels([80,130,180],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/sos_latitude.pdf', dpi=300, bbox_inches='tight')

	data=pd.read_csv('./data/latitude_eos.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)

	ax.set_xlabel('EOS', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([220,290,360])
	ax.set_xticklabels([220,290,360],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/eos_latitude.pdf', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_evimax.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('EVI$_{max}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(25,65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([0.1,0.4,0.7])
	ax.set_xticklabels([0.1,0.4,0.7],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/evimax_latitude.pdf', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_eviarea.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('EVI$_{area}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([10,40,70])
	ax.set_xticklabels([10,40,70],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/eviarea_latitude.pdf', dpi=300, bbox_inches='tight')
			
def latitude_plot_aot40():
	data=pd.read_csv('./data/latitude_aot40_spring.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('SOS', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([80,130,180])
	ax.set_xticklabels([80,130,180],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_aot40_spring.png', dpi=300, bbox_inches='tight')

	data=pd.read_csv('./data/latitude_aot40_autumn.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)

	ax.set_xlabel('EOS', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([220,290,360])
	ax.set_xticklabels([220,290,360],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_aot40_autumn.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_aot40_summer.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('EVI$_{max}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(25,65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([0.1,0.4,0.7])
	ax.set_xticklabels([0.1,0.4,0.7],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_aot40_summer.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_aot40_all.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('EVI$_{area}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([10,40,70])
	ax.set_xticklabels([10,40,70],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_aot40_all.png', dpi=300, bbox_inches='tight')

def latitude_plot_ozone():
	data=pd.read_csv('./data/latitude_o3_spring.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('Ozone$_{spring}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([80,130,180])
	ax.set_xticklabels([80,130,180],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_o3_spring.png', dpi=300, bbox_inches='tight')

	data=pd.read_csv('./data/latitude_o3_autumn.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)

	ax.set_xlabel('Ozone$_{autumn}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([220,290,360])
	ax.set_xticklabels([220,290,360],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_o3_autumn.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_o3_summer.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('Ozone$_{summer}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(25,65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([0.1,0.4,0.7])
	ax.set_xticklabels([0.1,0.4,0.7],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_o3_summer.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_o3_all.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('Ozone$_{all}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([10,40,70])
	ax.set_xticklabels([10,40,70],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_o3_all.png', dpi=300, bbox_inches='tight')

def latitude_plot_temp():
	data=pd.read_csv('./data/latitude_temp_spring.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('T$_{spring}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([80,130,180])
	ax.set_xticklabels([80,130,180],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_temp_spring.png', dpi=300, bbox_inches='tight')

	data=pd.read_csv('./data/latitude_temp_autumn.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)

	ax.set_xlabel('T$_{autumn}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([220,290,360])
	ax.set_xticklabels([220,290,360],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_temp_autumn.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_temp_summer.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('T$_{summer}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(25,65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([0.1,0.4,0.7])
	ax.set_xticklabels([0.1,0.4,0.7],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_temp_summer.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_temp_all.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('T$_{all}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([10,40,70])
	ax.set_xticklabels([10,40,70],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_temp_all.png', dpi=300, bbox_inches='tight')
	
def latitude_plot_co2():
	data=pd.read_csv('./data/latitude_co2_summer.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('CO$_{2-summer}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_xlim(25,65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([0.1,0.4,0.7])
	ax.set_xticklabels([0.1,0.4,0.7],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_co2_summer.png', dpi=300, bbox_inches='tight')
	
	data=pd.read_csv('./data/latitude_co2_all.csv',index=False)
	bin_centers=np.array(data['bin'])
	mean_values=np.array(data['mean'])
	std_values=np.array(data['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('CO$_{2-all}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 65)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([10,40,70])
	ax.set_xticklabels([10,40,70],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55,65])
	ax.set_yticklabels([25,35,45,55,65], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/latitude_co2_all.png', dpi=300, bbox_inches='tight')
	
def partial_year_plot_aot40():	
	area=['CN','US','EU']
	gas=['O3','AOT40']
	gas1=['O$_{3}$','AOT40']
	cat=['all_EVI2_Growing_Season_Area_1','autumn_Date_Mid_Senescence_Phase_1','spring_Date_Mid_Greenup_Phase_1','summer_EVI2_Onset_Greenness_Maximum_1']
	letters=['(a)','(b)','(c)','(d)']	
	data=pd.read_csv(r"./data/corr_aot40.csv")	
	cn_r=np.array(data['CN_r'])
	eu_r=np.array(data['EU_r'])
	us_r=np.array(data['US_r'])
	cn_std=np.array(data['CN_std'])
	eu_std=np.array(data['EU_std'])
	us_std=np.array(data['US_std'])
	fig=plt.figure(figsize=(10, 5))
	ax=fig.add_subplot(1,1,1)			
	ax.bar(np.arange(0,len(cn_r),1)-0.15,us_r,yerr=np.abs(us_std),width = 0.15,color='#E63946',label='U.S.',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1),eu_r,yerr=np.abs(eu_std),width = 0.15,color='#AAE5F4',label='Europe',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1)+0.15,cn_r,yerr=np.abs(cn_std),width = 0.15,color='orange',label='China',error_kw=dict(capsize=3))

	ax.axhline(y=0, color='black', linewidth=1)
	ax.set_xticks(np.arange(0,len(cn_r),1))
	ax.set_xticklabels(['SOS','EOS','EVI$_{max}$','EVI$_{area}$'],fontdict={'family':'arial','weight':'normal','size':16,})
	ax.set_yticks([-0.5,-0.25,0,0.25,0.5])
	ax.set_yticklabels([-0.5,-0.25,0,0.25,0.5], fontdict={'family':'arial','weight':'normal','size':16,})
	ax.set_ylabel('${_R}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.legend(prop={'family':'arial','weight':'normal','size':16,},loc='upper right',ncol=1,frameon=False)
	plt.savefig('./figure/aot40_partial.pdf', dpi=300, bbox_inches='tight')

def partial_year_plot_o3():			
	data=pd.read_csv(r"./data/corr_o3.csv")
	cn_r=np.array(data['CN_r'])
	eu_r=np.array(data['EU_r'])
	us_r=np.array(data['US_r'])
	cn_std=np.array(data['CN_std'])
	us_std=np.array(data['US_std'])
	eu_std=np.array(data['EU_std'])
	fig=plt.figure(figsize=(15, 10))
	ax=fig.add_subplot(1,1,1)			
	ax.bar(np.arange(0,len(cn_r),1)-0.15,us_r,yerr=np.abs(us_std),width = 0.15,color='#E63946',label='U.S.',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1),eu_r,yerr=np.abs(eu_std),width = 0.15,color='#AAE5F4',label='Europe',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1)+0.15,cn_r,yerr=np.abs(cn_std),width = 0.15,color='orange',label='China',error_kw=dict(capsize=3))
	
	ax.axhline(y=0, color='black', linewidth=1)
	ax.set_xticks(np.arange(0,len(cn_r),1))
	ax.set_xticklabels(['SOS','EOS','EVI$_{max}$','EVI$_{area}$'],fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(-0.5,0.75,0.25))
	ax.set_yticklabels([-0.5,-0.25,0,0.25,0.5], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylabel('${_R}$', fontdict={'family':'arial','weight':'normal','size':50,})
	ax.legend(prop={'family':'arial','weight':'normal','size':26,},loc='upper left',ncol=3)
	plt.savefig('./figure/o3_partial.png', dpi=300, bbox_inches='tight')
	
def partial_year_plot_temp():		
	data=pd.read_csv(r"./data/corr_temp.csv")			
	cn_r=np.array(data['CN_r'])
	eu_r=np.array(data['EU_r'])
	us_r=np.array(data['US_r'])
	cn_std=np.array(data['CN_std'])
	us_std=np.array(data['US_std'])
	eu_std=np.array(data['EU_std'])
	fig=plt.figure(figsize=(15, 10))
	ax=fig.add_subplot(1,1,1)			
	ax.bar(np.arange(0,len(cn_r),1)-0.15,us_r,yerr=np.abs(us_std),width = 0.15,color='#E63946',label='U.S.',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1),eu_r,yerr=np.abs(eu_std),width = 0.15,color='#AAE5F4',label='Europe',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1)+0.15,cn_r,yerr=np.abs(cn_std),width = 0.15,color='orange',label='China',error_kw=dict(capsize=3))
	ax.axhline(y=0, color='black', linewidth=1)
	ax.set_xticks(np.arange(0,len(cn_r),1))
	ax.set_xticklabels(['SOS','EOS','EVI$_{max}$','EVI$_{area}$'],fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks([-1,-0.5,0,0.5,1])
	ax.set_yticklabels([-1,-0.5,0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylabel('${_R}$', fontdict={'family':'arial','weight':'normal','size':50,})
	ax.legend(prop={'family':'arial','weight':'normal','size':26,},loc='upper left',ncol=3)
	plt.savefig('./figure/temp_partial.png', dpi=300, bbox_inches='tight')
	
def partial_year_plot_co2():	
	data=pd.read_csv(r"./data/corr_co2.csv")			
	cn_r=np.array(data['CN_r'])
	eu_r=np.array(data['EU_r'])
	us_r=np.array(data['US_r'])
	cn_std=np.array(data['CN_std'])
	us_std=np.array(data['US_std'])
	eu_std=np.array(data['EU_std'])
	fig=plt.figure(figsize=(15, 10))
	ax=fig.add_subplot(1,1,1)			
	ax.bar(np.arange(0,len(cn_r),1)-0.15,us_r,yerr=np.abs(us_std),width = 0.15,color='#E63946',label='U.S.',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1),eu_r,yerr=np.abs(eu_std),width = 0.15,color='#AAE5F4',label='Europe',error_kw=dict(capsize=3))
	ax.bar(np.arange(0,len(cn_r),1)+0.15,cn_r,yerr=np.abs(cn_std),width = 0.15,color='orange',label='China',error_kw=dict(capsize=3))	
	ax.axhline(y=0, color='black', linewidth=1)
	ax.set_xticks(np.arange(0,len(cn_r),1))
	ax.set_xticklabels(['EVI$_{max}$','EVI$_{area}$'],fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks([0,0.25,0.5,0.75,1])
	ax.set_yticklabels([0,0.25,0.5,0.75,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylabel('${_R}$', fontdict={'family':'arial','weight':'normal','size':50,})
	ax.legend(prop={'family':'arial','weight':'normal','size':26,},loc='upper left',ncol=3)
	plt.savefig('./figure/co2_partial.png', dpi=300, bbox_inches='tight')
	
def temporal_all_map_aot40():
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	data111=pd.read_csv(r"./data/temporal.csv")
	lat=np.array(data111['lat'])
	lon=np.array(data111['lon'])	
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_spring'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{AOT40-SOS}$',fontdict={'family':'arial','weight':'normal','size':16,})

	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/aot40_temporal_sos.pdf', dpi=300, bbox_inches='tight')

	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	crs=ccrs.PlateCarree()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_autumn'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{AOT40-EOS}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/aot40_temporal_eos.pdf', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_summer'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{AOT40-EVI_{max}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/aot40_temporal_evimax.pdf', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_all'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{AOT40-EVI_{area}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))  # 经度每30度一个标签
	gl.ylocator = mticker.FixedLocator([20,50,80])     # 纬度每10度一个标签
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True  # 不显示顶部标签
	gl.right_labels = True  # 不显示右侧标签
	plt.savefig('./figure/aot40_temporal_eviarea.pdf', dpi=300, bbox_inches='tight')

def temporal_all_map_o3():
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	data111=pd.read_csv(r"./data/ozone_temporal.csv")
	lat=np.array(data111['lat'])
	lon=np.array(data111['lon'])	
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_spring'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{Ozone-SOS}$',fontdict={'family':'arial','weight':'normal','size':16,})

	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))  # 经度每30度一个标签
	#gl.ylocator = mticker.FixedLocator(np.arange(0, 91, 10))     # 纬度每10度一个标签
	gl.ylocator = mticker.FixedLocator([20,50,80])     # 纬度每10度一个标签
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True  # 不显示顶部标签
	gl.right_labels = True  # 不显示右侧标签
	plt.savefig('./figure/ozone_temporal_sos.png', dpi=300, bbox_inches='tight')

	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	crs=ccrs.PlateCarree()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_autumn'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{Ozone-EOS}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/ozone_temporal_eos.png', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_summer'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{Ozone-EVI_{max}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/ozone_temporal_evimax.png', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_all'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{AOT40-EVI_{area}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/ozone_temporal_eviarea.png', dpi=300, bbox_inches='tight')
	
def temporal_all_map_temp():
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	data111=pd.read_csv(r"./data/temp_temporal.csv")
	lat=np.array(data111['lat'])
	lon=np.array(data111['lon'])	
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_spring'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{T-SOS}$',fontdict={'family':'arial','weight':'normal','size':16,})

	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/temp_temporal_sos.png', dpi=300, bbox_inches='tight')

	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	crs=ccrs.PlateCarree()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_autumn'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{T-EOS}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/temp_temporal_eos.png', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_summer'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{T-EVI_{max}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/temp_temporal_evimax.png', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_all'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{T-EVI_{area}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/temp_temporal_eviarea.png', dpi=300, bbox_inches='tight')
	
def temporal_all_map_co2():	
	data111=pd.read_csv(r"./data/co2_temporal.csv")
	lat=np.array(data111['lat'])
	lon=np.array(data111['lon'])
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_summer'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{CO_{2}-EVI_{max}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/co2_temporal_evimax.png', dpi=300, bbox_inches='tight')
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	crs=ccrs.PlateCarree()
	filepath='./worldmap/worldmap.shp'
	reader=shpreader.Reader(filepath)
	geoms=reader.geometries()
	ax.add_geometries(geoms,crs,lw=0.5,fc='none')		
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	Date_Mid_Greenup_Phase_1_r=np.array(data111['r_all'])
	cs=ax.scatter(lon,lat,c=Date_Mid_Greenup_Phase_1_r,s=6,vmin=-1,vmax=1,cmap=colormap_res11(),transform=ccrs.PlateCarree())
	
	fig.subplots_adjust()
	l=0.19
	b=0.035
	w=0.655
	h=0.0155
	rect=[l,b,w,h]
	cbar_ax=fig.add_axes(rect)
	cb=fig.colorbar(cs,cax=cbar_ax,extend='both',orientation='horizontal')
	cb.set_ticks(np.arange(-1,1.5,0.5))
	cb.ax.tick_params(labelsize=16)
	cb.set_label('R$_{CO_{2}-EVI_{area}}$',fontdict={'family':'arial','weight':'normal','size':16,})
	
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/co2_temporal_eviarea.png', dpi=300, bbox_inches='tight')
		
def latitude_temporal_plot():
	data11=pd.read_csv(r"./data/latitude_r_spring.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{AOT40-SOS}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/aot40_temporal_latitude_sos.pdf', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_autumn.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{AOT40-EOS}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/aot40_temporal_latitude_eos.pdf', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_summer.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{AOT40-EVI_{max}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/aot40_temporal_latitude_evimax.pdf', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_all.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{AOT40-EVI_{area}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/aot40_temporal_latitude_eviarea.pdf', dpi=300, bbox_inches='tight')

def latitude_temporal_plot_o3():
	data11=pd.read_csv(r"./data/latitude_r_ozone_spring.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{Ozone-SOS}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/o3_temporal_latitude_spring.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_ozone_autumn.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{Ozone-EOS}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/o3_temporal_latitude_autumn.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_ozone_summer.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{Ozone-EVI_{max}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/o3_temporal_latitude_summer.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_ozone_all.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{Ozone-EVI_{area}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/o3_temporal_latitude_all.png', dpi=300, bbox_inches='tight')

def latitude_temporal_plot_temp():
	data11=pd.read_csv(r"./data/latitude_r_temp_spring.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{T-SOS}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/temp_temporal_latitude_spring.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_temp_autumn.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{T-EOS}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/temp_temporal_latitude_autumn.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_temp_summer.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{T-EVI_{max}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/temp_temporal_latitude_summer.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/latitude_r_temp_all.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{T-EVI_{area}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/temp_temporal_latitude_all.png', dpi=300, bbox_inches='tight')
	
def latitude_temporal_plot_co2():
	data11=pd.read_csv(r"./data/latitude_r_co2_summer.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{CO_{2}-EVI_{max}}$', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/co2_temporal_latitude_summer.png', dpi=300, bbox_inches='tight')

	data11=pd.read_csv(r"./data/latitude_r_co2_all.csv")
	bin_centers=np.array(data11['bin'])
	mean_values=np.array(data11['mean'])
	std_values=np.array(data11['std'])
	fig = plt.figure(figsize=(3, 8))
	ax=fig.add_subplot(1,1,1)
	ax.plot(mean_values, bin_centers, 'b-', linewidth=2)
	ax.fill_betweenx(bin_centers, 
					 mean_values - std_values, 
					 mean_values + std_values, 
					 color='b', alpha=0.2)
	ax.set_xlabel('R$_{CO_{2}-EVI_{area}}$', fontdict={'family':'arial','weight':'normal','size':23,})
	ax.set_ylabel('Latitude', fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_ylim(25, 55)
	ax.set_xlim(np.nanmin(mean_values - std_values) * 0.9, 
			np.nanmax(mean_values + std_values) * 1.1)
	ax.set_xticks([-1,0,1])
	ax.set_xticklabels([-1,0,1],fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks([25,35,45,55])
	ax.set_yticklabels([25,35,45,55], fontdict={'family':'arial','weight':'normal','size':26,})
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.savefig('./figure/co2_temporal_latitude_all.png', dpi=300, bbox_inches='tight')
		
def gaussian(x, mean, std_dev):
    return (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    
def temporal_all_map_histogram_aot40():
	data11=pd.read_csv(r"./data/temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_spring'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, patches =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')	
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a+0.01,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	ax.set_xticks(np.arange(-1,1.5,0.5))
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/aot40_histogram_sos.pdf', dpi=300, bbox_inches='tight')

	data11=pd.read_csv(r"./data/temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_autumn'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.01,-0.51,-0.01,0.49,0.99])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/aot40_histogram_eos.pdf', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_summer'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.05,-0.55,-0.05,0.45,0.95])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/aot40_histogram_evimax.pdf', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_all'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.02,-0.52,-0.02,0.48,0.98])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/aot40_histogram_area.pdf', dpi=300, bbox_inches='tight')

def temporal_all_map_histogram_o3():
	data11=pd.read_csv(r"./data/ozone_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_spring'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, patches =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')	
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a+0.01,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	ax.set_xticks(np.arange(-1,1.5,0.5))
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/ozone_histogram_sos.png', dpi=300, bbox_inches='tight')

	data11=pd.read_csv(r"./data/ozone_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_autumn'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.01,-0.51,-0.01,0.49,0.99])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/ozone_histogram_eos.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/ozone_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_summer'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.05,-0.55,-0.05,0.45,0.95])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/ozone_histogram_evimax.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/ozone_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_all'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.02,-0.52,-0.02,0.48,0.98])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/ozone_histogram_area.png', dpi=300, bbox_inches='tight')
	
def temporal_all_map_histogram_temp():
	data11=pd.read_csv(r"./data/temp_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_spring'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, patches =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')	
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a+0.01,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	ax.set_xticks(np.arange(-1,1.5,0.5))
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/temp_histogram_sos.png', dpi=300, bbox_inches='tight')

	data11=pd.read_csv(r"./data/temp_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_autumn'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.01,-0.51,-0.01,0.49,0.99])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/temp_histogram_eos.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/temp_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_summer'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.05,-0.55,-0.05,0.45,0.95])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/temp_histogram_evimax.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/temp_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_all'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.02,-0.52,-0.02,0.48,0.98])
	ax.set_xticks([-1,-0.5,-0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/temp_histogram_area.png', dpi=300, bbox_inches='tight')
	
def temporal_all_map_histogram_co2():
	data11=pd.read_csv(r"./data/co2_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_summer'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1,-0.55,-0.05,0.45,1])
	ax.set_xticks([-1,-0.5,0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/co2_histogram_evimax.png', dpi=300, bbox_inches='tight')
	
	data11=pd.read_csv(r"./data/co2_temporal.csv")
	Date_Mid_Greenup_Phase_1_r=np.array(data11['r_all'])
	a=np.nanmean(Date_Mid_Greenup_Phase_1_r)
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	hist, bins, _ =ax.hist(Date_Mid_Greenup_Phase_1_r, bins=50, density=True,edgecolor='white',color='silver')
	params, _ = curve_fit(gaussian, bins[:-1], hist)
	mean, std_dev = params
	x_range = np.linspace(min(bins), max(bins), 100)
	print(x_range)
	fitted_curve = gaussian(x_range, mean, std_dev)
	ax.plot(x_range, fitted_curve, 'r-', label='Fitted Curve',linewidth=3)
	ax.axvline(0,color='black', linestyle='--',linewidth=3)
	ax.axvline(a,color='red', linestyle='--',linewidth=3)
	ax.text(a-0.5,1.1,str(round(a,2)), fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_ylim(0,1.225)
	#ax.set_xticks([-1.02,-0.52,-0.02,0.48,0.98])
	ax.set_xticks([-1,-0.5,0,0.5,1])
	ax.set_xticklabels([-1,-0.5,-0,0.5,1], fontdict={'family':'arial','weight':'normal','size':36,})
	ax.set_yticks(np.arange(0,1.5,0.5))
	ax.set_yticklabels([0,0.5,1.0], fontdict={'family':'arial','weight':'normal','size':36,})
	plt.savefig('./figure/co2_histogram_area.png', dpi=300, bbox_inches='tight')
	
def temporal_boxplot():
	data1=pd.read_csv(r"./data/temporal.csv")
	aot40spring=np.array(data1['r_spring'])
	aot40autumn=np.array(data1['r_autumn'])
	aot40summer=np.array(data1['r_summer'])
	aot40all=np.array(data1['r_all'])
	data2=pd.read_csv(r"./data/ozone_temporal.csv")
	o3spring=np.array(data2['r_spring'])
	o3autumn=np.array(data2['r_autumn'])
	o3summer=np.array(data2['r_summer'])
	o3all=np.array(data2['r_all'])
	data3=pd.read_csv(r"./data/temp_temporal.csv")
	tempspring=np.array(data3['r_spring'])
	tempautumn=np.array(data3['r_autumn'])
	tempsummer=np.array(data3['r_summer'])
	tempall=np.array(data3['r_all'])		
	data4=pd.read_csv(r"./data/co2_temporal.csv")
	co2summer=np.array(data4['r_summer'])
	co2all=np.array(data4['r_all'])
		
	data=pd.DataFrame()	
	data['aot40spring']=aot40spring
	data['tempspring']=tempspring
	data['aot40autumn']=aot40autumn
	data['tempautumn']=tempautumn
	data['aot40summer']=aot40summer
	data['tempsummer']=tempsummer
	data['co2summer']=co2summer
	data['aot40all']=aot40all
	data['tempall']=tempall
	data['co2all']=co2all
	data=data.dropna()
	fig=plt.figure(figsize=(10, 5))
	ax=fig.add_subplot(1,1,1)	
	group_config = [
		{
			'name': 'SOS',
			'vars': ['aot40spring', 'tempspring'],
			'color': ['#AAE5F3','#E53945'], 
			'position': [0.9, 1.1]
		},
		{
			'name': 'EOS',
			'vars': ['aot40autumn', 'tempautumn'],
			'color': ['#AAE5F3','#E53945'], 
			'position': [1.9, 2.1]
		},
		{
			'name': 'EVI$_{max}$',
			'vars': ['aot40summer', 'tempsummer', 'co2summer'],
			'color': ['#AAE5F3','#E53945','#FEA500'],
			'position': [2.85, 3, 3.15]
		},
		{
			'name': 'EVI$_{area}$',
			'vars': ['aot40all', 'tempall', 'co2all'],
			'color': ['#AAE5F3','#E53945','#FEA500'], 
			'position': [3.85, 4, 4.15]
		}
	]
	
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []

	for group in group_config:
		group_data = [data[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])

	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
               
	colors = [
		'#AAE5F3','#E53945',
		'#AAE5F3','#E53945',
		'#AAE5F3','#E53945','#FEA500',
		'#AAE5F3','#E53945','#FEA500'
	]
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_labels = [group['name'] for group in group_config]
	group_label_positions = [np.mean(group['position']) for group in group_config]
	print(group_label_positions, group_labels)
	ax.set_xlim(0,5)
	ax.set_xticks(group_label_positions, group_labels, fontdict={'family':'arial','weight':'normal','size':18,})
	ax.set_yticks([-1,-0.5,0,0.5,1])
	ax.set_yticklabels([-1,-0.5,0,0.5,1], fontdict={'family':'arial','weight':'normal','size':18,})	
	ax.set_ylabel('R', fontdict={'family':'arial','weight':'normal','size':18,})
	ax.axhline(y=0, color='black', linewidth=1,linestyle='--')
	plt.tight_layout()
	plt.savefig('./figure/temporal_boxplot.pdf', dpi=300, bbox_inches='tight')

def future_predict_spring():
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')

	a=data_us[['spring2022','spring','spring_fixed2022']]
	b=data_eu[['spring2022','spring','spring_fixed2022']]
	c=data_cn[['spring2022','spring','spring_fixed2022']]
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	group_config = [
		{
			'name': 'U.S.',
			'vars': ['spring2022','spring','spring_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [0.85, 1, 1.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [a[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)        
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'Europe',
			'vars': ['spring2022','spring','spring_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [1.85, 2, 2.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [b[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'China',
			'vars': ['spring2022','spring','spring_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [2.85, 3, 3.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [c[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
		
	group_labels = [group['name'] for group in group_config]
	group_label_positions = [np.mean(group['position']) for group in group_config]
	
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	#ax.set_yticks(np.arange(0,8,2))
	#ax.set_yticklabels(np.arange(0,8,2), fontdict={'family':'arial','weight':'normal','size':20,})
	ax.set_ylabel('SOS (Day of Year)',fontdict={'family':'arial','weight':'normal','size':26,})	
	plt.savefig('./figure/sos_future.png',bbox_inches='tight',dpi=300)

def future_predict_autumn():
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')
	
	autumn_us_2022=np.array(data_us['autumn2022'])
	autumn_us_predict=np.array(data_us['autumn'])
	autumn_us_fixed=np.array(data_us['autumn_fixed2022'])

	autumn_eu_2022=np.array(data_eu['autumn2022'])
	autumn_eu_predict=np.array(data_eu['autumn'])
	autumn_eu_fixed=np.array(data_eu['autumn_fixed2022'])
	
	autumn_cn_2022=np.array(data_cn['autumn2022'])
	autumn_cn_predict=np.array(data_cn['autumn'])
	autumn_cn_fixed=np.array(data_cn['autumn_fixed2022'])

	a=data_us[['autumn2022','autumn','autumn_fixed2022']]
	b=data_eu[['autumn2022','autumn','autumn_fixed2022']]
	c=data_cn[['autumn2022','autumn','autumn_fixed2022']]
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	group_config = [
		{
			'name': 'U.S.',
			'vars': ['autumn2022','autumn','autumn_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [0.85, 1, 1.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [a[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
               
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'Europe',
			'vars': ['autumn2022','autumn','autumn_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [1.85, 2, 2.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [b[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'China',
			'vars': ['autumn2022','autumn','autumn_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [2.85, 3, 3.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [c[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
		
	group_labels = [group['name'] for group in group_config]
	group_label_positions = [np.mean(group['position']) for group in group_config]
	
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	#ax.set_yticks(np.arange(0,8,2))
	#ax.set_yticklabels(np.arange(0,8,2), fontdict={'family':'arial','weight':'normal','size':20,})
	ax.set_ylabel('EOS (Day of Year)',fontdict={'family':'arial','weight':'normal','size':26,})	
	plt.savefig('./figure/eos_future.png',bbox_inches='tight',dpi=300)
	#plt.show()
	
def future_predict_summer():
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')
	
	summer_us_2022=np.array(data_us['summer2022'])
	summer_us_predict=np.array(data_us['summer'])
	summer_us_fixed=np.array(data_us['summer_fixed2022'])

	summer_eu_2022=np.array(data_eu['summer2022'])
	summer_eu_predict=np.array(data_eu['summer'])
	summer_eu_fixed=np.array(data_eu['summer_fixed2022'])
	
	summer_cn_2022=np.array(data_cn['summer2022'])
	summer_cn_predict=np.array(data_cn['summer'])
	summer_cn_fixed=np.array(data_cn['summer_fixed2022'])

	a=data_us[['summer2022','summer','summer_fixed2022']]
	b=data_eu[['summer2022','summer','summer_fixed2022']]
	c=data_cn[['summer2022','summer','summer_fixed2022']]
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	group_config = [
		{
			'name': 'U.S.',
			'vars': ['summer2022','summer','summer_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [0.85, 1, 1.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [a[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
               
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'Europe',
			'vars': ['summer2022','summer','summer_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [1.85, 2, 2.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [b[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'China',
			'vars': ['summer2022','summer','summer_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [2.85, 3, 3.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [c[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
		
	group_labels = [group['name'] for group in group_config]
	group_label_positions = [np.mean(group['position']) for group in group_config]
	
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	#ax.set_yticks(np.arange(0,8,2))
	#ax.set_yticklabels(np.arange(0,8,2), fontdict={'family':'arial','weight':'normal','size':20,})
	ax.set_ylabel('EVI$_{max}$',fontdict={'family':'arial','weight':'normal','size':26,})	
	plt.savefig('./figure/evimax_future.png',bbox_inches='tight',dpi=300)
	#plt.show()
	
def future_predict_all():
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')
	
	all_us_2022=np.array(data_us['all2022'])
	all_us_predict=np.array(data_us['all'])
	all_us_fixed=np.array(data_us['all_fixed2022'])

	all_eu_2022=np.array(data_eu['all2022'])
	all_eu_predict=np.array(data_eu['all'])
	all_eu_fixed=np.array(data_eu['all_fixed2022'])
	
	all_cn_2022=np.array(data_cn['all2022'])
	all_cn_predict=np.array(data_cn['all'])
	all_cn_fixed=np.array(data_cn['all_fixed2022'])

	a=data_us[['all2022','all','all_fixed2022']]
	b=data_eu[['all2022','all','all_fixed2022']]
	c=data_cn[['all2022','all','all_fixed2022']]
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	group_config = [
		{
			'name': 'U.S.',
			'vars': ['all2022','all','all_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [0.85, 1, 1.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [a[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
               
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'Europe',
			'vars': ['all2022','all','all_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [1.85, 2, 2.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [b[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)

	group_config = [
		{
			'name': 'China',
			'vars': ['all2022','all','all_fixed2022'],
			'color': ['black','blue','red'], 
			'position': [2.85, 3, 3.15]
		},
	]
	all_data = []
	all_positions = []
	box_colors = []
	var_labels = []
	for group in group_config:
		group_data = [c[var] for var in group['vars']]
		all_data.extend(group_data)
		all_positions.extend(group['position'])
		box_colors.extend([group['color']] * len(group['vars']))
		var_labels.extend(group['vars'])
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(all_data, whis=0.25,positions=all_positions,
					 widths=0.1, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['black','blue','red']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
		
	group_labels = [group['name'] for group in group_config]
	group_label_positions = [np.mean(group['position']) for group in group_config]
	
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('EVI$_{area}$',fontdict={'family':'arial','weight':'normal','size':26,})	
	plt.savefig('./figure/eviarea_future.png',bbox_inches='tight',dpi=300)
	
def future_predict_delta():
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')
	
	spring_us_2022=np.array(data_us['spring2022'])
	spring_us_predict=np.array(data_us['spring'])
	spring_us_fixed=np.array(data_us['spring_fixed2022'])
	res_us=spring_us_predict-spring_us_fixed

	spring_eu_2022=np.array(data_eu['spring2022'])
	spring_eu_predict=np.array(data_eu['spring'])
	spring_eu_fixed=np.array(data_eu['spring_fixed2022'])
	res_eu=spring_eu_predict-spring_eu_fixed
	
	spring_cn_2022=np.array(data_cn['spring2022'])
	spring_cn_predict=np.array(data_cn['spring'])
	spring_cn_fixed=np.array(data_cn['spring_fixed2022'])
	res_cn=spring_cn_predict-spring_cn_fixed
	
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	a=[res_us,res_eu,res_cn]
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(a, whis=0.25, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['#E63946','#AAE5F4','orange']
	for box, color in zip(box['boxes'], colors):
		box.set_facecolor(color)
		
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks(np.arange(0,10,2))
	ax.set_yticklabels(np.arange(0,10,2), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('$\Delta$SOS (Days)',fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/sos_delta.pdf',bbox_inches='tight',dpi=300)
	
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./new/eu_predict.csv')
	data_cn=pd.read_csv('./new/cn_predict.csv')
	
	autumn_us_2022=np.array(data_us['autumn2022'])
	autumn_us_predict=np.array(data_us['autumn'])
	autumn_us_fixed=np.array(data_us['autumn_fixed2022'])
	res_us=autumn_us_predict-autumn_us_fixed

	autumn_eu_2022=np.array(data_eu['autumn2022'])
	autumn_eu_predict=np.array(data_eu['autumn'])
	autumn_eu_fixed=np.array(data_eu['autumn_fixed2022'])
	res_eu=autumn_eu_predict-autumn_eu_fixed
	
	autumn_cn_2022=np.array(data_cn['autumn2022'])
	autumn_cn_predict=np.array(data_cn['autumn'])
	autumn_cn_fixed=np.array(data_cn['autumn_fixed2022'])
	res_cn=autumn_cn_predict-autumn_cn_fixed
	
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	a=[res_us,res_eu,res_cn]
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(a, whis=0.25, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['#E63946','#AAE5F4','orange']
	for box, color in zip(box['boxes'], colors):
		box.set_facecolor(color)
		
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_yticks(np.arange(0,-8,-2))
	ax.set_yticklabels(np.arange(0,-8,-2), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('$\Delta$EOS (Days)',fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/eos_delta.pdf',bbox_inches='tight',dpi=300)
	
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')
	
	summer_us_2022=np.array(data_us['summer2022'])
	summer_us_predict=np.array(data_us['summer'])
	summer_us_fixed=np.array(data_us['summer_fixed2022'])
	res_us=summer_us_predict-summer_us_fixed
	
	summer_eu_2022=np.array(data_eu['summer2022'])
	summer_eu_predict=np.array(data_eu['summer'])
	summer_eu_fixed=np.array(data_eu['summer_fixed2022'])
	res_eu=summer_eu_predict-summer_eu_fixed
	
	summer_cn_2022=np.array(data_cn['summer2022'])
	summer_cn_predict=np.array(data_cn['summer'])
	summer_cn_fixed=np.array(data_cn['summer_fixed2022'])
	res_cn=summer_cn_predict-summer_cn_fixed
	
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	a=[res_us,res_eu,res_cn]
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(a, whis=0.25, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['#E63946','#AAE5F4','orange']
	for box, color in zip(box['boxes'], colors):
		box.set_facecolor(color)
		
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('$\Delta$EVI$_{max}$',fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/evimax_delta.pdf',bbox_inches='tight',dpi=300)
	
	data_us=pd.read_csv('./data/us_predict.csv')
	data_eu=pd.read_csv('./data/eu_predict.csv')
	data_cn=pd.read_csv('./data/cn_predict.csv')
	
	all_us_2022=np.array(data_us['all2022'])
	all_us_predict=np.array(data_us['all'])
	all_us_fixed=np.array(data_us['all_fixed2022'])
	res_us=all_us_predict-all_us_fixed

	all_eu_2022=np.array(data_eu['all2022'])
	all_eu_predict=np.array(data_eu['all'])
	all_eu_fixed=np.array(data_eu['all_fixed2022'])
	res_eu=all_eu_predict-all_eu_fixed
	
	all_cn_2022=np.array(data_cn['all2022'])
	all_cn_predict=np.array(data_cn['all'])
	all_cn_fixed=np.array(data_cn['all_fixed2022'])
	res_cn=all_cn_predict-all_cn_fixed
	
	fig=plt.figure(figsize=(8, 8))
	ax=fig.add_subplot(1,1,1)	
	a=[res_us,res_eu,res_cn]
	meanpointprops = dict(marker='D', markeredgecolor='black',
						  markerfacecolor='yellow',markersize=6,color='yellow')
	box = ax.boxplot(a, whis=0.25, patch_artist=True,
					 showfliers=False, 
					 meanline=False,medianprops={'color': 'none', 'linewidth': 0},meanprops=meanpointprops,showmeans=True)
	colors = ['#E63946','#AAE5F4','orange']
	for box, color in zip(box['boxes'], colors):
		box.set_facecolor(color)
		
	ax.tick_params(axis='y', labelsize=26)
	ax.set_xticks(np.arange(1,4,1))
	ax.set_xticklabels(['U.S.','Europe','China'], fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('$\Delta$EVI$_{area}$',fontdict={'family':'arial','weight':'normal','size':26,})	
	plt.savefig('./figure/eviarea_delta.pdf',bbox_inches='tight',dpi=300)

def pvalue_aot40():
	data=pd.read_csv(r"./data/temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	Date_Mid_Greenup_Phase_1_aot40_r=np.array(data['r_spring'])
	Date_Mid_Senescence_Phase_1_aot40_r=np.array(data['r_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	Date_Mid_Greenup_Phase_1_aot40_p=np.array(data['p_spring'])
	Date_Mid_Senescence_Phase_1_aot40_p=np.array(data['p_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
	latpostivesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]	
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80]) 
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True 
	plt.savefig('./figure/pvalue_aot40_sos.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80]) 
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True 
	plt.savefig('./figure/pvalue_aot40_eos.png', dpi=300, bbox_inches='tight')

	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80]) 
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True 
	plt.savefig('./figure/pvalue_aot40_evimax.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80]) 
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True 
	gl.right_labels = True 
	plt.savefig('./figure/pvalue_aot40_eviarea.png', dpi=300, bbox_inches='tight')

def pvalue_ozone():
	data=pd.read_csv(r"./data/ozone_temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	Date_Mid_Greenup_Phase_1_aot40_r=np.array(data['r_spring'])
	Date_Mid_Senescence_Phase_1_aot40_r=np.array(data['r_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	Date_Mid_Greenup_Phase_1_aot40_p=np.array(data['p_spring'])
	Date_Mid_Senescence_Phase_1_aot40_p=np.array(data['p_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
	latpostivesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]	
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_ozone_sos.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_ozone_eos.png', dpi=300, bbox_inches='tight')

	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_ozone_evimax.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_ozone_eviarea.png', dpi=300, bbox_inches='tight')

def pvalue_temp():
	data=pd.read_csv(r"./data/temp_temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	Date_Mid_Greenup_Phase_1_aot40_r=np.array(data['r_spring'])
	Date_Mid_Senescence_Phase_1_aot40_r=np.array(data['r_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	Date_Mid_Greenup_Phase_1_aot40_p=np.array(data['p_spring'])
	Date_Mid_Senescence_Phase_1_aot40_p=np.array(data['p_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
	latpostivesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]	
	
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_temp_sos.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_temp_eos.png', dpi=300, bbox_inches='tight')

	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_temp_evimax.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_temp_eviarea.png', dpi=300, bbox_inches='tight')

def pvalue_co2():
	data=pd.read_csv(r"./data/co2_temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	EVI2_Onset_Greenness_Maximum_1_co2_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_co2_r=np.array(data['r_all'])
	EVI2_Onset_Greenness_Maximum_1_co2_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_co2_p=np.array(data['p_all'])
	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_co2_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_co2_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_co2_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_co2_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_co2_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_co2_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_co2_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_co2_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_co2_r<0)]	
	
	fig = plt.figure()
	projections = [ccrs.AzimuthalEquidistant(central_longitude=0.0, central_latitude=90.0)]
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_co2_evimax.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_co2_p<=0.05)&(EVI2_Growing_Season_Area_1_co2_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_co2_p<=0.05)&(EVI2_Growing_Season_Area_1_co2_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_co2_p<=0.05)&(EVI2_Growing_Season_Area_1_co2_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_co2_p<=0.05)&(EVI2_Growing_Season_Area_1_co2_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_co2_p>0.05)&(EVI2_Growing_Season_Area_1_co2_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_co2_p>0.05)&(EVI2_Growing_Season_Area_1_co2_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_co2_p>0.05)&(EVI2_Growing_Season_Area_1_co2_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_co2_p>0.05)&(EVI2_Growing_Season_Area_1_co2_r<0)]	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, projection=projections[0])
	extents = [-180, 180, 15, 60]
	ax.set_extent(extents, crs=ccrs.PlateCarree())
	ax.coastlines()
	ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='black')	
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black',color='floralwhite')
	ax.scatter(lonpostivenosig,latpostivenosig,s=6,color='blue',label='Postive',transform=ccrs.PlateCarree())	
	ax.scatter(lonnegativenosig,latnegativenosig,s=6,color='cyan',label='Negative',transform=ccrs.PlateCarree())
	ax.scatter(lonnegativesig,latnegativesig,s=6,color='green',label='Negative${^*}$',transform=ccrs.PlateCarree())
	ax.scatter(lonpostivesig,latpostivesig,s=6,color='red',label='Postive${^*}$',transform=ccrs.PlateCarree())
	gl = ax.gridlines(
		crs=ccrs.PlateCarree(),
		draw_labels=True,
		linewidth=1,
		color='gray',
		alpha=0.5,
		linestyle='--'
	)
	gl.xlocator = mticker.FixedLocator(np.arange(-180, 210, 30))
	gl.ylocator = mticker.FixedLocator([20,50,80])
	gl.xformatter = LONGITUDE_FORMATTER
	gl.yformatter = LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 10, 'color': 'black'}
	gl.ylabel_style = {'size': 10, 'color': 'black'}
	gl.top_labels = True
	gl.right_labels = True
	plt.savefig('./figure/pvalue_co2_eviarea.png', dpi=300, bbox_inches='tight')

def pvalue_aot40_hist():
	data=pd.read_csv(r"./data/temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	Date_Mid_Greenup_Phase_1_aot40_r=np.array(data['r_spring'])
	Date_Mid_Senescence_Phase_1_aot40_r=np.array(data['r_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	Date_Mid_Greenup_Phase_1_aot40_p=np.array(data['p_spring'])
	Date_Mid_Senescence_Phase_1_aot40_p=np.array(data['p_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
	
	latpostivesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_aot40_sos_hist.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_aot40_eos_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_aot40_evimax_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_aot40_eviarea_hist.png', dpi=300, bbox_inches='tight')

def pvalue_ozone_hist():
	data=pd.read_csv(r"./data/ozone_temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	Date_Mid_Greenup_Phase_1_aot40_r=np.array(data['r_spring'])
	Date_Mid_Senescence_Phase_1_aot40_r=np.array(data['r_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	Date_Mid_Greenup_Phase_1_aot40_p=np.array(data['p_spring'])
	Date_Mid_Senescence_Phase_1_aot40_p=np.array(data['p_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
	
	latpostivesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_ozone_sos_hist.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_ozone_eos_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_ozone_evimax_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_ozone_eviarea_hist.png', dpi=300, bbox_inches='tight')

def pvalue_temp_hist():
	data=pd.read_csv(r"./data/temp_temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	Date_Mid_Greenup_Phase_1_aot40_r=np.array(data['r_spring'])
	Date_Mid_Senescence_Phase_1_aot40_r=np.array(data['r_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	Date_Mid_Greenup_Phase_1_aot40_p=np.array(data['p_spring'])
	Date_Mid_Senescence_Phase_1_aot40_p=np.array(data['p_autumn'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
	
	latpostivesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Greenup_Phase_1_aot40_p<=0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Greenup_Phase_1_aot40_p>0.05)&(Date_Mid_Greenup_Phase_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_temp_sos_hist.png', dpi=300, bbox_inches='tight')
	
	latpostivesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativesig=lat[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativesig=lon[(Date_Mid_Senescence_Phase_1_aot40_p<=0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	latpostivenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	lonpostivenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r>0)]
	latnegativenosig=lat[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]
	lonnegativenosig=lon[(Date_Mid_Senescence_Phase_1_aot40_p>0.05)&(Date_Mid_Senescence_Phase_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_temp_eos_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_temp_evimax_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_temp_eviarea_hist.png', dpi=300, bbox_inches='tight')
	
def pvalue_co2_hist():
	data=pd.read_csv(r"./data/co2_temporal.csv")
	lat=np.array(data['lat'])
	lon=np.array(data['lon'])
	EVI2_Onset_Greenness_Maximum_1_aot40_r=np.array(data['r_summer'])
	EVI2_Growing_Season_Area_1_aot40_r=np.array(data['r_all'])
	EVI2_Onset_Greenness_Maximum_1_aot40_p=np.array(data['p_summer'])
	EVI2_Growing_Season_Area_1_aot40_p=np.array(data['p_all'])
		
	latpostivesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p<=0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Onset_Greenness_Maximum_1_aot40_p>0.05)&(EVI2_Onset_Greenness_Maximum_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_co2_evimax_hist.png', dpi=300, bbox_inches='tight')
		
	latpostivesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativesig=lat[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativesig=lon[(EVI2_Growing_Season_Area_1_aot40_p<=0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	latpostivenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	lonpostivenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r>0)]
	latnegativenosig=lat[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]
	lonnegativenosig=lon[(EVI2_Growing_Season_Area_1_aot40_p>0.05)&(EVI2_Growing_Season_Area_1_aot40_r<0)]	
	a=len(latpostivesig)/len(lat)*100
	b=len(latnegativesig)/len(lat)*100
	c=len(latpostivenosig)/len(lat)*100
	d=len(latnegativenosig)/len(lat)*100
	
	count=[a,b,c,d]
	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(np.arange(0,len(count)/2,0.5),count,color=['red','green','blue','cyan'],label=['Positive${^*}$','Negative${^*}$','Postive','Negative'],width=0.25)
	ax.set_xticks(np.arange(0,len(count)/2,0.5))
	ax.set_xticklabels(['Pos.${^*}$','Neg.${^*}$','Pos.','Neg.'],fontdict={'family':'arial','weight':'normal','size':26,})

	ax.set_yticks(np.arange(0,60,10))
	ax.set_yticklabels(np.arange(0,60,10), fontdict={'family':'arial','weight':'normal','size':26,})
	ax.set_ylabel('Percentage (%)', fontdict={'family':'arial','weight':'normal','size':26,})
	plt.savefig('./figure/pvalue_co2_eviarea_hist.png', dpi=300, bbox_inches='tight')
								
def main(args):
	#phenology()
	#latitude_plot()
	#latitude_plot_aot40()
	#latitude_plot_ozone()
	#latitude_plot_temp()
	#latitude_plot_co2()
	#partial_year_plot_aot40()
	#partial_year_plot_o3()
	#partial_year_plot_co2()
	#partial_year_plot_temp()
	#latitude_temporal_plot()
	#latitude_temporal_plot_o3()
	#latitude_temporal_plot_temp()
	#latitude_temporal_plot_co2()
	#temporal_all_map_aot40()
	#temporal_all_map_o3()
	#temporal_all_map_temp()
	#temporal_all_map_co2()
	#temporal_all_map_histogram_aot40()
	#temporal_all_map_histogram_o3()
	#temporal_all_map_histogram_temp()
	#temporal_all_map_histogram_co2()
	temporal_boxplot()
	#future_predict_delta()
	#future_predict_spring()
	#future_predict_autumn()
	#future_predict_summer()
	#future_predict_all()
	#pvalue_aot40()
	#pvalue_ozone()
	#pvalue_temp()
	#pvalue_co2()
	#pvalue_aot40_hist()
	#pvalue_ozone_hist()
	#pvalue_temp_hist()
	#pvalue_co2_hist()
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
