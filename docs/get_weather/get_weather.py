import json
import os
from typing import Dict, Any, Optional
# from pprint import pprint

import requests
from dotenv import load_dotenv


def load_environment() -> Optional[str]:
    """
    Loads environment variables from a .env file and retrieves the WEATHER_API key.

    Returns:
        Optional[str]: The value of the WEATHER_API environment variable if found,
                       otherwise None.
    """
    load_dotenv()
    API_KEY = os.getenv("WEATHER_API")
    return API_KEY


def search_weather(location: str) -> Dict[str, Any]:
    """
    Fetches current weather data for a given location using the Weatherstack API.

    Args:
        location (str): The name of the location (e.g., city or region) to search for.

    Returns:
        Dict[str, Any]: A dictionary containing the weather data returned by the API.
                        If the request fails, an empty dictionary is returned.

    Raises:
        TypeError: If the input location is not a string.
        Prints error messages for HTTP or general exceptions.
    """

    if not isinstance(location, str):
        raise TypeError("Input must be a string.")

    API_KEY = load_environment()
    URL = f"https://api.weatherstack.com/current?query={location}&access_key={API_KEY}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return {}


def extract_weather_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts key weather details from the full API response.

    Args:
        data (Dict[str, Any]): The full JSON response from the weather API.

    Returns:
        Dict[str, Any]: A dictionary containing selected weather information:
                        - name of the location
                        - region
                        - local time
                        - temperature
                        - feels like temperature
    """
    return {
        "name": data["location"]["name"],
        "region": data["location"]["region"],
        "local_time": data["location"]["localtime"],
        "temperature": data["current"]["temperature"],
        "feels_like": data["current"]["feelslike"],
    }


def inspect_response(weather_response: Dict[str, Any]) -> str:
    """
    Converts a weather response dictionary into a pretty-printed JSON string.

    Args:
        weather_response (Dict[str, Any]): The weather data to format.

    Returns:
        str: A formatted JSON string representation of the weather data.
    """
    result = json.dumps(weather_response, indent=4)
    return result


weather_data = search_weather("Athens")

print(inspect_response(weather_data))

weather_summary = extract_weather_info(weather_data)

print(
    f"The temperature in {weather_summary['name']} is {weather_summary['temperature']} degrees Celcius and feels like {weather_summary['feels_like']} degrees."
)
