# 1. Use a slim, official Python image for a smaller attack surface and faster builds
FROM python:3.11-slim

# 2. Set environment variables to prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies (if any, e.g., build tools for certain Python packages)
# For asyncpg (PostgreSQL driver), we need libpq-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy ONLY the requirements file first (leverages Docker build cache)
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. SECURITY BEST PRACTICE: Create a non-root user and switch to it
# Running as root in a container is a major security risk in production
RUN useradd -m -u 1000 appuser
USER appuser

# 8. Copy the rest of the application code
COPY --chown=appuser:appuser . .

# 9. Expose the port the app runs on
EXPOSE 8000

# 10. The command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]