# 🎬 Video Text Extractor - Standalone Edition

**Two files. Zero complexity. Maximum power.**

Extract text from any video URL using AI-powered speech recognition with intelligent summaries. This standalone edition contains only the essential files needed to run the complete application.

## 📁 Essential Files Only

```
video_text/
├── simple_server.py           # Complete backend server (auto-installs dependencies)
├── standalone_complete.html   # Complete web interface with demo mode
├── requirements_minimal.txt   # Dependencies list (optional)
└── README_STANDALONE.md       # This file
```

## 🚀 One-Command Start

```bash
# Download the project and run:
python3 simple_server.py
```

**That's it!** The server will:
- ✅ Auto-install missing dependencies 
- ✅ Start on http://localhost:8000
- ✅ Be ready for video processing

Then open `standalone_complete.html` in your browser.

## ✨ Features

- 🤖 **AI Transcription**: OpenAI Whisper for accurate speech-to-text
- 🧠 **AI Summaries**: Llama-4 generates insights and key ideas  
- 📊 **Smart Analysis**: Extracts meaningful insights about life and technology
- ⏱️ **VTT Timing**: Subtitle-ready timestamps
- 🌍 **Multi-Language**: 10+ languages with auto-detection
- 📺 **Wide Support**: YouTube, Vimeo, and many platforms
- 🎯 **Server Status**: Real-time connection monitoring
- 📱 **Demo Mode**: Works offline with simulated results

## 🔧 Prerequisites

- **Python 3.8+** 
- **FFmpeg** (for audio processing)

### Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian  
sudo apt install ffmpeg

# Windows - Download from https://ffmpeg.org/
```

## 📱 How to Use

1. **Start the server**: `python3 simple_server.py`
2. **Open the interface**: Double-click `standalone_complete.html`
3. **Check status**: Green dot = connected, red = demo mode
4. **Paste video URL** and click "Extract Text"
5. **Get transcription + AI summary** with insights and ideas

## 🎛️ What You Get

### Transcription
- Clean formatted text with paragraphs
- Source attribution and language detection
- VTT-style timing for subtitles

### AI Summary  
- **Insights**: Key takeaways and wisdom
- **Ideas**: Interesting concepts identified
- **Social Post**: Ready-to-share content for social media

## 🛠️ Troubleshooting

### Server Won't Start
```bash
# Install dependencies manually if auto-install fails
pip install fastapi uvicorn openai-whisper yt-dlp requests

# Then start server
python3 simple_server.py
```

### Red Status Indicator
- Server not running - check terminal for errors
- FFmpeg not installed - install with your package manager
- Port 8000 in use - stop other services or change port in code

### Video Processing Fails
- Try YouTube URLs first (most reliable)
- Verify video is public and accessible
- Check internet connection for downloads

### No Summary Generated  
- Network issue preventing API access
- Summary generation takes 30-60 seconds
- Check browser console for errors

## 🎯 Example URLs to Test

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://vimeo.com/123456789
```

## 🔒 Privacy & Security

- **Local Processing**: Videos processed on your machine only
- **Temporary Files**: Downloaded videos automatically deleted
- **No Data Storage**: No transcripts stored on external servers  
- **API Usage**: Only summary generation uses external OpenRouter API
- **Open Source**: Complete code transparency

## 📊 Performance

- **First Run**: Downloads Whisper model (~244MB) once
- **Processing Time**: ~1-3 minutes for 10-minute video
- **Languages**: English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese
- **Platforms**: YouTube, Vimeo, Dailymotion, Twitch, Facebook, Instagram, TikTok

## 🆘 Need Help?

1. **Check server status** in the web interface
2. **View terminal output** where you started the server
3. **Try demo mode** first (works without server)
4. **Test with short videos** (under 2 minutes)
5. **Verify FFmpeg** with `ffmpeg -version`

## 🎉 That's It!

This standalone edition gives you the full power of AI video transcription in just two essential files. No complex setup, no multiple interfaces, no confusion.

**Start transcribing videos with AI in under 60 seconds! 🚀**