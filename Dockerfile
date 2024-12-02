FROM python:3.9-slim

# Install system dependencies for Tkinter and X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variable for display
ENV DISPLAY=:0

# Command to run the application
CMD ["python", "app.py"]
