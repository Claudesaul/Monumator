# Config Module

Contains configuration settings for SEED API reports and database connections.

## Files

- **`report_config.py`** - SEED report IDs, download paths, API settings
- **`database_config.py`** - Database connection settings

## How It Works

Centralizes all settings in one place. Import configurations directly:

```python
from config.report_config import SEED_REPORTS
from config.database_config import get_lightspeed_connection
```

## Usage

### Get Report IDs
```python
from config.report_config import SEED_REPORTS
report_id = SEED_REPORTS["daily_fill_oos"]  # Returns "33105"
```

### Get Database Connection
```python
from config.database_config import get_lightspeed_connection
conn = get_lightspeed_connection()
```

## Adding New Configuration

### New SEED Report
Edit `report_config.py`:
```python
SEED_REPORTS = {
    "existing_report": "33105",
    "new_report_name": "NEW_REPORT_ID"  # Add here
}
```

### New Database Connection
Edit `database_config.py`:
```python
NEW_DB_CONNECTION = {
    "dsn": "NewDB",
    "uid": "User", 
    "pwd": "Password",
    "database": "DatabaseName"
}

def get_new_db_connection():
    return get_database_connection_by_config(NEW_DB_CONNECTION)
```

## Environment Variables

Create `.env` file for sensitive data:
```bash
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```