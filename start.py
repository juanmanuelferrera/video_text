#!/usr/bin/env python3
"""
Simple starter for Video Text Extractor
This ensures proper environment activation
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def main():
    print("🎬 Video Text Extractor Starter")
    print("=" * 35)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("💡 Please run setup first:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        return 1
    
    print("✅ Virtual environment found")
    
    # Start server using the virtual environment python directly
    if os.name == 'nt':  # Windows
        python_executable = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        python_executable = venv_path / "bin" / "python"
    
    if not python_executable.exists():
        print(f"❌ Python executable not found: {python_executable}")
        return 1
    
    print("🚀 Starting server...")
    
    # Start server as background process
    try:
        server_process = subprocess.Popen([str(python_executable), "main.py"])
        
        # Wait a moment and check if server started
        time.sleep(3)
        
        # Check if process is still running
        if server_process.poll() is None:
            print("✅ Server started successfully!")
            
            # Open browser
            html_file = script_dir / "standalone.html"
            if html_file.exists():
                print("🌐 Opening web interface...")
                webbrowser.open(f"file://{html_file.resolve()}")
            
            print("\n🎉 Video Text Extractor is running!")
            print("📋 Usage:")
            print("   • Paste video URL in the web interface")
            print("   • Click 'Extract Text' to transcribe")
            print("   • Press Ctrl+C here to stop the server")
            print("\n💡 Server: http://localhost:8000")
            
            # Wait for user to stop
            try:
                server_process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                server_process.terminate()
                try:
                    server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server_process.kill()
                print("✅ Server stopped")
        else:
            print("❌ Server failed to start")
            return 1
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())