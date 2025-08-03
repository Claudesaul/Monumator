# Database Module

This module handles all database connections and SQL queries for the Monumator system.

## What This Module Contains

- **`connection.py`** - Database connection management for LightSpeed and Level databases
- **`queries.py`** - All SQL queries for stockout reports and data processing

## Purpose

Provides a unified interface for connecting to dual databases (LightSpeed and Level) and executing complex queries that replicate your Access database logic.

## Quick Reference

**Main Database Files:**
- `connection.py` - Connection management with clean logging
- `queries.py` - All SQL queries and pandas processing

**Direct imports** - No package structure:
```python
from database.connection import get_lightspeed_connection, test_database_connection
from database.queries import execute_all_queries, get_sample_data
```

## Key Features

- **Dual Database Support**: Connects to both LightSpeed and Level databases
- **Cross-Database Merging**: Merges data using pandas when SQL JOINs aren't possible
- **Query Optimization**: Handles complex aggregations and filtering
- **Connection Pooling**: Manages database connections efficiently

## How It Works

1. **Connection Management**: `connection.py` handles ODBC connections to both databases
2. **Query Execution**: `queries.py` contains all SQL queries and data processing logic
3. **Data Merging**: Python pandas merges data from separate databases
4. **Access Logic Replication**: Complex aggregations match your original Access queries

## Usage Examples

### Basic Database Connection
```python
from database.connection import get_lightspeed_connection, get_level_connection

# Connect to LightSpeed database
lightspeed_conn = get_lightspeed_connection()

# Connect to Level database  
level_conn = get_level_connection()
```

### Execute Stockout Queries
```python
from database.queries import execute_all_queries, get_sample_data

# Get real data from database
data = execute_all_queries()

# Or use sample data for testing
sample_data = get_sample_data()
```

### Test Database Connection
```python
from database.connection import test_database_connection

if test_database_connection():
    print("Database connection successful")
```

## Adding New Queries

### Step 1: Add Query Function
Create a new function in `queries.py`:

```python
def get_new_analysis_data():
    """
    Execute new analysis query
    
    Returns:
        pandas.DataFrame: Analysis results
    """
    query = """
    SELECT 
        product, quantity, location
    FROM dbo.ItemView 
    WHERE orderDate = '{today}' AND itemActive = TRUE
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        today = datetime.now().date()
        query_formatted = query.format(today=today)
        df = execute_query(lightspeed_conn, query_formatted)
        lightspeed_conn.close()
        
        print(f"New analysis query completed - {len(df)} records")
        return df
    except Exception as e:
        print(f"New analysis query failed: {str(e)}")
        raise
```

### Step 2: Add Processing Function (if needed)
```python
def _process_new_analysis_data(df):
    """Process and clean new analysis data"""
    # Add your data processing logic here
    processed_df = df.fillna('')
    return processed_df
```

### Step 3: Update Main Query Function
Add your new query to `execute_all_queries()`:

```python
def execute_all_queries():
    results = {}
    results['highlights'] = get_highlights_data()
    results['markets'] = get_markets_data()
    results['null_orders'] = get_null_orders_data()
    results['ocs'] = get_ocs_data()
    results['new_analysis'] = get_new_analysis_data()  # Add this
    return results
```

## Database Schema

### LightSpeed Database Tables
- **`dbo.ItemView`** - Contains order and item data
  - Key columns: `product`, `locID`, `machineBarcode`, `quantity`, `updatedQuantity`, `orderDate`

### Level Database Tables  
- **`dbo.AreaItemParView`** - Contains inventory and location data
  - Key columns: `itemName`, `currentQty`, `itemActive`

## Configuration

Database settings are configured in `../config/database_config.py`:

```python
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
```

## Error Handling

- All functions include comprehensive error handling
- Connection failures are logged and re-raised
- Query failures provide detailed error messages
- Sample data fallback available for testing

## Dependencies

- `pyodbc` - ODBC database connectivity
- `pandas` - Data manipulation and merging
- `datetime` - Date handling for queries

## Testing

Test database connectivity:
```bash
cd /path/to/Monumator
python -c "from database.connection import test_database_connection; test_database_connection()"
```