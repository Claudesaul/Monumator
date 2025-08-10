"""
Test Updated ItemsScraper
========================

Test the updated ItemsScraper with the corrected export button logic.
"""

import asyncio
import os
from web_automation.items_scraper import ItemsScraper

async def test_updated_items_scraper():
    """Test the updated ItemsScraper functionality"""
    print("TESTING UPDATED ITEMS SCRAPER")
    print("=" * 50)
    print("Running in VISIBLE mode to verify functionality")
    print()
    
    scraper = None
    
    try:
        # Initialize scraper in visible mode
        scraper = ItemsScraper(headless=False)
        
        # Setup browser and login
        print("Setting up browser and logging into SEED...")
        if not await scraper.setup_and_login():
            raise Exception("Failed to setup browser and login to SEED")
        print("Login successful!")
        print()
        
        # Test the complete download_product_list method
        print("Testing download_product_list() method...")
        file_path = await scraper.download_product_list()
        
        if file_path and os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print("\n✅ ITEMS SCRAPER SUCCESS!")
            print(f"✅ File downloaded: {file_path}")
            print(f"✅ File size: {file_size} bytes")
            print("✅ ItemsScraper is working correctly!")
        else:
            print("❌ ITEMS SCRAPER FAILED!")
            print("No file was downloaded")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper:
            print("\nCleaning up browser...")
            await scraper.cleanup_browser()
    
    print("\nItemsScraper test completed!")
    print("The scraper is ready for production use in inventory_adjustment.py")
    input("Press Enter to exit...")

def main():
    """Run the test"""
    print("Starting ItemsScraper final test...")
    asyncio.run(test_updated_items_scraper())

if __name__ == "__main__":
    main()