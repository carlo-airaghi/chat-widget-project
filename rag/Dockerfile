# Dockerfile for RAG Pipeline

# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run when starting the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
