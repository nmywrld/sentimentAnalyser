from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient

import sys
import os
import requests
from datetime import datetime

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

def query_sentiments(search_term):
    sentiments = db.sentiments.find({"search": search_term})
    output = []

    if sentiments is None:
        # call /scraper endpoint and wait for reply
        # call /add_sentiments endpoint with scraper results in request and wait for reply

        return None
    else:
        for sentiment in sentiments:
            # if sentiment is less than 1 hour old
            if (datetime.now() - sentiment['datetime']).seconds < 3600:
                output.append({
                    "datetime" : sentiment['datetime'],
                    "search" : sentiment['search'],
                    'sentiment_score' : sentiment['sentiment_score'],
                    'emotion' : sentiment['emotion'],
                    'keyword' : sentiment['keyword']
                })
    
    # else, query sentiment service
        # wait for reply from /search 
        # return calculated results 


# @app.route('/search') 
    # send request to sentiment service with companny name in query 
                
# @app.route('/scraper')
# def scraper():
#     # call scraper service
#     response = requests.get(scraper_service_url + "/scrape")
#     return response.text


@app.route('/add_sentiments')
def add_sentiments():
    # call sentiment_service_url/analyse_headlines
    response = requests.get(sentiment_service_url + "/analyse_headlines")

    # get the results from the response
    results = response.json()

    # add the results to the database
    db.sentiments.insert_one({
        "datetime" : datetime.now(),
        "search" : "test",
        'sentiment_score' : results['headlines_score'] + results['description_score'],
        'emotion' : results['emotions'],
        'keyword' : {"test": 0}
    })
    



@app.route('/get_sentiments', methods=["POST"])
def get_sentiments():

    # get the search term from the request
    search_term = request.get_json()['search']
    
    sentiments = db.sentiments.find({"search": search_term})
    output = []

    for sentiment in sentiments:
        output.append({
            "datetime" : sentiment['datetime'],
            "search" : sentiment['search'],
            'sentiment_score' : sentiment['sentiment_score'],
            'emotion' : sentiment['emotion'],
            'keyword' : sentiment['keyword']
        })

    return jsonify({'result' : output})


@app.route('/get_sentiments', methods=["GET"])
def get_sentiments_old():
    
    # get the search term from the request
    search_term = request.args.get('search')
    
    sentiments = db.sentiments.find({"search": search_term})
    output = []

    for sentiment in sentiments:
        output.append({
            "datetime" : sentiment['datetime'],
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





