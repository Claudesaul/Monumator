"""
Inventory Confirmation Report Workflow
=====================================

Complete workflow for generating Inventory Confirmation Reports via web scraping.
"""

from web_automation.inventory_scraper import run_inventory_confirmation_scraper

def process_inventory_confirmation_report(headless=True):
    """
    Complete workflow for processing Inventory Confirmation Report
    
    Args:
        headless (bool): Run browser in headless mode
        
    Returns:
        dict: Results dictionary with success status and details
    """
    print("🚀 Starting Inventory Confirmation Report processing...")
    
    # Use the consolidated inventory scraper
    results = run_inventory_confirmation_scraper(headless=headless)
    
    if results['success']:
        print("✅ Inventory Confirmation Report completed successfully")
    else:
        print("❌ Inventory Confirmation Report failed")
    
    return results

def get_inventory_confirmation_status():
    """
    Get current status of inventory confirmation processing capabilities
    
    Returns:
        dict: Status information
    """
    import os
    from datetime import datetime
    
    # Check template file
    template_path = "templates/Daily Inventory SEED.xlsx"
    template_exists = os.path.exists(template_path)
    
    # Check selenium availability
    try:
        import selenium
        selenium_available = True
    except ImportError:
        selenium_available = False
    
    status = {
        'ready_for_processing': template_exists and selenium_available,
        'template_exists': template_exists,
        'template_path': template_path,
        'selenium_available': selenium_available,
        'target_routes': ["Rt 102", "Rt 106", "Rt 206", "Rt 305"],
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status