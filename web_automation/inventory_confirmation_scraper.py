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
        
        print("🔍 Scanning for routes with missing inventory...")
        
        # Get all table rows and find routes with missing inventory
        rows = await self.page.locator("table tr").all()
        routes_with_missing = []
        
        # Check route data rows (starting from row 6 where route data begins)
        for i in range(6, len(rows)):
            row = rows[i]
            cells = await row.locator("td").all()
            
            if len(cells) < 5:
                continue
                
            route_name = (await cells[1].text_content() or "").strip()
            missing_text = (await cells[4].text_content() or "").strip()
            
            # Only process routes with missing inventory
            if route_name.startswith('Rt') and missing_text.isdigit():
                routes_with_missing.append((route_name, int(missing_text)))
                print(f"🔴 Found: {route_name} ({missing_text} missing)")
        
        print(f"📊 Found {len(routes_with_missing)} routes with missing inventory")
        
        route_data = []
        
        # Process each route
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
                # Click the missing count number in column 4 (5th td, 0-indexed)
                route_name_clean = ' '.join(route_name.split())
                route_row = self.page.locator(f"tr:has(td:has-text('{route_name_clean}'))")
                missing_link = route_row.locator("td:nth-child(5) a").first
                
                # Click the link
                await missing_link.click()
                await self.page.wait_for_timeout(2000)
                
                # Find rows with YES/NO status
                yes_no_rows = await self.page.locator("tr:has(td:text-is('YES/NO'))").all()
                
                for row in yes_no_rows:
                    cells = await row.locator("td").all()
                    if len(cells) < 5:
                        continue
                    
                    asset_id = (await cells[0].text_content() or "").strip()
                    location = (await cells[1].text_content() or "").strip()
                    asset_type = (await cells[2].text_content() or "").strip()
                    restock_time = (await cells[3].text_content() or "").strip() if len(cells) > 3 else ""
                    inventory_status = (await cells[4].text_content() or "").strip() if len(cells) > 4 else "YES/NO"
                    
                    # Skip if contains excluded keywords
                    excluded = ['COFFEE', 'FF', 'STATIC', 'CONDIMENT']
                    combined_text = f"{asset_id} {asset_type}".upper()
                    if any(x in combined_text for x in excluded):
                        continue
                    
                    # Track this incomplete asset with all required fields
                    route_info['incomplete_assets'].append({
                        'asset_id': asset_id,
                        'location': location,
                        'type': asset_type,
                        'restock_time': restock_time,
                        'inventory_taken': inventory_status
                    })
                
                # Navigate back
                await self.page.go_back()
                print(f"✅ {route_name}: {len(route_info['incomplete_assets'])} incomplete assets found")
                
            except Exception as e:
                print(f"❌ Error processing {route_name}: {str(e)}")
                route_info['status'] = 'Error'
            
            route_data.append(route_info)
        
        return route_data