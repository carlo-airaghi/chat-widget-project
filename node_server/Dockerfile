# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify that Node.js and npm are installed
RUN node -v && npm -v

# Set the working directory
WORKDIR /app

# Copy application code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
RUN npm install

# Make start.sh executable
RUN chmod +x start.sh

# Expose the port that the Node.js app listens on
EXPOSE 5000

# Start both the Node.js server and the Python server
CMD ["./start.sh"]
