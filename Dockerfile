# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run tests
CMD ["python", "-m", "unittest", "discover", "-s", "tests"]

