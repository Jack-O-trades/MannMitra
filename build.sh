#!/bin/bash

# Install Python packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input