#!/usr/bin/env python3
"""
Simple one-click launcher for Video Text Extractor
Just run this file and everything starts automatically!
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def run_server():
    """Run the FastAPI server"""
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Activate virtual environment and run server
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && python main.py"
        subprocess.run(activate_cmd, shell=True)
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate && python main.py"
        subprocess.run(activate_cmd, shell=True, executable='/bin/bash')

def open_browser_after_delay():
    """Open browser after server starts"""
    time.sleep(3)  # Wait for server to start
    html_file = Path(__file__).parent / "standalone.html"
    webbrowser.open(f"file://{html_file.resolve()}")
    print(f"🌐 Opened: {html_file}")

if __name__ == "__main__":
    print("🎬 Starting Video Text Extractor...")
    
    # Start browser opener in separate thread
    browser_thread = threading.Thread(target=open_browser_after_delay)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run server (this will block)
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        sys.exit(0)