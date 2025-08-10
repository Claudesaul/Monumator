"""
SEED Browser Management - Playwright Edition
============================================

Async SEED login and navigation with Playwright and Firefox.
Provides reusable SEED-specific browser operations.
"""

import os
from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeout
from dotenv import load_dotenv

class SeedBrowser:
    """
    Manages SEED-specific browser operations with async Playwright
    """
    
    def __init__(self, page: Page):
        """
        Initialize SEED browser manager
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
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
            # Construct routes summary URL with date
            routes_url = f"{self.base_url}/cs4/Reports/RoutesSummary?date={target_date}"
            print(f"🧭 Navigating to routes summary for {target_date}")
            
            await self.page.goto(routes_url)
            await self.page.wait_for_load_state('networkidle')
            
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
            export_url = f"{self.base_url}/cs4/ItemImportExport/ExcelExport"
            await self.page.goto(export_url)
            
            # Wait for Vue.js app to load
            print("⏳ Waiting for Vue.js application to load...")
            await self.page.wait_for_load_state('networkidle', timeout=15000)
            
            # Additional wait for Vue components
            try:
                await self.page.wait_for_selector("[data-v-]", timeout=5000)
            except:
                pass  # Vue attribute check is optional
            
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
    
    async def wait_for_element(self, selector: str, timeout: int = 10000):
        """
        Wait for element to be present
        
        Args:
            selector: CSS selector, text selector, or XPath
            timeout: Maximum wait time in milliseconds
            
        Returns:
            Element handle or None if not found
        """
        try:
            element = await self.page.wait_for_selector(selector, timeout=timeout)
            return element
        except PlaywrightTimeout:
            print(f"⚠️ Element not found: {selector}")
            return None
    
    async def wait_for_clickable(self, selector: str, timeout: int = 10000):
        """
        Wait for element to be clickable (visible and enabled)
        
        Args:
            selector: CSS selector, text selector, or XPath
            timeout: Maximum wait time in milliseconds
            
        Returns:
            Element handle or None if not found
        """
        try:
            element = await self.page.wait_for_selector(
                selector, 
                state='visible',
                timeout=timeout
            )
            if element and await element.is_enabled():
                return element
            return None
        except PlaywrightTimeout:
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
                # Additional check - look for logout button or user menu
                try:
                    await self.page.wait_for_selector("body", timeout=1000)
                    # Check for common logged-in indicators
                    if "dashboard" in current_url or "Reports" in current_url or "cs4" in current_url:
                        return True
                except:
                    pass
            return False
                
        except Exception:
            return False