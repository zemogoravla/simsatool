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


#%% DIRECTORIES AND FILENAMES --------------------------------------

# The simulation results will be created under this 
# directory
simulation_base_dir = 'data/SIMULATION_EXAMPLE_1' 

# The configuration to run the stereo reconstruction will be created 
# under "<simulation_base_dir>/S2P_CONFIGS"
s2p_configs_dir = os.path.join(simulation_base_dir, 'S2P_CONFIGS') 

# The generated images will be views of the 3D scene (choose a scene)  
#blender_scene_filename ='data/model/cylinder_scene.blend'
blender_scene_filename ='data/model/city_scene.blend'

# Each generated image can be approximately matched in values and noise 
# to a target image (choose an image or set to None)
#target_image = None
target_image_filename = 'data/images/IARPA_15DEC18140510.tif'

#%% VIEWS AND SUN ORIENTATION ---------------------------------------

# Generate pairs of images [(ref)erence - (sec)ondary]
# The reference image is an almost nadir view (zenith angle of 5º, elevation=85º) 
# looking from the north (azimuth angle 0º). The sun is from the north-east (southern hemisphere sun)
# with an elevation of 55º (zenith angle of 35º) 
ref_zenith_list = [5]
ref_azimuth_list = [0]
ref_sun_zenith_list = [35]
ref_sun_azimuth_list = [40]
# The secondary image is a view from the south-west (azimuth angle of 210º) and a zenith angle of 25º  
sec_zenith_list = [25] 
sec_azimuth_list = [210] 
sec_sun_zenith_list =[40]
sec_sun_azimuth_list = [60]

#%% SETUP THE SIMULATOR AND S2PCONFIGURATOR -------------------------
# Initialize the simulator
satellite = Satellite()
blender = Blender(blender_scene_filename, image_xy_size=(600,600))
location = Location() #Location(lon_lat_alt_origin=[-58.5881805419922, -34.4899978637695,0])
sim = Simulator(simulation_base_dir, satellite, blender, location)

# Initialize the S2P configurator
s2p_configurator = S2PConfigurator(s2p_configs_dir)


#%% GENERATE THE IMAGE PAIR AND S2P CONFIGURATION------------------------
# Generate the pair and the configuration to run the stereo reconstruction 
for i in range(len(ref_zenith_list)):
    ref_image_filename, ref_rpc_filename = sim.simulate_image_and_rpcfit(ref_zenith_list[i], ref_azimuth_list[i], None,
                                                                         ref_sun_zenith_list[i], 
                                                                         ref_sun_azimuth_list[i], 
                                                                         overwrite=False,
                                                                         target_img_filename = target_image_filename)
    sec_image_filename, sec_rpc_filename = sim.simulate_image_and_rpcfit(sec_zenith_list[i], sec_azimuth_list[i], None,
                                                                         sec_sun_zenith_list[i], sec_sun_azimuth_list[i], 
                                                                         overwrite=False,
                                                                         target_img_filename = target_image_filename)
    
    s2p_config_filename = s2p_configurator.create_config(ref_image_filename, ref_rpc_filename, 
                                                         sec_image_filename, sec_rpc_filename, 
                                                         overwrite=False)

