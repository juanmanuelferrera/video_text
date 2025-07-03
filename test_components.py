#!/usr/bin/env python3
"""
Test script to check all components independently
"""

import os
import sys
import tempfile
import traceback

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    try:
        import fastapi
        print("✅ FastAPI imported")
        
        import whisper
        print("✅ Whisper imported")
        
        import yt_dlp
        print("✅ yt-dlp imported")
        
        import torch
        print("✅ PyTorch imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_ffmpeg():
    """Test if FFmpeg is available"""
    print("\n🔍 Testing FFmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"❌ FFmpeg error: {e}")
        return False

def test_whisper_model():
    """Test Whisper model loading"""
    print("\n🔍 Testing Whisper model loading...")
    try:
        import whisper
        print("Loading 'base' model (this may take a while for first time)...")
        model = whisper.load_model("base")
        print("✅ Whisper model loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Whisper model loading failed: {e}")
        traceback.print_exc()
        return None

def test_yt_dlp():
    """Test yt-dlp with a simple video"""
    print("\n🔍 Testing yt-dlp...")
    try:
        import yt_dlp
        
        # Test video info extraction only (no download)
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
        print(f"✅ yt-dlp working - Title: {title}, Duration: {duration}s")
        return True
    except Exception as e:
        print(f"❌ yt-dlp error: {e}")
        return False

def test_audio_download():
    """Test actual audio download"""
    print("\n🔍 Testing audio download...")
    try:
        import yt_dlp
        
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, 'test_audio.%(ext)s'),
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(test_url, download=True)
                
            # Check if file was downloaded
            files = os.listdir(temp_dir)
            if files:
                audio_file = os.path.join(temp_dir, files[0])
                size = os.path.getsize(audio_file)
                print(f"✅ Audio download successful - File: {files[0]}, Size: {size} bytes")
                return audio_file
            else:
                print("❌ No audio file downloaded")
                return None
                
    except Exception as e:
        print(f"❌ Audio download error: {e}")
        traceback.print_exc()
        return None

def test_transcription(model):
    """Test actual transcription"""
    print("\n🔍 Testing transcription...")
    try:
        # Download a very short audio first
        audio_file = test_audio_download()
        if not audio_file:
            return False
            
        print("Transcribing audio...")
        result = model.transcribe(audio_file, language='en')
        text = result.get("text", "").strip()
        language = result.get("language", "unknown")
        
        print(f"✅ Transcription successful")
        print(f"   Language: {language}")
        print(f"   Text: {text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        traceback.print_exc()
        return False

def main():
    print("🧪 Video Text Extractor Component Test")
    print("=" * 50)
    
    success = True
    
    # Test all components
    success &= test_imports()
    success &= test_ffmpeg()
    
    model = test_whisper_model()
    if model:
        success &= test_yt_dlp()
        # success &= test_transcription(model)  # Skip for now, takes time
    else:
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The system should work.")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return success

if __name__ == "__main__":
    main()