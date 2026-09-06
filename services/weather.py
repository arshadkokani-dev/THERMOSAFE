import requests
import streamlit as st


@st.cache_data(ttl=600, show_spinner=False)
def get_location_weather(location):
    """Get current weather for a location using Open-Meteo."""

    # -----------------------------
    # 1. Geocode location
    # -----------------------------
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

    except requests.RequestException as exc:
        raise ConnectionError(
            f"Weather service unavailable while locating {location}."
        ) from exc

    except ValueError as exc:
        raise ValueError(
            f"Invalid geocoding response for {location}."
        ) from exc

    if not geo_data.get("results"):
        raise ValueError(f"Location not found: {location}")

    place = geo_data["results"][0]

    latitude = place["latitude"]
    longitude = place["longitude"]

    # -----------------------------
    # 2. Get current weather
    # -----------------------------
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    try:
        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10,
        )
        weather_response.raise_for_status()
        data = weather_response.json()

    except requests.RequestException as exc:
        raise ConnectionError(
            f"Weather service unavailable for {location}."
        ) from exc

    except ValueError as exc:
        raise ValueError(
            f"Invalid weather response for {location}."
        ) from exc

    # -----------------------------
    # 3. Validate weather data
    # -----------------------------
    current = data.get("current")

    if not current:
        raise ValueError(
            f"Current weather data unavailable for {location}."
        )

    temperature = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    wind = current.get("wind_speed_10m")

    if temperature is None or humidity is None or wind is None:
        raise ValueError(
            f"Incomplete weather data received for {location}."
        )

    # -----------------------------
    # 4. Return standardized data
    # -----------------------------
    return {
        "location": place["name"],
        "temperature": float(temperature),
        "humidity": float(humidity),
        "wind": float(wind),
    }