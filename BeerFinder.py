#!/usr/bin/python

from flask import Flask, jsonify, request
import json
from VTInfoClient import *

app = Flask(__name__)

#Loads the list of beer information from the local JSON file to keep things simple for now
json_data = open('./NewHollandBeers.json')
data = json.load(json_data)
json_data.close()

@app.route('/beers', methods=['GET'])
def beer_info():
    return jsonify(beers=data)

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
    app.run(host='0.0.0.0', port=5000)
