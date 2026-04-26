#!/bin/bash
set -x

echo "Python version:"
python --version

echo "Current directory:"
pwd

echo "Listing files:"
ls -R

echo "Starting app..."
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
