# Utils Module

Contains utility functions used throughout the Monumator system.

## Files

- **`downloader.py`** - SEED API downloads with concurrent support
- **`menu_navigator.py`** - Arrow-key menu navigation

## How It Works

Provides reusable utility functions:
- **Downloader** - SEED API authentication and concurrent downloads
- **Menu Navigator** - Console arrow-key navigation for menus

## Usage

### Single Report Download
```python
from utils.downloader import download_seed_report

success = download_seed_report(
    report_id="33105",
    filename="daily_report.xlsx", 
    download_path="downloads/daily/"
)
```

### Multiple Reports (Concurrent)
```python
from utils.downloader import download_multiple_reports_concurrent

reports_list = [
    ("33105", "daily_fill_oos.xlsx"),
    ("33106", "weekly_sales_market.xlsx"),
    ("33107", "weekly_sales_delivery.xlsx")
]

successful, failed = download_multiple_reports_concurrent(reports_list, "downloads/")
print(f"Downloaded: {len(successful)}, Failed: {len(failed)}")
```

### Arrow-Key Navigation
```python
from utils.menu_navigator import MenuNavigator

options = ["Option 1", "Option 2", "Option 3"]
navigator = MenuNavigator(options, "Select Option")
choice = navigator.navigate()  # Returns selected index
```

### SEED Credentials
```python
from utils.downloader import get_seed_credentials

username, password = get_seed_credentials()  # From .env file
```

## Adding New Utility Functions

### Step 1: Add to Appropriate File
Add to `downloader.py` for download/API utilities:
```python
def new_download_utility(param1, param2):
    """
    Description of utility function
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        result: Description
    """
    try:
        # Implementation here
        result = perform_operation(param1, param2)
        print(f"✅ Operation successful: {result}")
        return result
    except Exception as e:
        print(f"❌ Operation failed: {str(e)}")
        raise
```

Add to `menu_navigator.py` for UI utilities:
```python
def new_ui_utility():
    """New UI utility function"""
    # Implementation here
    pass
```

### Step 2: Import and Use
```python
from utils.downloader import new_download_utility
from utils.menu_navigator import new_ui_utility

result = new_download_utility("param1", "param2")
new_ui_utility()
```

## Core Functions

### downloader.py
- **`download_seed_report()`** - Single report download
- **`download_multiple_reports_concurrent()`** - Concurrent downloads (max 5)
- **`get_seed_credentials()`** - Load from environment variables
- **`basic_auth()`** - Generate auth headers

### menu_navigator.py  
- **`MenuNavigator`** - Arrow-key navigation class
- **`display()`** - Show menu with highlighting
- **`navigate()`** - Handle ↑↓ arrows, Enter, Q

## Environment Variables

Required in `.env` file:
```bash
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```

## Concurrent Processing Pattern

For adding new concurrent utilities:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_multiple_items_concurrent(items, max_workers=5):
    successful = []
    failed = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {
            executor.submit(process_single_item, item): item 
            for item in items
        }
        
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            try:
                result = future.result()
                successful.append((item, result))
            except Exception as e:
                failed.append((item, str(e)))
    
    return successful, failed
```