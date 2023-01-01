#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWST Data Release "Bot"
Created on Sun Jan  1 08:03:24 2023

@author: https://github.com/g-r-a-e-m-e
"""

# Boilerplate
import arrow
from astroquery.mast import Observations
from astropy.time import Time

# Get today's date/time (UTC)
utc = arrow.utcnow().format('YYYY-MM-DD HH:mm')

# Create observation table
obs_table = Observations.query_criteria(obs_collection = 'JWST',
                                        dataproduct_type = ['image'],
                                        calib_level = [3,4])

# Impute ISO Date column for accessibility
obs_table['t_obs_release_iso'] = Time(obs_table['t_obs_release'], format = 'mjd').to_value('iso', subfmt = 'date_hm')

# Filter observation table for data releases on or after today
obs_table_filtered = obs_table[obs_table['t_obs_release_iso'] >= utc]

# Set next_release_date_iso variable
next_release_date_iso = min(obs_table_filtered['t_obs_release_iso'])

# Define countdown function to count down the time until the next data release
#def countdown(start, end):
    
