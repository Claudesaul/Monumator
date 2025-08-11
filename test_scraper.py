"""Test scraper login functionality"""
import asyncio
from web_automation.seed_browser import SeedBrowser

async def test_login():
    print("Testing SEED scraper login...")
    
    try:
        # Test with headless browser
        seed = SeedBrowser(headless=True)
        print("SeedBrowser initialized")
        
        # Setup browser and attempt login
        result = await seed.setup_and_login()
        await seed.cleanup_browser()
        
        if result:
            print("SUCCESS: Web scraper login working")
            return True
        else:
            print("FAILED: Web scraper login failed")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_login())
    exit(0 if result else 1)