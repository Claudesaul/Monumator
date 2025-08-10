"""
Inventory Confirmation Scraper - Playwright Edition
===================================================

Async inventory confirmation scraping with Playwright and Firefox.
Extracts route data and generates Excel reports.
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
from playwright.async_api import Page, ElementHandle
from playwright.async_api import TimeoutError as PlaywrightTimeout
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser
from excel_processing.base_excel import ensure_directory_exists

class InventoryConfirmationScraper(BaseScraper):
    """
    Async scraper for inventory confirmation data from SEED
    """
    
    def __init__(self, headless: bool = True):
        """Initialize inventory confirmation scraper"""
        super().__init__(headless)
        self.seed_browser: Optional[SeedBrowser] = None
        self.target_routes = ["Rt 102", "Rt 106", "Rt 206", "Rt 305"]
        
    def get_previous_business_day(self) -> str:
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
    
    async def find_routes_with_missing_inventory(self) -> List[str]:
        """
        Find routes that have missing inventory (red indicators)
        
        Returns:
            List of route names with missing inventory
        """
        missing_routes = []
        
        try:
            print("🔍 Scanning for routes with missing inventory...")
            
            # Look for all route links
            route_links = await self.page.locator("a[href*='RouteDetails']").all()
            
            for link in route_links:
                try:
                    route_text = (await link.text_content() or "").strip()
                    
                    # Check if this is one of our target routes
                    if any(target in route_text for target in self.target_routes):
                        # Look for red indicator (missing inventory) in parent row
                        parent_row = link.locator("xpath=ancestor::tr").first
                        
                        # Check for red background or missing inventory indicators
                        style = await parent_row.get_attribute("style") or ""
                        class_name = await parent_row.get_attribute("class") or ""
                        
                        if "red" in style.lower() or "missing" in class_name.lower():
                            missing_routes.append(route_text)
                            print(f"🔴 Found missing inventory: {route_text}")
                        else:
                            print(f"✅ Route complete: {route_text}")
                            
                except Exception as e:
                    print(f"⚠️ Error checking route: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error finding routes with missing inventory: {str(e)}")
        
        print(f"📊 Found {len(missing_routes)} routes with missing inventory")
        return missing_routes
    
    async def scrape_route_data(self, target_date: str) -> List[Dict[str, Any]]:
        """
        Scrape data for all target routes
        
        Args:
            target_date: Date in YYYY-MM-DD format
            
        Returns:
            List of route data dictionaries
        """
        route_data = []
        
        try:
            # Find routes with missing inventory
            missing_routes = await self.find_routes_with_missing_inventory()
            
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
                    # Find and click route link
                    route_link = self.page.locator(f"a:has-text('{route}')").first
                    await route_link.click()
                    await self.page.wait_for_load_state('networkidle')
                    
                    # Extract asset data if on route details page
                    if "RouteDetails" in self.page.url:
                        assets = await self.extract_asset_data()
                        route_info['assets_processed'] = len(assets)
                        route_info['missing_items'] = self.find_missing_items(assets)
                        
                        print(f"📊 {route}: {len(assets)} assets, {len(route_info['missing_items'])} missing items")
                    
                    # Navigate back to summary
                    await self.page.go_back()
                    await self.page.wait_for_load_state('networkidle')
                    
                except Exception as e:
                    print(f"⚠️ Could not process {route}: {str(e)}")
                    route_info['status'] = 'Error'
                
                route_data.append(route_info)
                
        except Exception as e:
            print(f"❌ Error scraping route data: {str(e)}")
        
        return route_data
    
    async def extract_asset_data(self) -> List[Dict[str, str]]:
        """
        Extract asset data from current route details page
        
        Returns:
            List of asset data dictionaries
        """
        assets = []
        
        try:
            # Wait for table to load
            await self.page.wait_for_selector("table", timeout=5000)
            
            # Look for asset table rows (skip header)
            rows = await self.page.locator("table tr").all()
            
            for i, row in enumerate(rows):
                if i == 0:  # Skip header row
                    continue
                    
                try:
                    cells = await row.locator("td").all()
                    if len(cells) >= 3:
                        asset_data = {
                            'asset_id': (await cells[0].text_content() or "").strip(),
                            'location': (await cells[1].text_content() or "").strip(),
                            'status': (await cells[2].text_content() or "").strip()
                        }
                        
                        # Filter out certain asset types
                        asset_id = asset_data['asset_id'].upper()
                        if not any(exclude in asset_id for exclude in ['FF', 'STATIC', 'COFFEE', 'CONDIMENTS']):
                            assets.append(asset_data)
                            
                except Exception as e:
                    print(f"⚠️ Error extracting asset row: {str(e)}")
                    continue
                    
        except PlaywrightTimeout:
            print("⚠️ No asset table found on page")
        except Exception as e:
            print(f"❌ Error extracting asset data: {str(e)}")
        
        return assets
    
    def find_missing_items(self, assets: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Identify missing items from asset data
        
        Args:
            assets: List of asset data
            
        Returns:
            List of missing items
        """
        missing_items = []
        
        for asset in assets:
            if 'missing' in asset.get('status', '').lower():
                missing_items.append({
                    'asset_id': asset['asset_id'],
                    'location': asset['location']
                })
        
        return missing_items
    
    def generate_excel_report(self, route_data: List[Dict], output_directory: str = "downloads/daily") -> str:
        """
        Generate Excel report from route data
        
        Args:
            route_data: List of route data dictionaries
            output_directory: Directory to save report
            
        Returns:
            Path to generated Excel file
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
    
    async def run_inventory_confirmation_scraper(self) -> Dict[str, Any]:
        """
        Complete async workflow for inventory confirmation scraping
        
        Returns:
            Results dictionary with success status and details
        """
        import time
        start_time = time.time()
        
        try:
            print("🚀 Starting inventory confirmation scraper...")
            
            # Setup browser and SEED connection
            await self.setup_browser()
            self.seed_browser = SeedBrowser(self.page)
            
            # Login to SEED
            if not await self.seed_browser.login():
                raise Exception("Failed to login to SEED")
            
            # Calculate target date
            target_date = self.get_previous_business_day()
            
            # Navigate to routes summary
            if not await self.seed_browser.navigate_to_route_summary(target_date):
                raise Exception("Failed to navigate to routes summary")
            
            # Scrape route data
            route_data = await self.scrape_route_data(target_date)
            
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
            await self.cleanup_browser()

# Async wrapper function for backward compatibility
async def run_inventory_confirmation_scraper_async(headless: bool = True) -> Dict[str, Any]:
    """
    Run inventory confirmation scraper asynchronously
    
    Args:
        headless: Run in headless mode
        
    Returns:
        Results dictionary
    """
    scraper = InventoryConfirmationScraper(headless=headless)
    return await scraper.run_inventory_confirmation_scraper()

# Synchronous wrapper for menu system integration
def run_inventory_confirmation_scraper(headless: bool = True) -> Dict[str, Any]:
    """
    Run inventory confirmation scraper (synchronous wrapper)
    
    Args:
        headless: Run in headless mode
        
    Returns:
        Results dictionary
    """
    return asyncio.run(run_inventory_confirmation_scraper_async(headless))