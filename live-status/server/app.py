#!/usr/bin/env python
from functools import wraps
from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/status/*": {"origins": "*"}})

# json endpoint decorator
def json(func):
    """Returning a object gets JSONified"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs)[0]), func(*args, **kwargs)[1]
    return decorated_function

@app.route("/status/3d-mojo.json")
@json
def mojo_status():
    status = {"running": True, "finish": "2014"}
    return dict({'message': "success"}, **status), 200

if __name__ == "__main__":
    app.debug = True
    app.run()
