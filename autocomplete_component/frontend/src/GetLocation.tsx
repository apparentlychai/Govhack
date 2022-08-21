import React, { useEffect, useState }from "react";
import { useGeolocated } from "react-geolocated";
import { Intent, Callout } from "@blueprintjs/core";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

const GetLocation = () => {

    const defaultState = { lat: null, lon: null }
    const [value, setValue] = useState(defaultState);

    useEffect(() => Streamlit.setFrameHeight());
    const { coords, isGeolocationAvailable, isGeolocationEnabled } =
        useGeolocated({
            positionOptions: {
                enableHighAccuracy: false,
            },
            userDecisionTimeout: 5000,
    });
    
    const locationPossible = isGeolocationAvailable || isGeolocationEnabled
    const cardTitle = locationPossible ? (coords ? "Location found" : "Finding location") : "Enter your address below"
    const location = coords ? { lat: coords.latitude, lon: coords.longitude } : defaultState
    const locationIntent: Intent = locationPossible ? (coords ? "success" : "primary") : "none"

    Streamlit.setComponentValue(location)

    function Coordinates() {
        return (
            <div>
                <p>Latitude: {location.lat}</p>
                <p>Longitude: {location.lon}</p>
            </div>
        );
    }

    function NoLocation() {
        return (
            <p>Please enter your address in the field below</p>
        );
    }

    return (
        <Callout intent={locationIntent} title={cardTitle}>
            {locationPossible && coords
                ? <Coordinates />
                : <NoLocation />
            }
        </Callout>
    )
};

export default withStreamlitConnection(GetLocation);