"""
SEED Browser Management - Playwright Edition
============================================

Async SEED login and navigation with Playwright and Firefox.
Provides reusable SEED-specific browser operations.
"""

import os
from playwright.async_api import TimeoutError as PlaywrightTimeout
from dotenv import load_dotenv
from .base_scraper import BaseScraper

class SeedBrowser(BaseScraper):
    """
    Manages SEED-specific browser operations with async Playwright
    Inherits browser setup/cleanup from BaseScraper
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize SEED browser manager with browser capabilities
        
        Args:
            headless: Run browser in headless mode
        """
        super().__init__(headless)
        self.base_url = "https://mycantaloupe.com"
        
        # Load environment variables
        load_dotenv()
        self.username = os.getenv('SEED_USERNAME')
        self.password = os.getenv('SEED_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("SEED_USERNAME and SEED_PASSWORD must be set in environment variables")
    
    async def login(self) -> bool:
        """
        Perform SEED login process
        
        Returns:
            bool: True if login successful
        """
        try:
            # Navigate to SEED
            await self.page.goto(self.base_url)
            
            # Fill credentials and login
            await self.page.fill(".testEmailInput", self.username)
            await self.page.fill(".testPasswordInput", self.password)
            await self.page.click(".testSignInButton")
            
            # Wait for successful navigation after login
            await self.page.wait_for_url("**/cs1/Home**")
            
            return True
                
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    async def navigate_to_route_summary(self, target_date: str) -> bool:
        """
        Navigate to routes summary page for specific date
        
        Args:
            target_date: Date in YYYY-MM-DD format
            
        Returns:
            bool: True if navigation successful
        """
        try:
            # Convert YYYY-MM-DD to MM%2FDD%2FYYYY%2000%3A00%3A00 format
            from datetime import datetime
            date_obj = datetime.strptime(target_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m%%2F%d%%2F%Y%%2000%%3A00%%3A00")
            
            # Construct routes summary URL with properly formatted date
            routes_url = f"{self.base_url}/cs1/Scheduling/RoutesSummary?ScheduleDateOnly={formatted_date}"
            print(f"🧭 Navigating to routes summary for {target_date}")
            
            await self.page.goto(routes_url)
            
            # Check if we're on the correct page
            if "RoutesSummary" in self.page.url:
                print("✅ Successfully navigated to routes summary")
                return True
            else:
                print("❌ Failed to navigate to routes summary")
                return False
                
        except Exception as e:
            print(f"❌ Navigation failed: {str(e)}")
            return False
    
    async def navigate_to_item_import_export(self) -> bool:
        """
        Navigate to Item Import/Export page
        
        Returns:
            bool: True if navigation successful
        """
        try:
            print("🧭 Navigating to Item Import/Export page...")
            
            # Direct navigation to ItemImportExport
            export_url = f"{self.base_url}/cs1/ItemImportExport/"
            await self.page.goto(export_url)
            
            # Check if we're on the correct page
            if "ItemImportExport" in self.page.url:
                print("✅ Successfully navigated to Item Import/Export")
                return True
            else:
                print("❌ Failed to navigate to Item Import/Export")
                return False
                
        except Exception as e:
            print(f"❌ Navigation failed: {str(e)}")
            return False
    
    async def wait_for_element(self, selector: str, timeout: int = 5000):
        """
        Wait for element to be present (reduced timeout - Playwright auto-waits)
        
        Args:
            selector: CSS selector, text selector, or XPath
            timeout: Maximum wait time in milliseconds
            
        Returns:
            Element handle or None if not found
        """
        try:
            element = await self.page.locator(selector).first
            return element
        except Exception:
            print(f"⚠️ Element not found: {selector}")
            return None
    
    async def wait_for_clickable(self, selector: str, timeout: int = 5000):
        """
        Wait for element to be clickable (simplified - Playwright auto-waits)
        
        Args:
            selector: CSS selector, text selector, or XPath
            timeout: Maximum wait time in milliseconds
            
        Returns:
            Element handle or None if not found
        """
        try:
            element = await self.page.locator(selector).first
            return element
        except Exception:
            print(f"⚠️ Element not clickable: {selector}")
            return None
    
    async def check_logged_in(self) -> bool:
        """
        Check if user is currently logged in to SEED
        
        Returns:
            bool: True if logged in
        """
        try:
            current_url = self.page.url
            
            # Check URL for indicators of being logged in
            if "mycantaloupe.com" in current_url and "login" not in current_url.lower():
                # Check for common logged-in indicators
                if "dashboard" in current_url or "Reports" in current_url or "cs4" in current_url:
                    return True
            return False
                
        except Exception:
            return False
    
    async def setup_and_login(self) -> bool:
        """
        Setup browser and login to SEED in one call
        
        Returns:
            bool: True if successful
        """
        try:
            await self.setup_browser()
            return await self.login()
        except Exception as e:
            print(f"❌ Setup and login failed: {str(e)}")
            return False