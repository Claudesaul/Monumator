"""
Product List Scraper - Playwright Edition
=========================================

Async product list scraping with Playwright and Firefox.
Downloads and processes Excel files from ItemImportExport page.
"""

import os
import asyncio
import tempfile
import shutil
from typing import Dict, Any, Optional
from pathlib import Path
import pandas as pd
from playwright.async_api import Page, Download
from playwright.async_api import TimeoutError as PlaywrightTimeout
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser

class ProductListScraper(BaseScraper):
    """
    Async scraper for product list data from SEED ItemImportExport page
    """
    
    def __init__(self, headless: bool = True):
        """Initialize product list scraper"""
        super().__init__(headless)
        self.seed_browser: Optional[SeedBrowser] = None
        self.download_dir: Optional[str] = None
        
    def setup_download_directory(self) -> str:
        """
        Setup temporary download directory
        
        Returns:
            Path to download directory
        """
        self.download_dir = tempfile.mkdtemp()
        print(f"📁 Created download directory: {self.download_dir}")
        return self.download_dir
    
    async def wait_for_vue_app(self) -> bool:
        """
        Wait for Vue.js application to fully load
        
        Returns:
            bool: True if app loaded
        """
        try:
            print("⏳ Waiting for Vue.js application to load...")
            
            # Wait for network idle and Vue attributes
            await self.page.wait_for_load_state('networkidle', timeout=15000)
            
            # Additional wait for Vue components (look for Vue-specific attributes)
            try:
                await self.page.wait_for_selector("[data-v-]", timeout=5000)
            except PlaywrightTimeout:
                # Vue attributes are optional, page might still be loaded
                pass
            
            print("✅ Vue.js application loaded")
            return True
            
        except Exception as e:
            print(f"⚠️ Vue.js app load warning: {str(e)}")
            return True  # Continue anyway
    
    async def find_and_click_export_button(self) -> Download:
        """
        Find and click the export button, wait for download
        
        Returns:
            Download object if successful
        """
        print("🔍 Looking for export button...")
        
        # Multiple selector strategies for export button
        button_selectors = [
            "button:has-text('Export')",
            "button:has-text('Download')",
            "input[type='button'][value*='Export']",
            "a:has-text('Export')",
            "button.export",
            "button.download"
        ]
        
        for selector in button_selectors:
            try:
                print(f"🔍 Trying selector: {selector}")
                
                # Check if button exists and is visible
                button = self.page.locator(selector).first
                if await button.count() > 0 and await button.is_visible():
                    print(f"✅ Found export button with selector: {selector}")
                    
                    # Start waiting for download before clicking
                    async with self.page.expect_download() as download_info:
                        await button.click()
                        print("🖱️ Export button clicked")
                    
                    download = await download_info.value
                    print("📥 Download started")
                    return download
                    
            except PlaywrightTimeout:
                continue
            except Exception as e:
                print(f"⚠️ Error with selector {selector}: {str(e)}")
                continue
        
        raise Exception("No export button found with any selector")
    
    async def handle_download(self, download: Download) -> str:
        """
        Handle the download and save to temporary location
        
        Args:
            download: Playwright Download object
            
        Returns:
            Path to saved file
        """
        try:
            # Get suggested filename
            suggested_filename = download.suggested_filename
            print(f"📥 Downloading: {suggested_filename}")
            
            # Save to download directory
            save_path = os.path.join(self.download_dir, suggested_filename)
            await download.save_as(save_path)
            
            print(f"✅ Download complete: {suggested_filename}")
            return save_path
            
        except Exception as e:
            print(f"❌ Download handling failed: {str(e)}")
            raise
    
    def validate_excel_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate downloaded Excel file and extract basic info
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            File validation results
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
    
    def copy_to_temp_location(self, source_path: str, temp_directory: str = "downloads/temp") -> str:
        """
        Copy downloaded file to standardized temp location
        
        Args:
            source_path: Source file path
            temp_directory: Target temp directory
            
        Returns:
            Path to copied file
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
    
    async def run_product_list_download(self) -> Dict[str, Any]:
        """
        Complete async workflow for product list download
        
        Returns:
            Results dictionary with success status and details
        """
        import time
        start_time = time.time()
        
        try:
            print("🚀 Starting product list download...")
            
            # Setup browser and download directory
            await self.setup_browser()
            self.setup_download_directory()
            self.seed_browser = SeedBrowser(self.page)
            
            # Login to SEED
            if not await self.seed_browser.login():
                raise Exception("Failed to login to SEED")
            
            # Navigate to ItemImportExport
            if not await self.seed_browser.navigate_to_item_import_export():
                raise Exception("Failed to navigate to ItemImportExport page")
            
            # Wait for Vue.js app
            await self.wait_for_vue_app()
            
            # Find and click export button, get download
            download = await self.find_and_click_export_button()
            
            # Handle the download
            downloaded_file = await self.handle_download(download)
            
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
            await self.cleanup_browser()
            self.cleanup_download_directory()

# Async wrapper function
async def download_product_list_with_browser_async(headless: bool = True) -> Dict[str, Any]:
    """
    Download product list using async browser automation
    
    Args:
        headless: Run in headless mode
        
    Returns:
        Results dictionary
    """
    scraper = ProductListScraper(headless=headless)
    return await scraper.run_product_list_download()

# Synchronous wrapper for menu system integration
def download_product_list_with_browser(headless: bool = True) -> Dict[str, Any]:
    """
    Download product list using browser automation (synchronous wrapper)
    
    Args:
        headless: Run in headless mode
        
    Returns:
        Results dictionary
    """
    return asyncio.run(download_product_list_with_browser_async(headless))