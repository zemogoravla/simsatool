import os

import numpy as np
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from skimage.exposure import match_histograms

import ponomarenko

def match_image_values_and_noise(img, ref_img, ponomarenko_num_bins=10):
    """Adapts img to match image values frecquencies and the noise of ref_img
       by histogram matching and Ponomarenko noise estimation

       Noise adaptation is only approximate. Noise estimated on the output image 
       is similar or greater than the noise estimated in the reference image. 

    Args:
        img (np.array): Source image
        ref_img (np.array): Reference image
        ponomarenko_num_bins (int, optional): Number of bins to estimate the noise. Defaults to 10.

    Returns:
        np.array: Matched image
    """

    # Match histograms of the image and the reference image
    matched_img = match_histograms(img, ref_img)

    # Noise estimation with Ponomarenko algorithm
    ref_pono_bins, ref_pono_noise_std = ponomarenko.estimate_noise(ref_img, num_bins=ponomarenko_num_bins)

    # Noise sigma per pixel value in reference image 
    idxs_r = get_closest_indices(ref_pono_bins, matched_img.ravel())
    ref_img_noise_sigma = np.reshape(ref_pono_noise_std[idxs_r], matched_img.shape)

    # matched noise
    matched_noise = np.random.normal(0,1,img.shape) * ref_img_noise_sigma

    output_img = matched_img + matched_noise
    
    return output_img

def match_image_values_and_noise_ex(img_filename, ref_img_filename, output_filename, ponomarenko_num_bins=10):
    """ Version of "match_image_values_and_noise" with images read and written to disk

    Args:
        img_filename (str): Source image filename
        ref_img_filename (str): Reference image filename
        output_filename (str): Matched image filename
        ponomarenko_num_bins (int, optional): Number of bins to estimate the noise. Defaults to 10.
    """
    img = imread(img_filename)
    ref_img = imread(ref_img_filename)
    
    matched_img = match_image_values_and_noise(img, ref_img, ponomarenko_num_bins)

    imsave(output_filename, matched_img)



# Auxiliary function------------------------------------
def get_closest_indices(array, values):
    """Searchs in array the values and returns the indices where the respective 
       closest values are found.
       Adapted from:
       https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
       
    Args:
        array (array or list): Array where the values are searched
        values (array or list): Values to be searched

    Returns:
        array: Indices of the closest values
    """
    #

    # make sure array is a numpy array
    array = np.array(array)

    # get insert positions
    idxs = np.searchsorted(array, values, side="left")
    
    # find indexes where previous index is closer
    prev_idx_is_less = ((idxs == len(array))|(np.fabs(values - array[np.maximum(idxs-1, 0)]) < np.fabs(values - array[np.minimum(idxs, len(array)-1)])))
    idxs[prev_idx_is_less] -= 1
    
    return idxs