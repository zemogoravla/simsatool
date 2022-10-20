import numpy as np
from scipy.spatial.transform import Rotation
import json


class Blender():
    """Blender manager
    """
    def __init__(self, scene_filename, image_xy_size):
        self.scene_filename = scene_filename
        self.image_xy_size = image_xy_size

        self.image_settings_file_format = 'TIFF'
        self.image_settings_color_mode = 'BW'
        self.image_settings_color_depth = '16'
        


    def __str__(self):
        s = 'Blender\n'
        s+= f'Scene filename: {self.scene_filename}\n'
        s+= f'Image xy size: {self.image_xy_size}\n'
        s+= f'Image file format: {self.image_settings_file_format}\n'
        s+= f'Image color mode: {self.image_settings_color_mode}\n'
        s+= f'Image color depth: {self.image_settings_color_depth}'
        return(s)
    
    

    
    def get_blender_camera_position_script(self, R, K, R_sun=None):
        """Python script to position the camera and the sun in the Blender scene

        Args:
            R (3x3 or 2x3 np.array): Extrinsics of the camera
            K (): Intrinsics of the camera
            R_sun (3x3 or 2x3 np.array, optional): Sun rotation matrix. Defaults to None.
                                                   If None sun is placed at nadir.     

        Returns:
            str: script
        """
        
        L = np.min(self.image_xy_size)
        
        if R.shape[0]==2:
            R_last_row =  np.cross(R[0,:], R[1,:] )
            R_3x3 = np.vstack((R,R_last_row))
        else:
            R_3x3 = R
    
        # invert y and z axes for Blender
        R_3x3[1,:] *= -1
        R_3x3[2,:] *= -1
    
        r = Rotation.from_matrix(R_3x3.T)
        quat = r.as_quat()
        #print(r.as_quat())
        #print(r.as_rotvec())
    
    
        #  GENERATE THE SCRIPT
        # blender uses quaternion w,x,y,z
        # scipy.spatial.transform uses quaternion x,y,z,w
        script = 'import bpy';
        script += '\n'
        
        script += 'cam = bpy.data.objects["Camera"]';
        script += '\n'
        script += 'cam.data.type = "ORTHO"';
        script += '\n'
        
        # ROTATION
        script += 'cam.rotation_mode = "QUATERNION"';
        script += '\n'
        for i in range(4): 
            blender_order = [3,0,1,2]  #blender uses quaternion w,x,y,z;  scipy.spatial.transform uses quaternion x,y,z,w
            j = blender_order[i]
            script += 'cam.rotation_quaternion[{}] = {}'.format(i,quat[j])
            script += '\n'
            #print('cam.rotation_quaternion[{}] = {}'.format(i,quat[j]))
        
        # TRASLATION
        # (corresponds to the direction of projection, the 3rd row of R)
        # traslation_scale is just to see the camera above the scene
        traslation_scale = 200
        for i in range(3):
            script += 'cam.location[{}] = {}'.format(i, R_3x3[2,i] * traslation_scale)
            script += '\n'
            #print('cam.location[{}] = {}'.format(i, R_3x3[2,i] * traslation_scale)) 
                    
        #ORTHO SCALE
        script += 'cam.data.ortho_scale = {}'.format( L / ((K[0,0]+K[1,1])/2) )  
        script += '\n'
    
        #OUTPUT
        script += 'bpy.context.scene.render.resolution_x = {}'.format(self.image_xy_size[0])
        script += '\n'
        script += 'bpy.context.scene.render.resolution_y = {}'.format(self.image_xy_size[1]) 
        script += '\n'
        script += f'bpy.context.scene.render.image_settings.file_format = "{self.image_settings_file_format}"'
        script += '\n'
        script += f'bpy.context.scene.render.image_settings.color_mode = "{self.image_settings_color_mode}"'
        script += '\n'
        script += f'bpy.context.scene.render.image_settings.color_depth = "{self.image_settings_color_depth}"'

        #---------------------------------------------------------------------------
        # SUN rotation --------------------------------


        if R_sun is None:   
            return script

        
        if R_sun.shape[0]==2:
            R_last_row =  np.cross(R_sun[0,:], R_sun[1,:] )
            R_3x3 = np.vstack((R_sun,R_last_row))
        else:
            R_3x3 = R_sun

        # dar vuelta los ejes y y z para blender
        R_3x3[1,:] *= -1
        R_3x3[2,:] *= -1

        r = Rotation.from_matrix(R_3x3.T)
        quat = r.as_quat()

        #print(r.as_quat())
        #print(r.as_rotvec())
        
        # blender uses quaternion w,x,y,z
        # scipy.spatial.transform uses quaternion x,y,z,w
        script += '\n'
        script += '#-----------------------------';
        script += '\n'
        
        script += 'sun = bpy.data.objects["Light"]';
        script += '\n'
        
        # ROTACION
        script += 'sun.rotation_mode = "QUATERNION"';
        script += '\n'
        for i in range(4): 
            blender_order = [3,0,1,2]  #
            j = blender_order[i]
            script += 'sun.rotation_quaternion[{}] = {}'.format(i,quat[j])
            script += '\n'
            #print('cam.rotation_quaternion[{}] = {}'.format(i,quat[j]))


        return script
    
    
    def get_blender_command(self, blender_python_script_filename, blender_render_filename):
        """Command to execute Blender and generate the rendered image

        Args:
            blender_python_script_filename (str): filename of the python script to setup the camera and sun
            blender_render_filename (str): filename for the image to be rendered

        Returns:
            str: command to run Blender and do the job
        """
        command = 'blender -b ' + self.scene_filename + ' '          # execute in backgroud
        command += '-P ' + blender_python_script_filename + ' '      # run the python script
        command += '-o ' + blender_render_filename + ' '             # output filename with no extension
        command += '-f 1 '                                           # render frame
        
        return command

