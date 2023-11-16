# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy your Python application and requirements.txt to the container
COPY python/app.py .
COPY python/requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "app.py"]
