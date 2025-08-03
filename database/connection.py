"""
Database Connection Management
============================

Handles all database connections for Lightspeed and Level databases.
Provides connection pooling and error handling.
"""

import pyodbc
import pandas as pd
from datetime import datetime
from config.database_config import LIGHTSPEED_CONNECTION, LEVEL_CONNECTION, QUERY_TIMEOUT, CONNECTION_TIMEOUT

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
        else:
            connection_config = LIGHTSPEED_CONNECTION
            
        connection = pyodbc.connect(
            connection_config["connection_string"],
            timeout=CONNECTION_TIMEOUT
        )
        return connection
    except Exception as e:
        raise

def get_lightspeed_connection():
    """Get connection to LightSpeed database (for dbo.ItemView)"""
    return get_database_connection("lightspeed")

def get_level_connection():
    """Get connection to Level database (for dbo.AreaItemParView)"""
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
        import warnings
        # Suppress pandas SQLAlchemy warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if params:
                df = pd.read_sql(query, connection, params=params)
            else:
                df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        raise

def test_database_connection():
    """
    Test both database connections
    
    Returns:
        bool: True if both connections successful, False otherwise
    """
    try:
        # Test LightSpeed database
        lightspeed_conn = get_lightspeed_connection()
        test_query_ls = "SELECT TOP 1 * FROM dbo.ItemView"
        execute_query(lightspeed_conn, test_query_ls)
        lightspeed_conn.close()
        
        # Test Level database
        level_conn = get_level_connection()
        test_query_level = "SELECT TOP 1 * FROM dbo.AreaItemParView"
        execute_query(level_conn, test_query_level)
        level_conn.close()
        
        return True
    except Exception as e:
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