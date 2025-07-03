#!/bin/bash

# Video Text Extractor - Quick Launcher
# This script starts the server and opens the web interface

echo "🎬 Video Text Extractor - Quick Launcher"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Setting up virtual environment..."
    python3 -m venv venv
    
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    
    # Install PyTorch first
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    
    # Install other dependencies
    pip install fastapi uvicorn python-multipart openai-whisper yt-dlp python-dotenv requests
    
    echo "✅ Setup complete!"
fi

# Activate virtual environment
source venv/bin/activate

# Start server in background
echo "🚀 Starting backend server..."
python main.py &
SERVER_PID=$!

# Wait a moment for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Server is ready!"
    
    # Open web interface
    echo "🌐 Opening web interface..."
    
    # Try different commands based on OS
    if command -v open > /dev/null 2>&1; then
        # macOS
        open standalone.html
    elif command -v xdg-open > /dev/null 2>&1; then
        # Linux
        xdg-open standalone.html
    elif command -v start > /dev/null 2>&1; then
        # Windows (if running in WSL or Git Bash)
        start standalone.html
    else
        echo "Please manually open standalone.html in your browser"
    fi
    
    echo ""
    echo "🎉 Video Text Extractor is now running!"
    echo "📋 Instructions:"
    echo "   • Paste any video URL in the input field"
    echo "   • Click 'Extract Text' to transcribe"
    echo "   • Use the sidebar to save/load transcriptions"
    echo "   • Press Ctrl+C to stop the server"
    echo ""
    echo "💡 Server: http://localhost:8000"
    echo "🌐 Web interface opened in your browser"
    echo ""
    echo "Press Ctrl+C to stop..."
    
    # Wait for Ctrl+C
    trap "echo ''; echo '🛑 Stopping server...'; kill $SERVER_PID; exit 0" INT
    wait $SERVER_PID
else
    echo "❌ Server failed to start"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi