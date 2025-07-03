# 🎬 Video Text Extractor

**AI-powered video transcription with smart summaries in 2 simple steps.**

## ⚡ Quick Start (30 seconds)

```bash
# 1. Start the server
python3 server.py

# 2. Open index.html in your browser
```

**Done!** You now have:
- 🤖 AI transcription (Whisper)
- ⏱️ VTT subtitles with timing
- 🧠 Smart summaries (Llama-4)
- 📺 Support for YouTube, Vimeo, etc.

---

## 📁 What You Get

```
video_text/
├── server.py                  # Complete backend server
├── index.html                 # Web interface with toggle views
├── requirements.txt           # Dependencies (auto-installed)
└── README.md                  # This documentation
```

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

1. **Paste any video URL** (YouTube, Vimeo, etc.)
2. **Click "Extract Text"** and wait ~2 minutes
3. **Switch between views**:
   - 📄 **Transcript**: Clean, readable text
   - ⏱️ **VTT Timing**: Subtitle format with timestamps
   - 📝 **AI Summary**: Key insights and ideas
4. **Copy or download** results as needed

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

**Server won't start?**
```bash
pip install fastapi uvicorn openai-whisper yt-dlp requests
python3 server.py
```

**Red status indicator?**
- Install FFmpeg: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux)
- Check terminal for error messages

**Video processing fails?**
- Try YouTube URLs first (most reliable)
- Ensure video is public and accessible
- First run downloads AI model (~244MB)

---

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