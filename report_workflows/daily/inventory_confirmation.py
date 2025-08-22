"""
Inventory Confirmation Report Workflow
=====================================

Complete workflow for generating Inventory Confirmation Reports via web scraping.
Orchestrates scraping and Excel generation.
"""

import asyncio
import time
from typing import Dict, Any
from web_automation.inventory_confirmation_scraper import InventoryConfirmationScraper
from excel_processing.inventory_confirmation_excel import generate_inventory_confirmation_report

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
        
        # Calculate total assets
        total_assets = sum(len(route.get('incomplete_assets', [])) for route in route_data)
        print(f"🎯 Total incomplete assets found: {total_assets}")
        
        # Generate Excel report using the new processor
        excel_file = generate_inventory_confirmation_report(route_data)
        
        # Calculate results
        elapsed_time = time.time() - start_time
        print(f"✅ Inventory confirmation completed in {elapsed_time:.1f} seconds")
        return
        
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