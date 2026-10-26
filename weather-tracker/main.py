import streamlit as st
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city):
  params = {
      "name": city,
      "count": 5,
      "language": "en",
      "format" : "json"
  }

  response = requests.get(
      GEOCODING_URL,
      params=params,
      timeout=10
  )

  data = response.json()
  locations = data.get("results", [])

  if not locations:
    return None

  location = locations[0]

  city_info = {
    "name": location["name"],
    "country": location.get("country", "Unknown"),
    "latitude": location["latitude"],
    "longitude": location["longitude"]
    }

  return city_info

print(get_coordinates("Medan"))

def get_current_weather(latitude, longitude):
  params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code",
    "timezone": "auto"
}

  response = requests.get(
      WEATHER_URL,
      params=params,
      timeout=10
  )

  data = response.json()

  current = data["current"]

  weather_info = {
    "temperature": current["temperature_2m"],
    "humidity": current["relative_humidity_2m"],
    "apparent_temperature": current["apparent_temperature"],
    "weather_code": current["weather_code"],
    "time": current["time"]
  }
  

  return weather_info

def get_weather_description(weather_code):
  weather_d = {
      0: "Clear sky",
      1: "Mainly clear",
      2: "Partly cloudy",
      3: "Overcast",
      45: "Fog",
      48: "Fog",
      51: "Drizzle",
      53: "Drizzle",
      55: "Drizzle",
      61: "Rain",
      63: "Rain",
      65: "Rain",
      71: "Snowfall",
      73: "Snowfall",
      75: "Snowfall",
      80: "Rain showers",
      81: "Rain showers",
      82: "Rain showers",
      95: "Thunderstorm",
      96: "Thunderstorm with hail",
      99: "Thunderstorm with hail"
  }

  if weather_code not in weather_d:
    return "Unknown weather code."
    
  return weather_d[weather_code]

def get_weather_for_city(city):
    city_info = get_coordinates(city)

    if city_info is None:
        return None

    weather_info = get_current_weather(
        city_info["latitude"],
        city_info["longitude"]
    )

    if weather_info is None:
        return None

    condition = get_weather_description(
        weather_info["weather_code"]
    )

    output = {
        "city": city_info["name"],
        "country": city_info["country"],
        "apparent_temperature": weather_info["apparent_temperature"],
        "humidity": weather_info["humidity"],
        "condition": condition
    }

    return output


st.set_page_config(
    page_title="Real-Time Weather Dashboard",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ Real-Time Weather Dashboard")
st.write("Check the current weather in a city around the world.")

city = st.text_input(
    "Enter a city name",
    placeholder="e.g. Singapore, Tokyo, London"
)

if st.button("Get Weather"):
    if not city.strip():
        st.warning("Please enter a city name.")

    else:
        with st.spinner("Fetching current weather..."):
            result = get_weather_for_city(city)

        if result is None:
            st.error(
                "We couldn't retrieve the weather. "
                "Check the city name or try again later."
            )

        else:
            st.subheader(
                f"📍 {result['city']}, {result['country']}"
            )

            st.metric(
                "🌡️ Temperature",
                f"{result['temperature']} °C"
            )

            st.metric(
                "💧 Relative Humidity",
                f"{result['humidity']}%"
            )

            st.metric(
                "🌡️ Feels Like",
                f"{result['apparent_temperature']} °C"
            )

            st.success(
                f"🌦️ Current Condition: {result['condition']}"
            )

            st.caption(
                f"Weather observation time: {result['time']}"
            )

st.divider()
st.caption("Weather data provided by Open-Meteo.")
