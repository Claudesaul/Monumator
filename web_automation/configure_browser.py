# configure_browser.py
import asyncio
from base_scraper import BaseScraper

async def configure_browser():
    scraper = BaseScraper(headless=False)
    try:
        print("🔧 Opening Firefox for configuration...")
        await scraper.setup_browser()
        print("Browser ready! Configure extensions, themes, settings as needed.")
        print("Close the browser window when done (settings auto-save).")
        
        # Wait for user to close browser manually
        while scraper.page and not scraper.page.is_closed():
            await asyncio.sleep(1)
            
    except Exception:
        pass  # Suppress all errors
    finally:
        try:
            await scraper.cleanup_browser()
        except Exception:
            pass  # Suppress cleanup errors

if __name__ == "__main__":
    asyncio.run(configure_browser())