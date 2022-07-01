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

cols = ['pl_name', 'hostname', 'default_flag', 'sy_snum', 'sy_pnum', 
'discoverymethod', 'disc_year', 'disc_facility', 'soltype', 
'pl_controv_flag', 'pl_refname', 'pl_orbper', 'pl_orbpererr1', 
'pl_orbpererr2', 'pl_orbperlim', 'pl_orbsmax', 'pl_orbsmaxerr1', 
'pl_orbsmaxerr2', 'pl_orbsmaxlim', 'pl_rade', 'pl_radeerr1', 
'pl_radeerr2', 'pl_radelim', 'pl_radj', 'pl_radjerr1', 'pl_radjerr2', 
'pl_radjlim', 'pl_bmasse', 'pl_bmasseerr1', 'pl_bmasseerr2', 
'pl_bmasselim', 'pl_bmassj', 'pl_bmassjerr1', 'pl_bmassjerr2', 
'pl_bmassjlim', 'pl_bmassprov', 'pl_orbeccen', 'pl_orbeccenerr1', 
'pl_orbeccenerr2', 'pl_orbeccenlim', 'pl_insol', 'pl_insolerr1', 
'pl_insolerr2', 'pl_insollim', 'pl_eqt', 'pl_eqterr1', 'pl_eqterr2', 
'pl_eqtlim', 'ttv_flag', 'st_refname', 'st_spectype', 'st_teff', 
'st_tefferr1', 'st_tefferr2', 'st_tefflim', 'st_rad', 'st_raderr1', 
'st_raderr2', 'st_radlim', 'st_mass', 'st_masserr1', 'st_masserr2', 
'st_masslim', 'st_met', 'st_meterr1', 'st_meterr2', 'st_metlim', 
'st_metratio', 'st_logg', 'st_loggerr1', 'st_loggerr2', 'st_logglim', 
'sy_refname', 'rastr', 'ra', 'decstr', 'dec', 'sy_dist', 'sy_disterr1', 
'sy_disterr2', 'sy_vmag', 'sy_vmagerr1', 'sy_vmagerr2', 'sy_kmag', 
'sy_kmagerr1', 'sy_kmagerr2', 'sy_gaiamag', 'sy_gaiamagerr1', 
'sy_gaiamagerr2', 'rowupdate', 'pl_pubdate', 'releasedate']

col_string = ''

for i in range(len(cols)):
    if i < len(cols) - 1:
        col_string += cols[i] + ','
    else:
        col_string += cols[i]
    
col_string

# Specify output format
out_format = "&format=csv"

# Query
query = f"{base_url}SELECT+{col_string}+FROM+ps+WHERE+discoverymethod+LIKE+'%Transit%'+AND+disc_facility+LIKE+'%Kepler%'+AND+soltype+LIKE+'%Confirmed%'+AND+pl_radestr+IS+NOT+NULL+{out_format}"

# Read in the data to a pandas DataFrame
df = pd.read_csv(query, low_memory = False)

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
                   facet_col = 'spectral_class', facet_col_wrap = 3,
                   log_x = True, log_y = True,
                   height = 1200, width = 1200,
                   category_orders = {1:'O', 2:'B', 3:'A', 4:'F', 5:'G', 6:'K', 7:'M' })

st.plotly_chart(fig_1, height = 1200, width = 1200)