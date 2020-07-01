# Base image
FROM python:3.7-alpine

# Set up a workdir
WORKDIR /src
COPY app.py /src

# Install dependency
RUN pip install --no-cache-dir requests

