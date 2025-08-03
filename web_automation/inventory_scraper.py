"""
Inventory Confirmation Scraper
==============================

Scrapes inventory confirmation data from SEED routes summary.
Extracts route data and generates Excel reports.
"""

import os
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import pandas as pd
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser
from excel_processing.base_excel import ensure_directory_exists

class InventoryConfirmationScraper(BaseScraper):
    """
    Scrapes inventory confirmation data from SEED
    """
    
    def __init__(self, headless=True):
        """Initialize inventory confirmation scraper"""
        super().__init__(headless)
        self.seed_browser = None
        self.target_routes = ["Rt 102", "Rt 106", "Rt 206", "Rt 305"]
        
    def get_previous_business_day(self):
        """
        Calculate the target date for inventory confirmation
        Monday = Friday (3 days ago), other days = previous day
        
        Returns:
            str: Date in YYYY-MM-DD format
        """
        today = datetime.now()
        
        if today.weekday() == 0:  # Monday
            target_date = today - timedelta(days=3)  # Friday
            print("📅 Monday detected - using Friday's data (3 days ago)")
        else:
            target_date = today - timedelta(days=1)  # Previous day
            print("📅 Using previous business day data")
        
        return target_date.strftime("%Y-%m-%d")
    
    def find_routes_with_missing_inventory(self):
        """
        Find routes that have missing inventory (red indicators)
        
        Returns:
            list: List of route names with missing inventory
        """
        missing_routes = []
        
        try:
            print("🔍 Scanning for routes with missing inventory...")
            
            # Look for all route links
            route_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'RouteDetails')]")
            
            for link in route_links:
                try:
                    route_text = link.text.strip()
                    
                    # Check if this is one of our target routes
                    if any(target in route_text for target in self.target_routes):
                        # Look for red indicator (missing inventory)
                        parent_row = link.find_element(By.XPATH, "./ancestor::tr")
                        
                        # Check for red background or other missing inventory indicators
                        style = parent_row.get_attribute("style") or ""
                        class_name = parent_row.get_attribute("class") or ""
                        
                        if "red" in style.lower() or "missing" in class_name.lower():
                            missing_routes.append(route_text)
                            print(f"🔴 Found missing inventory: {route_text}")
                        else:
                            print(f"✅ Route complete: {route_text}")
                            
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    print(f"⚠️ Error checking route: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error finding routes with missing inventory: {str(e)}")
        
        print(f"📊 Found {len(missing_routes)} routes with missing inventory")
        return missing_routes
    
    def scrape_route_data(self, target_date):
        """
        Scrape data for all target routes
        
        Args:
            target_date (str): Date in YYYY-MM-DD format
            
        Returns:
            list: List of route data dictionaries
        """
        route_data = []
        
        try:
            # Find routes with missing inventory
            missing_routes = self.find_routes_with_missing_inventory()
            
            # Process each target route
            for route in self.target_routes:
                print(f"📋 Processing {route}...")
                
                route_info = {
                    'route': route,
                    'date': target_date,
                    'status': 'Complete' if route not in missing_routes else 'Missing Inventory',
                    'assets_processed': 0,
                    'missing_items': []
                }
                
                # Try to navigate to route details
                try:
                    route_link = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{route}')]")
                    route_link.click()
                    time.sleep(3)
                    
                    # Extract asset data if on route details page
                    if "RouteDetails" in self.driver.current_url:
                        assets = self.extract_asset_data()
                        route_info['assets_processed'] = len(assets)
                        route_info['missing_items'] = self.find_missing_items(assets)
                        
                        print(f"📊 {route}: {len(assets)} assets, {len(route_info['missing_items'])} missing items")
                    
                    # Navigate back to summary
                    self.driver.back()
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"⚠️ Could not process {route}: {str(e)}")
                    route_info['status'] = 'Error'
                
                route_data.append(route_info)
                
        except Exception as e:
            print(f"❌ Error scraping route data: {str(e)}")
        
        return route_data
    
    def extract_asset_data(self):
        """
        Extract asset data from current route details page
        
        Returns:
            list: List of asset data dictionaries
        """
        assets = []
        
        try:
            # Look for asset table
            asset_rows = self.driver.find_elements(By.XPATH, "//table//tr[position()>1]")
            
            for row in asset_rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:
                        asset_data = {
                            'asset_id': cells[0].text.strip(),
                            'location': cells[1].text.strip(),
                            'status': cells[2].text.strip()
                        }
                        
                        # Filter out certain asset types
                        asset_id = asset_data['asset_id'].upper()
                        if not any(exclude in asset_id for exclude in ['FF', 'STATIC', 'COFFEE', 'CONDIMENTS']):
                            assets.append(asset_data)
                            
                except Exception as e:
                    print(f"⚠️ Error extracting asset data: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error extracting asset data: {str(e)}")
        
        return assets
    
    def find_missing_items(self, assets):
        """
        Identify missing items from asset data
        
        Args:
            assets (list): List of asset data
            
        Returns:
            list: List of missing items
        """
        missing_items = []
        
        for asset in assets:
            if 'missing' in asset.get('status', '').lower():
                missing_items.append({
                    'asset_id': asset['asset_id'],
                    'location': asset['location']
                })
        
        return missing_items
    
    def generate_excel_report(self, route_data, output_directory="downloads/daily"):
        """
        Generate Excel report from route data
        
        Args:
            route_data (list): List of route data dictionaries
            output_directory (str): Directory to save report
            
        Returns:
            str: Path to generated Excel file
        """
        try:
            # Ensure output directory exists
            ensure_directory_exists(output_directory)
            
            # Create DataFrame
            df = pd.DataFrame(route_data)
            
            # Generate filename
            today = datetime.now()
            date_str = today.strftime("%m.%d.%y")
            filename = f"Daily Inventory Confirmation {date_str}.xlsx"
            output_path = os.path.join(output_directory, filename)
            
            # Save to Excel
            df.to_excel(output_path, index=False, sheet_name="Inventory Confirmation")
            
            print(f"📊 Generated Excel report: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Failed to generate Excel report: {str(e)}")
            raise
    
    def run_inventory_confirmation_scraper(self):
        """
        Complete workflow for inventory confirmation scraping
        
        Returns:
            dict: Results dictionary with success status and details
        """
        start_time = time.time()
        
        try:
            print("🚀 Starting inventory confirmation scraper...")
            
            # Setup browser and SEED connection
            self.setup_browser()
            self.seed_browser = SeedBrowser(self.driver)
            
            # Login to SEED
            if not self.seed_browser.login():
                raise Exception("Failed to login to SEED")
            
            # Calculate target date
            target_date = self.get_previous_business_day()
            
            # Navigate to routes summary
            if not self.seed_browser.navigate_to_route_summary(target_date):
                raise Exception("Failed to navigate to routes summary")
            
            # Scrape route data
            route_data = self.scrape_route_data(target_date)
            
            if not route_data:
                raise Exception("No route data found")
            
            # Generate Excel report
            excel_file = self.generate_excel_report(route_data)
            
            # Calculate results
            elapsed_time = time.time() - start_time
            routes_found = len(route_data)
            assets_processed = sum(route.get('assets_processed', 0) for route in route_data)
            
            results = {
                'success': True,
                'excel_file': excel_file,
                'elapsed_time': elapsed_time,
                'routes_found': routes_found,
                'assets_processed': assets_processed,
                'route_data': route_data
            }
            
            print(f"✅ Inventory confirmation scraping completed in {elapsed_time:.1f} seconds")
            return results
            
        except Exception as e:
            print(f"❌ Inventory confirmation scraping failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }
        finally:
            self.cleanup_browser()

# Convenience function for backward compatibility
def run_inventory_confirmation_scraper(headless=True):
    """
    Run inventory confirmation scraper (backward compatibility function)
    
    Args:
        headless (bool): Run in headless mode
        
    Returns:
        dict: Results dictionary
    """
    scraper = InventoryConfirmationScraper(headless=headless)
    return scraper.run_inventory_confirmation_scraper()