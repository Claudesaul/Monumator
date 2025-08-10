"""
Inventory Confirmation Scraper - Simplified
===========================================

Checks SEED routes for incomplete inventory, excluding FF/STATIC assets.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from .seed_browser import SeedBrowser

class InventoryConfirmationScraper(SeedBrowser):
    """Scraper for inventory confirmation data"""
    
    def get_previous_business_day(self) -> str:
        """Get target date: Monday=Friday (3 days ago), else previous day"""
        today = datetime.now()
        days_back = 3 if today.weekday() == 0 else 1  # Monday=0
        target_date = today - timedelta(days=days_back)
        return target_date.strftime("%Y-%m-%d")
    
    async def get_incomplete_routes(self, target_date: str) -> List[Dict[str, Any]]:
        """
        Find routes with incomplete inventory dynamically
        
        Args:
            target_date: Date in YYYY-MM-DD format
            
        Returns:
            List of incomplete route data dictionaries
        """
        if not await self.navigate_to_route_summary(target_date):
            raise Exception("Failed to navigate to routes summary")
        
        # Find all routes with missing inventory by checking table data
        print("🔍 Scanning for routes with missing inventory...")
        
        # Playwright automatically waits for content - minimal explicit waiting needed
        
        # Get all table rows
        rows = await self.page.locator("table tr").all()
        routes_with_missing = []
        
        # Check route data rows (starting from row 6 where route data begins)
        for i in range(6, len(rows)):
            try:
                row = rows[i]
                cells = await row.locator("td").all()
                
                if len(cells) >= 5:  # Need at least 5 columns (0-4)
                    # Column 1: Route name
                    route_name = (await cells[1].text_content() or "").strip()
                    
                    # Column 4: Missing inventory count
                    missing_text = (await cells[4].text_content() or "").strip()
                    
                    if route_name.startswith('Rt'):  # Only process actual routes
                        # Check if missing inventory > 0
                        missing_count = 0
                        if missing_text.isdigit():
                            missing_count = int(missing_text)
                        
                        if missing_count > 0:
                            routes_with_missing.append((route_name, missing_count))
                            print(f"🔴 Found route with missing inventory: {route_name} ({missing_count} missing)")
                
            except Exception as e:
                print(f"⚠️ Error checking row {i}: {str(e)}")
                continue
        
        print(f"📊 Found {len(routes_with_missing)} routes with missing inventory")
        
        route_data = []
        
        # Process each route with missing inventory
        for route_name, missing_count in routes_with_missing:
            print(f"📋 Processing {route_name}...")
            
            route_info = {
                'route': route_name,
                'date': target_date,
                'status': 'Incomplete',
                'missing_count': missing_count,
                'incomplete_assets': []
            }
            
            try:
                # Try to find and click the route link
                # The route names might be clickable in the first column
                route_link = self.page.locator(f"a:has-text('{route_name}')").first
                
                if await route_link.count() == 0:
                    # If no direct link, try looking in table cells
                    route_cell = self.page.locator(f"td:has-text('{route_name}') a").first
                    if await route_cell.count() > 0:
                        route_link = route_cell
                
                if await route_link.count() > 0:
                    print(f"🔗 Found clickable link for {route_name}")
                    await route_link.click()
                    
                    # Route details page loaded automatically by Playwright
                    
                    # Extract incomplete assets (excluding FF/STATIC)
                    asset_rows = await self.page.locator("table tr").all()
                    
                    for row in asset_rows[1:]:  # Skip header
                        cells = await row.locator("td").all()
                        if len(cells) >= 3:
                            asset_id = (await cells[0].text_content() or "").strip().upper()
                            location = (await cells[1].text_content() or "").strip()
                            status = (await cells[2].text_content() or "").strip().lower()
                            
                            # Skip FF/STATIC assets and check for missing status
                            if not any(x in asset_id for x in ['FF', 'STATIC', 'COFFEE', 'CONDIMENTS']):
                                if 'missing' in status or 'incomplete' in status or 'not done' in status:
                                    route_info['incomplete_assets'].append({
                                        'asset_id': asset_id,
                                        'location': location,
                                        'status': status
                                    })
                    
                    # Navigate back to summary
                    await self.page.go_back()
                    print(f"🔴 {route_name}: {len(route_info['incomplete_assets'])} incomplete assets found")
                    
                else:
                    print(f"⚠️ No clickable link found for {route_name} - route data incomplete")
                    route_info['status'] = 'No Link Found'
                
            except Exception as e:
                print(f"❌ Error processing {route_name}: {str(e)}")
                route_info['status'] = 'Error'
            
            route_data.append(route_info)
        
        return route_data