#!/bin/bash

# Auto-restart script for the video text extractor server
# This will automatically restart the server if it exits

echo "Starting Video Text Extractor with auto-restart..."
echo "Press Ctrl+C to stop the server completely"
echo "Use the 'Restart Server' button in the web interface to restart gracefully"
echo "----------------------------------------"

while true; do
    echo "$(date): Starting server..."
    python3 main.py
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "$(date): Server exited normally, restarting in 2 seconds..."
        sleep 2
    else
        echo "$(date): Server exited with code $exit_code, restarting in 5 seconds..."
        sleep 5
    fi
done