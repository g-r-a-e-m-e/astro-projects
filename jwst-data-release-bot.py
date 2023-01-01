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
import numpy as np
import os

# Get today's date/time (UTC)
utc = arrow.utcnow().format('YYYY-MM-DD HH:mm')

# Create observation table
obs_table = Observations.query_criteria(obs_collection = 'JWST',
                                        dataproduct_type = ['image'],
                                        calib_level = [3,4])

# Impute ISO Date column for accessibility
obs_table['t_obs_release_iso'] = Time(obs_table['t_obs_release'], format = 'mjd').to_value('iso', subfmt = 'date_hm')
# target_release_dates_mjd = [d for d in obs_table['t_obs_release']]
# target_release_dates_iso = [Time(d, format = 'mjd').to_value('iso', subfmt = 'date_hm') for d in target_release_dates_mjd]



