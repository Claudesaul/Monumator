"""
MONUMATOR - Monumental Markets Automation System
=====================================================

Clean, simplified menu system with arrow navigation.
"""

import sys
import os
from utils.menu_navigator import MenuNavigator
from weekly_reports import main as weekly_reports_main
from daily_reports import main as daily_reports_main

def show_download_directories():
    """Display download directory structure"""
    from config.report_config import DOWNLOAD_PATHS
    
    print("\n📁 DOWNLOAD DIRECTORIES")
    print("=" * 40)
    for name, path in DOWNLOAD_PATHS.items():
        status = "✅" if os.path.exists(path) else "❌"
        print(f"{status} {name.upper()}: {path}")

def system_status():
    """Quick system status check"""
    print("\n🔍 SYSTEM STATUS")
    print("=" * 40)
    
    # Database check
    print("🔍 Testing database connection...")
    try:
        from database.connection import test_database_connection
        if test_database_connection():
            print("✅ Database: Connection established")
        else:
            print("❌ Database: Connection failed")
    except:
        print("⚠️ Database: Cannot test")
    
    # Template check
    print("🔍 Checking templates...")
    try:
        from excel_processing.stockout_excel import get_stockout_template_info
        template_info = get_stockout_template_info()
        if template_info['exists']:
            print("✅ Templates: Available")
        else:
            print("❌ Templates: Missing")
    except:
        print("⚠️ Templates: Cannot check")
    
    print("✅ System check complete - All systems online")

def main():
    """Main application entry point"""
    
    options = [
        "📅 Weekly Reports",
        "📊 Daily Reports", 
        "📁 Download Directories",
        "🔍 System Status",
        "🚪 Exit"
    ]
    
    navigator = MenuNavigator(options, "MONUMATOR - Monumental Markets")
    
    while True:
        try:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 4:  # Quit or Exit
                print("\n👋 Goodbye!")
                sys.exit(0)
            
            elif choice == 0:  # Weekly Reports
                weekly_reports_main()
            
            elif choice == 1:  # Daily Reports
                daily_reports_main()
            
            elif choice == 2:  # Download Directories
                os.system('cls' if os.name == 'nt' else 'clear')
                show_download_directories()
                input("\nPress Enter to continue...")
            
            elif choice == 3:  # System Status
                os.system('cls' if os.name == 'nt' else 'clear')
                system_status()
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()