# -*- coding: utf-8 -*-
"""
Exoplanet Dashboard

Created on Thu Jun 30 12:19:15 2022

@author: g-r-a-e-m-e
"""

# Import necessary packages
import numpy as np
import pandas as pd
import altair as alt
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

# Specify output format
out_format = "&format=csv"

# Query
query = f"{base_url}SELECT+{col_string}+FROM+ps+WHERE+soltype+LIKE+'%Confirmed%'+AND+pl_bmasse+IS+NOT+NULL+AND+pl_rade+IS+NOT+NULL+AND+st_rad+IS+NOT+NULL+AND+st_mass+IS+NOT+NULL+AND+st_teff+IS+NOT+NULL+{out_format}"

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
        clr = '#cad8ff'
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

# Assign simple color based on spectral class.
def set_simple_color(spectral_class):
    if sc == 'O':
        clr = 'blue'
    elif sc == 'B':
        clr = 'cyan'
    elif sc == 'A':
        clr = 'lightblue'
    elif sc == 'F':
        clr = 'white'
    elif sc == 'G':
        clr = 'yellow'
    elif sc == 'K':
        clr = 'orange'
    elif sc == 'M':
        clr = 'orangered'
    else:
        clr = 'darkred'
    
    return clr

# Set the spectral class
df['spectral_class'] = df['st_teff'].apply(lambda x: get_spectral_type(x))

# Get the unique spectral classes
spectral_classes = df['spectral_class'].unique()

# Set the color dictionary based on the color of the host star
color_dict = {}
for sc in spectral_classes:
    color_dict.update({sc : set_color(sc)})

# Set the simple color dictionary based on the color of the host star
simple_color_dict = {}
for sc in spectral_classes:
    simple_color_dict.update({sc : set_simple_color(sc)})

# The following begins to build the streamlit application

# Set the sidebar title
st.title('Exploring Exoplanets')

# Get the list of discovery years for the year_in slider
discovery_years = df['disc_year'].sort_values().unique()

# Create year_in slider to allow user to select time period of discovery
year_in = st.slider(label = 'Discovery Year', 
                    min_value = int(min(discovery_years)), 
                    max_value = int(max(discovery_years)),
                    value = [int(min(discovery_years)), int(max(discovery_years))])

# Create discovery method multiselect to allow user to select the discovery method
disc_method_in = st.multiselect(label = 'Discovery Method',
                                        options = df['discoverymethod'].sort_values().unique())

# Create facility multiselect to allow user to select the discovery facility
facility_in = st.multiselect(label = 'Discovery Facility', 
                             options = df['disc_facility'].sort_values().unique())

if ((facility_in == []) & (disc_method_in == [])):
    filtered_df =  df[(df['disc_year'] >= year_in[0]) & (df['disc_year'] <= year_in[1])]
elif ((facility_in != []) & (disc_method_in == [])):
    filtered_df = df[(df['disc_year'] >= year_in[0]) & (df['disc_year'] <= year_in[1]) & (df['disc_facility'].isin(facility_in))]
elif ((facility_in == []) & (disc_method_in != [])):
    filtered_df = df[(df['disc_year'] >= year_in[0]) & (df['disc_year'] <= year_in[1]) & (df['discoverymethod'].isin(disc_method_in))]
else:
    filtered_df = df[(df['disc_year'] >= year_in[0]) & (df['disc_year'] <= year_in[1]) & (df['disc_facility'].isin(facility_in)) & (df['discoverymethod'].isin(disc_method_in))]


# Create container 1
c1 = st.container()

with c1:
    # Display the number of exoplanets discovered since the user's slider selection
    st.subheader(f'Number of exoplanets discovered between {year_in[0]} and {year_in[1]}*:')
    st.caption('*with measured stellar and planetary masses and radii')
    st.metric(label = 'Count', value = len(filtered_df))

# Create figure 1, scatterplot of stellar radius vs. stellar mass, in
# Sol radii and Sol masses
fig_1 = px.scatter(data_frame = filtered_df,
                   x = 'st_mass', y = 'st_rad',
                   log_x = True, log_y = True,
                   color = 'spectral_class', color_discrete_map = simple_color_dict,
                   size = 'st_rad',
                   labels = {'st_mass' : 'Stellar Mass (Sol Masses)',
                             'st_rad' : 'Stellar Radius (Sol Radii)',
                             'spectral_class' : 'Host Star Spectral Class'},
                   category_orders = {'spectral_class' : ['A', 'F', 'G', 'K', 'M']},
                   render_mode = 'auto')

fig_1.update_layout(plot_bgcolor = 'black',
                    legend_orientation = 'h',
                    legend_y = -.25,
                    legend_itemclick = 'toggleothers')

fig_1.update_xaxes(gridcolor = 'grey')
fig_1.update_yaxes(gridcolor = 'grey')

# Create figure 2, scatterplot of planetary radius vs. planetary mass, in
# Earth radii and Earth masses
fig_2 = px.scatter(data_frame = filtered_df,
                   x = 'pl_bmasse', y = 'pl_rade',
                   log_x = True, log_y = True,
                   color = 'pl_rade', color_continuous_scale = 'jet',
                   size = 'pl_rade',
                   labels = {'pl_bmasse' : 'Planetary Mass (Earth Masses)',
                             'pl_rade' : 'Planetary Radius (Earth Radii)'},
                   render_mode = 'auto')

fig_2.update_coloraxes(colorbar_orientation = 'h',
                       colorbar_title_side = 'top')

fig_2.update_layout(plot_bgcolor = 'black')

fig_2.update_xaxes(gridcolor = 'grey')
fig_2.update_yaxes(gridcolor = 'grey')

# Create container 2
c2 = st.container()

with c2:
    st.header("Stellar and Planetary Radii vs. Mass")
    st.plotly_chart(fig_1, use_container_width = True)
    st.plotly_chart(fig_2, use_container_width = True)
    

# Create figure 3, boxplot of stellar mass distributions
fig_3 = px.box(data_frame = filtered_df,
               x = 'spectral_class', y = 'st_mass',
               log_y = True,
               color = 'spectral_class', color_discrete_map = simple_color_dict,
               labels = {'spectral_class': 'Spectral Class',
                         'st_mass' : 'Stellar Mass (Sol Masses)'},
               category_orders = {'spectral_class' : ['A', 'F', 'G', 'K', 'M']})

fig_3.update_layout(plot_bgcolor = 'black',
                    legend_orientation = 'h',
                    legend_y = -.25,
                    legend_itemclick = 'toggleothers')

fig_3.update_xaxes(gridcolor = 'grey')
fig_3.update_yaxes(gridcolor = 'grey')

# Create figure 4, boxplot of planetary mass distributions
fig_4 = px.box(data_frame = filtered_df,
               x = 'spectral_class', y = 'pl_bmasse',
               log_y = True,
               color = 'spectral_class', color_discrete_map = simple_color_dict,
               labels = {'spectral_class': 'Spectral Class of Host Star',
                         'pl_bmasse' : 'Planetary Mass (Earth Masses)'},
               category_orders = {'spectral_class' : ['A', 'F', 'G', 'K', 'M']})

fig_4.update_layout(plot_bgcolor = 'black',
                    legend_orientation = 'h',
                    legend_y = -.25,
                    legend_itemclick = 'toggleothers')

fig_4.update_xaxes(gridcolor = 'grey')
fig_4.update_yaxes(gridcolor = 'grey')

# Create container 3
c3 = st.container()
with c3:
    st.header("Stellar and Planetary Mass Distributions")
    st.plotly_chart(fig_3, use_container_width = True)
    st.plotly_chart(fig_4, use_container_width = True)
    
# Create figure 5, 3d scatterplot of stellar position
fig_5 = px.scatter_3d(data_frame = filtered_df,
                      x = 'ra', y = 'dec', z = 'sy_dist',
                      log_z = True,
                      size = 'st_rad',
                      color = 'spectral_class', color_discrete_map = simple_color_dict,
                      labels = {'ra' : 'Right Ascension',
                                'dec' : 'Declination',
                                'sy_dist' : 'Log Distance [pc]',
                                'spectral_class' : 'Spectral Class',
                                'st_rad' : 'Radius (Sol Radii)'},
                      category_orders = {'spectral_class' : ['A', 'F', 'G', 'K', 'M']})

fig_5.update_layout(scene = dict(xaxis = dict(backgroundcolor = 'black',
                                              gridcolor = 'grey'),
                                 yaxis = dict(backgroundcolor = 'black',
                                              gridcolor = 'grey'),
                                 zaxis = dict(backgroundcolor = 'black',
                                              gridcolor = 'grey'),
                                 aspectmode = 'cube'),
                    height = 750,
                    legend_orientation = 'h',
                    legend_y = -.25,
                    legend_itemclick = 'toggleothers')

# Create container 4
c4 = st.container()

with c4:
    st.header('Distribution of Stellar Distance')
    st.plotly_chart(fig_5, use_container_width = True)