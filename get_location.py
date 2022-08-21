def get_user_lan_lon(user_location, geolocator):
    user_location_geocode = geolocator.geocode(user_location)  # Add user location here
    user_lat_lon = (user_location_geocode.latitude, user_location_geocode.longitude)
    return user_lat_lon
