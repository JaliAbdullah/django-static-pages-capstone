const express = require('express');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.json());

// Load data from JSON files
const reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));

// Store data in memory
let reviews = reviews_data.reviews;
let dealerships = dealerships_data.dealerships;

console.log(`Loaded ${dealerships.length} dealerships and ${reviews.length} reviews`);

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Dealership API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    const dealerReviews = reviews.filter(review => review.dealership === dealerId);
    res.json(dealerReviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const stateDealers = dealerships.filter(dealer => dealer.state === state);
    res.json(stateDealers);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const dealer = dealerships.find(dealer => dealer.id === id);
    if (dealer) {
      res.json(dealer);
    } else {
      res.status(404).json({ message: 'Dealer not found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

//Express route to insert review
app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;
    const newId = Math.max(...reviews.map(r => r.id), 0) + 1;
    
    const review = {
      "id": newId,
      "name": data['name'],
      "dealership": data['dealership'],
      "review": data['review'],
      "purchase": data['purchase'],
      "purchase_date": data['purchase_date'],
      "car_make": data['car_make'],
      "car_model": data['car_model'],
      "car_year": data['car_year'],
    };

    reviews.push(review);
    res.json(review);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
