from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

import sys
import os
import requests
# import datetime as dt

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

    db_url = os.environ['DB_URL']
    print("URL retrieved from env variable: " + db_url)

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



# @app.route('/query')
    # scan DB 
    # if it exists, check time added
        # if valid, return stored results

    # else, query sentiment service
        # wait for reply from /search 
        # return calculated results 


# @app.route('/search') 
    # send request to sentiment service with companny name in query 



@app.route('/get_sentiments', methods=["POST"])
def get_sentiments():

    # json_data = request.get_json()
    

    sentiments = db.sentiments.find({"search": ""})
    output = []

    for sentiment in sentiments:
        output.append({
            # "datetime" : now()
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





