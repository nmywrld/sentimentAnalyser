import express from "express";

import Sentiment from './db_model.js';

import db_methods from "./db_methods.js";

const SentimentController = express.Router();


try {
    // // drop collection
    Sentiment.collection.drop();
    Sentiment.createCollection();

    // insert test document
    let newSentiment = new Sentiment({
        datetime: Date.now(),
        search: "test",
        sentiment_score: 0,
        emotion: "test",
        keyword: {"test": 0}
    });

    newSentiment.save();

} catch (error) {
    console.log(error);
}

SentimentController.get("/", (req, res) => {
    res.send('welcome to the sentiment db controller');
});

SentimentController.get("/query", async (req, res) => {
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

    console.log("Not in DB. Getting data...");
    // const response = await axios.get(`your_scraper_url?search_term=${search_term}`);
    
    const response = await db_methods.scraper(search_term);
    console.log(response);
    // return res.json({result: response});

    console.log("Analysing...");

    const results = await db_methods.add_sentiments(response);

    console.log("Inserting...");
    const newSentiment = new Sentiment({
        datetime: Date.now(),
        search: "test",
        sentiment_score: results.results.headlines_score + results.results.description_score,
        emotion: results.results.emotions,
        keyword: results.keyword_results
    });

    await newSentiment.save();

    return res.json({result: newSentiment});



});


export default SentimentController;











// get env variable and place it in url
// try {
//     const sentiment_service_url = process.env.SENTIMENT_SERVICE_URL;
//     console.log("URL retrieved from env variable: " + sentiment_service_url);

//     // test the url
//     axios.get(sentiment_service_url)
//         .then(response => console.log("sentiment_service_url is valid"))
//         .catch(error => console.log("sentiment_service_url failed"));
// } catch (error) {
//     console.log("sentiment_service_url failed");
// }

// require('./db_client.js');


// try {
//     // const db_url = process.env.DB_URL;
//     // console.log("URL retrieved from env variable: " + db_url);

//     // const DB_client = await connect();

//     console.log("Connecting to database");
//     DB_client()
//     // DB_client.connect()
//     // .then(() =>{
//     //     console.log("started");

//     //     collection = DB_client.db("sentiments").collection("sentiments");
//     //     console.log("Connected to database");

//     //     collection.drop();
//     //     console.log("Dropped collection");

//     //     collection.insertOne({
//     //         datetime: new Date(),   
//     //         search: "test",
//     //         sentiment_score: 'test',
//     //         emotion: 'test',
//     //         keyword: {"test": 0}
//     //     });

//     //     console.log("Inserted test document");
//     // })
//     // .catch((err) => {
//     //     console.log("Could not connect to database");
//     //     console.log(err)
//     // });

// } catch (error) {
//     console.log("Could not connect to database");
// }




// app.get('/query', async (req, res) => {
//     const search_term = req.query.search_term;

//     collection.find()

//     // const res = await collection.find({search: search_term});
//     // const output = [];
  
//     // if (sentiments) {
//     //   for (let sentiment of sentiments) {
//     //     if ((Date.now() - sentiment.datetime) / 1000 < 3600) {
//     //       output.push(sentiment);
//     //     }
//     //   }
  
//     //   if (output.length > 0) {
//     //     return res.json({result: output});
//     //   }
//     // }

  
//     console.log("getting data");
//     // const response = await axios.get(`your_scraper_url?search_term=${search_term}`);
//     const response = scraper(search_term)
//     const json_data = response.data;
//     console.log(json_data);
  
//     console.log("analysing");
//     const results = await add_sentiments(json_data);
  
//     console.log("inserting");
//     const newSentiment = new Sentiment({
//       datetime: Date.now(),
//       search: "test",
//       sentiment_score: results.results.headlines_score + results.results.description_score,
//       emotion: results.results.emotions,
//       keyword: results.keyword_results
//     });
  
//     await newSentiment.save();
//   });