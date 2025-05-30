# 1. Base image for installing dependencies with Poetry
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install project dependencies (without dev dependencies)
RUN poetry install --no-dev --no-interaction --no-ansi

# 2. Base image for running the application
FROM python:3.11-slim
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Copy virtual environment from builder stage (if poetry created one there - adjust if using system python)
# Since POETRY_VIRTUALENVS_CREATE=false, dependencies were installed into the system site-packages of the builder.
# We need to copy those installed packages.
# A more robust way is to copy the installed packages from the builder's site-packages.
# However, an easier approach for now is to re-run poetry install in this stage,
# but using the lock file and copying the source code.
# For a truly minimal image, one would copy only the installed packages from the builder.

# Copy poetry files and install dependencies
COPY --chown=app:app pyproject.toml poetry.lock ./
# Re-install poetry in this stage to run `poetry install`
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    poetry install --no-dev --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Expose port 8000
EXPOSE 8000

# Copy the entrypoint script and make it executable
COPY --chown=app:app ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Command to run Uvicorn (will be passed to the entrypoint script)
# Ensure the path to main:app is correct based on your directory structure inside backend/
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
