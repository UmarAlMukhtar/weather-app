const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 3002;
const apiKey = 'a91e773835815c49a57352b83325b848';

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Serve static files from the 'frontend' directory
app.use(express.static(path.join(__dirname, '../frontend')));

// MongoDB Atlas connection string
const mongoURI = 'mongodb+srv://vishalkodoth:Vishalkodoth30@cluster0.evxqycw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';

// Connect to MongoDB
mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log('MongoDB connected'))
  .catch(err => console.log('MongoDB connection error:', err));

// Calendar Entry Schema
const entrySchema = new mongoose.Schema({
  date: { type: String, required: true },
  location: {
    lat: { type: Number, required: true },
    lng: { type: Number, required: true }
  }
});

const Entry = mongoose.model('Entry', entrySchema);

// Routes
app.post('/api/entries', async (req, res) => {
  const { date, location } = req.body;
  try {
    const newEntry = new Entry({ date, location });
    await newEntry.save();
    res.status(201).json(newEntry);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.get('/api/entries', async (req, res) => {
  try {
    const entries = await Entry.find();
    res.status(200).json(entries);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// New route to fetch weather data
app.get('/api/weather', async (req, res) => {
  const { lat, lon } = req.query;
  if (!lat || !lon) {
    return res.status(400).json({ error: 'Latitude and longitude are required' });
  }

  try {
    const response = await axios.get(`https://api.openweathermap.org/data/2.5/weather`, {
      params: {
        lat: lat,
        lon: lon,
        appid: apiKey,
        units: 'metric'
      }
    });

    const weatherData = response.data;
    res.status(200).json(weatherData);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch weather data' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});