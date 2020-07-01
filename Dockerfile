# Base image
FROM python:3.7-alpine

# Set up a workdir
WORKDIR /src

# Copy source code to the image
COPY . /src

# Container's port
EXPOSE 9000

# Install dependency
RUN pip install -r requirements.txt
