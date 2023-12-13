import os
import sys
from fastapi.testclient import TestClient
import pytest

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app
from app.mymodules.advanced_research import GeoCoords
print(sys.path)
"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)

def test_class_GeoCoords_valid():
    geo_coords = GeoCoords(40.7128, -73.060)
    assert geo_coords.latitude == 40.7128
    assert geo_coords.longitude == -73.060

def test_corenercase_GeoCoords():
    geo_coords = GeoCoords(90, 180)
    assert geo_coords.latitude == 90
    assert geo_coords.longitude == 180

def test_corenercase_negative_GeoCoords():
    geo_coords = GeoCoords(-90, -180)
    assert geo_coords.latitude == -90
    assert geo_coords.longitude == -180

def test_invalid_latitude():
    with pytest.raises(ValueError, match='Invalid latitude or longitude values'):
        GeoCoords(-100, 0)

def test_invalid_longitude():
    with pytest.raises(ValueError, match='Invalid latitude or longitude values'):
        GeoCoords(0, 200)
    
