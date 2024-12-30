# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy backend files
COPY backend/ /app/backend/

# Copy frontend files
COPY frontend/ /app/frontend/

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Expose the port
EXPOSE 5000

# Environment variable to disable buffering for better logging
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "/app/backend/app.py"]
