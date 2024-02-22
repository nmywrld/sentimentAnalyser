import requests
import pandas as pd
import numpy as np

from flask import Flask
from modelLoader import ModelLoader
from flask import request, jsonify

app = Flask(__name__)
model_loader = ModelLoader()


@app.route('/')
def home():
    return 'welcome to sentiment service'


@app.route('/analyse_headlines', methods=['POST'])
def convert_json_to_csv():
    json_data = request.get_json()

    # Convert JSON to DataFrame
    df = pd.DataFrame(json_data)


    headlines_df = df.copy()
    headlines_df['headline_sentiment'] = 0
    headlines_df['description_sentiment'] = 0
    headlines_df['emotion'] = 0

    # call get_sentiment_and_emotion
    results = model_loader.get_sentiment_and_emotion(len(headlines_df), headlines_df)

    keyword_results = model_loader.get_keywords(" ".join(headlines_df['headline_text'].tolist()) + " ".join(headlines_df['description'].tolist()))


    # return headlines_df

# /test endpoint that reads ./testing/testData.csv and does the same as /analyse
@app.route('/test')
def test():
    # load the data
    data = pd.read_csv('./testing/testData.csv')
    
    # convert cols 
    data['publish_date'] = pd.to_datetime(data['publish_date'])
    data['headline_text'] = data['headline_text'].astype(str)
    data['description'] = data['description'].astype(str)

    # make a copy of the data
    headlines_df = data.copy()
    headlines_df['headline_sentiment'] = 0
    headlines_df['description_sentiment'] = 0
    headlines_df['emotion'] = None

    print(headlines_df.dtypes)

    # call get_sentiment_and_emotion
    results = model_loader.get_sentiment_and_emotion(len(headlines_df), headlines_df)
    results.head()

    keyword_results = model_loader.get_keywords(" ".join(headlines_df['headline_text'].tolist()) + " ".join(headlines_df['description'].tolist()))
    print(keyword_results)

    return headlines_df.to_json(orient='records')



@app.route('/get_sentiment_and_emotion')
def get_sentiment_and_emotion():
    # Call endpoint2
    # response = requests.get('http://localhost:5000/endpoint2')

    model_loader.get_sentiment_and_emotion()

    return None

@app.route('/get_keywords')
def get_keywords():
    return 'Hello from endpoint2'

if __name__ == '__main__':
    app.run(port=5002, debug=True, host="0.0.0.0")
