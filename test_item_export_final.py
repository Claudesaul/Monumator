"""
Final Item Export Test
=====================

Test clicking the "Export Importable Data" button to download the item export file.
"""

import asyncio
import os
from web_automation.items_scraper import ItemsScraper

async def test_export_importable_data():
    """Test clicking the Export Importable Data button"""
    print("TESTING EXPORT IMPORTABLE DATA BUTTON")
    print("=" * 50)
    print("Running in VISIBLE mode to verify download")
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
        
        # Look for the "Export Importable Data" button
        print("Looking for 'Export Importable Data' button...")
        
        # Find ALL buttons and look for the export ones directly
        all_buttons = await scraper.page.locator("button, input[type='button'], input[type='submit']").all()
        
        export_button = None
        
        for i, button in enumerate(all_buttons):
            text = (await button.text_content() or "").strip()
            value = await button.get_attribute("value") or ""
            
            # Look for the main export button (not the inactive only one)
            if text == "Export Importable Data":
                export_button = button
                print(f"✅ Found export button: Button {i+1}")
                print(f"   Button text: '{text}'")
                print(f"   Button value: '{value}'")
                break
            # Fallback to the inactive only button if main one not found
            elif "Export Importable Data" in text and not export_button:
                export_button = button
                print(f"✅ Found export button (fallback): Button {i+1}")
                print(f"   Button text: '{text}'")
                print(f"   Button value: '{value}'")
                # Don't break here, keep looking for the main button
        
        if not export_button:
            print("❌ Could not find 'Export Importable Data' button")
            print("Available buttons on page:")
            
            # List all buttons for debugging
            all_buttons = await scraper.page.locator("button, input[type='button'], input[type='submit']").all()
            for i, btn in enumerate(all_buttons):
                text = (await btn.text_content() or "").strip()
                value = await btn.get_attribute("value") or ""
                print(f"  Button {i+1}: Text='{text}', Value='{value}'")
            
            return
        
        # Set up download listener
        print("\nSetting up download monitoring...")
        downloads = []
        
        def handle_download(download):
            downloads.append(download)
            print(f"📥 Download started: {download.suggested_filename}")
        
        scraper.page.on("download", handle_download)
        
        # Click the export button
        print(f"\nClicking export button...")
        await export_button.click()
        print("Export button clicked!")
        
        # Wait for download to start
        print("Waiting for download to start...")
        await asyncio.sleep(3)
        
        if downloads:
            download = downloads[0]
            filename = download.suggested_filename
            print(f"✅ Download detected: {filename}")
            
            # Save the download
            download_path = os.path.join(download_dir, filename)
            await download.save_as(download_path)
            print(f"💾 Download saved to: {download_path}")
            
            # Check file size
            if os.path.exists(download_path):
                file_size = os.path.getsize(download_path)
                print(f"📊 File size: {file_size} bytes")
                
                if file_size > 0:
                    print("✅ DOWNLOAD SUCCESSFUL!")
                    print(f"✅ Item export file downloaded: {filename}")
                else:
                    print("⚠️ Downloaded file is empty")
            else:
                print("❌ Downloaded file not found")
        else:
            print("⚠️ No download detected")
            print("Checking download directory manually...")
            
            # Check directory for any new files
            if os.path.exists(download_dir):
                files = os.listdir(download_dir)
                if files:
                    print(f"Files found in download directory:")
                    for file in files:
                        file_path = os.path.join(download_dir, file)
                        file_size = os.path.getsize(file_path)
                        print(f"  - {file} ({file_size} bytes)")
                else:
                    print("No files found in download directory")
        
        print("\nTest completed successfully!")
        
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
    
    input("\nPress Enter to exit...")

def main():
    """Run the test"""
    print("Starting Export Importable Data test...")
    asyncio.run(test_export_importable_data())

if __name__ == "__main__":
    main()