import os
import sys
import re
import argparse
import random
import json
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try to import required packages, install if missing
try:
    from termcolor import colored
    import requests
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Installing dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    # Re-import after installation
    from termcolor import colored
    import requests

# Global variables
colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
patterns = []
alreadyfound = []
found_lock = threading.Lock()

def load_patterns():
    """Load patterns from JSON file"""
    global patterns
    with open("patterns.json", "r") as f:
        patterns_data = json.load(f)
        patterns = list(patterns_data.items())

def print_result(name, key, url, colorless=False):
    """Print found result in a thread-safe manner"""
    with found_lock:
        if key not in alreadyfound:
            if colorless:
                print(f"Name: {name}, Key: {key}, URL: {url}")
            else:
                color = random.choice(colors)
                print(colored(f"Name: {name}, Key: {key}, URL: {url}", color))
            alreadyfound.append(key)

def extract_secrets(file_path):
    """Extract secrets from a file using patterns"""
    try:
        with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
            contents = f.read()
            
            for pattern_name, pattern in patterns:
                # Improved regex pattern to handle start/end of string and various delimiters
                # Use word boundaries and common separators to reduce false positives
                # Properly escape the character classes in the f-string
                the_pattern = rf"(^|[:=/'\"\s`´,?\]\|}}&/*])({pattern})($|[:=/'\"\s`´,?\[{{|&/*])"
                compiled_pattern = re.compile(the_pattern)
                matches = compiled_pattern.findall(contents)
                
                for match in matches:
                    # The actual match is the second group in the tuple
                    secret = match[1]
                    print_result(pattern_name, str(secret), file_path, args.colorless)
    except Exception as e:
        # Handle file reading errors gracefully
        pass

def scan_zip_file(zip_path):
    """Scan contents of a ZIP file for secrets"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Get list of files in the ZIP
            for file_info in zf.infolist():
                # Skip directories
                if file_info.is_dir():
                    continue
                
                # Read file content
                with zf.open(file_info.filename) as f:
                    try:
                        # Try to decode as text
                        content = f.read().decode('utf-8', errors='ignore')
                        
                        # Check each pattern
                        for pattern_name, pattern in patterns:
                            the_pattern = rf"(^|[:=/'\"\s`´,?\]\|}}&/*])({pattern})($|[:=/'\"\s`´,?\[{{|&/*])"
                            compiled_pattern = re.compile(the_pattern)
                            matches = compiled_pattern.findall(content)
                            
                            for match in matches:
                                secret = match[1]
                                # Show which file inside the ZIP contains the secret
                                print_result(pattern_name, str(secret), f"{zip_path}/{file_info.filename}", args.colorless)
                    except Exception as e:
                        # Skip files that can't be read as text
                        pass
    except Exception as e:
        # Handle ZIP file errors
        pass

def main():
    global args
    # Parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, help="Set directory to scan")
    ap.add_argument("-t", "--threads", required=True, type=int, help="Number of threads")
    ap.add_argument("-z", "--zip", required=False, action='store_true', help="Scan ZIP files")
    ap.add_argument("--colorless", required=False, action='store_true', help="Disable colored output")
    args = ap.parse_args()
    
    # Load patterns
    load_patterns()
    
    # Collect all files to scan
    files = []
    zip_files = []
    
    for root, dirs, filenames in os.walk(args.dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            
            # Check if it's a ZIP file when --zip flag is set
            if args.zip and filename.lower().endswith(('.zip', '.jar', '.war', '.ear')):
                zip_files.append(file_path)
            else:
                files.append(file_path)
    
    # Process regular files using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Submit regular file tasks
        future_to_file = {executor.submit(extract_secrets, file): file for file in files}
        
        # Submit ZIP file tasks if --zip flag is set
        if args.zip:
            for zip_file in zip_files:
                future_to_file[executor.submit(scan_zip_file, zip_file)] = zip_file
        
        # Wait for all tasks to complete
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{file} generated an exception: {exc}')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(1)

