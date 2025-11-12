#!/bin/bash

# --- DEBUGGING START ---
echo "--- DEBUGGING DEPLOYMENT SCRIPT ---"
echo "AZURE_POSTGRESQL_CONNECTIONSTRING: $AZURE_POSTGRESQL_CONNECTIONSTRING"
echo "SECRET: $SECRET"
echo "--- END DEBUGGING ---"

# Stop on any error
set -e

# 1. Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# 2. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment script finished successfully."
