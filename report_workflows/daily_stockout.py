"""
Daily Stockout Report Workflow
==============================

Complete workflow for generating Daily Stockout Reports.
Orchestrates database queries and Excel generation.
"""

import time
from datetime import datetime
from database.queries import execute_all_queries
from database.connection import test_database_connection
from excel_processing.stockout_excel import StockoutExcelProcessor

def validate_prerequisites():
    """
    Validate all prerequisites for stockout report generation
    
    Returns:
        dict: Validation results
    """
    validation_results = {
        'database_connected': False,
        'all_valid': False
    }
    
    # Check database
    validation_results['database_connected'] = test_database_connection()
    
    # Overall validation
    validation_results['all_valid'] = validation_results['database_connected']
    
    if not validation_results['all_valid']:
        print("❌ Database connection failed")
    
    return validation_results

def fetch_stockout_data():
    """
    Fetch data for stockout report from database
        
    Returns:
        dict: Dictionary containing all query results
    """
    return execute_all_queries()

def process_stockout_data(raw_data):
    """
    Process and validate stockout data
    
    Args:
        raw_data (dict): Raw data from database queries
        
    Returns:
        dict: Processed and validated data
    """
    print("🔄 Processing data...")
    
    processed_data = {}
    
    for sheet_name, data in raw_data.items():
        if data is not None and not data.empty:
            # Basic data cleaning
            cleaned_data = data.fillna('')  # Replace NaN with empty strings
            processed_data[sheet_name] = cleaned_data
        else:
            if sheet_name in ['null_orders', 'ocs']:
                print(f"⚠️ No data for {sheet_name}")
            processed_data[sheet_name] = data
    
    return processed_data

def generate_stockout_excel(data_dict, output_directory="downloads/daily"):
    """
    Generate Excel report from processed data
    
    Args:
        data_dict (dict): Processed data dictionary
        output_directory (str): Output directory for Excel file
        
    Returns:
        str: Path to generated Excel file
    """
    print("📄 Generating Excel report...")
    
    # Create Excel processor
    excel_processor = StockoutExcelProcessor()
    
    # Generate report
    output_path = excel_processor.generate_stockout_report(data_dict, output_directory)
    
    print(f"💾 Saved: {output_path}")
    
    return output_path

def process_stockout_report(output_directory="downloads/daily"):
    """
    Complete workflow for processing Daily Stockout Report
    
    Args:
        output_directory (str): Directory to save the report
        
    Returns:
        dict: Results dictionary with success status and details
    """
    start_time = time.time()
    
    try:
        # Step 1: Validate prerequisites
        validation = validate_prerequisites()
        
        if not validation['all_valid']:
            if not validation['database_connected']:
                raise Exception("Database connection failed - cannot generate report")
        
        # Step 2: Fetch data
        raw_data = fetch_stockout_data()
        
        if not raw_data:
            raise Exception("No data retrieved")
        
        # Step 3: Process data
        processed_data = process_stockout_data(raw_data)
        
        # Step 4: Generate Excel report
        output_path = generate_stockout_excel(processed_data, output_directory)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare results
        results = {
            'success': True,
            'output_path': output_path,
            'processing_time': processing_time,
            'data_summary': {
                'highlights': len(processed_data.get('highlights', [])),
                'markets': len(processed_data.get('markets', [])),
                'null_orders': len(processed_data.get('null_orders', [])),
                'ocs': len(processed_data.get('ocs', []))
            },
            'validation': validation
        }
        
        print(f"✅ Report completed successfully ({processing_time:.1f}s)")
        
        return results
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Daily Stockout Report failed: {str(e)}")
        
        return {
            'success': False,
            'error': str(e),
            'processing_time': processing_time
        }

def get_stockout_processing_status():
    """
    Get current status of stockout processing capabilities
    
    Returns:
        dict: Status information
    """
    validation = validate_prerequisites()
    
    status = {
        'ready_for_processing': validation['all_valid'],
        'database': {
            'connected': validation['database_connected'],
            'dsn': 'Lightspeed',
            'user': 'LSReadOnly'
        },
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status