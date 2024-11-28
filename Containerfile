# Multi-stage Containerfile for FastAPI

# Stage 1: Builder stage
FROM python:3.11.1-slim AS builder

# Set up a non-root user
#RUN groupadd -r fastapi && useradd --no-log-init -r -g fastapi fastapi

# Set the working directory
#WORKDIR app

# Install dependencies with a lower privilege level, and remove build dependencies
COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && pip install --no-cache-dir --upgrade -r requirements.txt 
#    && apt-get purge -y --auto-remove gcc \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# Copy application code
#COPY app app

# Stage 2: Final, minimal image
FROM python:3.11.1-slim

# Set up working directory
WORKDIR app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=app

# Set up a non-root user and group
RUN groupadd -r fastapi && useradd --no-log-init -r -g fastapi fastapi

# Copy only application related code from the builder stage to the final stage
COPY app app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Default PostgreSQL environment variables
ENV POSTGRES_DB=book
ENV POSTGRES_USER=book_user
ENV POSTGRES_PASSWORD=bookp_pass
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432
ENV POSTGRES_SCHEMA=bookstore

# Change ownership to the non-root user and restrict permissions
RUN chown -R fastapi:fastapi app && chmod -R 755 app

# Switch to non-root user
USER fastapi

# Expose the port for FastAPI
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
