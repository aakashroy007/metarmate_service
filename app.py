from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
from datetime import datetime

app = FastAPI()

BASE_URL = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/"

@app.get("/metar/ping")
def ping():
    return {"data": "pong"}

@app.get("/metar/info")
async def get_metar_info(scode: str, nocache: int = 0):
    station_url = BASE_URL + scode.upper() + ".TXT"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(station_url, follow_redirects=True)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Weather data not available")
        
        metar_data = response.text
        parsed_data = parse_metar(metar_data)
        
        if nocache == 1:
            # Fetch live data from METAR and refresh the cache
            # You can implement your cache refreshing logic here
            pass
        
        return {"data": parsed_data}

def parse_metar(metar_data):
    lines = metar_data.split('\n')
    last_line = lines[-2]  # The last line contains the latest METAR data
    
    # Extract relevant data from METAR report (customize this as needed)
    last_observation = last_line[5:19]
    temperature = last_line[20:last_line.index("C")]
    wind_info = last_line[last_line.index("kt")-4:last_line.index("kt")+2]
    
    # Convert wind speed in knots to mph
    wind_speed_knots = int(wind_info.split()[0])
    wind_speed_mph = round(wind_speed_knots * 1.15078)
    
    # Convert wind direction to cardinal direction
    wind_direction = wind_info.split()[1]
    if wind_direction == "VRB":
        wind_direction = "Variable"
    
    return {
        "station": scode,
        "last_observation": last_observation,
        "temperature": f"{temperature} C ({temperature * 1.8 + 32} F)",
        "wind": f"{wind_direction} at {wind_speed_mph} mph ({wind_speed_knots} knots)"
    }
