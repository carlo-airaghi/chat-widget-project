# THEAPESHAPE AI Chat Widget

The **THEAPESHAPE AI Chat Widget** is an interactive AI-powered chatbot designed to provide personalized fitness coaching and guidance to advanced fitness enthusiasts. It leverages a retrieval-augmented generation (RAG) system using OpenAI's GPT models and Haystack to deliver relevant and contextual responses.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contribution](#contribution)

## Overview

The project is part of **The Ape Shape** app, a platform designed for fitness enthusiasts looking to optimize their workout routines and diet plans. This widget is embedded into the app's interface, allowing users to interact with an AI-based coach for personalized advice.

## Features

- **Personalized Responses**: Provides advice based on the user's fitness data, including weight, height, body fat percentage, and caloric expenditure.
- **Retrieval-Augmented Generation**: Combines a document retriever with OpenAI's GPT to deliver highly relevant responses.
- **Privacy and Survey Integration**: Includes a privacy policy acknowledgment and a post-chat survey for user feedback.
- **Dynamic Chat Interface**: Fully customizable widget with an intuitive interface.
- **PDF Document Indexing**: Supports knowledge retrieval from PDF documents.

## Tech Stack

- **Backend**: Flask, Haystack, OpenAI API
- **Frontend**: JavaScript, HTML, CSS
- **Containerization**: Docker
- **Document Processing**: PyPDF
- **Database**: In-memory document store (Haystack)

## Installation

### Prerequisites

- Docker and Docker Compose installed on your system.
- OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/the-ape-shape-ai-chat-widget.git
   cd the-ape-shape-ai-chat-widget
2. Build the Docker image:
```
docker build -t the-ape-shape-chat-widget .
```
3. Run the container:
```
docker run -p 5000:5000 -e OPENAI_API_KEY=your_openai_api_key the-ape-shape-chat-widget
Access the widget at http://127.0.0.1:5000.
```
4. Open the test page (test1.html or test2.html) with the vs code extension "Live Server"  

### Usage
1. Open the test.html file in a browser to interact with the chat widget locally.
2. Update the embedded script in the test.html file to include user data.
3. Use the chat interface to send messages and receive AI-generated responses.
4. Provide feedback via the post-chat survey to test survey functionality.

### Project Structure
```
.
├── Dockerfile
├── app.py
├── directory_tree.txt
├── requirements.txt
├── static_bmw
│   ├── chat-widget.css
│   ├── chat-widget.js
│   ├── fonts
│   └── images
├── static_theapeshape
│   ├── chat-widget.css
│   ├── chat-widget.js
│   ├── documents
│   ├── fonts
│   └── images
├── test1.html
└── test2.html
```
### Future Enhancements

- Database Integration: Replace the in-memory store with a persistent database.
- Advanced Analytics: Incorporate analytics to track user interactions and improve performance.