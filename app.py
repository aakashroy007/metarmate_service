from fastapi import FastAPI, HTTPException
import redis
import httpx
from bs4 import BeautifulSoup
from datetime import datetime

app = FastAPI()

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

BASE_URL = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/"


@app.get("/metar/ping")
def ping():
    return {"data": "pong"}


@app.get("/metar/info")
async def get_metar_info(scode: str, nocache: int = 0):
    cached_data = redis_client.get(scode)
    if not cached_data or nocache == 1:
        station_url = BASE_URL + scode.upper() + ".TXT"

        async with httpx.AsyncClient() as client:
            response = await client.get(station_url, follow_redirects=True)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Weather data not available",
                )

            metar_data = response.text
            parsed_data = parse_metar(metar_data)
            parsed_data["source"] = "Live"

            redis_client.setex(scode, 300, str(parsed_data))
    else:
        parsed_data = eval(cached_data)
        parsed_data["source"] = "Cache"

    return {"data": parsed_data}


def parse_temperature(temperature_str):
    temperature_parts = temperature_str.split("/")
    current_temp_str = temperature_parts[0]

    if current_temp_str.startswith("M"):
        temp_c = int(current_temp_str[1:]) * -1
    else:
        temp_c = int(current_temp_str)

    temp_f = round(temp_c * 1.8 + 32)
    return f"{temp_c} C ({temp_f} F)"


def parse_wind(wind_info):
    direction = int(wind_info[:3])
    velocity = int(wind_info[3:5])
    direction_str = get_cardinal_direction(direction)
    velocity_mph = int(velocity * 1.15078)

    return f"{direction_str} at {velocity_mph} mph ({velocity} knots)"


def get_cardinal_direction(degrees):
    cardinal_directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    index = round(degrees / 22.5) % 16
    return cardinal_directions[index]


def parse_timestamp(timestamp_str):
    timestamp = datetime.strptime(timestamp_str, "%Y/%m/%d %H:%M")
    formatted_timestamp = timestamp.strftime("%Y/%m/%d at %H:%M GMT")
    return formatted_timestamp


def parse_wind_and_temperature(data_list):
    wind_info = None
    temperature_info = None

    for line in data_list:
        if line.endswith("KT"):
            wind_info = line
        elif "/" in line:
            temperature_info = line

    if wind_info:
        wind = parse_wind(wind_info)
    else:
        wind = "Wind data not available"

    if temperature_info:
        temperature = parse_temperature(temperature_info)
    else:
        temperature = "Temperature data not available"

    return wind, temperature


def parse_metar(metar_data):
    lines = metar_data.split("\n")
    first_line = lines[0]
    second_line = lines[-2].split(" ")

    observation_datetime = parse_timestamp(first_line)
    station = second_line[0]
    wind_info, temp_info = parse_wind_and_temperature(second_line)

    return {
        "station": station,
        "last_observation": observation_datetime,
        "temperature": temp_info,
        "wind": wind_info,
    }
