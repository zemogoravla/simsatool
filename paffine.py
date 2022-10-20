
import os
import numpy as np


import sys






def camera_rotation_matrix_from_view_angles(zenith_in_degrees, 
                                            azimuth_in_degrees, 
                                            roll_in_degrees=None):
    '''
    Camera_rotation_matrix_from_view_angles
    

    Parameters
    ----------
    zenith_in_degrees : float in [0,90)
        Angle between the viewing direction and the vertical.
    azimuth_in_degrees : float in [0,360)
        Angle from the north direction to the view direction projected
        to the horizontal plane
    roll_in_degrees : float or None
        Angle of rotation around the viewing direction axis where zero is with
        the camera facing up

    Raises
    ------
    ValueError if a roll angle is passed
        roll rotation is not implemented yet.

    Returns
    -------
    R : 3x3 np.array
        Camera matrix.

    '''

    z = np.deg2rad(zenith_in_degrees)
    a = np.deg2rad(azimuth_in_degrees)
    projection_direction = [np.sin(a)*np.sin(z), np.cos(a)*np.sin(z), np.cos(z)]
    projection_direction /= np.linalg.norm(projection_direction)
    
    # intialize R array
    R = np.eye(3, dtype=np.double)
    
    # The third row of R is the axis of the camera in the world reference
    # the axis points to the scene, opposite to the projection direction
    R[2,:] = - projection_direction 
    

    #TODO  Implement the roll angle    
    if roll_in_degrees is None:
        # select two axis orthogonal to  R[2,:]
        if np.abs(R[2,0]) > np.abs(R[2,1]):
            R[1,:] = [R[2,2], 0, -R[2,0]]
        else:
            R[1,:] = [0, R[2,2], -R[2,1]]
        
        R[1,:] /= np.linalg.norm(R[1,:])    
        
        R[0,:] = np.cross(R[1,:], R[2,:])
    else:
        raise ValueError('roll angle not implemented!!')    
    
    return R












def compute_P_affine(zenith_in_degrees, 
                     azimuth_in_degrees,
                     roll_in_degrees,
                     image_xy_size,
                     pixels_per_meter,
                     ):
    '''
    Computes an affine matrix and the decomposition from the position angles and image size and resolution

    Parameters
    ----------
    zenith_in_degrees : float in [0,90)
        Angle between the viewing direction and the vertical.
    azimuth_in_degrees : float in [0,360)
        Angle from the north direction to the view direction projected
        to the horizontal plane
    roll_in_degrees : float or None
        NOT IMPLEMENTED YET 
        Angle of rotation around the viewing direction axis where zero is with
        the camera facing up
    image_xy_size : (int,int)
        Width and height of image in pixels.
    pixels_per_meter : float
        Resolution in pixels per meter.
    

    Returns
    -------
    P_affine : 2x4 np.array
        Affine projection matrix
    K : 2x2 np.array
        Intrinsic matrix
    R : 2x3 np.array
        Extrinsic rotation
    t : 2x1 np.array
        Translation

    P_affine = [KR|t]
    '''
       
    if not roll_in_degrees is None:
        raise ValueError('Roll angle not implemented')
        
    R = camera_rotation_matrix_from_view_angles(zenith_in_degrees, 
                                                azimuth_in_degrees,
                                                roll_in_degrees)
    
    K = np.array([[pixels_per_meter, 0],[0, pixels_per_meter]])
    
    KR = K @ R[:2,:]
    P_affine = np.zeros((2,4))
    P_affine[:,:3] = KR
    P_affine[:,3] = np.array([image_xy_size[0], image_xy_size[1]])/2
    t = P_affine[:,3]
    
    return P_affine, K, R, t
    

