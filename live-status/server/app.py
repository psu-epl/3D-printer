#!/usr/bin/env python
from functools import wraps
from flask import Flask, jsonify, request
from flask.ext.cors import CORS, cross_origin
from redis import StrictRedis
from os import getenv
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
import json
app = Flask(__name__)

# Set up redis
REDIS_URL = getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = StrictRedis.from_url(REDIS_URL)

# Set CORS header
cors = CORS(app, resources={r"/status/*": {"origins": "*"}})

# Get public key
PUBLIC_KEY = redis.get('cid-status-mojo-key')


@app.route("/status/3d-mojo.json", methods=['GET', 'PUT'])
def mojo_status():

    # PUT --------------------------------------------------------------------
    if request.method == 'PUT':

        # Get data out of request
        rawdata = request.form['data']
        signature = request.form['signature']

        # Check signature
        rsakey = RSA.importKey(PUBLIC_KEY) 
        signer = PKCS1_v1_5.new(rsakey) 
        digest = SHA256.new() 
        digest.update(rawdata)
        if signer.verify(digest, b64decode(signature)):

            # Varified, update redis
            data = json.loads(rawdata)
            for key, value in data.items():
                redis.hset('cid-status-mojo', key, str(value))
            return jsonify(dict({'message': "success"})), 200

        # Signature Fail
        return jsonify(dict({'message': "signature failed"})), 401

    # GET --------------------------------------------------------------------
    status = {}
    for key in redis.hkeys('cid-status-mojo'):
        status[key] = redis.hget('cid-status-mojo', key)

    # Reply with current status
    return jsonify(dict({'message': "success"}, **status)), 200


if __name__ == "__main__":
    app.debug = True
    app.run()
