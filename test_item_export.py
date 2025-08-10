"""
Test Item Import/Export Download
===============================

Test the ItemsScraper to ensure it can successfully download the item export file.
"""

import asyncio
import os
from web_automation.items_scraper import ItemsScraper

async def test_item_export_download():
    """Test the item export download functionality"""
    print("TESTING ITEM EXPORT DOWNLOAD")
    print("=" * 50)
    print("Running in VISIBLE mode to verify download process")
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
        
        # Setup download directory
        download_dir = scraper.setup_download_directory()
        print(f"Download directory: {download_dir}")
        print()
        
        # Navigate to item import/export page
        print("Navigating to Item Import/Export page...")
        if not await scraper.navigate_to_item_import_export():
            raise Exception("Failed to navigate to Item Import/Export page")
        print("Navigation successful!")
        print()
        
        # Wait for Vue.js app to load
        print("Waiting for Vue.js application...")
        if not await scraper.wait_for_vue_app():
            print("Warning: Vue.js app may not have loaded completely")
        print()
        
        # Test download functionality
        print("TESTING DOWNLOAD FUNCTIONALITY:")
        print("Looking for export/download buttons on the page...")
        
        # Look for common export button patterns
        export_buttons = [
            "button:has-text('Export')",
            "button:has-text('Download')",
            "[data-testid*='export']",
            "[class*='export']",
            "input[type='submit']",
            ".btn:has-text('Excel')",
            ".btn:has-text('Export')"
        ]
        
        found_buttons = []
        for selector in export_buttons:
            try:
                buttons = await scraper.page.locator(selector).all()
                if buttons:
                    for i, button in enumerate(buttons):
                        text = (await button.text_content() or "").strip()
                        if text:
                            found_buttons.append(f"Button: '{text}' (selector: {selector})")
                            print(f"Found button: '{text}'")
            except:
                continue
        
        if found_buttons:
            print(f"\nFound {len(found_buttons)} potential export buttons:")
            for btn in found_buttons:
                print(f"  - {btn}")
            
            # Try to click the first export-like button
            print("\nAttempting to trigger download...")
            
            # Look for the most likely export button
            likely_selectors = [
                "button:has-text('Export')",
                "input[type='submit']", 
                "button:has-text('Download')"
            ]
            
            download_triggered = False
            for selector in likely_selectors:
                try:
                    button = scraper.page.locator(selector).first
                    if await button.count() > 0:
                        print(f"Clicking button: {selector}")
                        await button.click()
                        download_triggered = True
                        break
                except Exception as e:
                    print(f"Failed to click {selector}: {str(e)}")
                    continue
            
            if download_triggered:
                print("Download attempt completed!")
                print("Checking download directory...")
                
                # Wait a moment for download to complete
                await asyncio.sleep(3)
                
                # Check download directory
                if os.path.exists(download_dir):
                    files = os.listdir(download_dir)
                    if files:
                        print(f"\n✅ DOWNLOAD SUCCESS!")
                        print(f"Files downloaded:")
                        for file in files:
                            file_path = os.path.join(download_dir, file)
                            file_size = os.path.getsize(file_path)
                            print(f"  - {file} ({file_size} bytes)")
                    else:
                        print("\n⚠️ No files found in download directory")
                        print("Download may still be in progress or failed")
                else:
                    print("\n❌ Download directory not found")
            else:
                print("\n⚠️ Could not find or click export button")
                print("Manual investigation needed")
        else:
            print("\n⚠️ No export buttons found on the page")
            print("The page structure may have changed")
        
        print("\nPAGE STRUCTURE ANALYSIS:")
        print("Current URL:", scraper.page.url)
        
        # Check for forms
        forms = await scraper.page.locator("form").all()
        print(f"Found {len(forms)} forms on the page")
        
        # Check for inputs
        inputs = await scraper.page.locator("input").all()
        print(f"Found {len(inputs)} input elements")
        
        # Check for Vue components
        vue_elements = await scraper.page.locator("[data-v-]").all()
        print(f"Found {len(vue_elements)} Vue.js components")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper:
            print("\nCleaning up browser...")
            await scraper.cleanup_browser()
            
            # Cleanup download directory
            if hasattr(scraper, 'download_dir') and scraper.download_dir:
                try:
                    import shutil
                    shutil.rmtree(scraper.download_dir)
                    print("Download directory cleaned up")
                except:
                    pass
    
    print("\nItem export test completed!")
    input("Press Enter to exit...")

def main():
    """Run the test"""
    print("Starting item export download test...")
    asyncio.run(test_item_export_download())

if __name__ == "__main__":
    main()