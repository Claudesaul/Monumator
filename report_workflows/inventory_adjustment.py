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
from utils.downloader import download_seed_report, download_items
from excel_processing.inventory_adjustment_excel import InventoryExcelProcessor
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
            except Exception as e:
                print(f"⚠️ Could not remove temp file {file_path}: {str(e)}")

def process_inventory_adjustment_summary(output_directory="downloads/daily", headless=True):
    """
    Complete workflow for processing Inventory Adjustment Summary
    
    Args:
        output_directory (str): Directory to save the report
        headless (bool): Run browser in headless mode for items download
        
    Returns:
        dict: Results dictionary with success status and details
    """
    start_time = time.time()
    iad_file_path = None
    items_file_path = None
    
    try:
        print("🚀 Starting Inventory Adjustment Summary processing...")
        
        # Ensure temp directory exists
        temp_dir = "downloads/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Step 1: Get report ID info
        report_id, description = get_inventory_adjustment_report_id()
        
        # Step 2: Download IAD report
        iad_file_path = download_iad_report()
        
        # Step 3: Download items list
        items_file_path = download_items(headless=headless)
        
        # Step 4: Load and process data
        iad_data = pd.read_excel(iad_file_path)
        
        items_data = pd.read_excel(items_file_path)
        
        # Clean data (replace NaN with empty strings)
        iad_data = iad_data.fillna('')
        
        # Step 5: Generate Excel report
        print("📄 Generating inventory adjustment Excel report...")
        excel_processor = InventoryExcelProcessor()
        output_path = excel_processor.generate_inventory_adjustment_report(
            iad_data, items_data, output_directory
        )
        
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
                'rows': len(iad_data),
                'columns': len(iad_data.columns) if hasattr(iad_data, 'columns') else 0
            }
        }
        
        print(f"✅ Inventory Adjustment Summary completed successfully")
        
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
        cleanup_temp_files(iad_file_path, items_file_path)

def get_inventory_adjustment_status():
    """
    Get current status of inventory adjustment processing capabilities
    
    Returns:
        dict: Status information
    """
    report_id, description = get_inventory_adjustment_report_id()
    
    status = {
        'ready_for_processing': True,
        'report_id': report_id,
        'description': description,
        'current_date': datetime.now().strftime('%Y-%m-%d'),
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status