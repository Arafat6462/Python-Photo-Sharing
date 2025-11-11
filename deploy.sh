#!/bin/bash

# Stop on any error
set -e

# 1. Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 2. Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# 3. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment script finished successfully."
