# -*- coding: utf-8 -*-
"""
JWST Data Release App
Created on Sun Jan  1 08:03:24 2023

@author: https://github.com/g-r-a-e-m-e
"""

# Boilerplate
import arrow
from astroquery.mast import Observations
from astropy.time import Time
import numpy as np
import pandas as pd
import streamlit as st

# Get today's date/time (UTC)
utc = arrow.utcnow().format('YYYY-MM-DD HH:mm')

# Create observation table
obs_table = Observations.query_criteria(obs_collection = 'JWST',
                                        dataproduct_type = ['image'],
                                        calib_level = [2,3,4])

# Impute ISO Date column for accessibility
obs_table['t_obs_release_iso'] = Time(obs_table['t_obs_release'], format = 'mjd').to_value('iso', subfmt = 'date_hm')

# Filter observation table for data releases on or after today
obs_table_filtered = obs_table[obs_table['t_obs_release_iso'] >= utc]

# Set next_release_date_time_iso variable
next_release_date_time_iso = arrow.get(min(obs_table_filtered['t_obs_release_iso']))

# Set release_date and release_time variables
release_date = next_release_date_time_iso.format('YYYY-MM-DD')
release_time = next_release_date_time_iso.format('HH:mm')

# Create next_observation_df to display a sample of the upcoming data
next_observation_df = obs_table_filtered[obs_table_filtered['t_obs_release_iso'] == min(obs_table_filtered['t_obs_release_iso'])].to_pandas()

# Create the list of next_targets from next_observation_df
next_targets = [next_observation_df['target_name'].unique()]

# Create target_label for streamlit app
if len(next_targets) > 1:
    target_label = ', '.join(next_targets)
else:
    target_label = ''.join(next_targets[0])

### Streamlit configuration
st.title(f'The next JWST image data are scheduled for release on {release_date} at {release_time} UTC.')
st.header(f'Target(s): {target_label}')
st.subheader('Observation Data Preview*')
st.markdown("**Observation data are generated from astroquery.mast.Observations using the following query_criteria* \
           \n- [obs_collection] = 'JWST' \
           \n- [dataproduct_type] = ['image'] \
           \n- [calib_level] = [2,3,4]")
st.dataframe(next_observation_df)