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

