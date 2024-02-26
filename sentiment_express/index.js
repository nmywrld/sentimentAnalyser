// basic express backend

import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import fetch from 'node-fetch';

import {MongoClient} from 'mongodb';
import axios from 'axios';


const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cors());


let db = null;

// get env variable and place it in url
try {
    const sentiment_service_url = process.env.SENTIMENT_SERVICE_URL;
    console.log("URL retrieved from env variable: " + sentiment_service_url);

    // test the url
    axios.get(sentiment_service_url)
        .then(response => console.log("sentiment_service_url is valid"))
        .catch(error => console.log("sentiment_service_url failed"));
} catch (error) {
    console.log("sentiment_service_url failed");
}

async function get_db() {
    // const client = new MongoClient('mongodb://localhost:27017', {
    const client = new MongoClient('mongodb://root:root@sentiment_db:27017', {
        authSource: "admin",
        useUnifiedTopology: true
    });

    client.connect()
        .then(() => console.log('Database connected successfully'))
        .catch(err => console.log(err));

    db = client.db('sentiments');
}

try {
    const db_url = process.env.DB_URL;
    console.log("URL retrieved from env variable: " + db_url);

    db = get_db();
    console.log("Connected to database");

    const sentiments = db.collection('sentiments');
    sentiments.drop();
    console.log("Dropped collection");

    sentiments.insertOne({
        datetime: new Date(),
        search: "test",
        sentiment_score: 'test',
        emotion: 'test',
        keyword: {"test": 0}
    });
    console.log("Inserted test document");
} catch (error) {
    console.log("Could not connect to database");
}







app.get('/', (req, res) => {
      res.send('welcome to the express sentiment microservice');
    }
);
 
app.get('/query', async (req, res) => {
    const search_term = req.query.search_term;

    const sentiments = await Sentiment.find({search: search_term});
    const output = [];
  
    if (sentiments) {
      for (let sentiment of sentiments) {
        if ((Date.now() - sentiment.datetime) / 1000 < 3600) {
          output.push(sentiment);
        }
      }
  
      if (output.length > 0) {
        return res.json({result: output});
      }
    }
  
    console.log("getting data");
    const response = await axios.get(`your_scraper_url?search_term=${search_term}`);
    const json_data = response.data;
    console.log(json_data);
  
    console.log("analysing");
    const results = await add_sentiments(json_data);
  
    console.log("inserting");
    const newSentiment = new Sentiment({
      datetime: Date.now(),
      search: "test",
      sentiment_score: results.results.headlines_score + results.results.description_score,
      emotion: results.results.emotions,
      keyword: results.keyword_results
    });
  
    await newSentiment.save();
  });
  
  app.listen(5001, () => console.log('Server running on port 5001'));
  
//   async function add_sentiments(json_data) {}
