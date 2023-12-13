import json
from flask import Flask, render_template, request
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange

from ast import literal_eval

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'

def request_attr_list():
    try:
        # Make the HTTP request within the Flask request context
        with app.test_request_context():
            response = requests.get('http://backend/attractions')
            response.raise_for_status()  # Raise an exception for HTTP errors
            # Assuming the backend returns a list of attractions as JSON
            attr_list = response.json()
            return attr_list
    except requests.exceptions.RequestException as e:
        print(f"Error in the request to the backend: {e}")
        return None

class SeachBnBForm(FlaskForm):
    n_attr = SelectField('How many attractions do you plan on visiting?:',
                         choices=['0-5', '5-10', '10-20'])
    trees_bool = SelectField('Do you want to be in a green area:',
                             choices=['True', 'False'])
    crime_rate = SelectField('How much do you care for a crime-free area?:',
                             choices=['Not at all', 'Very little', 'Enough',
                                      'Extremely'])
    sorting_key = SelectField('Sort by:', choices = [('price', 'Price'),
                                                               ('review_scores_rating','Reviews')])
    sorting_order = SelectField('Sorting Order:', choices= [(0,'Ascending'), (1,'Descending')])

    submit = SubmitField('Search')


class neighbourhoodBnbForm(FlaskForm):
    sorting_key = SelectField('Sort by:', choices = [('price', 'Price'),
                                                     ('review_scores_rating','Reviews')])
    sorting_order = SelectField('Sorting Order:', choices= [(0,'Ascending'), (1,'Descending')])
    submit = SubmitField('Search')


class AdvancedSearch(FlaskForm):
    selected_attractions = SelectMultipleField(choices=request_attr_list(), validators=[DataRequired()])
    distance_m = IntegerField('Distance (m)', validators=[NumberRange(min=0), DataRequired()])
    sorting_key = SelectField('Sort by:', choices = [('price', 'Price'),
                                                     ('review_scores_rating','Reviews')])
    sorting_order = SelectField('Sorting Order:', choices= [(0,'Ascending'), (1,'Descending')])
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
def index():
    response = requests.get('http://backend/index/596dff3ac05aeb906e63803d2bfcf01a')
    error_message = None

    if response.status_code == 200:
        data = response.json()
        return render_template('index.html', borough_list = data)
    elif response.status_code == 404:
        error_message = f"Error: {response.json().get('detail')}"
    else:
        error_message = f'Error: Unable to fetch data from FastAPI Backend'
        return render_template('index.html', error_message=error_message)
    

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SeachBnBForm()
    error_message = None

    if form.validate_on_submit():
        if form.n_attr.data == '0-5':
            min = 0
            max = 5
        elif form.n_attr.data == '5-10':
            min = 5
            max = 10
        else:
            min = 10
            max = 20

        if form.crime_rate.data == 'Not at all':
            crime_rate = 1
        elif form.crime_rate.data == 'Very little':
            crime_rate = 2
        elif form.crime_rate.data == 'Enough':
            crime_rate = 3
        elif form.crime_rate.data == 'Extremely':
            crime_rate = 4

        trees_bool = form.trees_bool.data

        response = requests.get(
            'http://backend/search',
            params={
                'min': min,
                'max': max,
                'trees_bool': trees_bool,
                'crime_rate': crime_rate
            }
        )

        if response.status_code == 200:
            data = response.json()
            data = json.loads(data)
            data = [elem for elem in data]
            if form.sorting_key.data == 'review_scores_rating':
                data = sorted(data, key = lambda x: int(x[form.sorting_key.data]*100), reverse = bool(int(form.sorting_order.data)))
            else: 
                data = sorted(data, key = lambda x: x[form.sorting_key.data], reverse = bool(int(form.sorting_order.data)))
            return render_template('search.html',
                                   form=form,
                                   string_list=data,
                                   error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch data from FastAPI Backend'

    return render_template('search.html', form=form, result=None,
                           error_message=error_message)


@app.route('/neighbourhood', methods=['GET', 'POST'])
def return_borough():
    neighbourhood = request.args.get('neighbourhood')
    form = neighbourhoodBnbForm()
    error_message = None

    if form.validate_on_submit():
        response = requests.get(
                'http://backend/neighbourhood',
                params={
                    'neighbourhood': neighbourhood
                }
            )
        if response.status_code == 200:
                data = response.json()
                data = json.loads(data)
                data = [elem for elem in data]
                if form.sorting_key.data == 'review_scores_rating':
                    data = sorted(data, key = lambda x: int(x[form.sorting_key.data]*100), reverse = bool(int(form.sorting_order.data)))
                else: 
                    data = sorted(data, key = lambda x: x[form.sorting_key.data], reverse = bool(int(form.sorting_order.data)))
                return render_template('neighbourhood.html',
                                    form=form,
                                    bnb_list=data,
                                    neighbourhood = neighbourhood,
                                    error_message=error_message)
        elif response.status_code == 404:
            error_message = f"Error: {response.json().get('detail')}"
        else:
            error_message = f'Error: Unable to fetch data from FastAPI Backend'
    return render_template('neighbourhood.html', form=form, result=None, neighbourhood = neighbourhood,
                           error_message=error_message)


@app.route('/advanced', methods = ['GET', 'POST'])
def advanced():
    form = AdvancedSearch()
    error_message = None
    if form.validate_on_submit():
        distance_m = form.distance_m.data
        selected_attractions = form.selected_attractions.data
        selected_attractions = str(selected_attractions)
        distance_m = int(distance_m)
        response = requests.get(
            'http://backend/advanced',
            params={
                'attractions' : selected_attractions,
                'range' : distance_m
            }
        )
        response_attractions = requests.get(
            'http://backend/map',
            params={
                'attraction' : selected_attractions
            }
        )
        if response.status_code == 200 and response_attractions.status_code == 200:
            data = response.json()
            data = json.loads(data)
            data = [elem for elem in data]

            attractions = response_attractions.json()
            attractions = json.loads(attractions)
            attractions = [elem for elem in attractions]

            if form.sorting_key.data == 'review_scores_rating':
                data = sorted(data, key = lambda x: int(x[form.sorting_key.data]*100), reverse = bool(int(form.sorting_order.data)))
            else: 
                data = sorted(data, key = lambda x: x[form.sorting_key.data], reverse = bool(int(form.sorting_order.data)))
            return render_template('advanced.html',
                                form=form,
                                bnb_list=data,
                                attractions  = attractions,
                                error_message=error_message)
        elif response.status_code == 422:
            error_message = f"Error: {response.json().get('detail')}"

        elif response.status_code == 404:
            error_message = f"Error: {response.json().get('detail')}"
        else:
            error_message = 'Error: Unable to fetch data from FastAPI Backend'
    return render_template('advanced.html', form=form, result=None,
                           error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)