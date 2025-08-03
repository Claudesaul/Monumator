# Config Module

This module contains all configuration settings and constants for the Monumator system.

## What This Module Contains

- **`report_config.py`** - SEED API report IDs, download paths, and API settings
- **`database_config.py`** - Database connection settings and management functions

## Purpose

Centralizes all configuration to make the system easy to maintain and modify. Changes to report IDs, database settings, or API endpoints only need to be made in one place.

## Quick Reference

**Main Configuration Files:**
- `report_config.py` - Add new SEED report IDs here
- `database_config.py` - Database connection strings and timeouts

**No package structure** - Files are imported directly:
```python
from config.report_config import SEED_REPORTS
from config.database_config import get_lightspeed_connection
```

## Key Features

- **Centralized Configuration**: All settings in one location
- **Environment Separation**: Different settings for development/production
- **Easy Maintenance**: Add new reports or modify settings easily
- **Type Safety**: Clear data structures and validation

## Configuration Files

### report_config.py

Contains SEED API configuration and report definitions:

```python
# SEED API Report IDs
SEED_REPORTS = {
    "daily_fill_oos": "33105",
    "Weekly Sales Reporting Market": "33106", 
    "Weekly Sales Reporting Delivery": "33107",
    # ... more reports
}

# Download directory paths
DOWNLOAD_PATHS = {
    "weekly": "downloads/weekly/",
    "daily": "downloads/daily/", 
    "temp": "downloads/temp/"
}

# API settings
SEED_API_HOST = "https://api.mycantaloupe.com"
MAX_CONCURRENT_DOWNLOADS = 5
```

### database_config.py

Contains database connection settings and helper functions:

```python
# Database connections
LIGHTSPEED_CONNECTION = {
    "dsn": "Lightspeed",
    "uid": "LSReadOnly", 
    "pwd": "LightSpeed100!",
    "database": "LightSpeed"
}

LEVEL_CONNECTION = {
    "dsn": "Lightspeed", 
    "uid": "LSReadOnly",
    "pwd": "LightSpeed100!",
    "database": "Level"
}

# Timeout settings
QUERY_TIMEOUT = 300  # 5 minutes
CONNECTION_TIMEOUT = 60  # 1 minute
```

## Usage Examples

### Import Report Configuration
```python
from config.report_config import SEED_REPORTS, DOWNLOAD_PATHS, WEEKLY_REPORTS

# Get report ID
report_id = SEED_REPORTS["daily_fill_oos"]

# Get download path
download_path = DOWNLOAD_PATHS["daily"]

# Get list of weekly reports
weekly_reports = WEEKLY_REPORTS
```

### Import Database Configuration
```python
from config.database_config import get_lightspeed_connection, test_database_connection

# Get database connection
conn = get_lightspeed_connection()

# Test connection
is_connected = test_database_connection()
```

### Access API Settings
```python
from config.report_config import SEED_API_HOST, MAX_CONCURRENT_DOWNLOADS

# Use in API calls
api_url = f"{SEED_API_HOST}/Reports/Run?ReportId={report_id}"

# Use for concurrent downloads
max_workers = MAX_CONCURRENT_DOWNLOADS
```

## Adding New Reports

### Step 1: Add Report ID
Edit `report_config.py`:

```python
SEED_REPORTS = {
    # Existing reports...
    "new_report_name": "NEW_REPORT_ID",  # Add your new report here
}
```

### Step 2: Add to Report Type Lists
```python
# For weekly reports
WEEKLY_REPORTS = [
    "Weekly Sales Reporting Market",
    "Weekly Sales Reporting Delivery", 
    "MKT Fills Per Visit By Section",
    "Product Activity Weekly",
    "new_weekly_report"  # Add here if it's a weekly report
]

# For daily reports
DAILY_REPORTS = [
    "daily_fill_oos",
    "new_daily_report"  # Add here if it's a daily report
]

# For inventory adjustment reports
INVENTORY_ADJUSTMENT_REPORTS = [
    "inventory_adjustment_previous_day",
    "inventory_adjustment_3_days_ago",
    "new_inventory_report"  # Add here if it's an inventory report
]
```

### Step 3: Use in Code
```python
from config.report_config import SEED_REPORTS

# Your new report is now available
new_report_id = SEED_REPORTS["new_report_name"]
```

## Modifying Database Settings

### Add New Database Connection
Edit `database_config.py`:

```python
NEW_DATABASE_CONNECTION = {
    "dsn": "NewDatabase",
    "uid": "ReadOnlyUser",
    "pwd": "Password123!",
    "database": "NewDB",
    "connection_string": "DSN=NewDatabase;UID=ReadOnlyUser;PWD=Password123!;DATABASE=NewDB"
}

def get_new_database_connection():
    """Get connection to new database"""
    return get_database_connection_by_config(NEW_DATABASE_CONNECTION)
```

### Modify Timeout Settings
```python
# Increase timeouts if needed
QUERY_TIMEOUT = 600  # 10 minutes instead of 5
CONNECTION_TIMEOUT = 120  # 2 minutes instead of 1
```

## Environment Variables

Some sensitive settings should be stored in environment variables:

### Create .env file
```bash
# SEED API Credentials
SEED_USERNAME=your_username
SEED_PASSWORD=your_password

# Database passwords (if different from config)
LIGHTSPEED_PASSWORD=alternative_password
```

### Load in Configuration
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variables for sensitive data
SEED_USERNAME = os.getenv('SEED_USERNAME')
SEED_PASSWORD = os.getenv('SEED_PASSWORD')
```

## Configuration Validation

### Validate Report IDs
```python
def validate_report_config():
    """Validate that all report IDs are properly configured"""
    errors = []
    
    for report_name, report_id in SEED_REPORTS.items():
        if not report_id or not report_id.isdigit():
            errors.append(f"Invalid report ID for {report_name}: {report_id}")
    
    for path_name, path in DOWNLOAD_PATHS.items():
        if not path or not isinstance(path, str):
            errors.append(f"Invalid path for {path_name}: {path}")
    
    if errors:
        raise ValueError(f"Configuration errors: {errors}")
    
    return True
```

### Validate Database Configuration
```python
def validate_database_config():
    """Validate database configuration"""
    required_keys = ["dsn", "uid", "pwd", "database", "connection_string"]
    
    for config_name, config in [("LIGHTSPEED", LIGHTSPEED_CONNECTION), ("LEVEL", LEVEL_CONNECTION)]:
        for key in required_keys:
            if key not in config or not config[key]:
                raise ValueError(f"Missing {key} in {config_name}_CONNECTION")
    
    return True
```

## Configuration Constants

### Report Type Categories
```python
# All weekly report names
WEEKLY_REPORTS = [
    "Weekly Sales Reporting Market",
    "Weekly Sales Reporting Delivery", 
    "MKT Fills Per Visit By Section",
    "Product Activity Weekly"
]

# All daily report names
DAILY_REPORTS = [
    "daily_fill_oos"
]

# Inventory adjustment reports with smart date logic
INVENTORY_ADJUSTMENT_REPORTS = [
    "inventory_adjustment_previous_day",    # Tuesday-Friday
    "inventory_adjustment_3_days_ago"       # Monday (Friday data)
]
```

### File Path Constants
```python
# Standard download directories
DOWNLOAD_PATHS = {
    "weekly": "downloads/weekly/",
    "daily": "downloads/daily/", 
    "temp": "downloads/temp/"
}

# Template file paths
TEMPLATE_PATHS = {
    "stockout": "templates/Daily Stockout Report.xlsx",
    "inventory_adjustment": "templates/Inventory Adjustment Summary.xlsx",
    "inventory_confirmation": "templates/Daily Inventory SEED.xlsx"
}
```

### API Configuration
```python
# SEED API settings
SEED_API_HOST = "https://api.mycantaloupe.com"
SEED_API_ENDPOINT = "/Reports/Run"
SEED_WEB_HOST = "https://mycantaloupe.com"

# Download settings
MAX_CONCURRENT_DOWNLOADS = 5
DEFAULT_DOWNLOAD_TIMEOUT = 300  # 5 minutes

# Product List API
PRODUCT_LIST_API_ENDPOINT = "https://mycantaloupe.com/cs4/ItemImportExport/ExcelExport"
```

## Testing Configuration

### Test Report Configuration
```bash
cd /path/to/Monumator
python -c "from config.report_config import SEED_REPORTS; print(f'Configured {len(SEED_REPORTS)} reports')"
```

### Test Database Configuration
```bash
python -c "from config.database_config import test_database_connection; print('DB connected:', test_database_connection())"
```

### Validate All Configuration
```bash
python -c "
from config.report_config import SEED_REPORTS, DOWNLOAD_PATHS
from config.database_config import LIGHTSPEED_CONNECTION, LEVEL_CONNECTION
print('Report IDs:', len(SEED_REPORTS))
print('Download paths:', len(DOWNLOAD_PATHS))
print('Database configs: 2')
print('Configuration loaded successfully')
"
```

## Dependencies

- `python-dotenv` - For environment variable loading
- `pyodbc` - For database connection management
- `os` - For environment variable access

## Security Notes

1. **Never commit passwords** to version control
2. **Use environment variables** for sensitive data
3. **Restrict database permissions** to read-only where possible
4. **Validate configuration** before using in production