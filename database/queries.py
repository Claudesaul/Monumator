"""
Database Queries for Stockout Reports
=====================================

All SQL queries for daily stockout reports using direct SQL processing.
Simplified to use SQL for all logic instead of pandas post-processing.
"""

import pandas as pd
import warnings
from datetime import datetime
from .connection import get_lightspeed_connection, execute_query

def get_highlights_data():
    """
    Execute the Highlights query with all logic in SQL
    
    Returns:
        pandas.DataFrame: Highlights data with stockout information
    """
    query = """
    WITH MergedData AS (
        SELECT 
            iv.product,
            iv.locID,
            iv.machineBarcode,
            iv.coil,
            iv.quantity,
            iv.updatedQuantity,
            ap.currentQty
        FROM ItemView iv
        INNER JOIN Level.dbo.AreaItemParView ap 
            ON LTRIM(RTRIM(iv.product)) = LTRIM(RTRIM(ap.itemName))
        WHERE iv.orderDate = CAST(GETDATE() AS DATE)
            AND ap.itemActive = 1
            AND iv.quantity != iv.updatedQuantity
    )
    SELECT 
        product,
        COUNT(*) as numAccounts,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) as singlesOrdered,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) as singlesPicked,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) as casesOrdered,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) as casesPicked,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) as singlesDiff,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) as casesDiff,
        MAX(currentQty) as currentQty,
        SUM(CASE WHEN locID = 'OCS' OR LEFT(machineBarcode, 3) = 'OCS' THEN 1 ELSE 0 END) as numOCS,
        SUM(CASE WHEN locID != 'OCS' AND LEFT(machineBarcode, 3) != 'OCS' THEN 1 ELSE 0 END) as numMarkets
    FROM MergedData
    GROUP BY product
    HAVING (ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) < 
            ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0))
        OR (ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) < 
            ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0))
    ORDER BY 
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0),
        product
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_sql(query, lightspeed_conn)
        lightspeed_conn.close()
        
        return df
    except Exception as e:
        print(f"Highlights query failed: {str(e)}")
        raise

def get_markets_data():
    """
    Execute the Markets query with all logic in SQL
    
    Returns:
        pandas.DataFrame: Markets data with location-specific stockout information
    """
    query = """
    WITH MergedData AS (
        SELECT 
            iv.providerName,
            iv.locDescription,
            iv.machineBarcode as pogName,
            iv.product,
            iv.coil,
            iv.quantity,
            iv.updatedQuantity,
            ap.currentQty
        FROM ItemView iv
        INNER JOIN Level.dbo.AreaItemParView ap 
            ON LTRIM(RTRIM(iv.product)) = LTRIM(RTRIM(ap.itemName))
        WHERE iv.orderDate = CAST(GETDATE() AS DATE)
            AND ap.itemActive = 1
            AND iv.locID != 'OCS'
    )
    SELECT 
        providerName,
        locDescription,
        pogName,
        product,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) as singlesOrdered,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) as singlesPicked,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) as casesOrdered,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) as casesPicked,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) as singlesDiff,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) as casesDiff,
        MAX(currentQty) as currentQty
    FROM MergedData
    WHERE providerName = 'Seed'
    GROUP BY providerName, locDescription, pogName, product
    HAVING (ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) - 
            ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) < 0)
        OR (ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) - 
            ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) < 0)
    ORDER BY pogName, product
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_sql(query, lightspeed_conn)
        lightspeed_conn.close()
        
        return df
    except Exception as e:
        print(f"Markets query failed: {str(e)}")
        raise

def get_null_orders_data():
    """
    Execute the NullOrders query to get orders with null quantities
    
    Returns:
        pandas.DataFrame: Null orders data
    """
    query = """
    SELECT 
        locDescription AS location,
        machineBarcode AS assetID,
        product,
        quantity,
        updatedQuantity
    FROM ItemView
    WHERE orderDate = CAST(GETDATE() AS DATE)
        AND quantity > 0 
        AND updatedQuantity IS NULL 
        AND statusId > 0
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_sql(query, lightspeed_conn)
        lightspeed_conn.close()
        
        return df
    except Exception as e:
        print(f"NullOrders query failed: {str(e)}")
        raise

def get_ocs_data():
    """
    Execute the OCS query with all logic in SQL
    
    Returns:
        pandas.DataFrame: OCS data with OCS-specific stockout information
    """
    query = """
    WITH MergedData AS (
        SELECT 
            iv.cusDescription as vendsysName,
            iv.locDescription as seedName,
            iv.product,
            iv.coil,
            iv.quantity,
            iv.updatedQuantity,
            ap.currentQty
        FROM ItemView iv
        INNER JOIN Level.dbo.AreaItemParView ap 
            ON LTRIM(RTRIM(iv.product)) = LTRIM(RTRIM(ap.itemName))
        WHERE iv.orderDate = CAST(GETDATE() AS DATE)
            AND ap.itemActive = 1
            AND (iv.locID = 'OCS' OR LEFT(iv.machineBarcode, 3) = 'OCS')
    )
    SELECT 
        vendsysName,
        seedName,
        product,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) as singlesOrdered,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) as singlesPicked,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) as casesOrdered,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) as casesPicked,
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) as singlesDiff,
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) - 
        ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) as casesDiff,
        MAX(currentQty) as currentQty
    FROM MergedData
    GROUP BY vendsysName, seedName, product
    HAVING (ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN updatedQuantity END), 0) - 
            ISNULL(SUM(CASE WHEN coil != 'DeliveryCase' THEN quantity END), 0) < 0)
        OR (ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN updatedQuantity END), 0) - 
            ISNULL(SUM(CASE WHEN coil = 'DeliveryCase' THEN quantity END), 0) < 0)
    ORDER BY vendsysName, seedName, product
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_sql(query, lightspeed_conn)
        lightspeed_conn.close()
        
        return df
    except Exception as e:
        print(f"OCS query failed: {str(e)}")
        raise

def execute_all_queries():
    """
    Execute all four queries and return results
    
    Returns:
        dict: Dictionary containing all query results
    """
    results = {}
    try:
        print("🔍 Querying database...")
        
        results['highlights'] = get_highlights_data()
        results['markets'] = get_markets_data()
        results['null_orders'] = get_null_orders_data()
        results['ocs'] = get_ocs_data()
        
        # Log summary of what we found
        highlights_count = len(results['highlights']) if not results['highlights'].empty else 0
        markets_count = len(results['markets']) if not results['markets'].empty else 0
        
        print(f"📊 Found {highlights_count} stockout items, {markets_count} affected markets")
        
        return results
    except Exception as e:
        print(f"Query execution failed: {str(e)}")
        raise