# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install build tools needed for compiling Python packages like llama-cpp-python
# Using --no-install-recommends reduces the image size by skipping optional packages.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy the backend-specific requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code from the 'backend' subdirectory
COPY backend/ .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# The command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
