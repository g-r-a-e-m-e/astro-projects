# -*- coding: utf-8 -*-
"""
JWST NIRCAM .fits File Downloader
Created on Tue Dec 27 09:16:07 2022

@author: https://github.com/g-r-a-e-m-e
"""

# Boilerplate
import numpy as np
import os
from astroquery.mast import Observations

# Create observation table
obs_table = Observations.query_criteria(obs_collection = 'JWST',
                                        dataproduct_type = ['image'],
                                        calib_level = [3,4],
                                        instrument_name = ['NIRCAM'],
                                        dataRights = ['public'])

# Create list of unique targets within dataset
target_list = list(np.unique(obs_table['target_name']))

# Print target_list to console and prompt user for target input
print(f'Behold! The current JWST Target List:\n\n{target_list}')
target = input('\nEnter a target to download its .fits files: ')

# Define function to return a list of targets that meet the user's criteria
def get_specific_target(target_list, target):
    tl = target_list
    out_list = [t for t in tl if t.startswith(target)]
    return out_list

# Create specific targets list based on user input
s_targets = get_specific_target(target_list, target)

# Filter initial observation table on the list of specific targets
target_table = obs_table[obs_table['target_name'] == s_targets]

# Define function to get .fits file URLs from the observation table
def get_fits_urls(observation_table):
    ot = observation_table
    urls = []
    for i in range(len(ot)):
        url = ot[i]['dataURL']
        if url.endswith('.fits'):
            urls.append(url)
    
    return urls

# Create product URL list            
product_url_list = get_fits_urls(target_table)

# Print the length of product_url_list
# If length > 5, prompt user for confirmation to download excess files
print(f'\nThe number of urls is {len(product_url_list)}.')
override_length = 'False'
if len(product_url_list) > 5:
    override_length = input('If you would like to download excess .fits files, enter True, otherwise False: ')

# Prompt user for the directory to save the .fits files to, default is current directory    
path = input('You may specify the directory to save the .fits files. Default (blank) is the current working directory: ')
if path == '':
    path = os.chdir(os.getcwd())
else:
    path = os.chdir(path)

# Define function to download .fits files to the current working directory
def download_fits(url_list, override_length, path):
    if len(url_list) <= 5:
        for url in url_list:
            Observations.download_file(url, local_path = path)
    elif len(url_list) > 5 and override_length == 'False':
        for url in url_list[0:5]:
            Observations.download_file(url, local_path = path)
    elif len(url_list) > 5 and override_length == 'True':
        print(f'\nYou supplied a URL list of length {len(url_list)} and overrode the length limit.\
              \nThis may take some time...\n')
        for url in url_list:
            Observations.download_file(url, local_path = path)

# Download .fits files    
download_fits(product_url_list, override_length, path)