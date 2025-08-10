"""
Inventory Confirmation Report Workflow
=====================================

Complete workflow for generating Inventory Confirmation Reports via web scraping.
Orchestrates scraping and Excel generation.
"""

import asyncio
import time
import os
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from web_automation.inventory_confirmation_scraper import InventoryConfirmationScraper
from excel_processing.base_excel import ensure_directory_exists

async def run_inventory_confirmation_async(headless: bool = True) -> Dict[str, Any]:
    """
    Async workflow for inventory confirmation report
    
    Args:
        headless: Run browser in headless mode
        
    Returns:
        Results dictionary with success status and details
    """
    scraper = None
    start_time = time.time()
    
    try:
        print("🚀 Starting Inventory Confirmation Report processing...")
        
        # Initialize scraper with SEED capabilities
        scraper = InventoryConfirmationScraper(headless=headless)
        
        # Setup browser and login
        if not await scraper.setup_and_login():
            raise Exception("Failed to setup browser and login to SEED")
        
        # Get target date
        target_date = scraper.get_previous_business_day()
        
        # Scrape route data (finds incomplete routes dynamically)
        route_data = await scraper.get_incomplete_routes(target_date)
        
        if not route_data:
            raise Exception("No route data found")
        
        # Generate Excel report
        excel_file = generate_excel_report(route_data)
        
        # Calculate results
        elapsed_time = time.time() - start_time
        routes_found = len(route_data)
        assets_processed = sum(route.get('assets_processed', 0) for route in route_data)
        
        results = {
            'success': True,
            'excel_file': excel_file,
            'elapsed_time': elapsed_time,
            'routes_found': routes_found,
            'assets_processed': assets_processed,
            'route_data': route_data
        }
        
        print(f"✅ Inventory confirmation completed in {elapsed_time:.1f} seconds")
        return results
        
    except Exception as e:
        print(f"❌ Inventory confirmation failed: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'elapsed_time': time.time() - start_time
        }
    finally:
        if scraper:
            await scraper.cleanup_browser()

def generate_excel_report(route_data: list, output_directory: str = "downloads/daily") -> str:
    """
    Generate Excel report from route data
    
    Args:
        route_data: List of route data dictionaries
        output_directory: Directory to save report
        
    Returns:
        Path to generated Excel file
    """
    try:
        # Ensure output directory exists
        ensure_directory_exists(output_directory)
        
        # Create DataFrame
        df = pd.DataFrame(route_data)
        
        # Generate filename
        today = datetime.now()
        date_str = today.strftime("%m.%d.%y")
        filename = f"Daily Inventory Confirmation {date_str}.xlsx"
        output_path = os.path.join(output_directory, filename)
        
        # Save to Excel
        df.to_excel(output_path, index=False, sheet_name="Inventory Confirmation")
        
        print(f"📊 Generated Excel report: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Failed to generate Excel report: {str(e)}")
        raise

def process_inventory_confirmation_report(headless=True):
    """
    Complete workflow for processing Inventory Confirmation Report
    Synchronous wrapper for menu system integration
    
    Args:
        headless (bool): Run browser in headless mode
        
    Returns:
        dict: Results dictionary with success status and details
    """
    return asyncio.run(run_inventory_confirmation_async(headless=headless))

def get_inventory_confirmation_status():
    """
    Get current status of inventory confirmation processing capabilities
    
    Returns:
        dict: Status information
    """
    from datetime import datetime
    
    # Check Playwright availability
    try:
        import playwright
        playwright_available = True
    except ImportError:
        playwright_available = False
    
    status = {
        'ready_for_processing': playwright_available,
        'playwright_available': playwright_available,
        'target_routes': ["Rt 102", "Rt 106", "Rt 206", "Rt 305"],
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status