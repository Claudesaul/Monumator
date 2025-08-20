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
        super().__init__(headless)
        self.base_url = "https://mycantaloupe.com"
        self.cluster = None
        
        load_dotenv()
        self.username = os.getenv('SEED_USERNAME')
        self.password = os.getenv('SEED_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("SEED_USERNAME and SEED_PASSWORD must be set in environment variables")
    
    async def login(self) -> bool:
        try:
            await self.page.goto(self.base_url)
            
            await self.page.fill(".testEmailInput", self.username)
            await self.page.fill(".testPasswordInput", self.password)
            await self.page.click(".testSignInButton")
            
            await self.page.wait_for_url("**/cs*/Home**")
            
            import re
            current_url = self.page.url
            cluster_match = re.search(r'/cs(\d+)/', current_url)
            if cluster_match:
                self.cluster = f"cs{cluster_match.group(1)}"
                print(f"✅ Logged in successfully (cluster: {self.cluster})")
            
            return True
                
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    async def navigate_to_route_summary(self, target_date: str) -> bool:
        try:
            from datetime import datetime
            date_obj = datetime.strptime(target_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m%%2F%d%%2F%Y%%2000%%3A00%%3A00")
            
            cluster = self.cluster or "cs1"
            routes_url = f"{self.base_url}/{cluster}/Scheduling/RoutesSummary?ScheduleDateOnly={formatted_date}"
            print(f"🧭 Navigating to routes summary for {target_date}")
            
            await self.page.goto(routes_url)
            
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
        try:
            print("🧭 Navigating to Item Import/Export page...")
            
            cluster = self.cluster or "cs1"
            export_url = f"{self.base_url}/{cluster}/ItemImportExport/"
            await self.page.goto(export_url)
            
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
        try:
            current_url = self.page.url
            
            if "mycantaloupe.com" in current_url and "login" not in current_url.lower():
                if "dashboard" in current_url or "Reports" in current_url or "/cs" in current_url:
                    return True
            return False
                
        except Exception:
            return False
    
    async def setup_and_login(self) -> bool:
        try:
            await self.setup_browser()
            return await self.login()
        except Exception as e:
            print(f"❌ Setup and login failed: {str(e)}")
            return False
    
    def get_cluster_url(self, path: str) -> str:
        cluster = self.cluster or "cs1"
        return f"{self.base_url}/{cluster}/{path.lstrip('/')}"