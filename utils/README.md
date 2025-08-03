# Utils Module

This module contains utility functions that are used throughout the Monumator system.

## What This Module Contains

- **`downloader.py`** - SEED API download functionality with concurrent support
- **`menu_navigator.py`** - Arrow-key menu navigation utility

## Purpose

Provides core utility functions for common operations across the system. The utils module contains reusable components that don't fit into specific business logic modules.

## Quick Reference

**Main Utility Files:**
- `downloader.py` - SEED API downloads with concurrent processing
- `menu_navigator.py` - Arrow-key navigation for console menus

**Direct imports** - No package structure:
```python
from utils.downloader import download_seed_report, download_multiple_reports_concurrent
from utils.menu_navigator import MenuNavigator
```

## Key Features

- **Concurrent Downloads**: Multi-threaded API downloads for faster processing
- **Authentication Handling**: Automatic credential management for SEED API
- **Progress Tracking**: Real-time download progress with status messages
- **Error Recovery**: Comprehensive error handling and retry logic

## Usage Examples

### Single Report Download
```python
from utils.downloader import download_seed_report

# Download a single report
success = download_seed_report(
    report_id="33105",
    filename="daily_report.xlsx", 
    download_path="downloads/daily/"
)

if success:
    print("Download completed successfully")
else:
    print("Download failed")
```

### Multiple Reports Download (Concurrent)
```python
from utils.downloader import download_multiple_reports_concurrent

# Define reports to download
reports_list = [
    ("33105", "daily_fill_oos.xlsx"),
    ("33106", "weekly_sales_market.xlsx"),
    ("33107", "weekly_sales_delivery.xlsx")
]

# Download concurrently
successful, failed = download_multiple_reports_concurrent(
    reports_list, 
    download_path="downloads/"
)

print(f"Downloaded: {len(successful)}, Failed: {len(failed)}")
```

### Get SEED Credentials
```python
from utils.downloader import get_seed_credentials

username, password = get_seed_credentials()
print(f"Using credentials for user: {username}")
```

### Generate Authentication Header
```python
from utils.downloader import basic_auth

username, password = "user", "pass"
auth_header = basic_auth(username, password)
# Use in HTTP requests
```

## Core Functions

### download_seed_report()
Downloads a single report from SEED API.

**Parameters:**
- `report_id` (str): SEED report ID (e.g., "33105")
- `filename` (str): Local filename to save as
- `download_path` (str): Directory to save file in

**Returns:**
- `bool`: True if successful, False if failed

**Example:**
```python
success = download_seed_report("33105", "report.xlsx", "downloads/")
```

### download_multiple_reports_concurrent()
Downloads multiple reports concurrently using ThreadPoolExecutor.

**Parameters:**
- `reports_list` (list): List of tuples (report_id, filename)
- `download_path` (str): Directory to save files in
- `max_workers` (int): Maximum concurrent downloads (default: 5)

**Returns:**
- `tuple`: (successful_downloads, failed_downloads)

**Example:**
```python
reports = [("33105", "report1.xlsx"), ("33106", "report2.xlsx")]
successful, failed = download_multiple_reports_concurrent(reports, "downloads/")
```

### get_seed_credentials()
Loads SEED credentials from environment variables.

**Returns:**
- `tuple`: (username, password)

**Requires:**
Environment variables `SEED_USERNAME` and `SEED_PASSWORD` in `.env` file.

### basic_auth()
Generates Basic Authentication header for HTTP requests.

**Parameters:**
- `username` (str): Username
- `password` (str): Password

**Returns:**
- `dict`: Authorization header dictionary

## Configuration

### Environment Variables
Create `.env` file in project root:
```bash
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```

### Download Settings
Configured in `../config/report_config.py`:
```python
# API settings
SEED_API_HOST = "https://api.mycantaloupe.com"
SEED_API_ENDPOINT = "/Reports/Run"

# Concurrent download settings
MAX_CONCURRENT_DOWNLOADS = 5
```

## Adding New Utility Functions

### Step 1: Add Function to downloader.py
```python
def new_utility_function(param1, param2):
    """
    Description of what this utility function does
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
        
    Returns:
        type: Description of return value
    """
    try:
        # Implementation here
        result = perform_operation(param1, param2)
        print(f"✅ Utility operation successful: {result}")
        return result
    except Exception as e:
        print(f"❌ Utility operation failed: {str(e)}")
        raise

def download_with_retry(url, max_retries=3):
    """
    Download with automatic retry logic
    
    Args:
        url (str): URL to download
        max_retries (int): Maximum retry attempts
        
    Returns:
        requests.Response: HTTP response object
    """
    import requests
    import time
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️ Download attempt {attempt + 1} failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ Download failed after {max_retries} attempts: {str(e)}")
                raise
```

### Step 2: Import in Other Modules
```python
from utils.downloader import new_utility_function, download_with_retry

# Use in other modules
result = new_utility_function("param1", "param2")
response = download_with_retry("https://example.com/file.xlsx")
```

## Error Handling Patterns

### Standard Error Pattern
```python
def utility_function():
    try:
        # Main operation
        result = perform_operation()
        print(f"✅ Operation successful: {result}")
        return result
    except Exception as e:
        print(f"❌ Operation failed: {str(e)}")
        # Log error details if needed
        return None  # or raise depending on use case
```

### Progress Reporting Pattern
```python
def long_running_operation(items):
    total = len(items)
    for i, item in enumerate(items, 1):
        try:
            process_item(item)
            print(f"📊 Progress: {i}/{total} ({i/total*100:.1f}%)")
        except Exception as e:
            print(f"⚠️ Failed to process item {i}: {str(e)}")
```

## Concurrent Processing

### ThreadPoolExecutor Pattern
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_multiple_items_concurrent(items, max_workers=5):
    """
    Process multiple items concurrently
    
    Args:
        items (list): Items to process
        max_workers (int): Maximum concurrent workers
        
    Returns:
        tuple: (successful_results, failed_results)
    """
    successful = []
    failed = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_item = {
            executor.submit(process_single_item, item): item 
            for item in items
        }
        
        # Process completed tasks
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            try:
                result = future.result()
                successful.append((item, result))
                print(f"✅ Processed: {item}")
            except Exception as e:
                failed.append((item, str(e)))
                print(f"❌ Failed: {item} - {str(e)}")
    
    return successful, failed

def process_single_item(item):
    """Process a single item (implement your logic here)"""
    time.sleep(1)  # Simulate processing time
    return f"processed_{item}"
```

## File Management Utilities

### Safe File Operations
```python
import os
import shutil

def safe_file_copy(source, destination):
    """
    Safely copy file with error handling
    
    Args:
        source (str): Source file path
        destination (str): Destination file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Copy file
        shutil.copy2(source, destination)
        print(f"📁 File copied: {source} → {destination}")
        return True
    except Exception as e:
        print(f"❌ File copy failed: {str(e)}")
        return False

def cleanup_temp_files(*file_paths):
    """
    Clean up multiple temporary files
    
    Args:
        *file_paths: Variable number of file paths to clean up
    """
    for file_path in file_paths:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Removed temp file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"⚠️ Could not remove temp file {file_path}: {str(e)}")
```

## HTTP Request Utilities

### Request Helper Functions
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    """
    Create requests session with automatic retries
    
    Returns:
        requests.Session: Configured session
    """
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def download_file_with_progress(url, file_path, auth_header=None):
    """
    Download file with progress reporting
    
    Args:
        url (str): URL to download
        file_path (str): Local file path to save
        auth_header (dict): Optional authentication header
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        headers = auth_header or {}
        
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r📥 Downloading: {progress:.1f}%", end="", flush=True)
            
            print(f"\n✅ Download complete: {file_path}")
            return True
            
    except Exception as e:
        print(f"\n❌ Download failed: {str(e)}")
        return False
```

## Testing Utilities

### Test Download Functions
```bash
cd /path/to/Monumator
python -c "from utils.downloader import get_seed_credentials; print('Credentials loaded:', bool(get_seed_credentials()[0]))"
```

### Test Concurrent Downloads
```bash
python -c "
from utils.downloader import download_multiple_reports_concurrent
reports = [('33105', 'test1.xlsx'), ('33106', 'test2.xlsx')]
success, failed = download_multiple_reports_concurrent(reports, 'downloads/temp/')
print(f'Success: {len(success)}, Failed: {len(failed)}')
"
```

## Dependencies

- `requests` - HTTP requests and API calls
- `concurrent.futures` - Concurrent processing
- `python-dotenv` - Environment variable loading
- `base64` - Authentication encoding
- `os`, `shutil` - File operations
- `time` - Timing and delays