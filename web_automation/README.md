# 🌐 Web Automation Module

Browser automation for SEED website using Playwright and Firefox with clean inheritance architecture.

## 🏢 Architecture

### Inheritance Hierarchy
```
BaseScraper (browser setup/cleanup)
    ↓
SeedBrowser (SEED login/navigation) 
    ↓
InventoryConfirmationScraper (route inventory scraping)
ItemsScraper (item export downloads)
```

### Design Principles
- **Single Responsibility**: Each class has one clear purpose
- **No Redundancy**: Login and navigation handled once by SeedBrowser
- **Clean Separation**: Scrapers only contain domain-specific logic
- **Workflow Orchestration**: report_workflows/ handles complete processes

## 📄 Files

- **`base_scraper.py`** - Async Firefox browser setup/cleanup with Playwright
- **`seed_browser.py`** - Inherits BaseScraper, provides SEED login/navigation
- **`inventory_confirmation_scraper.py`** - Inherits SeedBrowser, finds routes with missing inventory
- **`items_scraper.py`** - Inherits SeedBrowser, downloads item export files

## 🛠️ Installation

```bash
# Install Playwright
pip install playwright

# Install Firefox browser
playwright install firefox
```

## 🚀 Usage Examples

### Direct Scraper Usage (Async)
```python
import asyncio
from web_automation.inventory_confirmation_scraper import InventoryConfirmationScraper

async def scrape_inventory():
    scraper = InventoryConfirmationScraper(headless=True)
    try:
        await scraper.setup_and_login()
        target_date = scraper.get_previous_business_day()
        route_data = await scraper.get_incomplete_routes(target_date)
        return route_data
    finally:
        await scraper.cleanup_browser()

data = asyncio.run(scrape_inventory())
```

### Workflow Integration (Recommended)
```python
# Workflows handle complete processes including Excel generation
from report_workflows.inventory_confirmation import process_inventory_confirmation_report

# This handles everything: scraping, Excel generation, cleanup
results = process_inventory_confirmation_report(headless=True)
if results['success']:
    print(f"Report saved to: {results['excel_file']}")
```

### Items Download Example
```python
import asyncio
from web_automation.items_scraper import ItemsScraper

async def download_items():
    scraper = ItemsScraper(headless=True)
    try:
        await scraper.setup_and_login()
        file_path = await scraper.download_product_list()
        return file_path
    finally:
        await scraper.cleanup_browser()

file_path = asyncio.run(download_items())
```

## ➕ Creating New Scrapers

### Inherit from SeedBrowser for New SEED Scrapers
```python
from typing import Dict, Any, List
from .seed_browser import SeedBrowser

class NewReportScraper(SeedBrowser):
    """
    Specialized scraper for new report type
    Inherits SEED login/navigation from SeedBrowser
    """
    
    def __init__(self, headless: bool = True):
        super().__init__(headless)
        # Add any specific initialization
    
    async def scrape_specific_data(self) -> List[Dict]:
        """Your specific scraping logic"""
        # Navigate using inherited methods
        await self.page.goto(f"{self.base_url}/cs4/Reports/NewReport")
        
        # Extract data
        elements = await self.page.locator(".data-row").all()
        data = []
        for element in elements:
            data.append({
                'name': await element.text_content(),
                'value': await element.get_attribute('data-value')
            })
        return data
```

### Create Workflow for Complete Process
```python
# report_workflows/new_report.py
import asyncio
from web_automation.new_report_scraper import NewReportScraper

async def run_new_report_async(headless=True):
    scraper = None
    try:
        scraper = NewReportScraper(headless)
        await scraper.setup_and_login()
        
        data = await scraper.scrape_specific_data()
        
        # Generate Excel or process data
        # ... your processing logic ...
        
        return {'success': True, 'data': data}
    finally:
        if scraper:
            await scraper.cleanup_browser()

def process_new_report(headless=True):
    """Sync wrapper for menu integration"""
    return asyncio.run(run_new_report_async(headless))
```

## 🔑 Key Methods

### SeedBrowser (Base for all SEED scrapers)
- `setup_and_login()` - Setup browser and login in one call
- `login()` - SEED authentication
- `navigate_to_route_summary(date)` - Navigate to routes page
- `navigate_to_item_import_export()` - Navigate to product export
- `check_logged_in()` - Verify login status

### InventoryConfirmationScraper
- `get_previous_business_day()` - Calculate target date (Monday=Friday, else previous day)
- `get_incomplete_routes(date)` - Find routes with missing inventory, excluding FF/STATIC assets

### ItemsScraper  
- `download_product_list()` - Complete download workflow for item export
- `find_and_click_export_button()` - Find and click "Export Importable Data" button
- `handle_download()` - Manage file download and save to temp directory
- `validate_excel_file()` - Verify downloaded Excel file

## ⚙️ Configuration

- **Browser**: Firefox (via Playwright)
- **Headless Mode**: Supported for production
- **Viewport**: 1024x600 default
- **Timeouts**: 10s default
- **Downloads**: Native Playwright handling
- **Profile**: Persistent Firefox profile in firefox_profile/

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
- Routes: `https://mycantaloupe.com/cs1/Scheduling/RoutesSummary?ScheduleDateOnly={date}`
- Item Export: `https://mycantaloupe.com/cs1/ItemImportExport/`

## 📋 Workflow vs Scraper

### Use Scrapers When:
- You need specific data extraction only
- Building custom workflows
- Testing individual components

### Use Workflows When:
- You need complete report generation
- Excel output is required
- Multiple data sources are involved
- This is the recommended approach for production

## 🔧 Troubleshooting

### Firefox Not Found
```bash
playwright install firefox
```

### Import Errors
Ensure proper inheritance:
```python
# Correct
from web_automation.seed_browser import SeedBrowser
class MyScraper(SeedBrowser):
    ...

# Wrong (creates redundancy)
from web_automation.base_scraper import BaseScraper
class MyScraper(BaseScraper):
    # Don't reimplement login!
```

### Async/Sync Issues
Always use workflow functions for menu integration:
```python
# For menus (sync)
from report_workflows.inventory_confirmation import process_inventory_confirmation_report

# For async contexts only
from web_automation.inventory_confirmation_scraper import InventoryConfirmationScraper
```

## 💡 Best Practices

1. **Inherit from SeedBrowser** for new SEED scrapers
2. **Keep scrapers focused** - only scraping logic
3. **Use workflows** for complete processes
4. **Let workflows handle** Excel generation
5. **Avoid redundancy** - don't reimplement login/navigation
6. **Clean separation** - scrapers scrape, workflows orchestrate