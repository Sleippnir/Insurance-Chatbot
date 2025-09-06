# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the frontend-specific requirements file
COPY frontend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application code from the 'frontend' subdirectory
COPY frontend/ .

# Expose port 8501 for the Streamlit application
EXPOSE 8501

# The command to run the Streamlit application
# The --server.enableCORS=false flag is a good practice for security when not needed.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
