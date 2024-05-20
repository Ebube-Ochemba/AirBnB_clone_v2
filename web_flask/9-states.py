#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Displays HTML page with list of all State objects"""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """Displays HTML page with cities of a specific State"""
    state = storage.all(State).get(f"State.{id}")
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=cities)
    else:
        return render_template('9-states.html')


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
