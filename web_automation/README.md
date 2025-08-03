# Web Automation Module

Handles browser automation and web scraping for SEED website interactions.

## Files

- **`base_scraper.py`** - Common browser setup (Edge/Chrome)
- **`seed_browser.py`** - SEED login and navigation
- **`inventory_scraper.py`** - Inventory confirmation scraping
- **`product_scraper.py`** - Product list downloads

## How It Works

Uses Selenium to automate SEED website interactions:
1. **BaseScraper** - Sets up browser with optimal settings
2. **SeedBrowser** - Handles SEED login automatically
3. **Specialized scrapers** - Task-specific data extraction

## Usage

### SEED Login
```python
from web_automation.base_scraper import BaseScraper
from web_automation.seed_browser import SeedBrowser

with BaseScraper(headless=True) as scraper:
    seed_browser = SeedBrowser(scraper.driver)
    if seed_browser.login():
        print("Successfully logged into SEED")
```

### Inventory Confirmation Scraping
```python
from web_automation.inventory_scraper import run_inventory_confirmation_scraper

results = run_inventory_confirmation_scraper(headless=True)
if results['success']:
    print(f"Generated report: {results['excel_file']}")
```

### Product List Download
```python
from web_automation.product_scraper import download_product_list_with_browser

results = download_product_list_with_browser(headless=True)
if results['success']:
    print(f"Downloaded: {results['file_path']}")
```

## Adding New Scrapers

### Step 1: Create Scraper
Create `new_scraper.py`:
```python
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser
from selenium.webdriver.common.by import By

class NewDataScraper(BaseScraper):
    def scrape_specific_data(self):
        # Navigate and extract data
        self.driver.get("https://mycantaloupe.com/specific-page")
        time.sleep(3)
        
        # Extract elements
        elements = self.driver.find_elements(By.CLASS_NAME, "data-item")
        data = [{'name': el.text, 'value': el.get_attribute('value')} for el in elements]
        return data
    
    def run_scraper(self):
        try:
            self.setup_browser()
            seed_browser = SeedBrowser(self.driver)
            
            if not seed_browser.login():
                raise Exception("Login failed")
                
            data = self.scrape_specific_data()
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            self.cleanup_browser()

def run_new_data_scraper(headless=True):
    scraper = NewDataScraper(headless=headless)
    return scraper.run_scraper()
```

### Step 2: Use in Workflow
```python
from web_automation.new_scraper import run_new_data_scraper

results = run_new_data_scraper(headless=True)
```

## Browser Configuration

- **Browser**: Microsoft Edge (headless supported)
- **Timeouts**: 30s page load, 10s implicit wait
- **Downloads**: Temp directory with auto-cleanup

## Environment Variables

Required in `.env`:
```bash
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```

## SEED Website Patterns

### Login Elements
- Email: `testEmailInput` class
- Password: `testPasswordInput` class  
- Login button: `testSignInButton` class

### Common URLs
- Login: `https://mycantaloupe.com`
- Routes: `https://mycantaloupe.com/cs4/Reports/RoutesSummary?date={date}`
- Product Export: `https://mycantaloupe.com/cs4/ItemImportExport/ExcelExport`

### Element Selection
```python
# By class (preferred)
element = driver.find_element(By.CLASS_NAME, "testEmailInput")

# By XPath for complex cases
links = driver.find_elements(By.XPATH, "//a[contains(@href, 'RouteDetails')]")

# With wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "target-class"))
)
```