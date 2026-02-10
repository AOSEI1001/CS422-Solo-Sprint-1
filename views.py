from flask import Blueprint, render_template
from flask import request
import requests
import os
import random
#from dotenv import load_dotenv
#load_dotenv()

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    
    weather_data = None
    error_message = None

    print(os.environ.get("WEATHER_KEY"))
    
    if request.method == 'POST':
        city = request.form.get('city', 'London')  


        if city:
            api_key = os.environ.get('WEATHER_KEY')
            api_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
            

            if api_response.status_code == 200:
                weather_data = api_response.json()
                print(weather_data)
            else:
                error_message = f"Error retrieving weather data: {api_response.status_code}"
             
        
        else:
            error_message = "Could not retrieve weather data. Please try again."

    return render_template('dashboard.html', weather_data=weather_data, error_message=error_message)



# @main_blueprint.route('/conditional')
# def conditional():
#     user = 'admin'
#     return render_template('conditional.html', user=user)


