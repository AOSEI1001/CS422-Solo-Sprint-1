import os
import requests
from flask import Blueprint, redirect, url_for, session
from flask import request


# Create a blueprint
main_blueprint = Blueprint('main', __name__)

# dogstring
@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    
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
        api_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        
        if api_response.status_code == 200:
            weather_data = api_response.json()
            session['weather_data'] = weather_data
            print(weather_data)
        else:
            session['error_message'] = f"Error retrieving weather data for {city}: {api_response.status_code}"
        
        return redirect(url_for('main.dashboard'))
    
    return redirect(url_for('main.dashboard'))


@main_blueprint.route('/dashboard')
def dashboard():
    from flask import render_template
    google_api_key = os.environ.get('GOOGLE_MAP_API')
    weather_data = session.get('weather_data')
    error_message = session.get('error_message')
    
    return render_template('dashboard.html', weather_data=weather_data, error_message=error_message, google_api_key=google_api_key)



# @main_blueprint.route('/conditional')
# def conditional():
#     user = 'admin'
#     return render_template('conditional.html', user=user)


