#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rpcm
import sys
import numpy as np

sys.path.append('../rpcfit')
from rpcfit import rpc_fit

from grid_util import get_voi_mesh, get_aoi_center
import utm

def compute_rpc_from_affine_camera(P_affine, aoi, altitude_range, 
                                   output_filename, lon_lat_alt_origin=None,
                                   horizontal_resolution=2, vertical_resolution=3,
                                   samples_train=50000, samples_test=100000,
                                   verbose=False):
    '''
    Compute an RPC model from an affine camera model using RPCFIT

    Parameters
    ----------
    P_affine : 2x4 np.array
        Local affine camera model. P_affine projects 3D points in local coordinates (e,n,u) to image pixels.
        (e,n,u) coordinates are respect to the origin of the scene that is the same as the (0,0,0) of Blender
    aoi : geojson Polygon
        Area of interest.
    altitude_range : TYPE
        DESCRIPTION.
    lon_lat_alt_origin : 3-tuple or list, optional
        The RPC camera model will point to that origin.
        If None, then the center of the AOI and altitude=0  are used
    output_filename : str
        DESCRIPTION.
    horizontal_resolution : TYPE, optional
        DESCRIPTION. The default is 2.
    vertical_resolution : TYPE, optional
        DESCRIPTION. The default is 3.
    samples_train : int, optional
        Number of samples in the VOI to fit the RPC. The default is 50000.
    samples_test : TYPE, optional
        Number of samples in the VOI to test the fitting. The default is 100000.
rpcfit
    Returns
    -------
    None. Saves the RPC in Ikonos format to output_filename

    '''
    
    #TODO check that the size of the mesh is not to small and not to big
    
    longitudes, latitudes, altitudes, easts, norths = \
    get_voi_mesh(aoi, altitude_range, horizontal_resolution, vertical_resolution)
        
    #
    if lon_lat_alt_origin is None:
        lon, lat = get_aoi_center(aoi)
        lon_lat_alt_origin = [lon, lat, 0]

    
    utm_origin = utm.from_latlon(lon_lat_alt_origin[1], lon_lat_alt_origin[0] )
    alt_origin = lon_lat_alt_origin[2]
    
    # GLOBAL GEODETIC COORDINATES OF THE VOI
    lons = longitudes.ravel()
    lats = latitudes.ravel()
    alts = altitudes.ravel()
    
    # LOCAL UTM COORDINATES OF THE VOI
    ee = (easts - utm_origin[0]).ravel()
    nn = (norths - utm_origin[1]).ravel()
    uu = (alts - alt_origin).ravel()

    # stack all the locs
    locs = np.vstack((lons, lats, alts)).T
    locs_enu = np.vstack((ee, nn, uu)).T

    #subsample the arrays with random indices
    indices_train = np.random.choice(np.arange(len(lons)),size=(samples_train),replace=False)
    indices_test = np.random.choice(np.arange(len(lons)),size=(samples_test),replace=False)

    # locs for train and test
    locs_train  = locs[indices_train]
    locs_test  = locs[indices_test]
    locs_enu_train = locs_enu[indices_train]
    locs_enu_test = locs_enu[indices_test]

    # targets for train and test (projected with P_affine)
    target_enu_train = P_affine @ np.vstack((locs_enu_train[:, 0],
                                                   locs_enu_train[:, 1],
                                                   locs_enu_train[:, 2],
                                                   np.ones((samples_train))))
    target_enu_train = target_enu_train.T

    target_enu_test = P_affine @ np.vstack((locs_enu_test[:, 0],
                                                  locs_enu_test[:, 1],
                                                  locs_enu_test[:, 2],
                                                  np.ones((samples_test))))
    target_enu_test = target_enu_test.T
    
    # fit on training set
    plot_option = False
    rpc_calib, log = rpc_fit.calibrate_rpc(target_enu_train, locs_train, separate=False, tol=1e-10
                                          , max_iter=20, method='initLcurve'
                                          , plot=plot_option, orientation = 'projloc', get_log=True )
    
    if verbose:
        # evaluate on training set
        rmse_err, mae, planimetry = rpc_fit.evaluate(rpc_calib, locs_train, target_enu_train)
        print('RPCFIT - Training set :   Mean X-RMSE {:e}     Mean Y-RMSE {:e}'.format(*rmse_err))
        
        # evaluate on the test set
        rmse_err, mae, planimetry = rpc_fit.evaluate(rpc_calib, locs_test, target_enu_test)
        print('RPCFIT - Test set :   Mean X-RMSE {:e}     Mean Y-RMSE {:e}'.format(*rmse_err))
        
    rpc_calib.write_to_file(output_filename)
    