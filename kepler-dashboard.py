# -*- coding: utf-8 -*-
"""
Kepler Exoplanet Dashboard

Created on Thu Jun 30 12:19:15 2022

@author: g-r-a-e-m-e
"""

# Import necessary packages
import astroquery
import astropy
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# The following set the base URL to the NASA exoplanet archive, set the query to
# run against the Planetary Systems table, and format the output as .csv to be 
# read in by pandas.

# NASA Exoplanet archive url
base_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

# Table query
table_query = "SELECT+*+FROM+ps+WHERE+discoverymethod+LIKE+'%Transit%'+AND+disc_facility+LIKE+'%Kepler%'+AND+soltype+LIKE+'%Confirmed%'+AND+pl_radestr+IS+NOT+NULL+"

# Specify output format
out_format = "&format=csv"

# Concatenate base_url, table_query, and out_format 
import_url = base_url + table_query + out_format

# Read in the data to a pandas DataFrame
df = pd.read_csv(import_url, low_memory = False)

# The following functions will create columns which will allow us to categorize 
# the data in our dashboard. This will allow the user to "slice and dice" the
# data in order to explore it.

# Simple stellar classification function
def get_spectral_type(temperature):
    t = temperature
    
    if t >= 3.0e5:
        sc = 'O'
    elif t < 3.0e5 and t >= 10.0e4:
        sc = 'B'
    elif t < 10.0e4 and t >= 7.5e3:
        sc = 'A'
    elif t < 7.5e3 and t >= 6.0e3:
        sc = 'F'
    elif t < 6.0e3 and t >= 5.2e3:
        sc = 'G'
    elif t < 5.2e3 and t >= 3.7e3:
        sc = 'K'
    elif t < 3.7e3 and t >= 2.4e3:
        sc = 'M'
    else:
        sc = 'C'
    
    return sc

# Assign color based on spectral class. Colors based off of 
# https://simple.wikipedia.org/wiki/Stellar_classification
def set_color(spectral_class):
    sc = spectral_class
    
    if sc == 'O':
        clr = '#9db4ff'
    elif sc == 'B':
        clr = '#aabfff'
    elif sc == 'A':
        clr = '#aabfff'
    elif sc == 'F':
        clr = '#f8f7ff'
    elif sc == 'G':
        clr = '#fff4ea'
    elif sc == 'K':
        clr = '#FFEECC'
    elif sc == 'M':
        clr = '#ffd2a1'
    else:
        clr = '#FFBBAA'
    
    return clr

# Get the spectral class
df['spectral_class'] = df['st_teff'].apply(lambda x: get_spectral_type(x))

# Map the color of the host star
df['color_map'] = df['spectral_class'].apply(lambda x: set_color(x))

discovery_years = df['disc_year'].sort_values().unique()

spectral_class = df['spectral_class'].unique()

# The following begins to build the streamlit application

st.sidebar.title('Kepler Exoplanets')
year_in = st.sidebar.select_slider('Discovery Year', discovery_years)
#spectral_class_in = st.sidebar.radio('Spectral Class', ['O', 'B', 'A', 'F', 'G', 'K', 'M', 'C'])

fig_1 = px.scatter(data_frame = df.loc[df['disc_year'] <= year_in], 
                   x = 'pl_bmasse', y = 'pl_rade',
                   size = 'pl_rade',
                   facet_row = 'spectral_class',
                   log_x = True, log_y = True,
                   height = 1200)

st.plotly_chart(fig_1, height = 1200)