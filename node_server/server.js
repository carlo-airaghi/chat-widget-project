// server.js

require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the 'widget' directory
app.use(express.static(path.join(__dirname, 'widget')));

// Serve test.html at the root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'widget', 'test.html'));
});

// Chat endpoint
app.post('/chat', async (req, res) => {
  const userMessage = req.body.message;

  try {
    // Use environment variable or default to 'rag_pipeline_server'
    const modelServerHost = process.env.MODEL_SERVER_HOST || 'rag_pipeline_server';
    const modelServerPort = process.env.MODEL_SERVER_PORT || 8000;

    // Forward the request to the Python backend
    const response = await axios.post(
      `http://${modelServerHost}:${modelServerPort}/ask`,
      { question: userMessage }
    );

    const assistantMessage = response.data.answer;
    res.json({ reply: assistantMessage });
  } catch (error) {
    console.error('Error communicating with the RAG pipeline server:', error.message);
    res.status(500).json({ error: 'An error occurred while processing your request.' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
