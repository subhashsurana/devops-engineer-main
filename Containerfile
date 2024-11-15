# Dockerfile for FastAPI
FROM python:3.11.1-slim as builder

# Set up a non-root user and group
RUN groupadd -r fastapi && useradd --no-log-init -r -g fastapi fastapi

# Set up working directory
WORKDIR app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=app

# Install dependencies with a lower privilege level, and remove build dependencies
COPY requirements.txt app/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && pip install --no-cache-dir --upgrade -r app/requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY /app app

# Change ownership to the non-root user and restrict permissions
RUN chown -R fastapi:fastapi app && chmod -R 755 app

# Switch to non-root user
USER fastapi

# Expose the port for FastAPI
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]