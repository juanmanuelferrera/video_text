#!/usr/bin/env python3
"""
Complete setup and launcher for Video Text Extractor
This handles everything from scratch
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show progress"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False

def main():
    print("🎬 Video Text Extractor - Complete Setup & Launch")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Create virtual environment
    venv_path = Path("venv")
    if not venv_path.exists():
        print("1️⃣ Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            return 1
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Step 2: Determine activation command and python path
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        python_path = "venv\\Scripts\\python"
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        python_path = "venv/bin/python"
        pip_path = "venv/bin/pip"
    
    # Step 3: Install PyTorch first
    print("2️⃣ Installing PyTorch (this may take a while)...")
    pytorch_cmd = f"{pip_path} install torch torchaudio --index-url https://download.pytorch.org/whl/cpu"
    if not run_command(pytorch_cmd, "Installing PyTorch"):
        print("⚠️ PyTorch installation failed, trying without index URL...")
        if not run_command(f"{pip_path} install torch torchaudio", "Installing PyTorch (fallback)"):
            return 1
    print("✅ PyTorch installed")
    
    # Step 4: Install other dependencies
    print("3️⃣ Installing other dependencies...")
    deps = ["fastapi", "uvicorn", "python-multipart", "openai-whisper", "yt-dlp", "python-dotenv", "requests"]
    for dep in deps:
        if not run_command(f"{pip_path} install {dep}", f"Installing {dep}"):
            print(f"⚠️ Failed to install {dep}, continuing...")
    print("✅ Dependencies installed")
    
    # Step 5: Test installation
    print("4️⃣ Testing installation...")
    test_cmd = f"{python_path} -c \"import fastapi, whisper, yt_dlp; print('All imports successful')\""
    if not run_command(test_cmd, "Testing imports"):
        print("❌ Some dependencies failed to install properly")
        return 1
    print("✅ All dependencies working")
    
    # Step 6: Start server
    print("5️⃣ Starting server...")
    try:
        server_process = subprocess.Popen([python_path, "main.py"])
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        # Check if server is running
        if server_process.poll() is None:
            print("✅ Server started successfully!")
            
            # Open browser
            html_file = script_dir / "standalone.html"
            if html_file.exists():
                print("6️⃣ Opening web interface...")
                webbrowser.open(f"file://{html_file.resolve()}")
                print("🌐 Web interface opened in browser")
            
            print("\n🎉 Video Text Extractor is now running!")
            print("📋 How to use:")
            print("   1. Paste any video URL (YouTube, Vimeo, etc.)")
            print("   2. Click 'Extract Text'")
            print("   3. Wait for AI transcription")
            print("   4. Copy or save the results")
            print("\n💡 Server running at: http://localhost:8000")
            print("🛑 Press Ctrl+C to stop")
            
            # Keep running until user stops
            try:
                server_process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                server_process.terminate()
                try:
                    server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server_process.kill()
                print("✅ Server stopped")
        else:
            print("❌ Server failed to start")
            # Try to get error output
            stdout, stderr = server_process.communicate()
            if stderr:
                print(f"Error output: {stderr}")
            return 1
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())