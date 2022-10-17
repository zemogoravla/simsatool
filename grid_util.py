#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from scipy.spatial.transform import Rotation
#import rpcm
#import camera_approximation
#import util
#import subprocess
#import json
from skimage.io import imread, imsave
#import glob
import utils
import utm

def get_voi_mesh(aoi, altitude_range=[-100,100], 
                 horizontal_resolution=2, vertical_resolution=3 ):
    '''
    get_voi_mesh
    

    Parameters
    ----------
    aoi : geojson.Polygon 
        GeoJSON polygon representing the Area of interest.
    altitude_range : [float,float], optional
        List or tuple of [min_altitude, max_altitude] in meters. The default is [-100,100].
    horizontal_resolution : float, optional
        Horizontal resolution in meters. The default is 2.
    vertical_resolution : float, optional
        Vertical resolution in meters. The default is 3.

    Returns
    -------
    longitudes : 3D np.array
        Longitude mesh coordinates of the VOI.
    latitudes : 3D np.array
        Latitude mesh coordinates of the VOI.
    altitudes : 3D np.array
        Altitude mesh coordinates of the VOI.
    easts : 3D np.array
        UTM Easting mesh coordinates of the VOI.
    norths : 3D np.array
        UTM Northing mesh coordinates of the VOI.

    '''
    
    min_easting,  max_easting, min_northing, max_northing = utils.utm_bounding_box_from_lonlat_aoi(aoi)
    resolution=horizontal_resolution
    Northings = np.arange(min_northing, max_northing+resolution, resolution)
    Eastings = np.arange(min_easting, max_easting+resolution, resolution)
        
    h_min = altitude_range[0]
    h_max = altitude_range[1]
    Heights = np.arange(h_min, h_max+vertical_resolution ,vertical_resolution) 
    
    #mesh grid (UTM)    
    easts,norths,altitudes = np.meshgrid(Eastings, Northings, Heights,indexing='ij' )
    
    #meshgrid (lon,lat)
    zone_number = utm.latlon_to_zone_number(aoi['coordinates'][0][0][1], aoi['coordinates'][0][0][0])
    zone_letter = utm.latitude_to_zone_letter(aoi['coordinates'][0][0][1])
    latitudes, longitudes = utm.to_latlon(easts.ravel().copy(), norths.ravel().copy(), zone_number, zone_letter)
    latitudes = np.reshape(latitudes, norths.shape)
    longitudes = np.reshape(longitudes, easts.shape)
    
    return longitudes, latitudes, altitudes, easts, norths


def get_aoi_center(aoi):
    coords = np.array(aoi['coordinates'][0])
    lons = coords[:,0]
    lats = coords[:,1]
    lon = (np.max(lons) + np.min(lons)) / 2
    lat = (np.max(lats) + np.min(lats)) / 2
    return lon, lat

