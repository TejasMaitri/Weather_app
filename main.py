import streamlit as st
import requests
import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import json
import urllib.parse
import folium
from io import StringIO
from streamlit_folium import folium_static

# Set your OpenWeatherMap API key here
openweathermap_api_key = "4c40176c136d36e215cd3e252efb6f45"


def fetch_weather_details(city_name):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city_name)}"
        f"&appid={openweathermap_api_key}&units=metric"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature_celsius = data["main"]["temp"]
        feels_like_celsius = data["main"]["feels_like"]
        weather_details = {
            "City": data["name"],
            "Weather": {
                "Condition": data["weather"][0]["main"],
                "Description": data["weather"][0]["description"]
            },
            "Main": {
                "Temperature": temperature_celsius,
                "Feels Like": feels_like_celsius,
                "Pressure": data["main"]["pressure"],
                "Humidity": data["main"]["humidity"],
            },
            "Visibility": data["visibility"],
            "Wind": {
                "Speed": data["wind"]["speed"],
                "Direction": data["wind"]["deg"],
            },
        }
        return weather_details
    else:
        st.error("Error fetching weather data from the API.")
        return None


def get_openweathermap_current_weather(city):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}"
        f"&appid={openweathermap_api_key}&units=metric"
    )
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def weather_map(city):
    try:
        weather_data = get_openweathermap_current_weather(city)
        if weather_data["cod"] == 200:
            lat = weather_data["coord"]["lat"]
            lon = weather_data["coord"]["lon"]
            temp = weather_data["main"]["temp"]

            # Create a Folium map
            m = folium.Map(location=[lat, lon], zoom_start=10)

            # Add marker with a popup
            folium.Marker(
                location=[lat, lon],
                popup=f"Temperature: {temp}°C",
                icon=folium.Icon(color='blue', icon='info-sign'),
            ).add_to(m)

            # Display the map
            folium_static(m)
        else:
            st.write(f"Error: {weather_data['message']}")
    except Exception as e:
        st.write(f"An error occurred: {e}")


# Streamlit app
def main():
    st.title("Weather Forecast App")

    # Input city name
    city_name = st.text_input("Enter City Name", "Goa")

    # Fetch current weather details
    if st.button("Show Current Weather"):
        weather_details = fetch_weather_details(city_name)

        if weather_details:
            st.write("### Current Weather Information:")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"City: {weather_details['City']}")
                st.write(f"Weather Condition: {weather_details['Weather']['Condition']}")
                st.write(f"Weather Description: {weather_details['Weather']['Description']}")
                st.write(f"Temperature: {weather_details['Main']['Temperature']:.2f} °C")
                st.write(f"Feels Like: {weather_details['Main']['Feels Like']:.2f} °C")
            with col2:
                st.write(f"Pressure: {weather_details['Main']['Pressure']} hPa")
                st.write(f"Humidity: {weather_details['Main']['Humidity']}%")
                st.write(f"Visibility: {weather_details['Visibility']} meters")
                st.write(f"Wind Speed: {weather_details['Wind']['Speed']} m/s")
                st.write(f"Wind Direction: {weather_details['Wind']['Direction']}°")

    # Button to show weather map
    if st.button("Show Weather Map"):
        weather_map(city_name)

    # Fetch historical weather data and predictions
    if st.button("Predictions For Next 3 Days"):
        visual_crossing_url = (
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/goa%20india/last15days?unitGroup=metric&include=days&key=LYGG94T8QU8G8VLSEXYSYSUYY&contentType=csv"
        )
        response = requests.get(visual_crossing_url)

        if response.status_code == 200:
            csv_data = response.text
            df = pd.read_csv(StringIO(csv_data))
            target_variables = ['temp', 'feelslike', 'humidity', 'windspeed', 'cloudcover', 'precip', 'dew', 'solarradiation']
            X = df[['tempmin', 'tempmax', 'feelslikemin', 'feelslikemax', 'humidity', 'windspeed', 'cloudcover', 'precip', 'dew', 'solarradiation']]
            dates = pd.to_datetime(df['datetime'])
            models = {var: RandomForestRegressor(n_estimators=100) for var in target_variables}

            for var in target_variables:
                models[var].fit(X, df[var])

            latest_data = X.iloc[-1:].copy()
            num_days = 4  # Extend prediction to 3 days
            for day in range(2, num_days + 1):
                formatted_date = (
                    dates.iloc[-1] + pd.DateOffset(days=day)).strftime("%Y-%m-%d")
                st.write(f"### Predictions for {formatted_date}:")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Temp: {round(models['temp'].predict(latest_data)[0], 2)} °C")
                    st.write(f"Feels Like: {round(models['feelslike'].predict(latest_data)[0], 2)} °C")
                    st.write(f"Humidity: {round(models['humidity'].predict(latest_data)[0], 2)}%")
                    st.write(f"Wind Speed: {round(models['windspeed'].predict(latest_data)[0], 2)} m/s")
                with col2:
                    st.write(f"Cloud Cover: {round(models['cloudcover'].predict(latest_data)[0], 2)}%")
                    st.write(f"Precipitation: {round(models['precip'].predict(latest_data)[0], 2)} mm")
                    st.write(f"Dew: {round(models['dew'].predict(latest_data)[0], 2)} °C")
                    st.write(f"Solar Radiation: {round(models['solarradiation'].predict(latest_data)[0], 2)} W/m^2")
                st.write("---")
        else:
            st.error("Failed to fetch data. Status code: " + str(response.status_code))


if __name__ == "__main__":
    main()
