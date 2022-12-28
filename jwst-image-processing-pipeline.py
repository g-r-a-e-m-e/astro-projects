# -*- coding: utf-8 -*-
"""
JWST Image Processing Pipeline
Created on Wed Dec 28 09:07:04 2022

@author: https://github.com/g-r-a-e-m-e
"""

from astropy.io import fits
import numpy as np
import os
#import matplotlib as mpl
import matplotlib.pyplot as plt
#from matplotlib.colors import ListedColormap

# Specify the directory where the .fits files are located
path = input('Enter the path to the directory where the .fits files are located: ')
path = os.chdir(path)

# Create a list of filenames
files = os.listdir(path)

fits_files = [f for f in files if f.endswith('.fits')]

### Developing color mapping
# Derived from https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-instrumentation/nircam-pupil-and-filter-wheels
# Figure 1. NIRCam pupil and filter wheels.
# Used https://color.adobe.com/ to analyze the colors of each filter wheel
# to determine the hex RGB color for plotting.
# filter_wheel_color_dict = {'F070W' : '#CBBAE4',
#                            'F090W' : '#BCB9EA',
#                            'F115W' : '#B8B9F3',
#                            'F150W' : '#C1DEF5',
#                            'F200W' : '#BAE5E2',
#                            'F212N' : '#6DCCBB',
#                            'F187N' : '#6FCAD1',
#                            'F210M' : '#6DCCBD',
#                            'F182M' : '#6FCBD7',
#                            'F140M' : '#6DAEE9',
#                            'F150W2' : '#E4F1FA'}

# filter_wheel_color_list = list(filter_wheel_color_dict.values())
# my_cmap = ListedColormap(filter_wheel_color_list, name = 'JWST')
# mpl.colormaps.register(cmap = my_cmap)

# Define function to iterate through each .fits file and extract the data
def get_fits_data(fits_file):
    hdul = fits.open(fits_file)
    data = hdul[1].data
    hdul.close()
    return data

# Get the data from each .fits file
fits_data = [get_fits_data(f) for f in fits_files]

# Determine the unique shapes of each .fits file for stacking
shapes = [d.shape for d in fits_data]
fits_shapes = list(set(shapes))     

# Define function to stack the .fits data and plot it using matplotlib
def stack_fits(fits_data, shape, cmap):
    stack_data = []
    for d in fits_data:
        if d.shape == shape:
            stack_data.append(d)
            
    final_image = np.sum(stack_data, axis = 0)
    plt.figure()
    plt.imshow(final_image, cmap = cmap)
    plt.colorbar()

# Stack the images associated with each shape and display them
for s in fits_shapes:
    stack_fits(fits_data, s, 'inferno')