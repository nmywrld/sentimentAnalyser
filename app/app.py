from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

import sys
import os
import requests

app = Flask(__name__)
db = None

# get env variable and place it in url
try:
    sentiment_service_url = os.environ['SENTIMENT_SERVICE_URL']
    print("URL retrieved from env variable: " + sentiment_service_url)

    # test the url
    response = requests.get(sentiment_service_url)
    print("sentiment_service_url is valid")

except:
    print("sentiment_service_url failed")


def get_db():
    client = MongoClient(host='sentiment_db',
                         port=27017, 
                         username='root', 
                         password='root',
                        authSource="admin")
    db = client["sentiments"]
    return db

try:
    db = get_db()
    print("Connected to database")

    db.sentiments.drop()
    print("created collection")

    db.sentiments.insert_one({
        "search" : "test",
        'sentiment_score' : 'test',
        'emotion' : 'test',
        'keyword' : {"test": 0}
    })
    print("inserted test document")

except:
    print("Could not connect to database")

@app.route('/')
def ping_server():
    return "Welcome to sentiments microservice."

@app.route('/get_sentiments')
def get_sentiments():
    sentiments = db.sentiments.find()
    output = []

    for sentiment in sentiments:
        output.append({
            "search" : sentiment['search'],
            'sentiment_score' : sentiment['sentiment_score'],
            'emotion' : sentiment['emotion'],
            'keyword' : sentiment['keyword']
        })

    return jsonify({'result' : output})

@app.route('/test_sentiments_service')
def test_sentiments_service():
    response = requests.get(sentiment_service_url)
    return response.text

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5001)