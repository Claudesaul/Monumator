"""
Daily Reports System - Simplified Menu with Sub-navigation
=========================================================

Streamlined daily reports system with clean navigation.
"""

import sys
import os
import msvcrt

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import MenuNavigator utility
from utils.menu_navigator import MenuNavigator

from report_workflows.daily.daily_stockout import process_stockout_report
from report_workflows.daily.inventory_adjustment import process_inventory_adjustment_summary
from report_workflows.daily.inventory_confirmation import process_inventory_confirmation_report

class DailyReportsSystem:
    """Daily reports menu system with sub-navigation"""
    
    def __init__(self):
        self.main_options = [
            "📈 Daily Stockout Report",
            "📋 Inventory Adjustment Summary", 
            "🌐 Inventory Confirmation Report",
            "🔙 Back to Main Menu"
        ]
    
    def stockout_submenu(self):
        """Daily Stockout Report sub-menu"""
        options = [
            "🔄 Process Report",
            "🔙 Back"
        ]
        
        navigator = MenuNavigator(options, "Daily Stockout Report")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 1:  # Quit or Back
                return
            
            elif choice == 0:  # Process Report
                os.system('cls' if os.name == 'nt' else 'clear')
                print("🚀 Processing Daily Stockout Report...")
                try:
                    results = process_stockout_report()
                    if not results['success']:
                        print(f"❌ Report failed: {results['error']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
    
    def inventory_adjustment_submenu(self):
        """Inventory Adjustment sub-menu"""
        options = [
            "🌐 Process Report (Headless)",
            "👁️ Process Report (Visible)",
            "📅 Check Date Logic",
            "🔙 Back"
        ]
        
        navigator = MenuNavigator(options, "Inventory Adjustment Summary")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 3:  # Quit or Back
                return
            
            elif choice in [0, 1]:  # Process Report
                headless = choice == 0
                mode = "Headless" if headless else "Visible"
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"🚀 Processing Inventory Adjustment Summary ({mode})...")
                try:
                    results = process_inventory_adjustment_summary(headless=headless)
                    if not results['success']:
                        print(f"❌ Report failed: {results['error']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
            
            elif choice == 2:  # Check Date Logic
                os.system('cls' if os.name == 'nt' else 'clear')
                print("📅 DATE LOGIC CHECK")
                print("=" * 40)
                from datetime import datetime
                
                today = datetime.now()
                weekday = today.weekday()  # 0=Monday, 6=Sunday
                
                print(f"Today: {today.strftime('%A, %B %d, %Y')}")
                
                if weekday == 0:  # Monday
                    print("📋 Report: Friday data (3 days ago)")
                    print("🆔 Report ID: inventory_adjustment_3_days_ago")
                else:
                    print("📋 Report: Previous business day")
                    print("🆔 Report ID: inventory_adjustment_previous_day")
                
                input("\nPress Enter to continue...")
    
    def inventory_confirmation_submenu(self):
        """Inventory Confirmation sub-menu"""
        options = [
            "🌐 Run Web Scraper (Headless)",
            "👁️ Run Web Scraper (Visible)",
            "📅 Check Date Logic",
            "🔙 Back"
        ]
        
        navigator = MenuNavigator(options, "Inventory Confirmation Report")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 3:  # Quit or Back
                return
            
            elif choice in [0, 1]:  # Run scraper
                headless = choice == 0
                mode = "Headless" if headless else "Visible"
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"🚀 Processing Inventory Confirmation Report ({mode})...")
                try:
                    process_inventory_confirmation_report(headless=headless)
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
            
            elif choice == 2:  # Check Date Logic
                os.system('cls' if os.name == 'nt' else 'clear')
                print("📅 DATE LOGIC CHECK")
                print("=" * 40)
                from datetime import datetime, timedelta
                
                today = datetime.now()
                weekday = today.weekday()  # 0=Monday, 6=Sunday
                
                print(f"Today: {today.strftime('%A, %B %d, %Y')}")
                
                if weekday == 0:  # Monday
                    target_date = today - timedelta(days=3)
                    print("📋 Target Date: Friday data (3 days ago)")
                else:
                    target_date = today - timedelta(days=1)
                    print("📋 Target Date: Previous business day")
                
                print(f"🗓️ Target Date: {target_date.strftime('%Y-%m-%d')}")
                
                input("\nPress Enter to continue...")
    
    
    def main_menu(self):
        """Main daily reports menu"""
        navigator = MenuNavigator(self.main_options, "Daily Reports System")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 3:  # Quit or Back
                return
            
            elif choice == 0:  # Daily Stockout Report
                self.stockout_submenu()
            
            elif choice == 1:  # Inventory Adjustment Summary
                self.inventory_adjustment_submenu()
            
            elif choice == 2:  # Inventory Confirmation Report
                self.inventory_confirmation_submenu()

def main():
    """Entry point for daily reports system"""
    system = DailyReportsSystem()
    system.main_menu()

if __name__ == "__main__":
    main()