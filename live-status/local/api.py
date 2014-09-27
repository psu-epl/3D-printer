"""
Connect to the webserver API that will report the status

"""
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

URI = 'http://localhost:5000/status/3d-mojo.json'
PRIVATE_KEY = RSA.importKey(open('mojo.key', 'r').read())

def update(payload):
    """Makes a signed update to the server

    :param str payload: stringified JSON data for the update

    """

    # sign the payload
    signer = PKCS1_v1_5.new(PRIVATE_KEY)
    digest = SHA256.new()
    digest.update(payload)
    signature = b64encode(signer.sign(digest))

    r = requests.put(URI, data={"data": payload, "signature": signature})
    print r.status_code, r.text
