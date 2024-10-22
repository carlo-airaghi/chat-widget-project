# Dockerfile

# Use the official Python image
FROM python:3.9-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Configure Git Credential Helper
RUN git config --global credential.helper store

# Install Hugging Face CLI and required Python packages
RUN pip install \
    transformers \
    accelerate \
    huggingface_hub \
    fastapi \
    uvicorn[standard] \
    torch \
    python-dotenv

# Use build arguments for the Hugging Face token and model name
ARG HUGGINGFACE_TOKEN
ARG MODEL_NAME

# Log in to Hugging Face and download the model using the token
RUN huggingface-cli login --token "${HUGGINGFACE_TOKEN}" --add-to-git-credential && \
    git lfs install && \
    mkdir /models && \
    cd /models && \
    git clone https://huggingface.co/${MODEL_NAME} || (echo "Model download failed"; exit 1) && \
    huggingface-cli logout

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8500
EXPOSE 8500

# Command to run when starting the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8500"]
