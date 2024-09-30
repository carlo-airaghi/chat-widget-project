require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 5000;
const path = require('path');

// Middleware
app.use(cors());
app.use(express.json());

// Serve test.html at the root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'widget', 'test.html'));
});

// Serve static files from the 'widget' directory
app.use(express.static(__dirname,'widget'));

// Use environment variable or default to 8000
const modelServerPort = process.env.MODEL_SERVER_PORT || 8000;

// Chat endpoint
app.post('/chat', async (req, res) => {
  const userMessage = req.body.message;

  try {
    // Forward the request to the Python backend using the service name
    const response = await axios.post(
      `http://${modelServerHost}:${modelServerPort}/generate`,
      { message: userMessage }
    );

    const assistantMessage = response.data.reply;
    res.json({ reply: assistantMessage });
  } catch (error) {
    console.error('Error communicating with local model API:', error.message);
    res.status(500).json({ error: 'An error occurred while processing your request.' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
