#!/usr/bin/python

from flask import Flask, jsonify, request
from VTInfoClient import *

app = Flask(__name__)

@app.route('/beerfinder', methods=['GET'])
def find_beers():
    return jsonify(results=findNewHollandBeers(request.args['lat'],
                                               request.args['long'],
                                               request.args['b'],
                                               request.args['t'],
                                               request.args['m'],
                                               request.args['d']))

@app.route('/listbeers', methods=['GET'])
def list_beers():
    return jsonify(beers=listBeers())

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=80)
