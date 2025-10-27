#!/bin/bash
# Start the FastAPI backend and the real-time fetcher

# Start the fetcher in the background
python /app/fetch_realtime.py &

# Start the main FastAPI application
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

