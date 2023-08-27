# Use an official Python runtime as a parent image
FROM python:3.8-slim

WORKDIR /Site

COPY requirements.txt /Site/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container at /app
COPY . /Site/

# Set environment variable for Celery to discover tasks
ENV C_FORCE_ROOT="true"

# Define the command to run your Celery worker
CMD ["celery", "-A", "run.celery", "worker", "--pool=solo", "--loglevel=info"]
