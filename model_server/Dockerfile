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

# Expose port 8000
EXPOSE 8000

# Download the model during the build process
RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('${MODEL_NAME:-gpt2}'); AutoTokenizer.from_pretrained('${MODEL_NAME:-gpt2}')"

# Start the server
CMD ["python", "model_server.py"]
