"""
Product List Scraper
===================

Scrapes product list data from SEED using browser automation.
Downloads and processes Excel files from ItemImportExport page.
"""

import os
import time
import tempfile
import shutil
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser

class ProductListScraper(BaseScraper):
    """
    Scrapes product list data from SEED ItemImportExport page
    """
    
    def __init__(self, headless=True):
        """Initialize product list scraper"""
        super().__init__(headless)
        self.seed_browser = None
        self.download_dir = None
        
    def setup_download_directory(self):
        """
        Setup temporary download directory
        
        Returns:
            str: Path to download directory
        """
        self.download_dir = tempfile.mkdtemp()
        print(f"📁 Created download directory: {self.download_dir}")
        return self.download_dir
    
    def wait_for_vue_app(self):
        """
        Wait for Vue.js application to fully load
        
        Returns:
            bool: True if app loaded, False otherwise
        """
        try:
            print("⏳ Waiting for Vue.js application to load...")
            time.sleep(10)  # Vue.js apps need time to initialize
            
            # Additional wait for dynamic content
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            print("✅ Vue.js application loaded")
            return True
            
        except Exception as e:
            print(f"⚠️ Vue.js app load warning: {str(e)}")
            return False
    
    def find_export_button(self):
        """
        Find and click the export button using multiple strategies
        
        Returns:
            bool: True if button found and clicked, False otherwise
        """
        print("🔍 Looking for export button...")
        
        # Multiple selector strategies for export button
        button_selectors = [
            "//button[contains(text(), 'Export')]",
            "//button[contains(@class, 'export')]",
            "//input[@type='button'][contains(@value, 'Export')]",
            "//a[contains(text(), 'Export')]",
            "//button[contains(text(), 'Download')]",
            "//button[contains(@class, 'download')]"
        ]
        
        for selector in button_selectors:
            try:
                print(f"🔍 Trying selector: {selector}")
                button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                
                if button:
                    print(f"✅ Found export button with selector: {selector}")
                    button.click()
                    print("🖱️ Export button clicked")
                    return True
                    
            except TimeoutException:
                continue
            except Exception as e:
                print(f"⚠️ Error with selector {selector}: {str(e)}")
                continue
        
        print("❌ No export button found with any selector")
        return False
    
    def monitor_download(self, timeout=60):
        """
        Monitor download directory for new Excel files
        
        Args:
            timeout (int): Maximum wait time in seconds
            
        Returns:
            str: Path to downloaded file, or None if not found
        """
        print("⏳ Monitoring for file download...")
        
        start_time = time.time()
        initial_files = set(glob.glob(os.path.join(self.download_dir, "*")))
        
        while time.time() - start_time < timeout:
            current_files = set(glob.glob(os.path.join(self.download_dir, "*")))
            new_files = current_files - initial_files
            
            if new_files:
                for file_path in new_files:
                    if file_path.endswith(('.xlsx', '.xls')) and not file_path.endswith('.tmp'):
                        # Wait a bit more to ensure download is complete
                        time.sleep(2)
                        
                        # Check if file size is stable (download complete)
                        if self.is_download_complete(file_path):
                            print(f"✅ Download complete: {os.path.basename(file_path)}")
                            return file_path
            
            time.sleep(1)
        
        print(f"❌ Download timeout after {timeout} seconds")
        return None
    
    def is_download_complete(self, file_path, stable_time=3):
        """
        Check if file download is complete by monitoring file size
        
        Args:
            file_path (str): Path to file
            stable_time (int): Time file size must be stable
            
        Returns:
            bool: True if download complete, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            initial_size = os.path.getsize(file_path)
            time.sleep(stable_time)
            final_size = os.path.getsize(file_path)
            
            return initial_size == final_size and final_size > 0
            
        except Exception:
            return False
    
    def validate_excel_file(self, file_path):
        """
        Validate downloaded Excel file and extract basic info
        
        Args:
            file_path (str): Path to Excel file
            
        Returns:
            dict: File validation results
        """
        try:
            # Try to read the Excel file
            df = pd.read_excel(file_path)
            
            validation_results = {
                'valid': True,
                'rows': len(df),
                'columns': len(df.columns),
                'file_size': os.path.getsize(file_path),
                'sample_columns': list(df.columns[:5]) if len(df.columns) > 0 else []
            }
            
            print(f"📊 Excel validation: {validation_results['rows']} rows, {validation_results['columns']} columns")
            return validation_results
            
        except Exception as e:
            print(f"❌ Excel validation failed: {str(e)}")
            return {
                'valid': False,
                'error': str(e),
                'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
    
    def copy_to_temp_location(self, source_path, temp_directory="downloads/temp"):
        """
        Copy downloaded file to standardized temp location
        
        Args:
            source_path (str): Source file path
            temp_directory (str): Target temp directory
            
        Returns:
            str: Path to copied file
        """
        try:
            # Ensure temp directory exists
            os.makedirs(temp_directory, exist_ok=True)
            
            # Generate target filename
            filename = "ItemImportExample.xlsx"
            target_path = os.path.join(temp_directory, filename)
            
            # Copy file
            shutil.copy2(source_path, target_path)
            print(f"📁 Copied file to: {target_path}")
            
            return target_path
            
        except Exception as e:
            print(f"❌ Failed to copy file: {str(e)}")
            raise
    
    def cleanup_download_directory(self):
        """
        Clean up temporary download directory
        """
        if self.download_dir and os.path.exists(self.download_dir):
            try:
                shutil.rmtree(self.download_dir)
                print(f"🗑️ Cleaned up download directory")
            except Exception as e:
                print(f"⚠️ Cleanup warning: {str(e)}")
    
    def run_product_list_download(self):
        """
        Complete workflow for product list download
        
        Returns:
            dict: Results dictionary with success status and details
        """
        start_time = time.time()
        
        try:
            print("🚀 Starting product list download...")
            
            # Setup browser and download directory
            self.setup_browser()
            self.setup_download_directory()
            self.seed_browser = SeedBrowser(self.driver)
            
            # Login to SEED
            if not self.seed_browser.login():
                raise Exception("Failed to login to SEED")
            
            # Navigate to ItemImportExport
            if not self.seed_browser.navigate_to_item_import_export():
                raise Exception("Failed to navigate to ItemImportExport page")
            
            # Wait for Vue.js app
            self.wait_for_vue_app()
            
            # Find and click export button
            if not self.find_export_button():
                raise Exception("Could not find or click export button")
            
            # Monitor download
            downloaded_file = self.monitor_download()
            if not downloaded_file:
                raise Exception("File download failed or timed out")
            
            # Validate Excel file
            validation = self.validate_excel_file(downloaded_file)
            if not validation['valid']:
                raise Exception(f"Downloaded file validation failed: {validation.get('error', 'Unknown error')}")
            
            # Copy to temp location
            temp_file = self.copy_to_temp_location(downloaded_file)
            
            # Calculate results
            elapsed_time = time.time() - start_time
            
            results = {
                'success': True,
                'file_path': temp_file,
                'elapsed_time': elapsed_time,
                'validation': validation,
                'original_file': downloaded_file
            }
            
            print(f"✅ Product list download completed in {elapsed_time:.1f} seconds")
            return results
            
        except Exception as e:
            print(f"❌ Product list download failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }
        finally:
            self.cleanup_browser()
            self.cleanup_download_directory()

# Convenience function for backward compatibility
def download_product_list_with_browser(headless=True):
    """
    Download product list using browser automation (backward compatibility)
    
    Args:
        headless (bool): Run in headless mode
        
    Returns:
        dict: Results dictionary
    """
    scraper = ProductListScraper(headless=headless)
    return scraper.run_product_list_download()