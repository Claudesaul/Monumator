"""
Database Configuration
======================

This module contains database connection configuration for the Lightspeed database.
Provides connection settings, connection management, and database utilities.
"""

import pyodbc
import pandas as pd
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database credentials from environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if not DB_USERNAME or not DB_PASSWORD:
    raise ValueError("DB_USERNAME and DB_PASSWORD must be set in .env file")

# Dual Database Connection Configuration
# Based on Access setup: dbo_ItemView connects to LightSpeed, dbo_AreaItemParView connects to Level
LIGHTSPEED_CONNECTION = {
    "dsn": "Lightspeed",
    "uid": DB_USERNAME, 
    "pwd": DB_PASSWORD,
    "database": "LightSpeed",
    "connection_string": f"DRIVER={{SQL Server}};SERVER=10.216.207.32;DATABASE=LightSpeed;UID={DB_USERNAME};PWD={DB_PASSWORD}"
}

LEVEL_CONNECTION = {
    "dsn": "Lightspeed", 
    "uid": DB_USERNAME,
    "pwd": DB_PASSWORD,
    "database": "Level",
    "connection_string": f"DRIVER={{SQL Server}};SERVER=10.216.207.32;DATABASE=Level;UID={DB_USERNAME};PWD={DB_PASSWORD}"
}

# Database query timeout settings
QUERY_TIMEOUT = 300  # 5 minutes
CONNECTION_TIMEOUT = 60  # 1 minute

def get_database_connection(database_type="lightspeed"):
    """
    Create and return a database connection to specified database
    
    Args:
        database_type (str): Either "lightspeed" or "level"
    
    Returns:
        pyodbc.Connection: Database connection object
        
    Raises:
        Exception: If connection fails
    """
    try:
        if database_type.lower() == "level":
            connection_config = LEVEL_CONNECTION
            db_name = "Level"
        else:
            connection_config = LIGHTSPEED_CONNECTION
            db_name = "LightSpeed"
            
        connection = pyodbc.connect(
            connection_config["connection_string"],
            timeout=CONNECTION_TIMEOUT
        )
        print(f"{db_name} database connection established at {datetime.now().strftime('%H:%M:%S')}")
        return connection
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        raise

def get_lightspeed_connection():
    """
    Get connection to LightSpeed database (for dbo_ItemView)
    """
    return get_database_connection("lightspeed")

def get_level_connection():
    """
    Get connection to Level database (for dbo_AreaItemParView)  
    """
    return get_database_connection("level")

def execute_query(connection, query, params=None):
    """
    Execute a SQL query and return results as a pandas DataFrame
    
    Args:
        connection (pyodbc.Connection): Database connection
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
        
    Returns:
        pandas.DataFrame: Query results
        
    Raises:
        Exception: If query execution fails
    """
    try:
        if params:
            df = pd.read_sql(query, connection, params=params)
        else:
            df = pd.read_sql(query, connection)
        
        print(f"Query executed successfully - {len(df)} rows returned")
        return df
    except Exception as e:
        print(f"Query execution failed: {str(e)}")
        raise

def test_database_connection():
    """
    Test both database connections and discover actual table names
    
    Returns:
        bool: True if both connections successful, False otherwise
    """
    try:
        # Test LightSpeed database (dbo.ItemView)
        print("Testing LightSpeed database connection...")
        lightspeed_conn = get_lightspeed_connection()
        test_query_ls = "SELECT TOP 1 * FROM dbo.ItemView"
        df_ls = execute_query(lightspeed_conn, test_query_ls)
        lightspeed_conn.close()
        print("LightSpeed database connection successful")
        
        # Test Level database (dbo.AreaItemParView)  
        print("\nTesting Level database connection...")
        level_conn = get_level_connection()
        test_query_level = "SELECT TOP 1 * FROM dbo.AreaItemParView"
        df_level = execute_query(level_conn, test_query_level)
        level_conn.close()
        print("Level database connection successful")
        
        print("\nBoth database connections test successful")
        
        return True
    except Exception as e:
        print(f"Database connection test failed: {str(e)}")
        return False

def get_connection_info():
    """
    Get database connection information for logging/debugging
    
    Returns:
        dict: Connection information
    """
    return {
        "dsn": LIGHTSPEED_CONNECTION["dsn"],
        "user": LIGHTSPEED_CONNECTION["uid"],
        "timeout": QUERY_TIMEOUT,
        "connection_timeout": CONNECTION_TIMEOUT
    } 