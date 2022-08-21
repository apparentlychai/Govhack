try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import streamlit as st
import pandas as pd 
import numpy as np 
from geopy.geocoders import Nominatim
import requests,dotenv,json
#import plotly.graph_objects as go
from EDtimes import get_ED_times,travel_time,get_loc_time
from os import environ

dotenv.load_dotenv()

URL = "https://ww2.health.wa.gov.au/Reports-and-publications/Emergency-Department-activity/Data?report=ed_activity_now"
page = requests.get(URL)

geolocator = Nominatim(user_agent="GovHackathon2022")

st.title('GOVHACK 2022')

user_location = st.sidebar.text_input('Add your address Here')
mode_of_trans = st.sidebar.radio("What is prefered travel option?",['Driving','Cycling','Walking'])

pharmacy =  st.sidebar.radio('Do you want to include pharmacy?',['No','Yes'])
medical_centre =  st.sidebar.radio('Do you want to include Medical Centre?',['No','Yes'])



if user_location:
    user_lat_lon, EDtable_df, lat_lon_df =  get_ED_times(page,geolocator, user_location)
    EDtable_df_less_preferred = travel_time(user_lat_lon, EDtable_df, lat_lon_df,mode_of_trans)

   #st.write(user_lat_lon)
    
    if pharmacy == 'Yes':
        r = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/pharmacy.json?type=poi&proximity={user_lat_lon[1]},{user_lat_lon[0]}&access_token={environ['API_TOKEN']}")
        map_data = r.json()
        loc_dur_df = get_loc_time(map_data, EDtable_df, user_lat_lon,mode_of_trans,'Pharmacy')
        
    if medical_centre == 'Yes':
        r = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/medical+centre.json?type=poi&proximity={user_lat_lon[1]},{user_lat_lon[0]}&access_token={environ['API_TOKEN']}")
        map_data = r.json()
        loc_dur_df = get_loc_time(map_data, EDtable_df, user_lat_lon,mode_of_trans,'Medical Centre')
        
   #st.write(map_data)
   

   




