#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Build React frontend if package.json exists
if [ -f "frontend/package.json" ]; then
    echo "Building React frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
fi

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
