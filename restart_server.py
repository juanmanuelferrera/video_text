#!/usr/bin/env python3
"""
Auto-restart wrapper for the video text extractor server.
This script will automatically restart the server when it exits.
"""

import subprocess
import sys
import time
import os
import signal

class ServerManager:
    def __init__(self):
        self.process = None
        self.should_restart = True
        
    def start_server(self):
        """Start the server process"""
        print("Starting video text extractor server...")
        self.process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        
    def stop_server(self):
        """Stop the server process"""
        if self.process:
            print("Stopping server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Force killing server...")
                self.process.kill()
                self.process.wait()
            self.process = None
            
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.should_restart = False
        self.stop_server()
        sys.exit(0)
        
    def run(self):
        """Main run loop with auto-restart"""
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("Video Text Extractor Server Manager")
        print("Press Ctrl+C to stop")
        print("-" * 40)
        
        while self.should_restart:
            try:
                self.start_server()
                exit_code = self.process.wait()
                
                if exit_code == 0:
                    print("Server exited normally, restarting in 2 seconds...")
                    time.sleep(2)
                else:
                    print(f"Server exited with code {exit_code}, restarting in 5 seconds...")
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                self.should_restart = False
                self.stop_server()
                break
            except Exception as e:
                print(f"Error managing server: {e}")
                time.sleep(5)
                
        print("Server manager stopped.")

if __name__ == "__main__":
    manager = ServerManager()
    manager.run()