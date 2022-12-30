"""
Basic example of the use of the Simulator and the S2PConfigurator.

A stereo pair of images is created with the Simulator and a configuration
to run a stereo reconstruction with the S2P pipeline is created with the 
S2PConfigurator.

"""
#%% 
import os
from simulator import Simulator
from satellite import Satellite
from location import Location
from blender import Blender
from s2p_configurator import S2PConfigurator

#%% DIRECTORIES AND FILENAMES -------------------------------
# The simulation results will be created under this directory
simulation_base_dir = 'data/SIMULATION_EXAMPLE_STEREO_PAIR' 

# Select the 3D scene
blender_scene_filename ='data/model/city_scene.blend'

# Each generated image can be approximately matched in values
# and noise to a different reference image.
# Here we use a single reference image for both images of the 
# pair.
target_image_filename = 'data/images/IARPA_15DEC18140510.tif'

# The configuration to run the stereo reconstruction 
# will be created under:
# <simulation_base_dir>/S2P_CONFIGS
s2p_configs_dir = os.path.join(simulation_base_dir,    
                               'S2P_CONFIGS') 

#%% VIEWS AND SUN ORIENTATION -------------------------------
# All angles are in degrees
# Generate a pair of images [(ref)erence - (sec)ondary]
ref_zenith = 5
ref_azimuth = 0
ref_sun_zenith = 35
ref_sun_azimuth = 156
# ---------------  
sec_zenith = 25
sec_azimuth = 210
sec_sun_zenith =21
sec_sun_azimuth = 137

#%% SETUP THE SIMULATOR  ------------------------------------
satellite = Satellite()
blender = Blender(blender_scene_filename, 
                  image_xy_size=(600,600))
location = Location()
sim = Simulator(simulation_base_dir, 
                satellite, blender, location)

#%% SETUP THE S2P CONFIGURATOR  -----------------------------
s2p_configurator = S2PConfigurator(s2p_configs_dir)

#%% GENERATE THE IMAGE PAIR AND S2P CONFIGURATION -----------

ref_image_filename, ref_rpc_filename = \
        sim.simulate_image_and_rpcfit(ref_zenith, 
                                      ref_azimuth, None,
                                      ref_sun_zenith, 
                                      ref_sun_azimuth,
                                      target_image_filename)
   
sec_image_filename, sec_rpc_filename = \
        sim.simulate_image_and_rpcfit(sec_zenith, 
                                      sec_azimuth, None,
                                      sec_sun_zenith, 
                                      sec_sun_azimuth,
                                      target_image_filename)

s2p_config_filename = \
        s2p_configurator.create_config(ref_image_filename, 
                                       ref_rpc_filename, 
                                       sec_image_filename, 
                                       sec_rpc_filename)   

