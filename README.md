# 🎬 Video Text Extractor

Extract text from any video URL using AI-powered speech recognition. Supports YouTube, Vimeo, and many other platforms with automatic language detection.

![Video Text Extractor](https://img.shields.io/badge/AI-Whisper-blue) ![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## ✨ Features

- 🤖 **AI-Powered**: Uses OpenAI Whisper for accurate transcription
- 🌍 **Multi-Language**: Automatic language detection (optimized for English/Spanish)
- 📺 **Wide Support**: YouTube, Vimeo, Dailymotion, Twitch, and more
- 📝 **Smart Formatting**: Automatic paragraphs, titles, and source attribution
- 💾 **History**: Save and manage transcription history
- 📋 **Copy Function**: One-click copy to clipboard
- 📱 **Responsive**: Works on desktop and mobile
- 🚀 **Self-Contained**: Single HTML file with embedded CSS/JS

## 🔧 Prerequisites

- **Python 3.8+**
- **FFmpeg** (for audio processing)

### Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## 🚀 Quick Start

### Option 1: One-Click Setup (Recommended)

```bash
# Clone or download the project
cd video_text

# Run the complete setup and launcher
python3 setup_and_run.py
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start the server
- ✅ Open your browser automatically

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install PyTorch (CPU version)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 4. Install other dependencies
pip install fastapi uvicorn python-multipart openai-whisper yt-dlp python-dotenv requests

# 5. Start the server
python main.py

# 6. Open the web interface
open standalone.html  # Or double-click the file
```

### Option 3: With Auto-Restart (Recommended for Development)

```bash
# Start with Python auto-restart wrapper
python3 restart_server.py

# OR use the shell script (macOS/Linux)
./start_with_restart.sh
```

This enables the "Restart Server" button to work automatically!

### Option 4: Quick Shell Script (macOS/Linux)

```bash
./launch.sh
```

## 📱 How to Use

1. **Start the application** using any of the methods above
2. **Paste a video URL** in the input field (e.g., YouTube link)
3. **Click "Extract Text"** and wait for processing
4. **View the transcription** with detected language
5. **Copy or save** the results to your history

### 🎛️ Control Buttons

- **Stop Job**: Cancel current video processing (red button)
- **Restart Server**: Restart the backend server (orange button) - *requires auto-restart mode*
- **Clear All**: Remove all saved transcriptions (red button)

### Example URLs to Test:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://vimeo.com/123456789
```

## 🎯 Available Interfaces

The project includes multiple interfaces for different needs:

### 1. **Full Interface** - `standalone.html`
- Complete feature set with sidebar history
- Responsive design
- Local storage for transcriptions
- Copy functionality

### 2. **Simple Test Interface** - `simple_test.html`
- Minimal interface for testing
- Step-by-step debugging
- Server health checks

### 3. **Server Test** - `test_server.html`
- Basic server connectivity test
- API health verification

## 🛠️ Troubleshooting

### Server Won't Start
```bash
# Check if virtual environment is activated
source venv/bin/activate

# Verify dependencies
python -c "import fastapi, whisper, yt_dlp; print('All dependencies OK')"

# Check for port conflicts
lsof -i :8000
```

### Browser Can't Connect
- Make sure server is running: http://127.0.0.1:8000/health
- Try the simple test interface first
- Check browser console for CORS errors

### Video Download Fails
- Verify the video URL is accessible
- Some platforms may block downloads
- Try a different video or platform

### Slow Transcription
- First-time model download takes time
- Longer videos take more time to process
- Consider using shorter test videos first

## 📂 Project Structure

```
video_text/
├── main.py                 # FastAPI backend server
├── standalone.html         # Full web interface
├── simple_test.html        # Simple test interface
├── test_server.html        # Server connectivity test
├── setup_and_run.py        # Complete setup script
├── launch.py               # Advanced launcher
├── launch.sh               # Shell script launcher
├── start.py                # Simple starter
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Server Settings
Edit `main.py` to modify:
- **Port**: Change `port=8000` to desired port
- **Host**: Modify `host="127.0.0.1"` for network access
- **Model**: Change `whisper.load_model("base")` for different accuracy

### Whisper Models
Available models (larger = more accurate but slower):
- `tiny` - Fastest, least accurate
- `base` - Good balance (default)
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Highest accuracy, slowest

## 🌐 Supported Platforms

- YouTube (`youtube.com`, `youtu.be`)
- Vimeo (`vimeo.com`)
- Dailymotion (`dailymotion.com`)
- Twitch (`twitch.tv`)
- Facebook (`facebook.com`)
- Instagram (`instagram.com`)
- TikTok (`tiktok.com`)
- And many more via yt-dlp

## 🤝 API Endpoints

### Health Check
```bash
GET http://127.0.0.1:8000/health
```

### Test Video URL
```bash
POST http://127.0.0.1:8000/test-extract
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=..."
}
```

### Extract Text
```bash
POST http://127.0.0.1:8000/extract-text
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=..."
}
```

## 🔒 Privacy & Security

- **No data collection**: All processing is local
- **No cloud services**: Videos processed on your machine
- **Local storage**: Transcriptions saved in browser only
- **No video storage**: Videos are downloaded temporarily and deleted

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🆘 Getting Help

### Quick Diagnostics
1. Run `python3 setup_and_run.py` for complete setup
2. Test with `simple_test.html` interface
3. Check server health at http://127.0.0.1:8000/health

### Common Issues
- **Import errors**: Virtual environment not activated
- **FFmpeg errors**: FFmpeg not installed or not in PATH
- **Network errors**: Firewall blocking connections
- **Slow processing**: Normal for first run (model download)

### Still Need Help?
1. Check the browser console for errors
2. Look at server logs in terminal
3. Try the test interfaces to isolate issues
4. Verify all prerequisites are installed

---

**🎉 Enjoy extracting text from videos with AI!**