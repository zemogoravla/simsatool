#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:28:33 2022

@author: agomez
"""
import os

from simulator import Simulator
from satellite import Satellite
from location import Location
from blender import Blender
from s2p_configurator import S2PConfigurator

#%% 
simulation_base_dir = 'data/SIMULATION_3'
s2p_configs_dir = os.path.join(simulation_base_dir, 'S2P_CONFIGS')  
blender_scene_filename ='data/model/cylinder_scene.blend'

# zenith = [0, 20] 
# azimuth = [0, 0]
# sun_zenith = [45, 45]
# sun_azimuth = [0, 90]

# Generate pairs of images [(ref)erence - (sec)ondary]
ref_zenith_list = [0]
ref_azimuth_list = [0]
ref_sun_zenith_list = [45]
ref_sun_azimuth_list = [0]

sec_zenith_list = [20]
sec_azimuth_list = [0]
sec_sun_zenith_list = [30]
sec_sun_azimuth_list = [90]


image_xy_size = (600,600)

# Initialize the simulator
satellite = Satellite()
blender = Blender(blender_scene_filename, image_xy_size)
location = Location(lon_lat_alt_origin=[-58.5881805419922, -34.4899978637695,0])
sim = Simulator(simulation_base_dir, satellite, blender, location)

sim.location.lon_lat_alt_origin = [1,2,3]
sim.serialize()

A = Simulator.deserialize('TMP.pkl')



# Initialize the S2P configurator
s2p_configurator = S2PConfigurator(s2p_configs_dir)


# ref_image_filename, ref_rpc_filename = sim.simulate_image_and_rpcfit(zenith[0], azimuth[0], roll, sun_zenith[0], sun_azimuth[0], overwrite=True)
# sec_image_filename, sec_rpc_filename = sim.simulate_image_and_rpcfit(zenith[1], azimuth[1], roll, sun_zenith[1], sun_azimuth[1], overwrite=True)

# s2p_config_filename = s2p_configurator.create_config(ref_image_filename, ref_rpc_filename, sec_image_filename, sec_rpc_filename, overwrite=True)

for i in range(len(ref_zenith_list)):
    ref_image_filename, ref_rpc_filename = sim.simulate_image_and_rpcfit(ref_zenith_list[i], ref_azimuth_list[i], None,
                                                                         ref_sun_zenith_list[i], 
                                                                         ref_sun_azimuth_list[i], 
                                                                         overwrite=False)
    sec_image_filename, sec_rpc_filename = sim.simulate_image_and_rpcfit(sec_zenith_list[i], sec_azimuth_list[i], None,
                                                                         sec_sun_zenith_list[i], sec_sun_azimuth_list[i], 
                                                                         overwrite=False)
    
    s2p_config_filename = s2p_configurator.create_config(ref_image_filename, ref_rpc_filename, 
                                                         sec_image_filename, sec_rpc_filename, 
                                                         overwrite=False)
