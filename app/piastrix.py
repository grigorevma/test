import hashlib
import requests
from app.config import Secret_to_piastrix


def create_sign(*args):
    string = ""
    for i in args:
        string += str(i) + ":"
    string = string[:-1] + Secret_to_piastrix
    hashstring = hashlib.sha256(string.encode('utf-8')).hexdigest()
    return hashstring


def send_json(data, invoice=False):
    url1 = 'https://core.piastrix.com/invoice/create'
    url2 = 'https://core.piastrix.com/bill/create'
    if invoice:
        r = requests.post(url1, json=data)
    else:
        r = requests.post(url2, json=data)
    return r.json()
