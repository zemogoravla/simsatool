"""
Basic example of the use of the Simulator.

Three images are gennerated with same view orientation and
different sun positions.

"""
#%% 
from simulator import Simulator
from satellite import Satellite
from location import Location
from blender import Blender

#%% DIRECTORIES AND FILENAMES -------------------------------
# The simulation results will be created under this directory
simulation_base_dir = 'data/SIMULATION_EXAMPLE_SUNPOS' 

# Select the 3D scene
blender_scene_filename ='data/model/city_scene.blend'

#%% VIEWS AND SUN ORIENTATION -------------------------------
# All angles are in degrees
ref_zenith_list =  [17, 17, 17]    
ref_azimuth_list = [210, 210, 210]
ref_sun_zenith_list =[21.74, 42.98, 54.23]
ref_sun_azimuth_list = [137.21, 156.32, 155.07]

#%% SETUP THE SIMULATOR  ------------------------------------
satellite = Satellite()
blender = Blender(blender_scene_filename, 
                  image_xy_size=(600,600))
location = Location()
sim = Simulator(simulation_base_dir, 
                satellite, blender, location)

#%% GENERATE THE IMAGES -------------------------------------
for i in range(len(ref_zenith_list)):
  ref_image_filename, ref_rpc_filename = \
    sim.simulate_image_and_rpcfit(ref_zenith_list[i],
                                  ref_azimuth_list[i], 
                                  None,
                                  ref_sun_zenith_list[i],
                                  ref_sun_azimuth_list[i]) 

