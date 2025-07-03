# 🎬 Video Text Extractor

Extract text from any video URL using AI-powered speech recognition with intelligent summarization. Supports YouTube, Vimeo, and many other platforms with automatic language detection and AI-generated insights.

![Video Text Extractor](https://img.shields.io/badge/AI-Whisper-blue) ![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![LLM](https://img.shields.io/badge/LLM-Llama--4-purple)

## ✨ Features

- 🤖 **AI-Powered Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- 🧠 **AI Summary Generation**: Powered by Llama-4 Maverick via OpenRouter API
- 📊 **Intelligent Insights**: Extracts key ideas, insights, and creates social media posts
- 🌍 **Multi-Language**: Automatic language detection with 10+ language support
- ⏱️ **Timing Information**: VTT-style timestamps for subtitle creation
- 📺 **Wide Platform Support**: YouTube, Vimeo, Dailymotion, Twitch, and more
- 📝 **Smart Formatting**: Automatic paragraphs, titles, and source attribution
- 💾 **History Management**: Save and organize transcription history
- 📋 **Copy Functions**: One-click copy for text and summaries
- 🎯 **Server Status Indicator**: Real-time connection monitoring
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 🚀 **Multiple Interfaces**: Full-featured and standalone versions

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

### Option 1: Instant Launch (Recommended)

```bash
# Clone or download the project
cd video_text

# One-command start (handles everything automatically)
python3 start.py
```

This will:
- ✅ Check virtual environment
- ✅ Activate environment automatically  
- ✅ Start the server on localhost:8000
- ✅ Open your browser automatically

### Option 2: Complete Setup (First Time)

```bash
# Run complete setup if dependencies aren't installed
python3 setup_and_run.py
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies (Whisper, yt-dlp, FastAPI)
- ✅ Start the server
- ✅ Open your browser automatically

### Option 3: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python3 start.py

# 5. Open the web interface
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

1. **Start the application** using `python3 start.py`
2. **Check server status** - Green indicator means connected
3. **Paste a video URL** in the input field (e.g., YouTube link)
4. **Click "Extract Text"** and wait for AI processing
5. **View both transcription and AI summary** with detected language
6. **Copy, save, or download** the results with VTT timing
7. **Toggle between clean and timing formats** for subtitles

### 🎛️ New AI Summary Features

- **📊 Insights Section**: Key takeaways and profound wisdom extracted
- **💡 Ideas Section**: Interesting and surprising concepts identified  
- **📱 Social Media Post**: Ready-to-share Facebook/social content
- **🎯 Specialized Analysis**: Focused on life, technology, and human flourishing topics

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

### 1. **Main Interface** - `index.html`
- Full feature set with transcription and AI summaries
- Server management controls (stop jobs, restart server)
- Sidebar history management
- Real-time progress tracking
- Job cancellation support

### 2. **Standalone Interface** - `standalone.html`
- Complete feature set with enhanced UI
- Server status monitoring with connection indicator
- VTT timing toggle and download
- Demo mode fallback when server is offline
- Advanced copy and save functionality

### 3. **Simple Test Interface** - `simple_test.html`
- Minimal interface for testing
- Step-by-step debugging
- Server health checks

### 4. **Server Test** - `test_server.html`
- Basic server connectivity test
- API health verification

## 🛠️ Troubleshooting

### Server Won't Start
```bash
# Use the recommended starter (auto-handles environment)
python3 start.py

# Or manually check virtual environment
source venv/bin/activate

# Verify dependencies
python -c "import fastapi, whisper, yt_dlp; print('All dependencies OK')"

# Check for port conflicts (kill existing server)
lsof -ti:8000 | xargs kill -9
```

### Browser Shows "Disconnected" Status
- Click the "Check" button to test server connection
- Make sure server is running: http://127.0.0.1:8000/health
- Try restarting with `python3 start.py`
- Check browser console for CORS errors

### Video Download/Extraction Fails
- Verify the video URL is accessible and public
- Some platforms may block downloads or require authentication
- Try with a different video (YouTube usually works best)
- Check that FFmpeg is properly installed

### No Summary Generated
- Summary requires OpenRouter API connection
- Check network connection for LLM access
- Summary generation may take 30-60 seconds
- View browser console for API errors

### Slow Transcription
- First-time Whisper model download takes time (~150MB)
- Longer videos take more time to process
- Consider using shorter test videos first (under 5 minutes)
- Audio extraction and AI processing are CPU-intensive

## 📂 Project Structure

```
video_text/
├── main.py                 # FastAPI backend server with Whisper + LLM
├── index.html              # Main interface with full features
├── standalone.html         # Enhanced interface with server status
├── simple_test.html        # Simple test interface
├── test_server.html        # Server connectivity test
├── setup_and_run.py        # Complete setup script
├── start.py                # Recommended launcher (auto-environment)
├── run.py                  # Alternative launcher
├── launch.py               # Advanced launcher
├── launch.sh               # Shell script launcher
├── restart_server.py       # Server restart wrapper
├── start_with_restart.sh   # Auto-restart shell script
├── requirements.txt        # Python dependencies
├── script.js               # Shared JavaScript components
├── styles.css              # Shared styling
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
- `tiny` - Fastest, least accurate (~39 MB)
- `base` - Good balance (~74 MB) 
- `small` - Better accuracy (~244 MB) **[Currently Used]**
- `medium` - High accuracy (~769 MB)
- `large` - Highest accuracy, slowest (~1550 MB)

### AI Summary Configuration
The LLM summary generation can be customized in `main.py`:
- **Model**: Currently using `meta-llama/llama-4-maverick:free`
- **API**: OpenRouter.ai integration
- **Focus**: Life, technology, consciousness, human flourishing
- **Output**: Insights, ideas, and social media content

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

### Extract Text with AI Summary
```bash
POST http://127.0.0.1:8000/extract-text
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=..."
}

# Response includes:
{
  "text": "Clean formatted transcription...",
  "text_with_timing": "VTT-style with timestamps...",
  "summary": "AI-generated insights and ideas...",
  "language": "English",
  "title": "Video Title",
  "duration": 213.0
}
```

### Debug Endpoints
```bash
# Test video URL validity
POST http://127.0.0.1:8000/test-extract

# Debug with detailed logging  
POST http://127.0.0.1:8000/debug-extract

# Restart server (if using restart wrapper)
POST http://127.0.0.1:8000/restart
```

## 🔒 Privacy & Security

- **Local Processing**: All video processing happens on your machine
- **Temporary Files**: Videos downloaded temporarily, then automatically deleted
- **Local Storage**: Transcriptions saved in browser localStorage only
- **API Usage**: Only summary generation uses external OpenRouter API
- **No Data Retention**: No videos or transcripts stored on external servers
- **Open Source**: All code is transparent and auditable

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🆘 Getting Help

### Quick Diagnostics
1. Run `python3 start.py` for instant launch
2. Check server status indicator in web interface (should be green)
3. Test with `simple_test.html` interface if issues persist  
4. Verify server health at http://127.0.0.1:8000/health

### Common Issues & Solutions
- **Import errors**: Run `python3 setup_and_run.py` to install dependencies
- **"Disconnected" status**: Server not running - use `python3 start.py`
- **FFmpeg errors**: Install FFmpeg (`brew install ffmpeg` on macOS)
- **No summary**: Network issue or OpenRouter API limit reached
- **Slow first run**: Normal - Whisper model downloads ~244MB initially

### Still Need Help?
1. **Check browser console** (F12) for JavaScript errors
2. **Look at terminal logs** where you started the server
3. **Try different interfaces**: start with `simple_test.html`
4. **Test with shorter videos** first (under 2 minutes)
5. **Verify prerequisites**: Python 3.8+, FFmpeg, internet connection

---

**🎉 Enjoy extracting text from videos with AI!**