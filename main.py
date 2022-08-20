try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import streamlit as st
import pandas as pd 
import numpy as np 
from geopy.geocoders import Nominatim
import requests,dotenv,json
import plotly.graph_objects as go
from EDtimes import get_ED_times,travel_time
from os import environ

dotenv.load_dotenv()

URL = "https://ww2.health.wa.gov.au/Reports-and-publications/Emergency-Department-activity/Data?report=ed_activity_now"
page = requests.get(URL)

geolocator = Nominatim(user_agent="GovHackathon2022")


user_location = st.text_input('Add your address Here')

pharmacy =  st.radio('Do you want to include pharmacy?',['yes','no'])



if user_location:
   user_lat_lon, EDtable_df, lat_lon_df =  get_ED_times(page,geolocator, user_location)
   st.write(user_lat_lon)
   r = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/pharmacy.json?type=poi&proximity={user_lat_lon[1]},{user_lat_lon[0]}&access_token={environ['API_TOKEN']}")
   map_data = r.json()
   st.write(map_data)

#    travel_time(user_lat_lon, EDtable_df, lat_lon_df)





