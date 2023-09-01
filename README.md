# METARMate Service

METARMate Service is a JSON web API built with FastAPI that provides the latest weather information from METAR stations. It offers endpoints to retrieve weather reports for specific station codes and supports caching using Redis.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aakashroy007/metarmate_service.git
   cd metarmate_service

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

## Usage

1. Make sure Redis is running locally or accessible at the configured host and port.

2. Start the FastAPI application using Uvicorn:

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8080

3. Access the API endpoints:

    - GET /metar/info?scode=STATION_CODE - Retrieve weather information for the specified station code.
    - Additional parameter: nocache=1 to fetch live data and refresh the cache.
    Example:

    ```bash
    curl "http://localhost:8080/metar/info?scode=KSGS&nocache=1"

## Assumptions

1. Response will be in the form:

    ```
    2001/11/17 15:38
    KSGS 171538Z AUTO 19005KT 7SM CLR M01/M05 A3021 RMK AO2
    ```
2. Second line starts with the station.

3. Wind info will end with "KT".

4. Temperature info will contain "/".

