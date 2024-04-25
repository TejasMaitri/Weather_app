Weather Forecast App
This is a simple web application built with Streamlit for displaying current weather information and making predictions for the next 3 days based on historical weather data.

Features:
Current Weather Display: Fetches and displays current weather information including temperature, weather condition, humidity, pressure, visibility, and wind speed/direction for a specified city.
Historical Weather Data: Retrieves historical weather data using the Visual Crossing Weather API to train predictive models.
Predictions: Utilizes machine learning (Random Forest Regressor) to predict weather conditions for the next 3 days based on historical data.
Interactive Map: Shows the location of the specified city on an interactive map with a marker indicating the current temperature.
Technologies Used:
Streamlit: For building the web application interface.
Requests: For making HTTP requests to fetch weather data from APIs.
Pandas: For data manipulation and analysis.
Scikit-learn: For implementing the Random Forest Regressor model.
Folium: For creating interactive maps within the application.

How to Use:
Enter the name of the city for which you want to fetch weather information.
Click on "Show Current Weather" to display the current weather details.
Click on "Predictions For Next 3 Days" to view weather predictions for the next 3 days.
Click on "Show Weather Map" to visualize the location of the city on the map with the current temperature marker.
Note:
Ensure you have a valid OpenWeatherMap API key for accessing weather data.
Historical weather data is fetched from the Visual Crossing Weather API, so an API key from Visual Crossing Weather is also required.
Feel free to contribute or provide feedback to improve the app!

This description provides an overview of the app's functionality, technologies used, and instructions for usage.
