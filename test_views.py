# pylint: disable=redefined-outer-name

"""
Test cases for the Flask web application. 
This file contains unit tests for the views
defined in views.py. The tests use the Flask
test client to simulate requests to the 
application and verify that the responses
are as expected. The tests cover various 
scenarios, including valid and invalid city 
names, and check that the correct data is 
stored in the session and rendered in the templates.
"""

from unittest.mock import patch, MagicMock
import pytest
from flask import Flask
from views import main_blueprint

@pytest.fixture
def test_app():
    """_summary_

    Returns:
        _type_: _description_
    """
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    app.register_blueprint(main_blueprint)
    return app

@pytest.fixture
def test_client(test_app):
    """_summary_

    Args:
        test_app (_type_): _description_

    Returns:
        _type_: _description_
    """
    return test_app.test_client()

def test_index_post_redirect(test_client):
    """_summary_

    Args:
        test_client (_type_): _description_
    """
    response = test_client.post('/', data={'city': 'Berlin'})
    assert response.status_code == 302
    assert '/?city=Berlin' in response.location

@patch('requests.get')
@patch.dict('os.environ', {'WEATHER_KEY': 'fake_key'})
def test_index_get_success(mock_get, test_client):
    """_summary_

    Args:
        mock_get (_type_): _description_
        test_client (_type_): _description_
    """
    mock_weather = MagicMock()
    mock_weather.status_code = 200
    mock_weather.json.return_value = {
        'coord': {'lat': 51.5, 'lon': -0.12},
        'main': {'temp': 15},
        'name': 'London'
    }

    mock_forecast = MagicMock()
    mock_forecast.status_code = 200
    mock_forecast.json.return_value = {
        'list': [
            {
                'dt_txt': '2026-02-15 12:00:00',
                'main': {'temp': 10},
                'weather': [{'description': 'cloudy', 'icon': '01d'}]
            }
        ]
    }
    mock_get.side_effect = [mock_weather, mock_forecast]

    response = test_client.get('/?city=London')
    with test_client.session_transaction() as sess:
        assert sess['weather_data']['name'] == 'London'
        assert len(sess['forecast_data']) == 1
        assert sess['forecast_data'][0]['day'] == 'Sun' # Feb 15, 2026 is Sunday

    assert response.status_code == 302
    assert response.location.endswith('/dashboard')

@patch('requests.get')
def test_index_weather_failure(mock_get, test_client):
    """_summary_

    Args:
        mock_get (_type_): _description_
        test_client (_type_): _description_
    """
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    test_client.get('/?city=InvalidCity')

    with test_client.session_transaction() as sess:
        assert 'error_message' in sess
        assert "Error retrieving weather data" in sess['error_message']

@patch('requests.get')
def test_index_forecast_failure(mock_get, test_client):
    """_summary_

    Args:
        mock_get (_type_): _description_
        test_client (_type_): _description_
    """
    mock_weather = MagicMock()
    mock_weather.status_code = 200
    mock_weather.json.return_value = {'coord': {'lat': 0, 'lon': 0}}
    mock_forecast = MagicMock()
    mock_forecast.status_code = 500
    mock_get.side_effect = [mock_weather, mock_forecast]

    test_client.get('/?city=London')

    with test_client.session_transaction() as sess:
        assert 'forecast_error_message' in sess
        assert "500" in sess['forecast_error_message']

@patch.dict('os.environ', {'GOOGLE_MAP_API': 'map_key'})
def test_dashboard_route(test_client):
    """_summary_

    Args:
        test_client (_type_): _description_
    """
    with test_client.session_transaction() as sess:
        sess['weather_data'] = {'name': 'London'}
        sess['forecast_data'] = []

    response = test_client.get('/dashboard')
    assert response.status_code == 200
