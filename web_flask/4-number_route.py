#!/usr/bin/python3
'''
flask web framework project
'''


from flask import Flask, abort
import re
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    '''root page'''
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''hbnb page'''
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    '''hbnb page'''
    text = re.sub('_', ' ', text)
    return f"C {text}"


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    '''hbnb page'''
    text = re.sub('_', ' ', text)
    return f"Python {text}"


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    '''hbnb page'''
    try:
        int_n = int(n)
        return f"{int_n} is a number"
    except ValueError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')
