import json
from flask import Flask, jsonify, request, redirect

from pymongo import MongoClient, ReturnDocument

from utils import get_db_client
from controller import create_url, get_url, recover_url_entry

app = Flask(__name__)


@app.route('/')
def ping_server():
    return "Welcome to the world of animals."


@app.route('/shortenurl', methods=['POST'])
def shorten_url():
    print('In shortenURL')
    return jsonify(create_url(request))


@app.route('/shortly/<key>', methods=['GET'])
def redirect_to_url(key):
    return get_url(request, key)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
