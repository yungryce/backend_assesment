# Backend Dockerfile

FROM python:3.10-slim

# Set the working directory for the whole project
WORKDIR /api-flask-backend

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y pkg-config \
                       build-essential \
                       python3-dev \
                       default-libmysqlclient-dev \
                       build-essential \
                       && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=development
ENV APP_ROLE=backend

# Copy the entire project directory (not just backend)
COPY . /api-flask-backend/

# Install dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r backend/requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
