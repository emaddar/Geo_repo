import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from datetime import datetime
import time
import streamlit as st

def My_plot_Basemap(df,  withnames, projection, margin, resolution, area_thresh):
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    
    fig = plt.subplots(figsize=(15,15))
    m = MymBasemap(df, projection , margin, resolution, area_thresh)
    if withnames == 1:
            for i in range(df.shape[0]):   #Add points labels
                x = df['lon'][i]
                y = df['lat'][i]
                tx= df['local_city_country_code'][i]
                xx, yy = m(x, y) #m is basemap object
                plt.text(xx,yy, tx, fontsize=25)
    plt.title('', fontsize=20)
    #plt.show()

def all_geo_info_from_address(df, geolocator):
    df['info'] = df['Location'].apply(lambda x: geolocator.geocode(x).raw)  # raw fonction generates lat and lon
    df = pd.concat([df.drop(['info'], axis=1), df['info'].apply(pd.Series)], axis=1)
    '''
    for i in range(len(ADD)):
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(ADD[i]) +'?format=json'
        response = requests.get(url).json()
        df.loc[i].lat = response[0]["lat"]
        df.loc[i].lon = response[0]["lon"]
    '''
    df['location'] = df.apply(lambda x:geolocator.reverse(x["lat"]+", "+x["lon"]).raw['address'], axis=1)
    df = pd.concat([df.drop(['location'], axis=1), df['location'].apply(pd.Series)], axis=1)
    df.loc[df['city'].isnull(),'city'] = df['city_district']
    df['local_city_country_code'] = df[['city', 'country_code']].apply("_".join, axis=1)
    return df


def MymBasemap(df, projection, margin, resolution, area_thresh):
            m = Basemap(
                projection=projection,
                lat_0     = df['lat'].mean(),
                lon_0     = df['lon'].mean(),
                llcrnrlat = min(df['lat'])-margin,
                urcrnrlat = max(df['lat'])+margin,
                llcrnrlon = min(df['lon'])-margin-0.5,
                urcrnrlon = max(df['lon'])+margin+0.5,
                resolution = resolution,
                area_thresh = area_thresh
                )
            m.drawcoastlines()
            m.drawcountries(color='red')
            #m.drawstates(color='blue')
            m.drawcounties(color='orange')
            #m.drawrivers(color='blue')
            #m.drawmapboundary(fill_color='#46bcec')
            m.drawmapboundary(fill_color='#46bcec')
            m.fillcontinents(color = 'white',lake_color='#46bcec')
            m.drawlsmask(land_color='lightgreen', ocean_color='aqua', lakes=True)
            #m.etopo()
            #m.bluemarble()
            #m.shadedrelief()
            m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False]) #np.arange(start,stop,step)
            m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])  #labels=[left,right,top,bottom]
            m.scatter(df['lon'],df['lat'], latlon=True, c = 'red', s=500)
            return m

def columns_radio(df,col):
    if len(df.columns)==1:
        Location_column = df.columns.values
    else:
        col.markdown("<h5 style='text-align: left; color: red;'>  Select addresses column : </h5>", unsafe_allow_html=True)
        radio = col.radio('', (df.columns.values))
        Location_column = radio
    return Location_column

def select_sheet_st(df, col):
                Sheet_names = df.sheet_names
                if len(Sheet_names)>1:
                    col.markdown("<h5 style='text-align: left; color: red;'>  Select Sheet Name </h5>", unsafe_allow_html=True)
                    df = pd.read_excel(df, sheet_name = col.radio(" ",Sheet_names))
                    col.dataframe(df)
                else : 
                    df = pd.read_excel(df)
                    col.dataframe(df)
                return df

def download_csv_st(df, col):
    df = df.to_csv(index = False).encode('utf-8')
    col.download_button(
                        label=f"Download data as CSV",
                        data=df,
                        file_name=f'GeoData_{datetime.now()}.CSV',
                        mime='text/csv',
                        )


def animated_markdown_st(t, text): 
                        for i in range(len(text) + 1):
                            t.write(" %s..." % text[0:i])   #https://discuss.streamlit.io/t/display-several-pieces-of-strings-incrementally-on-the-same-line/9279
                            time.sleep(0.02)