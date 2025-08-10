# 🌐 Web Automation Module

Browser automation for SEED website using Playwright and Firefox.

## 🏢 Architecture

- Async/await pattern
- Firefox browser
- Sync wrappers for menu integration
- Native download handling

## 📄 Files

- **`base_scraper.py`** - Async Firefox browser setup with Playwright
- **`seed_browser.py`** - Async SEED login and navigation
- **`inventory_scraper.py`** - Async inventory confirmation scraping
- **`product_scraper.py`** - Async product list downloads with native download handling

## 🛠️ Installation

```bash
# Install Playwright
pip install playwright

# Install Firefox browser
playwright install firefox
```

## 🚀 Usage Examples

### Async SEED Login
```python
import asyncio
from web_automation.base_scraper import BaseScraper
from web_automation.seed_browser import SeedBrowser

async def login_example():
    async with BaseScraper(headless=True) as scraper:
        await scraper.setup_browser()
        seed_browser = SeedBrowser(scraper.page)
        if await seed_browser.login():
            print("Successfully logged into SEED")

# Run async function
asyncio.run(login_example())
```

### Synchronous Usage (Menu Integration)
```python
# All modules provide sync wrappers for backward compatibility
from web_automation.inventory_scraper import run_inventory_confirmation_scraper

# This is a sync wrapper that handles async internally
results = run_inventory_confirmation_scraper(headless=True)
if results['success']:
    print(f"Generated report: {results['excel_file']}")
```

### Product Download with Native Handling
```python
from web_automation.product_scraper import download_product_list_with_browser

# Sync wrapper for menu system
results = download_product_list_with_browser(headless=True)
if results['success']:
    print(f"Downloaded: {results['file_path']}")
```

## ➕ Creating New Scrapers

### Async Scraper Template
```python
import asyncio
from typing import Dict, Any
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser

class NewDataScraper(BaseScraper):
    async def scrape_specific_data(self):
        # Navigate to page
        await self.page.goto("https://mycantaloupe.com/specific-page")
        await self.page.wait_for_load_state('networkidle')
        
        # Extract data using Playwright selectors
        elements = await self.page.locator(".data-item").all()
        data = []
        for element in elements:
            data.append({
                'name': await element.text_content(),
                'value': await element.get_attribute('value')
            })
        return data
    
    async def run_scraper(self) -> Dict[str, Any]:
        try:
            await self.setup_browser()
            seed_browser = SeedBrowser(self.page)
            
            if not await seed_browser.login():
                raise Exception("Login failed")
                
            data = await self.scrape_specific_data()
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            await self.cleanup_browser()

# Async function
async def run_new_scraper_async(headless=True):
    scraper = NewDataScraper(headless=headless)
    return await scraper.run_scraper()

# Sync wrapper for menu integration
def run_new_scraper(headless=True):
    return asyncio.run(run_new_scraper_async(headless))
```

## ✨ Playwright Features

- Auto-waiting for elements
- Network idle detection
- Concurrent operations

```python
await page.wait_for_selector(".testPasswordInput", timeout=10000)
```

### Better Selectors
```python
# CSS selectors
await page.click(".testSignInButton")

# Text selectors
await page.click("button:has-text('Export')")

# Chained selectors
await page.locator("tr").filter(has_text="Route 102").click()

# XPath (when needed)
await page.locator("xpath=//a[contains(@href, 'RouteDetails')]").click()
```

## ⚙️ Browser Configuration

- **Browser**: Firefox (via Playwright)
- **Headless Mode**: Supported with better performance
- **Viewport**: 1920x1080 default
- **Timeouts**: 30s default, configurable per operation
- **Downloads**: Native handling with progress monitoring

## 🔑 Environment Variables

Required in `.env`:
```bash
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```

## 🌱 SEED Website Patterns

### Login Elements
- Email: `.testEmailInput`
- Password: `.testPasswordInput`
- Login button: `.testSignInButton`

### Common URLs
- Login: `https://mycantaloupe.com`
- Routes: `https://mycantaloupe.com/cs4/Reports/RoutesSummary?date={date}`
- Product Export: `https://mycantaloupe.com/cs4/ItemImportExport/ExcelExport`

## 🎯 Features

- Async architecture
- Firefox browser
- Native downloads
- Screenshots
- Network interception

## 🔧 Troubleshooting

### Firefox Not Found
```bash
playwright install firefox
```

### Async Errors
Ensure you're using the sync wrappers for menu integration:
```python
# Use this for menu system
from web_automation.inventory_scraper import run_inventory_confirmation_scraper

# Not this (unless in async context)
from web_automation.inventory_scraper import run_inventory_confirmation_scraper_async
```

### Download Issues
Playwright handles downloads natively - no temp directory management needed.

## 💡 Usage Tips

- Use headless mode for production
- Reuse browser contexts
- Use network idle detection