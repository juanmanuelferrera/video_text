from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import tempfile
import os
import whisper
import logging
from pathlib import Path
import uvicorn
import traceback
import requests
import re
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Video Text Extractor", description="Extract text from video URLs using OpenAI Whisper")

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

model = None

def load_whisper_model():
    global model
    if model is None:
        logger.info("Loading whisper model (small for optimal speed/quality ratio)...")
        try:
            model = whisper.load_model("small")  # Optimal speed/quality ratio
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    return model

def extract_audio_from_video(video_url: str) -> tuple[str, str, float]:
    # Create a named temporary file that persists until we're done with it
    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_audio.close()
    
    try:
        # First download to temporary directory, then copy to persistent file
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
                logger.info(f"Downloading and extracting audio from: {video_url}")
                info = ydl.extract_info(video_url, download=True)
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                
                # Find the extracted audio file
                extracted_file = None
                for file in os.listdir(temp_dir):
                    if file.endswith('.wav'):
                        extracted_file = os.path.join(temp_dir, file)
                        break
                
                # If no .wav file, look for other audio formats and convert
                if not extracted_file:
                    for file in os.listdir(temp_dir):
                        if any(file.endswith(ext) for ext in ['.m4a', '.mp3', '.webm', '.ogg']):
                            input_path = os.path.join(temp_dir, file)
                            
                            # Use FFmpeg to convert to WAV
                            import subprocess
                            cmd = [
                                'ffmpeg', '-i', input_path, 
                                '-acodec', 'pcm_s16le', 
                                '-ar', '16000', 
                                '-ac', '1', 
                                temp_audio.name, '-y'
                            ]
                            
                            result = subprocess.run(cmd, capture_output=True, text=True)
                            if result.returncode == 0 and os.path.exists(temp_audio.name):
                                logger.info(f"Audio converted successfully: {temp_audio.name}")
                                return temp_audio.name, title, duration
                            else:
                                logger.error(f"FFmpeg conversion failed: {result.stderr}")
                            break
                else:
                    # Copy the extracted WAV file to our persistent location
                    import shutil
                    shutil.copy2(extracted_file, temp_audio.name)
                    logger.info(f"Audio extracted successfully: {temp_audio.name}")
                    return temp_audio.name, title, duration
                
                raise Exception("No audio file found after extraction and conversion attempts")
                
    except Exception as e:
        # Clean up the temp file if there was an error
        if os.path.exists(temp_audio.name):
            os.unlink(temp_audio.name)
        logger.error(f"Error extracting audio: {str(e)}")
        raise

def transcribe_audio(audio_path: str) -> tuple[str, str]:
    model = load_whisper_model()
    
    try:
        result = model.transcribe(audio_path, language=None)
        
        transcription = result["text"]
        detected_language = result["language"]
        
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
        
        language_display = language_names.get(detected_language, detected_language.upper())
        
        return transcription.strip(), language_display
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise

def format_transcription_clean(raw_text: str, title: str, video_url: str, language: str) -> str:
    """Format transcription with proper paragraphs, title, and source (clean version)"""
    
    if not raw_text.strip():
        return "No speech detected in this video."
    
    # Clean up the raw text
    text = raw_text.strip()
    
    # Split into sentences based on punctuation and natural breaks
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Group sentences into logical paragraphs
    paragraphs = []
    current_paragraph = []
    
    for i, sentence in enumerate(sentences):
        current_paragraph.append(sentence)
        
        # Start new paragraph based on:
        # - Every 3-4 sentences
        # - Topic changes (basic heuristic)
        # - Long sentences
        if (len(current_paragraph) >= 3 or 
            len(sentence) > 100 or 
            i == len(sentences) - 1):
            
            paragraph_text = '. '.join(current_paragraph)
            if paragraph_text:
                paragraphs.append(paragraph_text + '.')
            current_paragraph = []
    
    # If no paragraphs were created, use the original text
    if not paragraphs:
        paragraphs = [text]
    
    # Clean up title
    clean_title = title.replace('[', '').replace(']', '').strip()
    if len(clean_title) > 80:
        clean_title = clean_title[:77] + "..."
    
    # Format the final output (clean version)
    formatted_output = f"""# {clean_title}

**Source:** {video_url}

---

"""
    
    # Add paragraphs with proper spacing
    for i, paragraph in enumerate(paragraphs):
        formatted_output += paragraph.strip()
        if i < len(paragraphs) - 1:  # Don't add extra line after last paragraph
            formatted_output += "\n\n"
    
    return formatted_output

def format_transcription_with_timing(raw_text: str, title: str, video_url: str, language: str, duration: float) -> str:
    """Format transcription with VTT-style timing"""
    
    if not raw_text.strip():
        return "No speech detected in this video."
    
    # Clean up the raw text
    text = raw_text.strip()
    
    # Split into sentences
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Clean up title
    clean_title = title.replace('[', '').replace(']', '').strip()
    if len(clean_title) > 80:
        clean_title = clean_title[:77] + "..."
    
    # Calculate timing for each sentence
    total_sentences = len(sentences)
    if total_sentences == 0:
        return text
    
    time_per_sentence = duration / total_sentences if duration > 0 else 5
    
    def format_time(seconds):
        """Format seconds to MM:SS format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    # Format with VTT-style timing
    formatted_output = f"""# {clean_title}

**Source:** {video_url}
**Duration:** {format_time(duration)}

---

"""
    
    current_time = 0
    for i, sentence in enumerate(sentences):
        start_time = current_time
        end_time = current_time + time_per_sentence
        
        formatted_output += f"[{format_time(start_time)} --> {format_time(end_time)}]\n"
        formatted_output += f"{sentence.strip()}.\n\n"
        
        current_time = end_time
    
    return formatted_output

def generate_summary(transcript: str, title: str) -> str:
    """Generate a summary using OpenRouter AI with Llama-4 Maverick"""
    try:
        # OpenRouter API configuration
        api_key = "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"
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        model = "meta-llama/llama-4-maverick:free"
        
        # Clean transcript for summary
        clean_text = re.sub(r'\*\*.*?\*\*', '', transcript)  # Remove markdown
        clean_text = re.sub(r'#.*?\n', '', clean_text)       # Remove headers
        clean_text = re.sub(r'---.*?\n', '', clean_text)     # Remove separators
        clean_text = clean_text.strip()
        
        # Limit text length for API
        if len(clean_text) > 3000:
            clean_text = clean_text[:3000] + "..."
        
        prompt = f"""You extract surprising, powerful, and interesting insights from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

You create 15 word bullet points that capture the most important insights from the input.

Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

STEPS

Extract 3 to 10 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS, and write them on a virtual whiteboard in your mind using 15 word bullets. If there are less than 10 then collect all of them. Make sure you extract at least 3.

From those IDEAS, extract the most powerful and insightful of them and write them in a section called INSIGHTS. Make sure you extract at least 3 and up to 5.

OUTPUT INSTRUCTIONS

INSIGHTS are essentially higher-level IDEAS that are more abstracted and wise.

Extract a summary of the content in 25 words, including who is presenting and the content being discussed into a section called SUMMARY.

Output the SUMMARY first, then INSIGHTS, then IDEAS section.
Output in org-mode format.
Each bullet should be 15 words in length.
Do not give warnings or notes; only output the requested sections.
Sections start with * so they become headings in org-mode.
Do not start items with the same opening words.
After having all the text, make a 250 word post with a proper title with emojis, made by a vaishnava devotee. Keep it informative style for the average facebook user.
Ensure you follow ALL these instructions when creating your output.

Video title: "{title}"
Transcript content:

{clean_text}"""

        # Prepare the request payload
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert insight extractor who specializes in finding profound wisdom from content related to life, consciousness, technology, and human flourishing."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        # Make request to OpenRouter API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Video Text Extractor"
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        summary = result["choices"][0]["message"]["content"].strip()
        return summary
        
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        return f"Summary unavailable: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Video Text Extractor API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/restart")
async def restart_server():
    """Restart the server gracefully"""
    try:
        import asyncio
        import signal
        import sys
        
        async def shutdown_server():
            await asyncio.sleep(0.5)
            # Send shutdown signal
            if hasattr(signal, 'SIGTERM'):
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                sys.exit(0)
        
        # Schedule the shutdown
        asyncio.create_task(shutdown_server())
        
        return {"status": "restarting", "message": "Server is restarting..."}
    except Exception as e:
        logger.error(f"Restart error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to restart: {str(e)}")

@app.post("/debug-extract")
async def debug_extract(request: VideoRequest):
    """Debug endpoint with step-by-step logging"""
    try:
        logger.info(f"DEBUG: Starting extraction for {request.video_url}")
        
        # Step 1: Test Whisper model loading
        try:
            logger.info("DEBUG: Loading Whisper model...")
            model = load_whisper_model()
            logger.info(f"DEBUG: Model loaded successfully: {type(model)}")
        except Exception as e:
            return {"error": f"Model loading failed: {str(e)}", "step": "model_loading"}
        
        # Step 2: Test audio extraction
        try:
            logger.info("DEBUG: Starting audio extraction...")
            with tempfile.TemporaryDirectory() as temp_dir:
                # Simple yt-dlp download
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
                    'quiet': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(request.video_url, download=True)
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    
                    # Find downloaded file
                    files = os.listdir(temp_dir)
                    if not files:
                        return {"error": "No files downloaded", "step": "download"}
                    
                    audio_file = os.path.join(temp_dir, files[0])
                    logger.info(f"DEBUG: Downloaded {audio_file}, size: {os.path.getsize(audio_file)} bytes")
                    
                    # Step 3: Test transcription with very short audio
                    try:
                        logger.info("DEBUG: Starting transcription...")
                        result = model.transcribe(audio_file, language='en')
                        text = result.get("text", "").strip()
                        detected_lang = result.get("language", "unknown")
                        
                        return {
                            "success": True,
                            "title": title,
                            "duration": duration,
                            "text": text,
                            "language": detected_lang,
                            "audio_file_size": os.path.getsize(audio_file)
                        }
                    except Exception as e:
                        return {"error": f"Transcription failed: {str(e)}", "step": "transcription"}
                        
        except Exception as e:
            return {"error": f"Audio extraction failed: {str(e)}", "step": "audio_extraction"}
            
    except Exception as e:
        logger.error(f"DEBUG: Unexpected error: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}", "step": "unknown"}

@app.post("/test-extract")
async def test_extract(request: VideoRequest):
    """Test endpoint that shows detailed error information"""
    try:
        logger.info(f"TEST: Processing video URL: {request.video_url}")
        
        # Test yt-dlp without download first
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(request.video_url, download=False)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                formats = len(info.get('formats', []))
                
                return {
                    "status": "success",
                    "title": title,
                    "duration": duration,
                    "available_formats": formats,
                    "video_info": {
                        "id": info.get('id'),
                        "uploader": info.get('uploader'),
                        "view_count": info.get('view_count')
                    }
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/extract-text", response_model=TranscriptionResponse)
async def extract_text(request: VideoRequest):
    try:
        logger.info(f"Processing video URL: {request.video_url}")
        
        # Extract audio from video
        logger.info("Extracting audio from video...")
        audio_path, title, duration = extract_audio_from_video(request.video_url)
        
        try:
            # Transcribe the audio
            logger.info("Starting transcription...")
            raw_transcription, language = transcribe_audio(audio_path)
        finally:
            # Clean up the temporary audio file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
        
        # Format the transcription in both versions
        clean_transcription = format_transcription_clean(
            raw_transcription, title, request.video_url, language
        )
        
        timing_transcription = format_transcription_with_timing(
            raw_transcription, title, request.video_url, language, duration or 0
        )
        
        # Generate summary
        logger.info("Generating summary...")
        summary = generate_summary(clean_transcription, title)
        
        logger.info("Transcription completed and formatted successfully")
        
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
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Video Text Extractor API...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")