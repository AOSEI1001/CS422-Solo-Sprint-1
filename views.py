"""

Returns:
    _type_: _description_
"""

import os
from datetime import datetime
import requests
from flask import Blueprint, redirect, url_for, session
from flask import request
from flask import render_template


# Create a blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """
    This function handles the main route of
    the application. It processes both GET 
    and POST requests to retrieve weather 
    data for a specified city. The city can
    be provided through query parameters or 
    form data. The function makes API calls 
    to the OpenWeatherMap service to fetch 
    current weather and forecast data, which
    are then stored in the session for later
    use in the dashboard. If there are any 
    errors during the API calls, appropriate
    error messages are stored in the session. 
    Finally, the user is redirected to the 
    dashboard route to view the results.

    """

    city = request.args.get('city') or request.form.get('city')

    print(os.environ.get("WEATHER_KEY"))
    print(os.environ.get("GOOGLE_MAP_API"))

    if request.method == 'POST':
        city = request.form.get('city', 'London')
        # Redirect to GET with city parameter
        return redirect(url_for('main.index', city=city))

    # Handle GET request with city parameter
    if city:
        api_key = os.environ.get('WEATHER_KEY')
        api_response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
            , timeout=5)

        if api_response.status_code == 200:
            weather_data = api_response.json()
            lat = api_response.json()['coord']['lat']
            lon = api_response.json()['coord']['lon']
            payload = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'imperial'
            }
            forcecast_response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast", params=payload, timeout=5)
            session['weather_data'] = weather_data
            print(weather_data)

            if forcecast_response.status_code == 200:
                forecast_data = forcecast_response.json()
                filtered_forecast = []
                for entry in forecast_data['list']:
                    if '12:00:00' in entry['dt_txt']:
                        data_object = datetime.strptime(entry['dt_txt'],'%Y-%m-%d %H:%M:%S')
                        filtered_forecast.append({
                            'day': data_object.strftime('%a'),
                            'temp': entry['main']['temp'],
                            'description': entry['weather'][0]['description'],
                            'icon': entry['weather'][0]['icon']
                        })

                session['forecast_data'] = filtered_forecast
                session['forecast_raw_data'] = forecast_data
                print(filtered_forecast)
            else:
                session['forecast_error_message'] = (
                    f"Error retrieving forecast data for {city}: {forcecast_response.status_code}"
                )
        else:
            session['error_message'] = (
                f"Error retrieving weather data for {city}: {api_response.status_code}"
            )

        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.dashboard'))

@main_blueprint.route('/dashboard')
def dashboard():
    """
    This function handles the dashboard route of
    the application. It retrieves weather and 
    forecast data from the session, along with
    any error messages. The data is then 
    passed to the dashboard template for 
    rendering. The Google Maps API key is
    also retrieved from the environment 
    variables for use in the template.
    
    """
    google_api_key = os.environ.get('GOOGLE_MAP_API')
    weather_data = session.get('weather_data')
    forecast_data = session.get('forecast_data')
    forecast_raw_data = session.get('forecast_raw_data')
    error_message = session.get('error_message')
    forecast_error_message = session.get('forecast_error_message')
    return render_template('dashboard.html',
                           weather_data=weather_data,
                           forecast_data=forecast_data,
                           forecast_raw_data=forecast_raw_data,
                           error_message=error_message,
                           forecast_error_message=forecast_error_message,
                           google_api_key=google_api_key)
