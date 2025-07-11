#!/usr/bin/env python3
"""
Minimal Video Text Extractor Server
Essential backend for video transcription with AI summaries.
"""

import os
import sys
import tempfile
import logging
from pathlib import Path
import subprocess
import shutil

# Check dependencies and provide helpful guidance
def check_dependencies():
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn', 
        'faster_whisper': 'faster-whisper',
        'yt_dlp': 'yt-dlp',
        'requests': 'requests'
    }
    
    missing_packages = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages!")
        print(f"Please install: {', '.join(missing_packages)}")
        print("\n🔧 Installation options:")
        print("1. Use existing virtual environment:")
        print("   source venv/bin/activate")
        print(f"   pip install {' '.join(missing_packages)}")
        print("\n2. Create new virtual environment:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print(f"   pip install {' '.join(missing_packages)}")
        print("\n3. System install (not recommended):")
        print(f"   pip install --user {' '.join(missing_packages)}")
        return False
    return True

# Check dependencies 
if not check_dependencies():
    sys.exit(1)

# Now import the packages
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
from faster_whisper import WhisperModel
import requests
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Video Text Extractor", description="AI-powered video transcription")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_url: str

class TranscriptionResponse(BaseModel):
    text: str
    text_with_timing: str
    summary: str
    language: str
    title: str
    duration: float

# Global model variable
model = None

def load_whisper_model():
    global model
    if model is None:
        logger.info("Loading Faster-Whisper model (small)...")
        try:
            logger.info("Downloading Faster-Whisper model (this may take a few minutes on first run)...")
            model = WhisperModel("small", device="cpu", compute_type="int8")
            logger.info("Faster-Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    return model

def extract_audio_from_video(video_url: str) -> tuple[str, str, float]:
    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_audio.close()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_file = os.path.join(temp_dir, 'audio.%(ext)s')
            
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': audio_file,
                'noplaylist': True,
                'extractaudio': True,
                'audioformat': 'wav',
                'audioquality': '192K',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'prefer_ffmpeg': True,
                'keepvideo': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Downloading audio from: {video_url}")
                info = ydl.extract_info(video_url, download=True)
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                
                # Find extracted audio file
                extracted_file = None
                for file in os.listdir(temp_dir):
                    if file.endswith('.wav'):
                        extracted_file = os.path.join(temp_dir, file)
                        break
                
                if extracted_file:
                    shutil.copy2(extracted_file, temp_audio.name)
                    logger.info(f"Audio extracted: {temp_audio.name}")
                    return temp_audio.name, title, duration
                else:
                    raise Exception("No audio file found after extraction")
                
    except Exception as e:
        if os.path.exists(temp_audio.name):
            os.unlink(temp_audio.name)
        logger.error(f"Error extracting audio: {str(e)}")
        raise

def transcribe_audio(audio_path: str) -> tuple[str, str]:
    model = load_whisper_model()
    
    try:
        segments, info = model.transcribe(audio_path, language=None)
        
        # Combine all segments into full transcription
        transcription = ""
        for segment in segments:
            transcription += segment.text + " "
        
        detected_language = info.language
        
        language_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese'
        }
        
        language_display = language_names.get(detected_language, detected_language.upper())
        return transcription.strip(), language_display
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise

def format_transcription_clean(raw_text: str, title: str, video_url: str, language: str) -> str:
    if not raw_text.strip():
        return "No speech detected in this video."
    
    # Clean and format text
    text = raw_text.strip()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Group into paragraphs
    paragraphs = []
    current_paragraph = []
    
    for i, sentence in enumerate(sentences):
        current_paragraph.append(sentence)
        
        if (len(current_paragraph) >= 3 or len(sentence) > 100 or i == len(sentences) - 1):
            paragraph_text = '. '.join(current_paragraph)
            if paragraph_text:
                paragraphs.append(paragraph_text + '.')
            current_paragraph = []
    
    if not paragraphs:
        paragraphs = [text]
    
    # Format output
    clean_title = title.replace('[', '').replace(']', '').strip()
    if len(clean_title) > 80:
        clean_title = clean_title[:77] + "..."
    
    formatted_output = f"""# {clean_title}

**Source:** {video_url}
**Language:** {language}

---

"""
    
    for i, paragraph in enumerate(paragraphs):
        formatted_output += paragraph.strip()
        if i < len(paragraphs) - 1:
            formatted_output += "\n\n"
    
    return formatted_output

def format_transcription_with_timing(raw_text: str, title: str, video_url: str, language: str, duration: float) -> str:
    """Generate standard SRT format for direct use in video programs - PURE SRT ONLY"""
    logger.info(f"DEBUG: Received raw_text: '{raw_text[:200]}...'")
    
    if not raw_text.strip():
        return "1\n00:00:00,000 --> 00:00:05,000\nNo speech detected in this video."
    
    # Clean ONLY the pure spoken text from Whisper - remove any headers/metadata that might be added
    text = raw_text.strip()
    
    # Remove any potential headers or metadata (in case they got mixed in)
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        # Skip lines that look like headers or metadata
        if (not line.startswith('#') and 
            not line.startswith('**') and 
            not 'Source:' in line and 
            not 'Language:' in line and 
            not 'Duration:' in line and 
            not line.startswith('---') and
            line):
            clean_lines.append(line)
    
    # Join the clean text
    text = ' '.join(clean_lines).strip()
    
    logger.info(f"DEBUG: Cleaned text: '{text[:200]}...'")
    
    if not text:
        return "1\n00:00:00,000 --> 00:00:05,000\nNo valid text found."
    
    # Split into sentences for timing - use shorter segments for better readability
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    if not sentences:
        # If no sentences found, use the whole text as one subtitle
        sentences = [text]
    
    logger.info(f"DEBUG: Found {len(sentences)} sentences")
    
    # Calculate timing
    total_sentences = len(sentences)
    time_per_sentence = duration / total_sentences if duration > 0 else 5
    
    def format_srt_time(seconds):
        """Format time for SRT: HH:MM:SS,mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')
    
    # Generate SRT content with proper numbering
    srt_content = ""
    
    current_time = 0
    for i, sentence in enumerate(sentences, 1):
        start_time = current_time
        end_time = current_time + time_per_sentence
        
        # Standard SRT format: number, timing, text, blank line
        srt_content += f"{i}\n"
        srt_content += f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}\n"
        srt_content += f"{sentence.strip()}\n\n"
        
        current_time = end_time
    
    final_srt = srt_content.rstrip()
    logger.info(f"DEBUG: Final SRT preview: '{final_srt[:300]}...'")
    
    return final_srt

def generate_summary(transcript: str, title: str) -> str:
    try:
        api_key = "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"
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        model = "meta-llama/llama-4-maverick:free"
        
        # Clean transcript
        clean_text = re.sub(r'\*\*.*?\*\*', '', transcript)
        clean_text = re.sub(r'#.*?\n', '', clean_text)
        clean_text = re.sub(r'---.*?\n', '', clean_text)
        clean_text = clean_text.strip()
        
        if len(clean_text) > 3000:
            clean_text = clean_text[:3000] + "..."
        
        prompt = f"""Extract insights from this video content. Focus on meaningful ideas about life, technology, learning, and human potential.

Create a structured summary with:
1. A 25-word summary of the main topic
2. 3-5 key insights (15 words each)
3. 5-8 interesting ideas (15 words each)
4. A 250-word engaging social media post

Video: "{title}"
Content: {clean_text}

Format as:
*SUMMARY
[25 words]

*INSIGHTS
• [insight 1]
• [insight 2]
...

*IDEAS  
• [idea 1]
• [idea 2]
...

[Social media post with emojis and engaging tone]"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You extract meaningful insights from content about life, technology, and human flourishing."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        return f"Summary unavailable: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Video Text Extractor API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/extract-text", response_model=TranscriptionResponse)
async def extract_text(request: VideoRequest):
    try:
        logger.info(f"Processing video URL: {request.video_url}")
        
        # Extract audio
        logger.info("Extracting audio from video...")
        audio_path, title, duration = extract_audio_from_video(request.video_url)
        
        try:
            # Transcribe audio
            logger.info("Starting transcription...")
            raw_transcription, language = transcribe_audio(audio_path)
        finally:
            # Clean up temp file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
        
        # Format transcriptions
        clean_transcription = format_transcription_clean(
            raw_transcription, title, request.video_url, language
        )
        
        timing_transcription = format_transcription_with_timing(
            raw_transcription, title, request.video_url, language, duration or 0
        )
        
        # Debug: check what we're actually generating
        logger.info(f"Raw Whisper text: {raw_transcription[:100]}...")
        logger.info(f"SRT content preview: {timing_transcription[:200]}...")
        
        # Generate summary
        logger.info("Generating summary...")
        summary = generate_summary(clean_transcription, title)
        
        logger.info("Transcription completed successfully")
        
        return TranscriptionResponse(
            text=clean_transcription,
            text_with_timing=timing_transcription,
            summary=summary,
            language=language,
            title=title,
            duration=duration or 0
        )
        
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to download video: {str(e)}")
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Video Text Extractor API...")
    print("\n🎬 Video Text Extractor Server")
    print("=" * 30)
    print("✅ Server starting on http://localhost:8000")
    print("✅ Open index.html in your browser")
    print("✅ Press Ctrl+C to stop")
    print()
    
    # Preload model at startup to avoid timeout during first request
    logger.info("Preloading Faster-Whisper model...")
    try:
        load_whisper_model()
        print("✅ Model preloaded successfully")
    except Exception as e:
        print(f"❌ Failed to preload model: {e}")
        print("Model will be loaded on first transcription request")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")