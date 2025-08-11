"""
Items Scraper - Simplified
===========================

Focused items list download functionality.
Inherits SEED capabilities from SeedBrowser.
"""

import os
import tempfile
import shutil
from typing import Optional
import pandas as pd
from playwright.async_api import Download
from playwright.async_api import TimeoutError as PlaywrightTimeout
from .seed_browser import SeedBrowser

class ItemsScraper(SeedBrowser):
    """
    Specialized scraper for items list downloads
    Inherits SEED login/navigation from SeedBrowser
    """
    
    def __init__(self, headless: bool = True):
        """Initialize items scraper with SEED capabilities"""
        super().__init__(headless)
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
    
    
    async def find_and_click_export_button(self) -> Download:
        """Find and click export button"""
        # Use the more reliable has-text selector
        export_button = self.page.locator("button:has-text('Export Importable Data')").first
        
        async with self.page.expect_download() as download_info:
            await export_button.click()
        return await download_info.value
    
    async def handle_download(self, download: Download) -> str:
        """Handle download and save to temp directory"""
        filename = download.suggested_filename
        save_path = os.path.join(self.download_dir, filename)
        await download.save_as(save_path)
        return save_path
    
    def validate_excel_file(self, file_path: str) -> bool:
        """Validate Excel file"""
        try:
            pd.read_excel(file_path)
            return True
        except:
            return False
    
    def copy_to_temp_location(self, source_path: str) -> str:
        """Copy downloaded file to temp directory"""
        temp_dir = "downloads/temp"
        os.makedirs(temp_dir, exist_ok=True)
        target_path = os.path.join(temp_dir, "ItemImportExample.xlsx")
        shutil.copy2(source_path, target_path)
        print(f"📁 Copied to: {target_path}")
        return target_path
    
    def cleanup_download_directory(self):
        """Clean up temp directory"""
        if self.download_dir and os.path.exists(self.download_dir):
            try:
                shutil.rmtree(self.download_dir)
            except:
                pass
    
    async def download_items_list(self) -> str:
        """
        Download items list from ItemImportExport page
        
        Returns:
            Path to downloaded file
        """
        try:
            # Setup download directory
            self.setup_download_directory()
            
            # Navigate to ItemImportExport
            if not await self.navigate_to_item_import_export():
                raise Exception("Failed to navigate to ItemImportExport page")
            
            # Find and click export button, get download
            download = await self.find_and_click_export_button()
            
            # Handle the download
            downloaded_file = await self.handle_download(download)
            
            # Validate Excel file
            if not self.validate_excel_file(downloaded_file):
                raise Exception("Downloaded file validation failed")
            
            # Copy to temp location
            return self.copy_to_temp_location(downloaded_file)
            
        finally:
            self.cleanup_download_directory()