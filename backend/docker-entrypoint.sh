#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status.

# Apply database migrations
echo "Applying database migrations..."
poetry run alembic upgrade head

# Populate initial data
echo "Attempting to populate initial data..."
poetry run python -m app.initial_data
# The script has its own checks to prevent duplicate data, so it's safe to run on every start.
# Alternatively, use a lock file or a DB flag if it should only run once ever.

# Start the main application (Uvicorn server)
# The original CMD from the Dockerfile will be passed as arguments to this script "$@"
echo "Starting application..."
exec "$@"
