import os
import sys
from fastapi.testclient import TestClient
from attractions import attractions_list
import random
import pytest

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app


"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)

#this test will take some time to execute because it needs to wait the response of an API
def test_index_correctkey_nocache():
    CACHE_FILE = 'air_quality_cache.json'
    with open(CACHE_FILE, 'w') as cache_file:
        cache_file.write('')
    response = client.get("/index/596dff3ac05aeb906e63803d2bfcf01a")
    assert response is not None
    if response.status_code == 200:
        assert len(response.json()) == 5
    else:
        assert len(response.json()) == 1
        assert response.status_code == 404

def test_index_wrongkey():
    response = client.get("/index/fjkdashjfdjhsafhdjsahfjhds")
    assert response is not None
    if response.status_code == 200:
        assert len(response.json()) == 5
    else:
        assert len(response.json()) == 1
        assert response.status_code == 404

def test_index_correctkey_withcache():
    response = client.get("/index/596dff3ac05aeb906e63803d2bfcf01a")
    assert response is not None
    if response.status_code == 200:
        assert len(response.json()) == 5
    else:
        assert len(response.json()) == 1
        assert response.status_code == 404
        
def test_wrong_inputrange_search():
    response = client.get(
        "/search",
        params={
            'min': 1,
            'max': 3,
            'trees_bool': 'False',
            'crime_rate': 7
        }
    )
    assert response.status_code == 422

def test_wrong_inputtype_tree():
    response = client.get(
        "/search",
        params={
            'min': 1,
            'max': 10,
            'trees_bool': 'something wrong',
            'crime_rate': 3
        }
    )
    assert response.status_code == 404

def test_wrong_inputtype_crime():
    response = client.get(
        "/search",
        params={
            'min': 1,
            'max': 10,
            'trees_bool': 'True',
            'crime_rate': None
        }
    )
    assert response.status_code == 404

def test_cornercase_search2():
    response = client.get(
        "/search",
        params={
            'min': 0,
            'max': 20,
            'trees_bool': 'True',
            'crime_rate': 2
        }
    )
    assert response.status_code == 200


def test_cornercase_search3():
    response = client.get(
        "/search",
        params={
            'min': 0,
            'max': 20,
            'trees_bool': 'True',
            'crime_rate': 3
        }
    )
    assert response.status_code == 200

def test_cornercase_search4():
    response = client.get(
        "/search",
        params={
            'min': 0,
            'max': 20,
            'trees_bool': 'True',
            'crime_rate': 4
        }
    )
    assert response.status_code == 200



def test_right_search_main():
    response = client.get(
        "/search",
        params={
            'min': 0,
            'max': 5,
            'trees_bool': 'False',
            'crime_rate': 1
        }
    )
    assert response.status_code == 200


def test_wrong_neighbourhood_main():
    response = client.get(
                'http://backend/neighbourhood',
                params={
                    'neighbourhood': 'Ca tron'
                }
            )
    
    assert response.status_code == 404

def test_wrong_neighbourhood_main():
    response = client.get(
                'http://backend/neighbourhood',
                params={
                    'neighbourhood': None
                }
            )
    assert response.status_code == 404


def test_right_neighbourhood_main():
    response = client.get(
                'http://backend/neighbourhood',
                params={
                    'neighbourhood': 'Manhattan'
                }
            )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_attractions_list_main():
    response = client.get('http://backend/attractions')
    attr_list = [lista[1] for lista in response.json()]
    assert response.status_code == 200
    assert attr_list == attractions_list


def test_advanced_feature():

    def random_pick(attr_list, n):
        n = min(n, len(attr_list))
        return random.sample(attr_list, n)
    

    response = client.get(
            'http://backend/advanced',
            params={
                'attractions' : [random_pick(attractions_list, 4)],
                'range' : 1000
            }
        )
    assert response.status_code == 200


def test_advanced_feature_extremecaseLow():


    def random_pick(attr_list, n):
        n = min(n, len(attr_list))
        return random.sample(attr_list, n)
    

    response = client.get(
            'http://backend/advanced',
            params={
                'attractions' : [random_pick(attractions_list, 4)],
                'range' : 1
            }
        )
    assert response.status_code == 422

def test_advanced_feature_extremecaseHigh():


    def random_pick(attr_list, n):
        n = min(n, len(attr_list))
        return random.sample(attr_list, n)
    

    response = client.get(
            'http://backend/advanced',
            params={
                'attractions' : [random_pick(attractions_list, 4)],
                'range' : 1000000000000000000
            }
        )
    assert response.status_code == 422


def test_advanced_feature_invalidInput():


    def random_pick(attr_list, n):
        n = min(n, len(attr_list))
        return random.sample(attr_list, n)
    

    response = client.get(
            'http://backend/advanced',
            params={
                'attractions' : [random_pick(attractions_list, 4)],
                'range' : 'pippo'
            }
        )
    assert response.status_code == 404

def test_advanced_feature_invalidInputNumeric():


    def random_pick(attr_list, n):
        n = min(n, len(attr_list))
        return random.sample(attr_list, n)
    

    response = client.get(
            'http://backend/advanced',
            params={
                'attractions' : [random_pick(attractions_list, 4)],
                'range' : 0.10
            }
        )
    assert response.status_code == 404


def test_map_main():

    def random_pick(attr_list, n):
        n = min(n, len(attr_list))
        return random.sample(attr_list, n)
    
    response = client.get(
        'http://backend/map',
        params={
            'attraction' : [random_pick(attractions_list, 4)]
        }
    )
    assert response.status_code == 200