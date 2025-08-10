"""
Base Web Scraper - Playwright Edition
======================================

Async browser automation with Firefox and Playwright.
Handles browser setup, cleanup, and common utilities.
"""
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright.async_api import TimeoutError as PlaywrightTimeout

class BaseScraper:
    """
    Base class for async web scraping with Playwright and Firefox
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize base scraper
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    async def setup_browser(self) -> Page:
        """
        Setup Firefox browser with optimized configuration
        
        Returns:
            Page: Configured browser page
        """
        print("🦊 Setting up Firefox browser...")
        
        try:
            # Start Playwright
            self.playwright = await async_playwright().start()
            
            # Launch Firefox with persistent profile for extensions
            self.context = await self.playwright.firefox.launch_persistent_context(
                user_data_dir="./web_automation/firefox_profile",
                headless=self.headless,
                viewport={'width': 1024, 'height': 600},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
                accept_downloads=True,
                ignore_https_errors=True
            )
            
            # Set default timeout
            self.context.set_default_timeout(10000)
            
            # Use existing page from persistent context
            self.page = self.context.pages[0]
            
            print("✅ Firefox browser setup complete")
            return self.page
            
        except Exception as e:
            print(f"❌ Failed to setup browser: {str(e)}")
            await self.cleanup_browser()
            raise
    
    async def cleanup_browser(self):
        """
        Clean up browser resources
        """
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"⚠️ Browser cleanup warning: {str(e)}")
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None
    
    async def wait_for_page_load(self, timeout: int = 8000):
        """
        Wait for page to fully load (minimal waiting - Playwright handles most automatically)
        
        Args:
            timeout: Maximum time to wait in milliseconds
        """
        # Playwright automatically waits for most content, so minimal waiting needed
        return True
    
    async def safe_click(self, selector: str, max_retries: int = 3) -> bool:
        """
        Safely click an element with retry logic
        
        Args:
            selector: CSS selector or text selector
            max_retries: Maximum retry attempts
            
        Returns:
            bool: True if click succeeded
        """
        for attempt in range(max_retries):
            try:
                if self.page:
                    await self.page.click(selector, timeout=5000)
                    return True
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Click attempt {attempt + 1} failed, retrying...")
                else:
                    print(f"❌ Click failed after {max_retries} attempts: {str(e)}")
                    return False
        return False
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.setup_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup_browser()