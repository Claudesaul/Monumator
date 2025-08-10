# ⚙️ Config Module

Configuration files for SEED API reports and database connections.

## 📄 Files

- **`report_config.py`** - SEED report IDs, download paths, API settings
- **`database_config.py`** - SQL Server connection strings and database utilities

## 🚀 Usage

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

## ➕ Adding New Configuration

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
NEW_CONNECTION = {
    "connection_string": f"DRIVER={{SQL Server}};SERVER=server;DATABASE=db;UID={DB_USERNAME};PWD={DB_PASSWORD}"
}

def get_new_connection():
    return get_database_connection("new_type")
```

## 🔑 Environment Variables

Create `.env` file for sensitive data:
```bash
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
```