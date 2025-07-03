#!/usr/bin/env python3
"""
Video Text Extractor Launcher
Automatically starts the backend server and opens the web interface
"""

import subprocess
import webbrowser
import time
import sys
import os
import threading
import signal
from pathlib import Path

def check_dependencies():
    """Check if virtual environment and dependencies are set up"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found. Setting up...")
        return False
    
    activate_script = venv_path / "bin" / "activate"
    if not activate_script.exists():
        print("❌ Virtual environment activation script not found.")
        return False
    
    return True

def setup_environment():
    """Set up virtual environment and install dependencies"""
    print("🔧 Setting up virtual environment...")
    
    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
    
    # Install PyTorch first
    subprocess.run([pip_path, "install", "torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"], check=True)
    
    # Install other dependencies
    deps = [
        "fastapi", "uvicorn", "python-multipart", 
        "openai-whisper", "yt-dlp", "python-dotenv", "requests"
    ]
    subprocess.run([pip_path, "install"] + deps, check=True)
    
    print("✅ Environment setup complete!")

def start_server():
    """Start the FastAPI server in a separate process"""
    print("🚀 Starting backend server...")
    
    if os.name == 'nt':  # Windows
        cmd = ["venv\\Scripts\\python", "main.py"]
    else:  # Unix/Linux/macOS
        # Use bash to activate environment and run
        cmd = ["bash", "-c", "source venv/bin/activate && python main.py"]
    
    return subprocess.Popen(cmd)

def wait_for_server(max_attempts=30):
    """Wait for server to start and be ready"""
    import urllib.request
    import urllib.error
    
    for attempt in range(max_attempts):
        try:
            urllib.request.urlopen("http://localhost:8000/health", timeout=1)
            return True
        except (urllib.error.URLError, urllib.error.HTTPError):
            time.sleep(1)
    return False

def open_browser():
    """Open the web interface in the default browser"""
    html_file = Path("standalone.html").resolve()
    if html_file.exists():
        webbrowser.open(f"file://{html_file}")
        print(f"🌐 Opening web interface: {html_file}")
    else:
        print("❌ standalone.html not found!")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down...")
    sys.exit(0)

def main():
    """Main launcher function"""
    print("🎬 Video Text Extractor Launcher")
    print("=" * 40)
    
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if dependencies are installed
    if not check_dependencies():
        try:
            setup_environment()
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to set up environment: {e}")
            return 1
    
    # Start the server
    server_process = None
    try:
        server_process = start_server()
        
        # Wait for server to be ready
        print("⏳ Waiting for server to start...")
        if wait_for_server():
            print("✅ Server is ready!")
            
            # Open browser
            open_browser()
            
            print("\n🎉 Video Text Extractor is now running!")
            print("📋 Instructions:")
            print("   • Paste any video URL in the input field")
            print("   • Click 'Extract Text' to transcribe")
            print("   • Use the sidebar to save/load transcriptions")
            print("   • Press Ctrl+C to stop the server")
            print("\n💡 Server running at: http://localhost:8000")
            print("🌐 Web interface opened in your browser")
            
            # Keep the script running
            try:
                server_process.wait()
            except KeyboardInterrupt:
                pass
        else:
            print("❌ Server failed to start within timeout")
            return 1
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1
    finally:
        if server_process:
            print("\n🛑 Stopping server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == "__main__":
    sys.exit(main())