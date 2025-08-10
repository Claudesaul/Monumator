# 💾 Database Module

SQL Server connections and queries for LightSpeed and Level databases.

## 📄 Files

- **`connection.py`** - Database connection management
- **`queries.py`** - SQL queries and data processing

## 📊 Databases

- **LightSpeed** - `dbo.ItemView` (order data)
- **Level** - `dbo.AreaItemParView` (inventory data)

Server: 10.216.207.32

## 🚀 Usage

### Connect to Databases
```python
from database.connection import get_lightspeed_connection, get_level_connection

lightspeed_conn = get_lightspeed_connection()
level_conn = get_level_connection()
```

### Execute Queries
```python
from database.queries import execute_all_queries, get_sample_data

# Get real data
data = execute_all_queries()

# Use sample data for testing
sample_data = get_sample_data()
```

### Test Connection
```python
from database.connection import test_database_connection
is_connected = test_database_connection()
```

## ➕ Adding New Queries

### Step 1: Add Function to `queries.py`
```python
def get_new_data():
    """Execute new query"""
    query = """
    SELECT product, quantity, location
    FROM dbo.ItemView 
    WHERE orderDate = '{today}'
    """
    
    lightspeed_conn = get_lightspeed_connection()
    today = datetime.now().date()
    df = execute_query(lightspeed_conn, query.format(today=today))
    lightspeed_conn.close()
    return df
```

### Step 2: Add to Main Function
```python
def execute_all_queries():
    results = {}
    results['highlights'] = get_highlights_data()
    results['new_data'] = get_new_data()  # Add here
    return results
```

## Database Tables

- **LightSpeed.dbo.ItemView** - Order data (`product`, `quantity`, `orderDate`, `locID`)
- **Level.dbo.AreaItemParView** - Inventory data (`itemName`, `currentQty`, `itemActive`)

Merged on `product` = `itemName`.