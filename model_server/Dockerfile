# Use the official Python image as the base
FROM python:3.8-slim

# Declare build arguments at the top
ARG GENERATOR_MODEL_NAME
ARG RETRIEVER_QUERY_EMBEDDING_MODEL
ARG RETRIEVER_PASSAGE_EMBEDDING_MODEL
ARG MODEL_SERVER_PORT=8000

# Set environment variables using the build arguments
ENV GENERATOR_MODEL_NAME=${GENERATOR_MODEL_NAME}
ENV RETRIEVER_QUERY_EMBEDDING_MODEL=${RETRIEVER_QUERY_EMBEDDING_MODEL}
ENV RETRIEVER_PASSAGE_EMBEDDING_MODEL=${RETRIEVER_PASSAGE_EMBEDDING_MODEL}
ENV MODEL_SERVER_PORT=${MODEL_SERVER_PORT}

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file first
COPY requirements.txt ./

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the model download script
COPY download_model.py ./

# Download the models during the build process
RUN python download_model.py

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE ${MODEL_SERVER_PORT}

# Start the server
CMD ["python", "model_server.py"]