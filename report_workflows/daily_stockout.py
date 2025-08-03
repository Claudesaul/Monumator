"""
Daily Stockout Report Workflow
==============================

Complete workflow for generating Daily Stockout Reports.
Orchestrates database queries and Excel generation.
"""

import time
from datetime import datetime
from database.queries import execute_all_queries, get_sample_data
from database.connection import test_database_connection
from excel_processing.stockout_excel import StockoutExcelProcessor, get_stockout_template_info

def validate_prerequisites():
    """
    Validate all prerequisites for stockout report generation
    
    Returns:
        dict: Validation results
    """
    print("🔍 Validating prerequisites...")
    
    validation_results = {
        'template_exists': False,
        'database_connected': False,
        'all_valid': False
    }
    
    # Check template
    template_info = get_stockout_template_info()
    validation_results['template_exists'] = template_info['exists']
    validation_results['template_info'] = template_info
    
    if validation_results['template_exists']:
        print("✅ Template file found")
    else:
        print("❌ Template file not found")
    
    # Check database
    validation_results['database_connected'] = test_database_connection()
    
    # Overall validation
    validation_results['all_valid'] = all(validation_results.values())
    
    if validation_results['all_valid']:
        print("✅ All prerequisites validated")
    else:
        print("❌ Prerequisites validation failed")
    
    return validation_results

def fetch_stockout_data(use_sample_data=False):
    """
    Fetch data for stockout report
    
    Args:
        use_sample_data (bool): Use sample data instead of database
        
    Returns:
        dict: Dictionary containing all query results
    """
    if use_sample_data:
        print("📊 Using sample data for testing")
        return get_sample_data()
    else:
        print("📊 Fetching data from database...")
        return execute_all_queries()

def process_stockout_data(raw_data):
    """
    Process and validate stockout data
    
    Args:
        raw_data (dict): Raw data from database queries
        
    Returns:
        dict: Processed and validated data
    """
    print("🔄 Processing stockout data...")
    
    processed_data = {}
    
    for sheet_name, data in raw_data.items():
        if data is not None and not data.empty:
            # Basic data cleaning
            cleaned_data = data.fillna('')  # Replace NaN with empty strings
            processed_data[sheet_name] = cleaned_data
            print(f"📋 {sheet_name}: {len(cleaned_data)} rows processed")
        else:
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
    
    return output_path

def process_stockout_report(use_sample_data=False, output_directory="downloads/daily"):
    """
    Complete workflow for processing Daily Stockout Report
    
    Args:
        use_sample_data (bool): Use sample data for testing
        output_directory (str): Directory to save the report
        
    Returns:
        dict: Results dictionary with success status and details
    """
    start_time = time.time()
    
    try:
        print("🚀 Starting Daily Stockout Report processing...")
        
        # Step 1: Validate prerequisites
        validation = validate_prerequisites()
        
        if not validation['all_valid'] and not use_sample_data:
            if not validation['database_connected']:
                print("⚠️ Database not available, switching to sample data")
                use_sample_data = True
            elif not validation['template_exists']:
                raise Exception("Template file is required but not found")
        
        # Step 2: Fetch data
        raw_data = fetch_stockout_data(use_sample_data)
        
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
            'used_sample_data': use_sample_data,
            'validation': validation
        }
        
        print(f"✅ Daily Stockout Report completed successfully in {processing_time:.2f} seconds")
        print(f"📁 Output file: {output_path}")
        
        return results
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Daily Stockout Report failed: {str(e)}")
        
        return {
            'success': False,
            'error': str(e),
            'processing_time': processing_time,
            'used_sample_data': use_sample_data
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
        'template': validation['template_info'],
        'database': {
            'connected': validation['database_connected'],
            'dsn': 'Lightspeed',
            'user': 'LSReadOnly'
        },
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status