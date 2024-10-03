# Use the official Python image as the base
FROM python:3.8-slim

# Declare build arguments at the top
ARG MODEL_NAME
ARG MODEL_TYPE
ARG MODEL_SERVER_PORT=8000

# Set environment variables using the build arguments
ENV MODEL_NAME=${MODEL_NAME}
ENV MODEL_TYPE=${MODEL_TYPE}
ENV MODEL_SERVER_PORT=${MODEL_SERVER_PORT}

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies that don't change often
RUN pip install --upgrade pip setuptools

# Install model-independent Python packages
RUN pip install flask flask-cors

# Install packages required for model downloading
RUN pip install transformers torch

# Set the working directory
WORKDIR /app

# Copy the model download script first
COPY download_model.py ./

# Download the model during the build process
RUN python download_model.py

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE ${MODEL_SERVER_PORT}

# Start the server
CMD ["python", "model_server.py"]
