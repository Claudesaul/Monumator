"""
Inventory Adjustment Report Workflow
====================================

Complete workflow for generating Inventory Adjustment Reports.
Orchestrates data downloads, processing, and Excel generation.
"""

import os
import time
from datetime import datetime
from config.report_config import SEED_REPORTS
from utils.downloader import download_seed_report
from excel_processing.inventory_excel import InventoryExcelProcessor
from web_automation.product_scraper import download_product_list_with_browser
import pandas as pd

def get_inventory_adjustment_report_id():
    """
    Determine which inventory adjustment report to use based on current day
    Monday = 3 days ago (Friday data), Other days = previous day
    
    Returns:
        tuple: (report_id, description)
    """
    today = datetime.now().weekday()  # 0=Monday, 6=Sunday
    
    if today == 0:  # Monday
        report_id = SEED_REPORTS["inventory_adjustment_3_days_ago"]
        description = "Friday data (3 days ago)"
    else:  # Tuesday-Friday
        report_id = SEED_REPORTS["inventory_adjustment_previous_day"]
        description = "Previous business day"
    
    return report_id, description

def validate_inventory_prerequisites():
    """
    Validate prerequisites for inventory adjustment report
    
    Returns:
        dict: Validation results
    """
    print("🔍 Validating inventory adjustment prerequisites...")
    
    validation_results = {
        'temp_directory': True,  # We can create this
        'all_valid': False
    }
    
    # Ensure temp directory
    temp_dir = "downloads/temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Overall validation
    validation_results['all_valid'] = validation_results['temp_directory']
    
    if validation_results['all_valid']:
        print("✅ Inventory adjustment prerequisites validated")
    else:
        print("❌ Inventory adjustment prerequisites validation failed")
    
    return validation_results

def download_iad_report(temp_directory="downloads/temp"):
    """
    Download inventory adjustment detail report
    
    Args:
        temp_directory (str): Directory to save downloaded report
        
    Returns:
        str: Path to downloaded file
    """
    # Get appropriate report ID for current day
    report_id, description = get_inventory_adjustment_report_id()
    print(f"📥 Downloading IAD report: {description}")
    
    # Download report
    filename = "inventory_adjustment_detail.xlsx"
    success = download_seed_report(report_id, filename, temp_directory)
    
    if success:
        file_path = os.path.join(temp_directory, filename)
        print(f"✅ IAD report downloaded: {file_path}")
        return file_path
    else:
        raise Exception("Failed to download IAD report")

def download_product_list(temp_directory="downloads/temp"):
    """
    Download product list using browser automation
    
    Args:
        temp_directory (str): Directory to save downloaded file
        
    Returns:
        str: Path to downloaded file
    """
    print("📥 Downloading product list via browser automation...")
    
    # Use browser automation to download product list
    result = download_product_list_with_browser(headless=True)
    
    if result['success']:
        print(f"✅ Product list downloaded: {result['file_path']}")
        return result['file_path']
    else:
        raise Exception(f"Failed to download product list: {result.get('error', 'Unknown error')}")

def load_iad_data(file_path):
    """
    Load and validate IAD data from Excel file
    
    Args:
        file_path (str): Path to IAD Excel file
        
    Returns:
        pandas.DataFrame: Loaded IAD data
    """
    try:
        print("📊 Loading IAD data...")
        df = pd.read_excel(file_path)
        
        print(f"📋 Loaded {len(df)} rows of IAD data")
        return df
        
    except Exception as e:
        print(f"❌ Failed to load IAD data: {str(e)}")
        raise

def load_product_list_data(file_path):
    """
    Load and validate product list data from Excel file
    
    Args:
        file_path (str): Path to product list Excel file
        
    Returns:
        pandas.DataFrame: Loaded product list data
    """
    try:
        print("📊 Loading product list data...")
        df = pd.read_excel(file_path)
        
        print(f"📋 Loaded {len(df)} rows of product list data")
        return df
        
    except Exception as e:
        print(f"❌ Failed to load product list data: {str(e)}")
        raise

def process_iad_data(iad_df):
    """
    Process and clean IAD data
    
    Args:
        iad_df (pandas.DataFrame): Raw IAD data
        
    Returns:
        pandas.DataFrame: Processed IAD data
    """
    print("🔄 Processing IAD data...")
    
    # Basic data cleaning
    processed_df = iad_df.fillna('')  # Replace NaN with empty strings
    
    # Additional processing could be added here
    # For example: data validation, filtering, calculations
    
    print(f"✅ Processed {len(processed_df)} rows of IAD data")
    return processed_df

def generate_inventory_excel(iad_data, items_data, output_directory="downloads/daily"):
    """
    Generate Excel report from processed data
    
    Args:
        iad_data (pandas.DataFrame): Processed IAD data
        items_data (pandas.DataFrame): Product list data
        output_directory (str): Output directory for Excel file
        
    Returns:
        str: Path to generated Excel file
    """
    print("📄 Generating inventory adjustment Excel report...")
    
    # Create Excel processor
    excel_processor = InventoryExcelProcessor()
    
    # Generate report
    output_path = excel_processor.generate_inventory_adjustment_report(
        iad_data, items_data, output_directory
    )
    
    return output_path

def cleanup_temp_files(*file_paths):
    """
    Clean up temporary files
    
    Args:
        *file_paths: Variable number of file paths to clean up
    """
    for file_path in file_paths:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Removed temp file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"⚠️ Could not remove temp file {file_path}: {str(e)}")

def process_inventory_adjustment_summary(output_directory="downloads/daily"):
    """
    Complete workflow for processing Inventory Adjustment Summary
    
    Args:
        output_directory (str): Directory to save the report
        
    Returns:
        dict: Results dictionary with success status and details
    """
    start_time = time.time()
    iad_file_path = None
    product_file_path = None
    
    try:
        print("🚀 Starting Inventory Adjustment Summary processing...")
        
        # Step 1: Validate prerequisites
        validation = validate_inventory_prerequisites()
        
        if not validation['all_valid']:
            raise Exception("Prerequisites validation failed")
        
        # Step 2: Get report ID info
        report_id, description = get_inventory_adjustment_report_id()
        
        # Step 3: Download IAD report
        iad_file_path = download_iad_report()
        
        # Step 4: Download product list
        product_file_path = download_product_list()
        
        # Step 5: Load and process data
        iad_data = load_iad_data(iad_file_path)
        items_data = load_product_list_data(product_file_path)
        
        processed_iad_data = process_iad_data(iad_data)
        
        # Step 6: Generate Excel report
        output_path = generate_inventory_excel(processed_iad_data, items_data, output_directory)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare results
        results = {
            'success': True,
            'output_path': output_path,
            'processing_time': processing_time,
            'report_id': report_id,
            'description': description,
            'data_summary': {
                'rows': len(processed_iad_data),
                'columns': len(processed_iad_data.columns) if hasattr(processed_iad_data, 'columns') else 0
            },
            'validation': validation
        }
        
        print(f"✅ Inventory Adjustment Summary completed successfully in {processing_time:.2f} seconds")
        print(f"📁 Output file: {output_path}")
        
        return results
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Inventory Adjustment Summary failed: {str(e)}")
        
        return {
            'success': False,
            'error': str(e),
            'processing_time': processing_time
        }
    finally:
        # Cleanup temp files
        cleanup_temp_files(iad_file_path, product_file_path)

def get_inventory_adjustment_status():
    """
    Get current status of inventory adjustment processing capabilities
    
    Returns:
        dict: Status information
    """
    validation = validate_inventory_prerequisites()
    report_id, description = get_inventory_adjustment_report_id()
    
    status = {
        'ready_for_processing': validation['all_valid'],
        'report_id': report_id,
        'description': description,
        'current_date': datetime.now().strftime('%Y-%m-%d'),
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status