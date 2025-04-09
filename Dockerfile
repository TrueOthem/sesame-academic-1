FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including X11 and GUI libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-tk \
    tk-dev \
    libgl1-mesa-glx \
    xvfb \
    x11-utils \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app \
    FLASK_ENV=development \
    DISPLAY=:99 \
    SKIP_DB_CONNECTION=true \
    JWT_SECRET=test_secret

# Create a non-root user to run the application
RUN useradd -m sesame
RUN chown -R sesame:sesame /app
USER sesame

# Create a script to start Xvfb and run the application
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1024x768x16 &\nsleep 1\nexec "$@"' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run the web interface
CMD ["flask", "run", "--host=0.0.0.0"]
