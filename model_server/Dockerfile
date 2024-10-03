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

# Install git (if required by any packages)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE ${MODEL_SERVER_PORT}

# Run the model download script
RUN python download_model.py

# Start the server
CMD ["python", "model_server.py"]
