#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:54:17 2022

@author: agomez
"""

#%%
import numpy as np

import blender
from grid_util import get_voi_mesh, get_aoi_center
from  paffine import camera_rotation_matrix_from_view_angles
from satellite import satellite_distance_wrt_nadir
import satellite
import utils  
    
    
    
#%% TEST THE GRID
aoi = {
    "coordinates": [
        [
            [-58.58923437034032, -34.49059476958225],
            [-58.58923437034032, -34.4891885066768],
            [-58.58733243810684, -34.4891885066768],
            [-58.58733243810684, -34.49059476958225],
            [-58.58923437034032, -34.49059476958225],
        ]
    ],
    "type": "Polygon",
}
altitude_range = [-10,10]
horizontal_resolution = 50
vertical_resolution = 5

lon_origin, lat_origin = get_aoi_center(aoi)
alt_origin = 5



longitudes, latitudes, altitudes, easts, norths = \
get_voi_mesh(aoi, altitude_range,horizontal_resolution, vertical_resolution)

for v in ['longitudes', 'latitudes', 'altitudes', 'easts', 'norths']:
    print(v)
    print(eval(v))
    print('-----------------------------------------------')
    
    
print(latitudes.min(), latitudes.max())

# local mesh coordinates
east_origin, north_origin = utils.utm_from_lonlat([lon_origin], [lat_origin])
ee = easts - east_origin[0]
nn = norths - north_origin[0]
uu = altitudes - alt_origin


for v in ['ee', 'nn', 'uu']:
    print(v)
    print(eval(v))
    print('-----------------------------------------------')



#%% TEST camera_rotation_matrix_from_view_angles

zenith_in_degrees = 45 
azimuth_in_degrees = 90
roll_in_degrees=None



R = camera_rotation_matrix_from_view_angles(zenith_in_degrees, 
                                            azimuth_in_degrees,
                                            roll_in_degrees)


print(R)


#%% TEST satellite_distance_wrt_nadir


print(satellite_distance_wrt_nadir(0)  / np.cos(np.radians(0)) * 0.3)
print(satellite_distance_wrt_nadir(20) / np.cos(np.radians(20)) * 0.3)
print(satellite_distance_wrt_nadir(56) / np.cos(np.radians(56)) * 0.3)
print(satellite_distance_wrt_nadir(60) / np.cos(np.radians(60)) * 0.3)


# def generate_blender_s2p_pair(ref_zenith, ref_azimuth, sec_zenith, sec_azimuth, 
#                               base_dir, blender_filename, simulation_dir_name=None,
#                               overwrite=False,
#                               s2p_config_template_filename=None):
   
#     if not simulation_dir_name is None:
#         simulation_dir = os.path.join(base_dir, simulation_dir_name)
#     else:
#         simulation_dir = base_dir
        
#     os.makedirs(os.path.join(base_dir,'IMAGES'), exist_ok=True)
#     os.makedirs(os.path.join(base_dir,'BLENDER_CAMERA'), exist_ok=True)
#     os.makedirs(os.path.join(base_dir,'BLENDER_COMMAND'), exist_ok=True)
#     os.makedirs(os.path.join(base_dir,'RPCFIT'), exist_ok=True)
    
#     # ref ---------------------------------------------------------------------
#     ref_image_filename = os.path.join(base_dir,'IMAGES', f'ze_{ref_zenith:05.1f}_az_{ref_azimuth:05.1f}_0001.tif')
#     ref_image_filename_for_blender = ref_image_filename[:-8] #sin lo que agrega el render
#     ref_blender_camera_script_filename = os.path.join(base_dir,'BLENDER_CAMERA', f'blender_camera_ze_{ref_zenith:05.1f}_az_{ref_azimuth:05.1f}.py')
#     ref_blender_command_filename = os.path.join(base_dir,'BLENDER_COMMAND', f'blender_command_ze_{ref_zenith:05.1f}_az_{ref_azimuth:05.1f}.sh')
#     ref_rpcfit_filename = os.path.join(base_dir,'RPCFIT', f'rpcfit_ze_{ref_zenith:05.1f}_az_{ref_azimuth:05.1f}.txt')
    
    
#     if not os.path.isfile(ref_image_filename) or overwrite:
#         ref_P_affine, ref_blender_camera_script = compute_P_affine_and_blender_camera_script(ref_zenith, ref_azimuth)
#         compute_rpcfit_for_blender(ref_P_affine, ref_rpcfit_filename)
        
#         ref_blender_command = get_blender_command(blender_filename, ref_blender_camera_script_filename, ref_image_filename_for_blender)
        
#         #save scripts
#         save_txt(ref_blender_camera_script_filename, ref_blender_camera_script)
#         save_txt(ref_blender_command_filename, ref_blender_command)
        
#         # run blender
#         subprocess.call(ref_blender_command, shell=True)
        
    
    
#     #sec ----------------------------------------------------------------------
#     sec_image_filename = os.path.join(base_dir,'IMAGES', f'ze_{sec_zenith:05.1f}_az_{sec_azimuth:05.1f}_0001.tif')
#     sec_image_filename_for_blender = sec_image_filename[:-8] #sin lo que agrega el render
#     sec_blender_camera_script_filename = os.path.join(base_dir,'BLENDER_CAMERA', f'blender_camera_ze_{sec_zenith:05.1f}_az_{sec_azimuth:05.1f}.py')
#     sec_blender_command_filename = os.path.join(base_dir,'BLENDER_COMMAND', f'blender_command_ze_{sec_zenith:05.1f}_az_{sec_azimuth:05.1f}.sh')
#     sec_rpcfit_filename = os.path.join(base_dir,'RPCFIT', f'rpcfit_ze_{sec_zenith:05.1f}_az_{sec_azimuth:05.1f}.txt')
    
    
#     if not os.path.isfile(sec_image_filename) or overwrite:
#         sec_P_affine, sec_blender_camera_script = compute_P_affine_and_blender_camera_script(sec_zenith, sec_azimuth)
#         compute_rpcfit_for_blender(sec_P_affine, sec_rpcfit_filename)
        
#         sec_blender_command = get_blender_command(blender_filename, sec_blender_camera_script_filename, sec_image_filename_for_blender)
        
#         #save scripts
#         save_txt(sec_blender_camera_script_filename, sec_blender_camera_script)
#         save_txt(sec_blender_command_filename, sec_blender_command)
        
#         # run blender
#         subprocess.call(sec_blender_command, shell=True)
        
    
#     # -------------------------------------------------------------------------
#     # generate the s2p config
#     # load the config template
#     if s2p_config_template_filename is None:
#         s2p_config_template_filename = os.path.join(base_dir,'S2P_CONFIG','s2p_config_template.json')
#     s2p_config_filename = os.path.join(simulation_dir, 'S2P', f's2p_config_ref_ze_{ref_zenith:05.1f}_ref_az_{ref_azimuth:05.1f}_sec_ze_{sec_zenith:05.1f}_sec_az_{sec_azimuth:05.1f}.json')
#     s2p_output_dir = f'ref_ze_{ref_zenith:05.1f}_ref_az_{ref_azimuth:05.1f}_sec_ze_{sec_zenith:05.1f}_sec_az_{sec_azimuth:05.1f}'
#     with open(s2p_config_template_filename, 'r') as fp:
#         config_dict = json.load(fp)

#     config_dict['out_dir'] = s2p_output_dir
#     config_dict['images'][0]['img'] = os.path.relpath(ref_image_filename, os.path.join(simulation_dir, 'S2P'))
#     config_dict['images'][1]['img'] = os.path.relpath(sec_image_filename, os.path.join(simulation_dir, 'S2P'))
    
#     config_dict['images'][0]['rpc'] = os.path.relpath(ref_rpcfit_filename, os.path.join(simulation_dir, 'S2P'))
#     config_dict['images'][1]['rpc'] = os.path.relpath(sec_rpcfit_filename, os.path.join(simulation_dir, 'S2P'))

#     # PASAN A ESTAR EN EL TEMPLATE EN EL DIRECTORIO S2P_CONFIG dentro del SIMULATION DIR u  otro que se pase como parametro
#     # config_dict['dsm_resolution'] = 0.3
#     # config_dict['tile_size'] = 600
#     # config_dict['dsm_radius'] = 1
    
#     # config_dict["disp_range_method"] = "fixed_altitude_range"
#     # config_dict["alt_min"] = -5
#     # config_dict["alt_max"] = 35
    
#     # config_dict["register_with_shear"] = True
    
#     # # para que se mantengan las disparidades tiene que estar en False
#     # config_dict["clean_intermediate"] = False
    
    
#     # save the config
#     with open(s2p_config_filename, 'w') as fp:
#         json.dump(config_dict, fp, indent=2)
