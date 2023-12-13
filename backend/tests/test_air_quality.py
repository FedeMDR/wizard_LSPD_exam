import os
import sys
from fastapi.testclient import TestClient

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app
from app.mymodules.air_quality import air_quality_status

"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)

def test_air_quality_good():
    aqi = air_quality_status(1)

    assert aqi == 'Good'

def test_air_quality_fair():
    aqi = air_quality_status(2)

    assert aqi == 'Fair'

def test_air_quality_moderate():
    aqi = air_quality_status(3)

    assert aqi == 'Moderate'

def test_air_quality_poor():
    aqi = air_quality_status(4)

    assert aqi == 'Poor'


def test_air_quality_very_poor():
    aqi = air_quality_status(5)

    assert aqi == 'Very Poor'