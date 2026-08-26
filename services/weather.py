import requests


def get_location_weather(location):
    """Get current weather for a location using Open-Meteo."""

    # Geocode location
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(geo_url, params=geo_params, timeout=10)
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise ValueError(f"Location not found: {location}")

    place = geo_data["results"][0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    data = weather_response.json()
    current = data["current"]

    return {
        "location": place["name"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"]
    }