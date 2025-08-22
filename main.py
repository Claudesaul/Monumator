"""
MONUMATOR - Monumental Markets Automation System
=====================================================

Clean, simplified menu system with arrow navigation.
"""

import sys
import os
import time
from utils.menu_navigator import MenuNavigator
from reports.weekly_reports import main as weekly_reports_main
from reports.daily_reports import main as daily_reports_main

def goodbye_with_countdown():
    """Display countdown timer with goodbye message"""
    for i in range(3, 0, -1):
        print(f"\n⏰ This window will close in: {i}...")
        time.sleep(1)
    print("\n👋 Goodbye!")
    time.sleep(1)
    sys.exit(0)

def show_download_directories():
    """Display download directory structure"""
    from config.report_config import DOWNLOAD_PATHS
    
    print("\n📁 DOWNLOAD DIRECTORIES")
    print("=" * 40)
    for name, path in DOWNLOAD_PATHS.items():
        status = "✅" if os.path.exists(path) else "❌"
        print(f"{status} {name.upper()}: {path}")

async def test_scraper_login():
    """Test SEED login functionality - returns (success, error_message)"""
    try:
        from web_automation.seed_browser import SeedBrowser
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        # Check credentials first
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        if not os.getenv('SEED_USERNAME') or not os.getenv('SEED_PASSWORD'):
            return False, "Missing SEED credentials in environment variables"
        
        # Test login with suppressed output
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            seed = SeedBrowser(headless=True)
            result = await seed.setup_and_login()
            await seed.cleanup_browser()
            
        if result:
            return True, None
        else:
            return False, "Login failed - check credentials or SEED website availability"
            
    except Exception as e:
        return False, f"Browser setup failed: {str(e)}"

def system_status():
    """Quick system status check"""
    print("\n🔍 SYSTEM STATUS")
    print("=" * 40)

    # Level database check
    print("🔍 Testing Level database connection...")
    try:
        from database.connection import test_level_connection
        if test_level_connection():
            print("✅ Level Database: Connection established")
        else:
            print("❌ Level Database: Connection failed")
    except:
        print("⚠️ Level Database: Cannot test")
    
    # LightSpeed database check
    print("🔍 Testing LightSpeed database connection...")
    try:
        from database.connection import test_lightspeed_connection
        if test_lightspeed_connection():
            print("✅ LightSpeed Database: Connection established")
        else:
            print("❌ LightSpeed Database: Connection failed")
    except:
        print("⚠️ LightSpeed Database: Cannot test")
    
    # Scraper check
    print("🔍 Testing web scraper...")
    try:
        import asyncio
        success, error_msg = asyncio.run(test_scraper_login())
        if success:
            print("✅ Web scraper: Seed Login successful")
        else:
            print(f"❌ Web scraper: {error_msg}")
    except Exception as e:
        print(f"⚠️ Web scraper: Test failed - {str(e)}")
    
    print("✅ System check complete")

def main():
    """Main application entry point"""
    
    options = [
        "📅 Weekly Reports",
        "📊 Daily Reports", 
        "🔍 System Status Check",
        "🚪 Exit"
    ]
    
    navigator = MenuNavigator(options, "MONUMATOR - Monumental Markets")
    
    while True:
        try:
            choice = navigator.navigate()
            
            if choice == -1 or choice == 3:  # Quit or Exit
                goodbye_with_countdown()
            
            elif choice == 0:  # Weekly Reports
                weekly_reports_main()
            
            elif choice == 1:  # Daily Reports
                daily_reports_main()
            
            elif choice == 2:  # System Status Check
                os.system('cls' if os.name == 'nt' else 'clear')
                system_status()
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            goodbye_with_countdown()
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()