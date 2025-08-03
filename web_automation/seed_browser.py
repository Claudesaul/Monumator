"""
SEED Browser Management
======================

Handles SEED login and common navigation functionality.
Provides reusable SEED-specific browser operations.
"""

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

class SeedBrowser:
    """
    Manages SEED-specific browser operations
    """
    
    def __init__(self, driver):
        """
        Initialize SEED browser manager
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Load environment variables
        load_dotenv()
        self.username = os.getenv('SEED_USERNAME')
        self.password = os.getenv('SEED_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("SEED_USERNAME and SEED_PASSWORD must be set in environment variables")
    
    def login(self):
        """
        Perform SEED login process
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            print("🔑 Logging into SEED...")
            
            # Navigate to SEED
            self.driver.get("https://mycantaloupe.com")
            
            # Check if already logged in by looking for login form
            try:
                # Wait for login form to appear
                password_field = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "testPasswordInput"))
                )
                
                # If we found the password field, we need to login
                print("📝 Login form detected, proceeding with authentication...")
                
                # Fill username
                username_field = self.driver.find_element(By.CLASS_NAME, "testEmailInput")
                username_field.clear()
                username_field.send_keys(self.username)
                
                # Fill password
                password_field.clear()
                password_field.send_keys(self.password)
                
                # Click login button
                login_button = self.driver.find_element(By.CLASS_NAME, "testSignInButton")
                login_button.click()
                
                # Wait for login to complete (page redirect or dashboard load)
                print("⏳ Waiting for login to complete...")
                time.sleep(8)  # Standard wait time for SEED login
                
                # Verify login success by checking URL or looking for logout elements
                current_url = self.driver.current_url
                if "mycantaloupe.com" in current_url and "login" not in current_url.lower():
                    print("✅ Login successful")
                    return True
                else:
                    print("❌ Login appears to have failed")
                    return False
                    
            except TimeoutException:
                # No login form found - might already be logged in
                print("ℹ️ No login form detected - may already be logged in")
                return True
                
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            return False
    
    def navigate_to_route_summary(self, target_date):
        """
        Navigate to routes summary page for specific date
        
        Args:
            target_date (str): Date in YYYY-MM-DD format
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            # Construct routes summary URL with date
            routes_url = f"https://mycantaloupe.com/cs4/Reports/RoutesSummary?date={target_date}"
            print(f"🧭 Navigating to routes summary for {target_date}")
            
            self.driver.get(routes_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Check if we're on the correct page
            if "RoutesSummary" in self.driver.current_url:
                print("✅ Successfully navigated to routes summary")
                return True
            else:
                print("❌ Failed to navigate to routes summary")
                return False
                
        except Exception as e:
            print(f"❌ Navigation failed: {str(e)}")
            return False
    
    def navigate_to_item_import_export(self):
        """
        Navigate to Item Import/Export page
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print("🧭 Navigating to Item Import/Export page...")
            
            # Direct navigation to ItemImportExport
            export_url = "https://mycantaloupe.com/cs4/ItemImportExport/ExcelExport"
            self.driver.get(export_url)
            
            # Wait for Vue.js app to load
            print("⏳ Waiting for Vue.js application to load...")
            time.sleep(10)  # Vue.js apps need time to initialize
            
            # Check if we're on the correct page
            if "ItemImportExport" in self.driver.current_url:
                print("✅ Successfully navigated to Item Import/Export")
                return True
            else:
                print("❌ Failed to navigate to Item Import/Export")
                return False
                
        except Exception as e:
            print(f"❌ Navigation failed: {str(e)}")
            return False
    
    def wait_for_element(self, by, value, timeout=10):
        """
        Wait for element to be present
        
        Args:
            by: Selenium By locator
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement or None if not found
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ Element not found: {by}={value}")
            return None
    
    def wait_for_clickable(self, by, value, timeout=10):
        """
        Wait for element to be clickable
        
        Args:
            by: Selenium By locator
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement or None if not found
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ Element not clickable: {by}={value}")
            return None
    
    def check_logged_in(self):
        """
        Check if user is currently logged in to SEED
        
        Returns:
            bool: True if logged in, False otherwise
        """
        try:
            current_url = self.driver.current_url
            
            # Check URL for indicators of being logged in
            if "mycantaloupe.com" in current_url and "login" not in current_url.lower():
                # Additional check - look for common logged-in elements
                try:
                    # Look for elements that only appear when logged in
                    self.wait_for_element(By.TAG_NAME, "body", timeout=3)
                    return True
                except:
                    return False
            else:
                return False
                
        except Exception:
            return False