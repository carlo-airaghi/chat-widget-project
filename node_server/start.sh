#!/bin/sh

# Start the Python FastAPI server in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start the Node.js server
npm start
