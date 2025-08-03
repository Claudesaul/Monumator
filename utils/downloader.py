"""
SEED Report Downloader
======================

This module handles downloading reports from the SEED API (Cantaloupe).
It provides concurrent download capabilities with real-time progress tracking
and comprehensive error handling.

Features:
- Concurrent downloads with ThreadPoolExecutor
- Real-time progress messages
- Automatic authentication handling
- Comprehensive error reporting
- Success/failure tracking
"""

import requests
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from datetime import datetime
from dotenv import load_dotenv
from config.report_config import SEED_API_HOST, SEED_API_ENDPOINT, MAX_CONCURRENT_DOWNLOADS

# Load environment variables from .env file
load_dotenv()

def basic_auth(username, password):
    """
    Create Basic Authentication header for SEED API
    
    Args:
        username (str): SEED API username
        password (str): SEED API password
    
    Returns:
        str: Authorization header value
    """
    credentials = f"{username}:{password}"
    return "Basic " + b64encode(credentials.encode()).decode()

def get_seed_credentials():
    """
    Get SEED API credentials from environment variables
    
    Returns:
        tuple: (username, password) from environment variables
    """
    username = os.getenv("SEED_USERNAME")
    password = os.getenv("SEED_PASSWORD")
    
    if not username or not password:
        raise ValueError("SEED_USERNAME and SEED_PASSWORD must be set in .env file")
    
    return username, password

def download_seed_report(report_id, filename, download_path=""):
    """
    Download a single report from SEED API
    
    Args:
        report_id (str): The SEED report ID to download
        filename (str): Local filename to save the report as
        download_path (str): Optional path to save the file in
    
    Returns:
        dict: Result dictionary with success status and details
    """
    # Construct full file path
    full_path = os.path.join(download_path, filename) if download_path else filename
    
    # Get credentials
    username, password = get_seed_credentials()
    
    # Create API endpoint
    endpoint = f"{SEED_API_ENDPOINT}?ReportId={report_id}"
    
    # Create authentication header
    auth_header = basic_auth(username, password)
    
    try:
        # Make API request to download report
        response = requests.get(
            SEED_API_HOST + endpoint, 
            headers={'Authorization': auth_header}
        )
        
        if response.status_code == 200:
            # Ensure directory exists
            if download_path:
                os.makedirs(download_path, exist_ok=True)
            
            # Save the Excel file to disk
            with open(full_path, 'wb') as file:
                file.write(response.content)
            print(f"✅ SUCCESS: {filename} downloaded at {datetime.now().strftime('%H:%M:%S')}")
            return {"success": True, "filename": filename, "report_id": report_id, "path": full_path}
        else:
            print(f"❌ FAILED: Report {report_id} - Status code: {response.status_code}")
            return {"success": False, "filename": filename, "report_id": report_id, "path": full_path}
    except Exception as e:
        print(f"❌ ERROR: Report {report_id} - {str(e)}")
        return {"success": False, "filename": filename, "report_id": report_id, "path": full_path}

def download_multiple_reports_concurrent(reports_list, download_path=""):
    """
    Download multiple reports concurrently for faster processing
    
    Args:
        reports_list (list): List of tuples containing (report_id, filename)
        download_path (str): Optional path to save files in
    
    Returns:
        tuple: (successful_downloads, failed_downloads) lists
    """
    print(f"🚀 Starting download of {len(reports_list)} reports...")
    
    successful_downloads = []
    failed_downloads = []
    
    # Use ThreadPoolExecutor to download reports simultaneously
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
        # Submit all download jobs to the thread pool
        future_to_report = {
            executor.submit(download_seed_report, report_id, filename, download_path): (report_id, filename)
            for report_id, filename in reports_list
        }
        
        # Process results as they complete (real-time progress)
        for future in as_completed(future_to_report):
            result = future.result()
            if result["success"]:
                successful_downloads.append(result)
            else:
                failed_downloads.append(result)
    
    # Print final summary statistics
    print(f"\n📊 DOWNLOAD SUMMARY:")
    print(f"✅ Successful: {len(successful_downloads)}")
    print(f"❌ Failed: {len(failed_downloads)}")
    
    if len(failed_downloads) == 0:
        print("🎉 ALL REPORTS DOWNLOADED SUCCESSFULLY!")
    
    return successful_downloads, failed_downloads 