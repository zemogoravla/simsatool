#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paffine
from satellite import Satellite
from blender import Blender
from location import Location
import paffine
import rpcfit_util

import copy
import subprocess
import shutil
from util import save_txt

import pickle

class Simulator():
      
    def __init__(self, base_dir:str, 
                 satellite:Satellite=None, 
                 blender:Blender=None,
                 location:Location=None):
        """ Construction
            Simulator(base_dir)   for an existing sim
            Simulator(base_dir, satellite, blender, location)   for a new sim

        Args:
            base_dir (str): Base directory for the simulation
            satellite (Satellite, optional): Satellite instance. Defaults to None.
            blender (Blender, optional): Blender instance. Defaults to None.
            location (Location, optional): Location instance. Defaults to None.

        Raises:
            ValueError: if trying to overwrite an existing sim or trying to read an unexisting sim
        """

        self.base_dir = base_dir
        self.satellite = satellite
        self.blender = blender
        self.location = location
        
        self.init_directorynames_and_filenames()
        
        if os.path.exists(self.base_dir):
            print('Simulator: base directory exists! Loading configuration...')
            if os.path.exists(self.config_dir):
                sim = self.deserialize(self.simulator_config_filename)
                self.satellite = sim.satellite
                self.blender = sim.blender
                self.location = sim.location
                #self.load_configuration()
            else:
                raise ValueError('Simulator: base directory exists but is NOT VALID!')
        else:
            if self.satellite is None or self.blender is None:
                print('Simulator: base directory does not exist. Satellite and or Blender NOT VALID')
                exit(2)
            else:
                self.init_directories()

                # save blender model in the simulation tree
                shutil.copy(blender.scene_filename,  self.blender_model_dir)
                # update the blender scene filename
                blender.scene_filename = os.path.join(self.blender_model_dir, os.path.basename(blender.scene_filename))
                
                self.serialize()
                #self.save_configuration()

          
        
    def init_directorynames_and_filenames(self):
        self.config_dir = os.path.join(self.base_dir,'SIMULATION_CONFIG')
        self.images_dir = os.path.join(self.base_dir,'IMAGES')
        self.blender_camera_dir = os.path.join(self.base_dir,'BLENDER_CAMERA')
        self.blender_command_dir = os.path.join(self.base_dir,'BLENDER_COMMAND')
        self.blender_model_dir = os.path.join(self.base_dir,'BLENDER_MODEL')
        self.rpcfit_dir = os.path.join(self.base_dir,'RPCFIT')
        
        self.simulator_config_filename = os.path.join(self.config_dir,'simulator_config.pkl')

       
    def init_directories(self):
        os.makedirs(self.config_dir)
        os.makedirs(self.images_dir)
        os.makedirs(self.blender_camera_dir)
        os.makedirs(self.blender_command_dir)
        os.makedirs(self.blender_model_dir)
        os.makedirs(self.rpcfit_dir)
        
    
    
    
    def serialize(self):
        """Save the simulator as a pickle
        """
        with open(self.simulator_config_filename ,'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def deserialize(pickle_filename):
        """Load a simulator from a pickle

        Args:
            pickle_filename (str): Pickle filename

        Raises:
            ValueError: if the pickle does not have a Simulator instance

        Returns:
            Simulator: the retrieved sim
        """
        with open(pickle_filename, 'rb') as f:
            sim = pickle.load(f)
            if not isinstance(sim, Simulator):
                raise ValueError('Simulator.deserialize: NOT A VALID SIMULATOR PICKLE')
        return sim
        
    
    def simulate_image_and_rpcfit(self, zenith_in_degrees, azimuth_in_degrees, roll_in_degrees=None, 
                                  sun_zenith_in_degrees=0, sun_azimuth_in_degrees=0,
                                  overwrite=False,
                                  ):
        """Generates an image and an RPC file for the view defined by (zenith, azimuth, and roll angles)
        and the sun position defined by (zenith and azimuth)

        Args:
            zenith_in_degrees (double): Zenith angle of the view
            azimuth_in_degrees (double): Azimuth angle of the view
            roll_in_degrees (double, optional): Reserved for future use, not implemented yet. Defaults to None.
            sun_zenith_in_degrees (double, optional): Zenith angle of the sun. Defaults to 0.
            sun_azimuth_in_degrees (double, optional): Azimuth angle of the sun. Defaults to 0.
            overwrite (bool, optional): _description_. Defaults to False.

        Returns:
            str: Filename of the image
            str: Filename of the RPC
        """
        
        # Filenames ---------------------------------------------------------------
        view_and_sun_name = f'view_ze_{zenith_in_degrees:05.1f}_view_az_{azimuth_in_degrees:05.1f}_sun_ze_{sun_zenith_in_degrees:05.1f}_sun_az_{sun_azimuth_in_degrees:05.1f}'
        view_name = f'view_ze_{zenith_in_degrees:05.1f}_view_az_{azimuth_in_degrees:05.1f}' 
        # (a) the filename that will output the blender rendering
        image_filename = os.path.join(self.images_dir, f'{view_and_sun_name}_0001.tif')
        # (b) the filename we will tell to blender in order to finally get (a) 
        image_filename_for_blender = image_filename[:-8] 
        # (c) the filename of the python camera script for blender
        blender_camera_script_filename = os.path.join(self.blender_camera_dir, f'blender_camera_{view_and_sun_name}.py')
        # (d) the filename of the shell script that will run Blender
        blender_command_filename = os.path.join(self.blender_command_dir, f'blender_command_{view_and_sun_name}.sh')
        # (e) the filename for the rpc model
        rpcfit_filename = os.path.join(self.rpcfit_dir, f'rpcfit_{view_name}.txt')
        
        
        # Create the image and the rpc---------------------------------------------
        if (not os.path.isfile(image_filename) or not os.path.isfile(rpcfit_filename)) or overwrite:
            
            # Compute affine projection matrix from orientation
            P_affine, K, R, t = \
            paffine.compute_P_affine(zenith_in_degrees, azimuth_in_degrees, roll_in_degrees, self.blender.image_xy_size,
                                    self.satellite.view_pixels_per_meter(zenith_in_degrees))
            
            # Conpute the rpc from the affine projection matrix. Saves result in Ikonos format
            rpcfit_util.compute_rpc_from_affine_camera(P_affine, self.location.aoi, self.location.altitude_range, 
                                                       rpcfit_filename, lon_lat_alt_origin=self.location.lon_lat_alt_origin)
            
            # sun rotation from sun_zenith, sun_azimuth
            R_sun = paffine.camera_rotation_matrix_from_view_angles(sun_zenith_in_degrees, sun_azimuth_in_degrees)
            
            # Get the blender_camera_script
            blender_camera_script = self.blender.get_blender_camera_position_script(R, K, R_sun)
            
            # Get the blender command. 
            blender_command = self.blender.get_blender_command(blender_camera_script_filename, image_filename_for_blender)
            
            #save scripts
            save_txt(blender_camera_script_filename, blender_camera_script)
            save_txt(blender_command_filename, blender_command)
            
            # run Blender
            subprocess.call(blender_command, shell=True)

        return image_filename, rpcfit_filename
    