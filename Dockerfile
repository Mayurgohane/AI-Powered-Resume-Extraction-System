FROM python:3.8-slim-buster

# Expose the port for Streamlit
EXPOSE 8501

# Install system dependencies (and update pip)
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your app into the container
COPY . /app

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
