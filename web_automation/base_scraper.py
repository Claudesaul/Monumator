"""
Base Web Scraper
================

Common browser setup and utilities for all web scraping operations.
Handles Edge browser configuration and cleanup.
"""

import os
import sys
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import WebDriverException

class BaseScraper:
    """
    Base class for web scraping with common browser setup
    """
    
    def __init__(self, headless=True):
        """
        Initialize base scraper
        
        Args:
            headless (bool): Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.original_stderr = None
        
    def setup_browser(self):
        """
        Setup Edge browser with optimized configuration
        
        Returns:
            webdriver.Edge: Configured Edge driver
        """
        print("🌐 Setting up Microsoft Edge browser...")
        
        # Suppress stderr for headless mode
        if self.headless:
            self.original_stderr = sys.stderr
            sys.stderr = open(os.devnull, 'w')
        
        try:
            # Configure Edge options
            edge_options = Options()
            
            # Basic browser settings
            if self.headless:
                edge_options.add_argument("--headless")
            
            # Performance and stability options
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--disable-extensions")
            edge_options.add_argument("--disable-background-timer-throttling")
            edge_options.add_argument("--disable-renderer-backgrounding")
            edge_options.add_argument("--disable-backgrounding-occluded-windows")
            
            # Disable logging (extensive Chrome/Chromium suppression)
            edge_options.add_argument("--disable-logging")
            edge_options.add_argument("--disable-background-timer-throttling")
            edge_options.add_argument("--disable-backgrounding-occluded-windows")
            edge_options.add_argument("--disable-renderer-backgrounding")
            edge_options.add_argument("--disable-features=TranslateUI")
            edge_options.add_argument("--disable-ipc-flooding-protection")
            edge_options.add_argument("--disable-background-timer-throttling")
            edge_options.add_argument("--disable-backgrounding-occluded-windows")
            edge_options.add_argument("--disable-client-side-phishing-detection")
            edge_options.add_argument("--disable-component-update")
            edge_options.add_argument("--disable-default-apps")
            edge_options.add_argument("--disable-domain-reliability")
            edge_options.add_argument("--disable-features=VizDisplayCompositor")
            edge_options.add_argument("--disable-hang-monitor")
            edge_options.add_argument("--disable-prompt-on-repost")
            edge_options.add_argument("--disable-sync")
            edge_options.add_argument("--disable-web-security")
            edge_options.add_argument("--metrics-recording-only")
            edge_options.add_argument("--no-first-run")
            edge_options.add_argument("--safebrowsing-disable-auto-update")
            edge_options.add_argument("--enable-automation")
            edge_options.add_argument("--password-store=basic")
            edge_options.add_argument("--use-mock-keychain")
            
            # Download preferences (for product list downloads)
            temp_download_dir = tempfile.mkdtemp()
            prefs = {
                "download.default_directory": temp_download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True,
                "profile.default_content_settings.popups": 0,
                "profile.default_content_setting_values.automatic_downloads": 1
            }
            edge_options.add_experimental_option("prefs", prefs)
            
            # User agent
            edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")
            
            # Create Edge service
            service = Service()
            
            # Create driver
            self.driver = webdriver.Edge(service=service, options=edge_options)
            
            # Configure timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            print("✅ Edge browser setup complete")
            return self.driver
            
        except Exception as e:
            print(f"❌ Failed to setup browser: {str(e)}")
            self._cleanup_stderr()
            raise
    
    def cleanup_browser(self):
        """
        Clean up browser resources
        """
        if self.driver:
            try:
                self.driver.quit()
                print("🧹 Browser cleanup complete")
            except Exception as e:
                print(f"⚠️ Browser cleanup warning: {str(e)}")
            finally:
                self.driver = None
                
        self._cleanup_stderr()
    
    def _cleanup_stderr(self):
        """
        Restore stderr if it was redirected
        """
        if self.original_stderr:
            sys.stderr.close()
            sys.stderr = self.original_stderr
            self.original_stderr = None
    
    def wait_for_page_load(self, timeout=10):
        """
        Wait for page to fully load
        
        Args:
            timeout (int): Maximum time to wait in seconds
        """
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.driver.execute_script("return document.readyState") == "complete":
                    return True
                time.sleep(0.5)
            print(f"⚠️ Page load timeout after {timeout} seconds")
            return False
        except Exception as e:
            print(f"⚠️ Error waiting for page load: {str(e)}")
            return False
    
    def safe_click(self, element, max_retries=3):
        """
        Safely click an element with retry logic
        
        Args:
            element: WebElement to click
            max_retries (int): Maximum retry attempts
            
        Returns:
            bool: True if click succeeded, False otherwise
        """
        for attempt in range(max_retries):
            try:
                element.click()
                return True
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Click attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                else:
                    print(f"❌ Click failed after {max_retries} attempts: {str(e)}")
                    return False
        return False
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_browser()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup_browser()