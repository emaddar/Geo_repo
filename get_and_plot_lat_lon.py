#  https://www.youtube.com/watch?v=6GGcEoodLNM
# https://matplotlib.org/basemap/users/geography.html
# https://predictivelearning.github.io/projects/Project_054_Visualizing_Geographic_data_with_Basemap_toolkit__EUROSTAT.html
# https://stackoverflow.com/questions/44488167/plotting-lat-long-points-using-basemap

from doctest import DocFileCase
from pickle import TRUE
from pyparsing import col
import requests
import urllib.parse
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import streamlit as st
import EmadPy
import time




st.set_page_config(
    page_title="Find latitude and longitude from address",
    page_icon=":earth_africa:",
    layout="wide"
)
st.set_option('deprecation.showPyplotGlobalUse', False)
col1, col2, col3 = st.columns(3)
text1 = "Get lat. and long. from address"
text2 = "please wait this may take a few minutes"

t1 = col2.empty()
if "t1" not in st.session_state:
    for i in range(len(text1) + 1):
            t1.markdown("## %s..." % text1[0:i])   #https://discuss.streamlit.io/t/display-several-pieces-of-strings-incrementally-on-the-same-line/9279
            time.sleep(0.05)
    st.session_state['t1'] = t1
else : col2.header(text1+'...')

text= '*** Welcome ... please select your file with location column ***'
tt = col2.empty()
if "tt" not in st.session_state:
    for i in range(len(text) + 1):
            tt.markdown(" %s..." % text[0:i])   #https://discuss.streamlit.io/t/display-several-pieces-of-strings-incrementally-on-the-same-line/9279
            time.sleep(0.05)
    st.session_state['tt'] = tt
else : col2.write(text+'...')

for i in range(7):
    col1.markdown('')
    col3.markdown('')




data_type = col1.radio("File type :",("CSV", "Excel"))
if data_type == "CSV" :
            data_file = col1.file_uploader("Upload CSV",type=["csv"])
            if data_file :
                df_csv = pd.read_csv(data_file,encoding = "utf-8")
                if df_csv is not None:
                    col1.dataframe(df_csv)
                    Location_column = EmadPy.columns_radio(df_csv, col1)
                    col1.write(f'Location column is : {Location_column}')
                    df_csv['Location'] = df_csv[Location_column]
                    if "df_csv" not in st.session_state:
                        st.session_state.df_csv = df_csv
                    if "df_csv" in st.session_state:
                        geolocator = Nominatim(user_agent="geoapiExercises")
                        button= col2.button('Get geolocation from address')
                        if button:
                                t2 = col2.empty()
                                EmadPy.animated_markdown_st(t2,text2)

                                df2_csv = EmadPy.all_geo_info_from_address(st.session_state.df_csv, geolocator)
                                if "df2_csv" not in st.session_state:
                                    st.session_state.df2_csv = df2_csv

                    if "df2_csv" in st.session_state:    
                        col2.dataframe(st.session_state.df2_csv[['lat', 'lon', 'city','country', 'country_code']])
                        df3_csv = st.session_state.df2_csv
                        if 'df3_csv' not in st.session_state:
                            st.session_state.df3_csv = df3_csv
                        EmadPy.download_csv_st(st.session_state.df2_csv, col2) 
                        col2.write('If you want to convert csv to excel please click [here](https://csvexcel.herokuapp.com/)')

                    if "df3_csv" in st.session_state:
                        plot_buttom = col3.button("Plotting Geo-scatter plot")  
                        if plot_buttom:  
                            #t3 = col3.empty()
                            #EmadPy.animated_markdown_st(t3,text2)
                            st.session_state.df3_csv['lat'] = st.session_state.df3_csv['lat'].apply(lambda x: float(x))
                            st.session_state.df3_csv['lon'] = st.session_state.df3_csv['lon'].apply(lambda x: float(x))
                            col3.map(st.session_state.df3_csv)
                            #col3.pyplot(EmadPy.My_plot_Basemap(st.session_state.df3_csv, withnames = 1, projection = 'mill', margin =2.1, resolution = 'h', area_thresh = 100)) 
else:
            data_file = col1.file_uploader("Upload xlsx",type=["xlsx"])
            if data_file :
                df_xlsx = pd.ExcelFile(data_file)
                if df_xlsx is not None:
                    df_xlsx = EmadPy.select_sheet_st(df_xlsx, col1)
                    Location_column = EmadPy.columns_radio(df_xlsx, col1)
                    col1.write(f'Location column is : {Location_column}')
                    df_xlsx['Location'] = df_xlsx[Location_column]
                    if "df_xlsx" not in st.session_state:
                        st.session_state.df_xlsx = df_xlsx
                    if "df_xlsx" in st.session_state:
                        geolocator = Nominatim(user_agent="geoapiExercises")
                        button= col2.button('Get geolocation from address')
                        if button: 
                                t2 = col2.empty()
                                EmadPy.animated_markdown_st(t2,text2)


                                df2_xlsx = EmadPy.all_geo_info_from_address(st.session_state.df_xlsx, geolocator)
                                #col3.dataframe(df2_xlsx)  #********************
                                if "df2_xlsx" not in st.session_state:
                                    st.session_state.df2_xlsx = df2_xlsx

                    if "df2_xlsx" in st.session_state:    
                        col2.dataframe(st.session_state.df2_xlsx[['lat', 'lon', 'city','country', 'country_code']])
                        df3_xlsx = st.session_state.df2_xlsx
                        if 'df3_xlsx' not in st.session_state:
                            st.session_state.df3_xlsx = df3_xlsx
                        EmadPy.download_csv_st(st.session_state.df2_xlsx, col2) 
                        col2.write('If you want to convert csv to excel please click [here](https://csvexcel.herokuapp.com/)')

                    if "df3_xlsx" in st.session_state:
                            plot_buttom = col3.button("Plotting Geo-scatter plot")  
                            if plot_buttom:  
                                #t3 = col3.empty()
                                #EmadPy.animated_markdown_st(t3,text2)
                                st.session_state.df3_xlsx['lat'] = st.session_state.df3_xlsx['lat'].apply(lambda x: float(x))
                                st.session_state.df3_xlsx['lon'] = st.session_state.df3_xlsx['lon'].apply(lambda x: float(x))
                                col3.map(st.session_state.df3_xlsx)
                                #col3.pyplot(EmadPy.My_plot_Basemap(st.session_state.df3_xlsx, withnames = 1, projection = 'mill', margin =2.1, resolution = 'h', area_thresh = 100))