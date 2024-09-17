# Frontend Dockerfile

FROM python:3.10-slim

# Set the working directory for the whole project
WORKDIR /api-flask-frontend

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y pkg-config \
                       build-essential \
                       python3-dev \
                       default-libmysqlclient-dev \
                       build-essential \
                       && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV FLASK_APP=frontend/app.py
ENV FLASK_ENV=development
ENV APP_ROLE=frontend

# Copy the entire project directory (not just frontend)
COPY . /api-flask-frontend/

# Install dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r frontend/requirements.txt

# Expose port 5001 for frontend
EXPOSE 5001

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
