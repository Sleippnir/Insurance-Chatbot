# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file from the project root into the container
# This requires the build context to be set to the parent directory.
COPY ../requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir reduces the image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code into the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# The command to run the application using uvicorn
# The host 0.0.0.0 makes the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
