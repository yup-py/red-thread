FROM apache/airflow:2.8.1-python3.10

USER root
# Install git and basic tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt-get/lists/*

USER airflow

# Copy requirements and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt