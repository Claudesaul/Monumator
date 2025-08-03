"""
Daily Reports System - Simplified Menu with Sub-navigation
=========================================================

Streamlined daily reports system with clean navigation.
"""

import sys
import os
import msvcrt

# Import MenuNavigator utility
from utils.menu_navigator import MenuNavigator

from report_workflows.daily_stockout import process_stockout_report
from report_workflows.inventory_adjustment import process_inventory_adjustment_summary
from report_workflows.inventory_confirmation import process_inventory_confirmation_report

class DailyReportsSystem:
    """Daily reports menu system with sub-navigation"""
    
    def __init__(self):
        self.main_options = [
            "📈 Daily Stockout Report",
            "📋 Inventory Adjustment Summary", 
            "🌐 Inventory Confirmation Report",
            "🔗 Test Database Connection",
            "🔙 Back to Main Menu"
        ]
    
    def stockout_submenu(self):
        """Daily Stockout Report sub-menu"""
        options = [
            "🔄 Process Report",
            "📊 Use Sample Data (Testing)",
            "🔙 Back"
        ]
        
        navigator = MenuNavigator(options, "Daily Stockout Report")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 2:  # Quit or Back
                return
            
            elif choice == 0:  # Process Report
                os.system('cls' if os.name == 'nt' else 'clear')
                print("🚀 Processing Daily Stockout Report...")
                try:
                    results = process_stockout_report(use_sample_data=False)
                    if results['success']:
                        print(f"✅ Report completed successfully!")
                        print(f"📁 Output: {results['output_path']}")
                        print(f"⏱️ Time: {results['processing_time']:.2f}s")
                    else:
                        print(f"❌ Report failed: {results['error']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
            
            elif choice == 1:  # Use Sample Data
                os.system('cls' if os.name == 'nt' else 'clear')
                print("🧪 Processing with Sample Data...")
                try:
                    results = process_stockout_report(use_sample_data=True)
                    if results['success']:
                        print(f"✅ Test report completed!")
                        print(f"📁 Output: {results['output_path']}")
                    else:
                        print(f"❌ Test failed: {results['error']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
    
    def inventory_adjustment_submenu(self):
        """Inventory Adjustment sub-menu"""
        options = [
            "🔄 Process Report (Auto Download)",
            "📅 Check Date Logic",
            "🔙 Back"
        ]
        
        navigator = MenuNavigator(options, "Inventory Adjustment Summary")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 2:  # Quit or Back
                return
            
            elif choice == 0:  # Process Report
                os.system('cls' if os.name == 'nt' else 'clear')
                print("🚀 Processing Inventory Adjustment Summary...")
                print("📋 Auto-downloading IAD data and product list...")
                try:
                    results = process_inventory_adjustment_summary()
                    if results['success']:
                        print(f"✅ Report completed successfully!")
                        print(f"📁 Output: {results['output_path']}")
                        print(f"📊 Report ID: {results['report_id']} - {results['description']}")
                        print(f"⏱️ Time: {results['processing_time']:.2f}s")
                    else:
                        print(f"❌ Report failed: {results['error']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
            
            elif choice == 1:  # Check Date Logic
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
            "🔙 Back"
        ]
        
        navigator = MenuNavigator(options, "Inventory Confirmation Report")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 2:  # Quit or Back
                return
            
            elif choice in [0, 1]:  # Run scraper
                headless = choice == 0
                mode = "Headless" if headless else "Visible"
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"🚀 Processing Inventory Confirmation Report ({mode})...")
                try:
                    results = process_inventory_confirmation_report(headless=headless)
                    if results['success']:
                        print(f"✅ Report completed successfully!")
                        if 'excel_file' in results:
                            print(f"📁 Output: {results['excel_file']}")
                        print(f"🎯 Routes: {results['routes_found']}")
                        print(f"📊 Assets: {results['assets_processed']}")
                        if 'elapsed_time' in results:
                            print(f"⏱️ Time: {results['elapsed_time']:.1f}s")
                    else:
                        print(f"❌ Report failed: {results['error']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                input("\nPress Enter to continue...")
    
    def test_database(self):
        """Test database connection"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("🔍 TESTING DATABASE CONNECTION")
        print("=" * 40)
        
        try:
            from database.connection import test_database_connection
            print("Connecting to database...")
            
            if test_database_connection():
                print("✅ Connection established")
                print("✅ Test query successful") 
            else:
                print("❌ Connection failed")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Main daily reports menu"""
        navigator = MenuNavigator(self.main_options, "Daily Reports System")
        
        while True:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 4:  # Quit or Back
                return
            
            elif choice == 0:  # Daily Stockout Report
                self.stockout_submenu()
            
            elif choice == 1:  # Inventory Adjustment Summary
                self.inventory_adjustment_submenu()
            
            elif choice == 2:  # Inventory Confirmation Report
                self.inventory_confirmation_submenu()
            
            elif choice == 3:  # Test Database Connection
                self.test_database()

def main():
    """Entry point for daily reports system"""
    system = DailyReportsSystem()
    system.main_menu()

if __name__ == "__main__":
    main()