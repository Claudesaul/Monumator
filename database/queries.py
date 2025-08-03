"""
Database Queries for Stockout Reports
=====================================

All SQL queries and data processing for daily stockout reports.
Handles dual-database queries and pandas processing.
"""

import pandas as pd
from datetime import datetime
from .connection import get_lightspeed_connection, get_level_connection, execute_query

def get_highlights_data():
    """
    Execute the Highlights query to get stockout summary data
    Uses dual database connections: LightSpeed for ItemView, Level for AreaItemParView
    
    Returns:
        pandas.DataFrame: Highlights data with stockout information
    """
    today = datetime.now().date()
    itemview_query = f"""
    SELECT 
        product, locID, machineBarcode, coil, quantity, updatedQuantity
    FROM dbo.ItemView 
    WHERE orderDate = '{today}'
    """
    
    areaitem_query = """
    SELECT 
        itemName, currentQty, itemActive
    FROM dbo.AreaItemParView
    """
    
    try:
        # Get data from both databases
        lightspeed_conn = get_lightspeed_connection()
        df_items = execute_query(lightspeed_conn, itemview_query)
        lightspeed_conn.close()
        
        level_conn = get_level_connection()
        df_area = execute_query(level_conn, areaitem_query)
        level_conn.close()
        
        # Merge and process
        df_merged = df_items.merge(df_area, left_on='product', right_on='itemName', how='inner')
        df_merged = df_merged[df_merged['itemActive'] == True]
        df_processed = _process_highlights_data(df_merged)
        
        print(f"Highlights query completed - {len(df_processed)} stockout items found")
        return df_processed
    except Exception as e:
        print(f"Highlights query failed: {str(e)}")
        raise

def get_markets_data():
    """
    Execute the Markets query to get market-specific stockout data
    
    Returns:
        pandas.DataFrame: Markets data with location-specific stockout information
    """
    today = datetime.now().date()
    itemview_query = f"""
    SELECT 
        providerName, locDescription, machineBarcode, product, coil, quantity, updatedQuantity
    FROM dbo.ItemView 
    WHERE orderDate = '{today}' AND locID <> 'OCS'
    """
    
    areaitem_query = """
    SELECT 
        itemName, currentQty, itemActive
    FROM dbo.AreaItemParView
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        df_items = execute_query(lightspeed_conn, itemview_query)
        lightspeed_conn.close()
        
        level_conn = get_level_connection()
        df_area = execute_query(level_conn, areaitem_query)
        level_conn.close()
        
        df_merged = df_items.merge(df_area, left_on='product', right_on='itemName', how='inner')
        df_merged = df_merged[df_merged['itemActive'] == True]
        df_processed = _process_markets_data(df_merged)
        
        print(f"Markets query completed - {len(df_processed)} market stockout items found")
        return df_processed
    except Exception as e:
        print(f"Markets query failed: {str(e)}")
        raise

def get_null_orders_data():
    """
    Execute the NullOrders query to get orders with null quantities
    
    Returns:
        pandas.DataFrame: Null orders data
    """
    today = datetime.now().date()
    query = f"""
    SELECT locDescription AS location, machineBarcode AS assetID, product, quantity, updatedQuantity
    FROM dbo.ItemView
    WHERE orderDate = '{today}' AND quantity > 0 AND updatedQuantity IS NULL AND statusId > 0
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        df = execute_query(lightspeed_conn, query)
        lightspeed_conn.close()
        print(f"NullOrders query completed - {len(df)} null orders found")
        return df
    except Exception as e:
        print(f"NullOrders query failed: {str(e)}")
        raise

def get_ocs_data():
    """
    Execute the OCS query to get OCS-specific stockout data
    
    Returns:
        pandas.DataFrame: OCS data with OCS-specific stockout information
    """
    today = datetime.now().date()
    itemview_query = f"""
    SELECT 
        cusDescription, locDescription, product, coil, quantity, updatedQuantity, machineBarcode
    FROM dbo.ItemView 
    WHERE orderDate = '{today}' AND (locID = 'OCS' OR LEFT(machineBarcode, 3) = 'OCS')
    """
    
    areaitem_query = """
    SELECT 
        itemName, currentQty, itemActive
    FROM dbo.AreaItemParView
    """
    
    try:
        lightspeed_conn = get_lightspeed_connection()
        df_items = execute_query(lightspeed_conn, itemview_query)
        lightspeed_conn.close()
        
        level_conn = get_level_connection()
        df_area = execute_query(level_conn, areaitem_query)
        level_conn.close()
        
        df_merged = df_items.merge(df_area, left_on='product', right_on='itemName', how='inner')
        df_merged = df_merged[df_merged['itemActive'] == True]
        df_processed = _process_ocs_data(df_merged)
        
        print(f"OCS query completed - {len(df_processed)} OCS stockout items found")
        return df_processed
    except Exception as e:
        print(f"OCS query failed: {str(e)}")
        raise

def execute_all_queries():
    """
    Execute all four queries and return results
    
    Returns:
        dict: Dictionary containing all query results
    """
    print("Executing all Lightspeed queries...")
    
    results = {}
    try:
        results['highlights'] = get_highlights_data()
        results['markets'] = get_markets_data()
        results['null_orders'] = get_null_orders_data()
        results['ocs'] = get_ocs_data()
        
        total_rows = sum(len(df) for df in results.values())
        print(f"All queries completed successfully - {total_rows} total rows retrieved")
        return results
    except Exception as e:
        print(f"Query execution failed: {str(e)}")
        raise

def get_sample_data():
    """Get sample data for testing when database is not available"""
    print("Using sample data for testing")
    
    highlights_data = {
        'product': ['Coke 12oz', 'Pepsi 16oz', 'Snickers Bar'],
        'numAccounts': [5, 3, 8],
        'singlesOrdered': [50, 30, 80],
        'singlesPicked': [45, 25, 75],
        'casesOrdered': [10, 5, 15],
        'casesPicked': [8, 4, 12],
        'singlesDiff': [-5, -5, -5],
        'casesDiff': [-2, -1, -3],
        'currentQty': [100, 75, 200],
        'numOCS': [2, 1, 3],
        'numMarkets': [3, 2, 5]
    }
    
    markets_data = {
        'providerName': ['Seed', 'Seed', 'Seed'],
        'locDescription': ['Market A', 'Market B', 'Market C'],
        'pogName': ['POG001', 'POG002', 'POG003'],
        'product': ['Coke 12oz', 'Pepsi 16oz', 'Snickers Bar'],
        'singlesOrdered': [20, 15, 25],
        'singlesPicked': [18, 12, 22],
        'casesOrdered': [4, 3, 5],
        'casesPicked': [3, 2, 4],
        'singlesDiff': [-2, -3, -3],
        'casesDiff': [-1, -1, -1],
        'currentQty': [50, 40, 60]
    }
    
    null_orders_data = {
        'location': ['Market A', 'Market B'],
        'assetID': ['ASSET001', 'ASSET002'],
        'product': ['Coke 12oz', 'Pepsi 16oz'],
        'quantity': [10, 15],
        'updatedQuantity': [None, None]
    }
    
    ocs_data = {
        'vendsysName': ['VendSys A', 'VendSys B'],
        'seedName': ['OCS Location 1', 'OCS Location 2'],
        'product': ['Coke 12oz', 'Pepsi 16oz'],
        'singlesOrdered': [30, 25],
        'singlesPicked': [25, 20],
        'casesOrdered': [6, 5],
        'casesPicked': [5, 4],
        'singlesDiff': [-5, -5],
        'casesDiff': [-1, -1],
        'currentQty': [80, 70]
    }
    
    return {
        'highlights': pd.DataFrame(highlights_data),
        'markets': pd.DataFrame(markets_data),
        'null_orders': pd.DataFrame(null_orders_data),
        'ocs': pd.DataFrame(ocs_data)
    }

# Helper functions for data processing
def _process_highlights_data(df):
    """Process merged data to replicate Access Highlights query logic"""
    df_diff = df[
        (df['quantity'] != df['updatedQuantity']) & 
        (df['updatedQuantity'].notna())
    ].copy()
    
    if df_diff.empty:
        return pd.DataFrame()
    
    def calculate_highlights_stats(group):
        return pd.Series({
            'numAccounts': len(group),
            'singlesOrdered': group[group['coil'] != 'DeliveryCase']['quantity'].sum(),
            'singlesPicked': group[group['coil'] != 'DeliveryCase']['updatedQuantity'].sum(),
            'casesOrdered': group[group['coil'] == 'DeliveryCase']['quantity'].sum(),
            'casesPicked': group[group['coil'] == 'DeliveryCase']['updatedQuantity'].sum(),
            'currentQty': group['currentQty'].max(),
            'numOCS': ((group['locID'] == 'OCS') | (group['machineBarcode'].astype(str).str.startswith('OCS'))).sum(),
            'numMarkets': ((group['locID'] != 'OCS') & (~group['machineBarcode'].astype(str).str.startswith('OCS'))).sum()
        })
    
    grouped = df_diff.groupby('product').apply(calculate_highlights_stats).reset_index()
    grouped['singlesDiff'] = grouped['singlesPicked'] - grouped['singlesOrdered']
    grouped['casesDiff'] = grouped['casesPicked'] - grouped['casesOrdered']
    
    stockouts = grouped[(grouped['singlesPicked'] < grouped['singlesOrdered']) | 
                       (grouped['casesPicked'] < grouped['casesOrdered'])]
    
    column_order = [
        'product', 'numAccounts', 'singlesOrdered', 'singlesPicked', 
        'casesOrdered', 'casesPicked', 'singlesDiff', 'casesDiff', 
        'currentQty', 'numOCS', 'numMarkets'
    ]
    stockouts = stockouts[column_order]
    return stockouts.sort_values(['singlesDiff', 'product'])

def _process_markets_data(df):
    """Process merged data to replicate Access Markets query logic"""
    def calculate_markets_stats(group):
        return pd.Series({
            'singlesOrdered': group[group['coil'] != 'DeliveryCase']['quantity'].sum(),
            'singlesPicked': group[group['coil'] != 'DeliveryCase']['updatedQuantity'].sum(),
            'casesOrdered': group[group['coil'] == 'DeliveryCase']['quantity'].sum(),
            'casesPicked': group[group['coil'] == 'DeliveryCase']['updatedQuantity'].sum(),
            'currentQty': group['currentQty'].max()
        })
    
    grouped = df.groupby(['locDescription', 'providerName', 'machineBarcode', 'product']).apply(calculate_markets_stats).reset_index()
    grouped = grouped.rename(columns={'machineBarcode': 'pogName'})
    grouped['singlesDiff'] = grouped['singlesPicked'] - grouped['singlesOrdered']
    grouped['casesDiff'] = grouped['casesPicked'] - grouped['casesOrdered']
    
    stockouts = grouped[(grouped['providerName'] == 'Seed') & 
                       ((grouped['singlesDiff'] < 0) | (grouped['casesDiff'] < 0))]
    
    column_order = [
        'providerName', 'locDescription', 'pogName', 'product',
        'singlesOrdered', 'singlesPicked', 'casesOrdered', 'casesPicked',
        'singlesDiff', 'casesDiff', 'currentQty'
    ]
    stockouts = stockouts[column_order]
    return stockouts.sort_values(['pogName', 'product'])

def _process_ocs_data(df):
    """Process merged data to replicate Access OCS query logic"""
    def calculate_ocs_stats(group):
        return pd.Series({
            'singlesOrdered': group[group['coil'] != 'DeliveryCase']['quantity'].sum(),
            'singlesPicked': group[group['coil'] != 'DeliveryCase']['updatedQuantity'].sum(),
            'casesOrdered': group[group['coil'] == 'DeliveryCase']['quantity'].sum(),
            'casesPicked': group[group['coil'] == 'DeliveryCase']['updatedQuantity'].sum(),
            'currentQty': group['currentQty'].max()
        })
    
    grouped = df.groupby(['cusDescription', 'locDescription', 'product']).apply(calculate_ocs_stats).reset_index()
    grouped = grouped.rename(columns={'cusDescription': 'vendsysName', 'locDescription': 'seedName'})
    grouped['singlesDiff'] = grouped['singlesPicked'] - grouped['singlesOrdered']
    grouped['casesDiff'] = grouped['casesPicked'] - grouped['casesOrdered']
    
    stockouts = grouped[(grouped['singlesDiff'] < 0) | (grouped['casesDiff'] < 0)]
    
    column_order = [
        'vendsysName', 'seedName', 'product', 'singlesOrdered',
        'singlesPicked', 'casesOrdered', 'casesPicked', 'singlesDiff',
        'casesDiff', 'currentQty'
    ]
    stockouts = stockouts[column_order]
    return stockouts.sort_values(['vendsysName', 'seedName', 'product'])