# Use the official Python image as the base
FROM python:3.8-slim

# Install git (if required by any packages)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port specified in the environment or default to 8000
ARG MODEL_SERVER_PORT=8000
EXPOSE ${MODEL_SERVER_PORT}

# Set environment variables (if needed)
ENV MODEL_NAME=${MODEL_NAME}
ENV MODEL_TYPE=${MODEL_TYPE}
ENV MODEL_SERVER_PORT=${MODEL_SERVER_PORT}

# Download the model during the build process
RUN python -c "\
import os; \
from transformers import AutoModelForCausalLM, AutoModelForMaskedLM, AutoTokenizer; \
model_name = os.getenv('MODEL_NAME'); \
model_type = os.getenv('MODEL_TYPE'); \
if not model_name or not model_type: \
    raise ValueError('MODEL_NAME and MODEL_TYPE must be set'); \
tokenizer = AutoTokenizer.from_pretrained(model_name); \
if model_type == 'causal': \
    AutoModelForCausalLM.from_pretrained(model_name); \
elif model_type == 'masked': \
    AutoModelForMaskedLM.from_pretrained(model_name); \
else: \
    raise ValueError('Invalid MODEL_TYPE');"

# Start the server
CMD ["python", "model_server.py"]
