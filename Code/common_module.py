#!/usr/bin/env python3

"""
Created on Thu Feb 04 10:01:09 2022
@author: Youssef Ayachi

This common module assemble the commun functions needed to generate elements of
different MetroloJ reports.
"""

import numpy as np
import pandas as pd
from PIL import Image


def get_images_from_multi_tiff2(path):
    """
    Import .tif file from a given path

    Parameters
    ----------
    path : str
        .tif file path.

    Returns
    -------
    tiff_images : list
        retrns list of np.arrays enclosed in the .tif file.

    """
    img = Image.open(path)
    tiff_images = []
    for i in range(img.n_frames):
        img.seek(i)
        tiff_images.append(np.array(img))
    return tiff_images


"""
img = get_images_from_multi_tiff2(path_cv)
Image.fromarray(img[0])
Image.fromarray((img[0] * 255).astype(np.uint8))
img[0].shape
"""


def get_images_from_multi_tiff(path):
    """
    Import .tif file from a given path and convert it to a 3d np.array where
    the first dimension represent the image index.

    Parameters
    ----------
    path : str
        .tif file path.
        the tif file must carry only 2d arrays of the same dimensions.

    Returns
    -------
    tiff_images : np.array
        3d np.array where the first dimension represent the image index.
    """

    tiff_file = Image.open(path)
    # number of images in the tiff file
    zdim = tiff_file.n_frames
    # we assume that images from same tiff file have the same size
    xdim, ydim = np.array(tiff_file).shape
    # initialization of the desired output
    tiff_final = np.zeros((zdim, xdim, ydim)).astype(int)
    # get output
    for i in range(zdim):
        tiff_file.seek(i)  # Seeks to the given frame in this sequence file.
        tiff_final[i] = np.array(tiff_file)
    return tiff_final


"""
img = get_images_from_multi_tiff2(path_cv)
img[0]
Image.fromarray((-img[0]*255).astype(np.uint8))
"""


def get_microscopy_info(
        microscope_type, wavelength, NA, sampling_rate, pinhole
        ):
    """
    Organize microscopy info provided by the user into a dataframe.

    Parameters
    ----------
    microscope_type : str

    wavelength : float
        In nm.
    NA : int or float
        Numerical aperture.
    sampling_rate : str
        In number of pixels. Ex: "1.0x1.0x1.0".
    pinhole : int or float
        In airy units.

    Returns
    -------
    microscopy_info_df : pd.DataFrame
        dataframe resuming microscopy informations.
        2 columns: Labels and Values

    """

    info_values = [microscope_type, wavelength, NA, sampling_rate, pinhole]
    info_labels = ["Microscope type",
                   "wavelength (nm)",
                   "Nmerical Aperture",
                   "Sampling rate (pixel)",
                   "pinhole (airy units)"]

    # organize result in a dataframe
    microscopy_info_dict = {}
    microscopy_info_dict["Labels"] = info_labels
    microscopy_info_dict["Values"] = info_values

    microscopy_info_table = pd.DataFrame(microscopy_info_dict)

    return microscopy_info_table


"""
ex:
get_microscopy_info("Confocal", 460.0, 1.4, "1.0x1.0x1.0", 1.0)
"""
