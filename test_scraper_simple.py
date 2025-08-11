"""Test scraper login functionality without emojis"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Monkey patch print statements in scraper modules to avoid emoji issues
def safe_print(msg):
    # Remove emojis and special unicode characters
    cleaned_msg = ''.join(c for c in msg if ord(c) < 127)
    print(cleaned_msg)

# Replace print in all modules
import web_automation.base_scraper
import web_automation.seed_browser
web_automation.base_scraper.print = safe_print  
web_automation.seed_browser.print = safe_print

from web_automation.seed_browser import SeedBrowser

async def test_login():
    print("Testing SEED scraper login...")
    
    # Check environment variables first
    load_dotenv()
    username = os.getenv('SEED_USERNAME')
    password = os.getenv('SEED_PASSWORD')
    
    if not username or not password:
        print("ERROR: SEED credentials not found in environment")
        return False
    
    print(f"Found credentials for user: {username[:3]}...")
    
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