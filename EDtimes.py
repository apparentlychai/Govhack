try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import streamlit as st
import pandas as pd
import numpy as np
from geopy import distance
import dotenv,json,requests
from os import environ

dotenv.load_dotenv()
pd.options.display.float_format = "{:,.2f}".format

dict_lat_lon = {'lat': [], 'lon': []}

def get_ED_times(page,geolocator,user_location,geolocated=None):

    soup = get_page_Parsed(page)
    if geolocated:
        user_lat_lon = (geolocated["lat"], geolocated["lon"])
    else:
        user_lat_lon = get_User_lan_lon(user_location,geolocator)
    print(user_lat_lon)
    EDtable_df = get_ED_time_df(soup)
    

    distance_from_user = []
    for hospital in EDtable_df['Hospital']:
        #st.write(type(hospital))
        location_A_geocode = geolocator.geocode(str(hospital))
        if location_A_geocode is None:
            distance_from_user.append(None)
            dict_lat_lon['lat'].append(0)
            dict_lat_lon['lon'].append(0)
        else:     
            hospital_lat_lon = (location_A_geocode.latitude, location_A_geocode.longitude)
            dict_lat_lon['lat'].append(location_A_geocode.latitude)
            dict_lat_lon['lon'].append(location_A_geocode.longitude)
            distance_from_user.append(distance.distance(hospital_lat_lon,user_lat_lon).km)
        #st.write(location_A_geocode)
        
    lat_lon_df = pd.DataFrame(dict_lat_lon,columns = ['lat','lon'])
    EDtable_df['Distance from user'] = distance_from_user
   # st.write(EDtable_df)
    return user_lat_lon, EDtable_df, lat_lon_df
    

def travel_time(user_lat_lon, EDtable_df, lat_lon_df,mode_of_trans):
   
    #st.write(lat_lon_df)
    duration_to_destination = []
    for count,hospital in enumerate(EDtable_df['Hospital']):
        if lat_lon_df.iloc[count]['lon'] == 0:
               duration_to_destination.append(None)
        else:     
            r = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/{str(mode_of_trans).lower()}/{user_lat_lon[1]},{user_lat_lon[0]};{lat_lon_df.iloc[count]['lon']},{lat_lon_df.iloc[count]['lat']}?access_token={environ['API_TOKEN']}")
            map_data = r.json()

            duration_to_destination.append((map_data['routes'][0]['duration'])/60)
    EDtable_df['Duration (minutes)'] = duration_to_destination
    
    EDtable_df.set_index('Hospital', inplace=True)
    EDtable_df.rename(columns={EDtable_df.columns[0]:'Wait Time',EDtable_df.columns[1]:'Patients waiting',EDtable_df.columns[2]:'Total patient in ED'}, inplace=True)

    EDtable_df = EDtable_df.dropna()
    
    EDtable_df[EDtable_df.columns[0]] = pd.to_numeric(EDtable_df[EDtable_df.columns[0]])

    EDtable_df['sum_time'] = EDtable_df[EDtable_df.columns[0]] + EDtable_df[EDtable_df.columns[-1]]
    
    st.header('Earliest available ED')
    st.dataframe(EDtable_df.sort_values(by = ['sum_time'], ascending = [True]).iloc[0:3:,0:5], width=5500)

    return EDtable_df.sort_values(by = ['sum_time'], ascending = [True]).iloc[3:,0:5]


def get_page_Parsed(page):
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_User_lan_lon(user_location,geolocator):
    user_location_geocode = geolocator.geocode(user_location) # Add user location here
    user_lat_lon = (user_location_geocode.latitude, user_location_geocode.longitude)
    return user_lat_lon

def get_loc_time(map_data,EDtable_df,user_lat_lon,mode_of_trans,typeofloc):
    loc_df = pd.DataFrame(columns=['Name','Address','Duration (minutes)'])

    for i,data in enumerate( map_data['features']):
        
        loc_duration_request = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/{str(mode_of_trans).lower()}/{user_lat_lon[1]},{user_lat_lon[0]};{data['geometry']['coordinates'][0]},{data['geometry']['coordinates'][1]}?access_token={environ['API_TOKEN']}")
        time_to_loc = (loc_duration_request.json()['routes'][0]['duration'])/60
        temp_dict = {'Name':data['text'], 'Address':data['place_name'].split(',')[1:2],'Duration (minutes)':time_to_loc}
        loc_df = loc_df.append(temp_dict,ignore_index=True)

    
    st.header(f'Nearest {typeofloc}')
    st.write(loc_df.sort_values(by = ['Duration (minutes)'], ascending = [True]))
    
    return loc_df.sort_values(by = ['Duration (minutes)'], ascending = [True])




    #st.write(map_data)


def get_ED_time_df(soup):

    Edtable = soup.find('table', attrs={'class':'rg-table zebra'})
    header = []
    for i in Edtable.find_all('th'):
        header.append(i.text)
    EDtable_df = pd.DataFrame(columns = header)
    for j in Edtable.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(EDtable_df)
        EDtable_df.loc[length] = row
    return EDtable_df.dropna()