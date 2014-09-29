# The module to interact with forecast.io for current weather details

import forecastio

def current_weather(API_KEY, lat, lng):
    """
    Returns current weather conditions
    """

    forecast = forecastio.load_forecast(API_KEY, lat, lng)
    current = forecast.currently()

    return current
