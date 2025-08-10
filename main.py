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

async def test_scraper_login():
    """Test SEED login functionality - silent test"""
    try:
        import io
        from contextlib import redirect_stdout, redirect_stderr
        from web_automation.base_scraper import BaseScraper
        from web_automation.seed_browser import SeedBrowser
        
        # Suppress all output during test
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            scraper = BaseScraper(headless=True)
            await scraper.setup_browser()
            seed = SeedBrowser(scraper.page)
            result = await seed.login()
            await scraper.cleanup_browser()
            return result
    except:
        return False

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
    
    # Scraper check
    print("🔍 Testing web scraper...")
    try:
        import asyncio
        result = asyncio.run(test_scraper_login())
        if result:
            print("✅ Web scraper: Working successfully")
        else:
            print("❌ Web scraper: Login failed")
    except:
        print("⚠️ Web scraper: Cannot test")
    
    print("✅ System check complete - All systems tested")

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