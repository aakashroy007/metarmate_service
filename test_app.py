import httpx
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_ping():
    response = client.get("/metar/ping")
    assert response.status_code == 200
    assert response.json() == {"data": "pong"}


def test_get_metar_info():
    response = client.get("/metar/info?scode=agga")
    assert response.status_code == 200
    assert "data" in response.json()
