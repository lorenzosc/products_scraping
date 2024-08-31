# Start from a base image with the desired Python version
FROM python:3.11-slim

# Set build variables
ARG AIRFLOW_VERSION=2.7.0
ARG PYTHON_VERSION=3.11
ARG CONSTRAINTS_FILE=https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt


# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow 
ENV PYTHONPATH=/opt/airflow/scraper

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    google-chrome-stable \
    chromium \
    chromium-chromedriver

# Install Airflow
RUN pip install --upgrade pip \
    && pip install apache-airflow==${AIRFLOW_VERSION} \
    --constraint "${CONSTRAINTS_FILE}"

# Copy the requirements file
COPY requirements.txt .

# Install additional Python packages
RUN pip install -r requirements.txt

# Create Airflow directories
RUN mkdir -p ${AIRFLOW_HOME} /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins /opt/airflow/scraper /opt/airflow/data


# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libgconf-2-4 \
    libgbm1 \
    libappindicator3-1 \
    libatspi2.0-0 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxshmfence1 \
    libxi6 \
    libnss3 \
    xdg-utils

# Download and install Google Chrome
RUN curl -sS https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.86/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Set environment variables
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_BIN=/usr/local/bin/chromedriver

# Expose port
EXPOSE 8080

# Default command
CMD ["airflow", "webserver"]
