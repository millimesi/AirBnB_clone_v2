#!/usr/bin/python3
'''
flask web framework project
'''


from flask import Flask
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


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')
