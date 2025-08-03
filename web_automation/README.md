# Web Automation Module

This module handles all browser automation and web scraping operations for SEED website interactions.

## What This Module Contains

- **`base_scraper.py`** - Common browser setup and utilities
- **`seed_browser.py`** - SEED-specific login and navigation
- **`inventory_scraper.py`** - Inventory confirmation report scraping
- **`product_scraper.py`** - Product list download automation

## Purpose

Provides modular web automation capabilities for SEED website interactions with:
- **Reusable browser setup** 
- **Common SEED operations**
- **Specialized scrapers for different tasks**
- **Error handling and recovery**

## Quick Reference

**Main Web Automation Files:**
- `base_scraper.py` - Common browser setup for Edge/Chrome
- `seed_browser.py` - SEED login and navigation utilities
- `inventory_scraper.py` - Inventory confirmation scraping
- `product_scraper.py` - Product list download automation

**Direct imports** - No package structure:
```python
from web_automation.base_scraper import BaseScraper
from web_automation.seed_browser import SeedBrowser
from web_automation.inventory_scraper import run_inventory_confirmation_scraper
from web_automation.product_scraper import download_product_list_with_browser
```

## Key Features

- **Microsoft Edge Support**: Optimized for Edge browser with headless capability
- **SEED Authentication**: Handles login automatically with environment credentials
- **Vue.js Support**: Proper handling of Vue.js SPA loading
- **Download Management**: File download monitoring and validation
- **Error Recovery**: Comprehensive error handling with retries
- **Cross-Platform**: Works on Windows with proper driver management

## How It Works

1. **Base Setup**: `BaseScraper` configures browser with optimal settings
2. **SEED Navigation**: `SeedBrowser` handles login and common navigation
3. **Specialized Scrapers**: Task-specific scrapers inherit common functionality
4. **Resource Cleanup**: Automatic browser cleanup and temp file management

## Usage Examples

### Simple SEED Login
```python
from web_automation.base_scraper import BaseScraper
from web_automation.seed_browser import SeedBrowser

# Use context manager for automatic cleanup
with BaseScraper(headless=True) as scraper:
    seed_browser = SeedBrowser(scraper.driver)
    
    if seed_browser.login():
        print("Successfully logged into SEED")
        # Do your scraping here
```

### Inventory Confirmation Scraping
```python
from web_automation.inventory_scraper import run_inventory_confirmation_scraper

# Run complete inventory confirmation workflow
results = run_inventory_confirmation_scraper(headless=True)

if results['success']:
    print(f"Generated report: {results['excel_file']}")
    print(f"Routes processed: {results['routes_found']}")
else:
    print(f"Scraping failed: {results['error']}")
```

### Product List Download
```python
from web_automation.product_scraper import download_product_list_with_browser

# Download product list via browser automation
results = download_product_list_with_browser(headless=True)

if results['success']:
    print(f"Downloaded file: {results['file_path']}")
    print(f"Validation: {results['validation']}")
else:
    print(f"Download failed: {results['error']}")
```

## Adding New SEED Scrapers

### Step 1: Create New Scraper
Create `new_scraper.py`:

```python
import time
from selenium.webdriver.common.by import By
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser

class NewDataScraper(BaseScraper):
    """
    Scrapes new data from SEED
    """
    
    def __init__(self, headless=True):
        super().__init__(headless)
        self.seed_browser = None
        
    def scrape_specific_data(self):
        """
        Your specific scraping logic
        
        Returns:
            list: Scraped data
        """
        scraped_data = []
        
        try:
            # Navigate to specific page
            specific_url = "https://mycantaloupe.com/specific-page"
            self.driver.get(specific_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Extract data using Selenium
            data_elements = self.driver.find_elements(By.CLASS_NAME, "data-item")
            
            for element in data_elements:
                item_data = {
                    'name': element.find_element(By.CLASS_NAME, "item-name").text,
                    'value': element.find_element(By.CLASS_NAME, "item-value").text
                }
                scraped_data.append(item_data)
                
            print(f"Scraped {len(scraped_data)} items")
            return scraped_data
            
        except Exception as e:
            print(f"❌ Scraping failed: {str(e)}")
            raise
    
    def run_new_data_scraper(self):
        """
        Complete workflow for new data scraping
        
        Returns:
            dict: Results with success status and data
        """
        start_time = time.time()
        
        try:
            print("🚀 Starting new data scraper...")
            
            # Setup browser and SEED connection
            self.setup_browser()
            self.seed_browser = SeedBrowser(self.driver)
            
            # Login to SEED
            if not self.seed_browser.login():
                raise Exception("Failed to login to SEED")
            
            # Scrape specific data
            scraped_data = self.scrape_specific_data()
            
            if not scraped_data:
                raise Exception("No data scraped")
            
            # Calculate results
            elapsed_time = time.time() - start_time
            
            results = {
                'success': True,
                'data': scraped_data,
                'elapsed_time': elapsed_time,
                'items_count': len(scraped_data)
            }
            
            print(f"✅ New data scraping completed in {elapsed_time:.1f} seconds")
            return results
            
        except Exception as e:
            print(f"❌ New data scraping failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }
        finally:
            self.cleanup_browser()

# Convenience function for external use
def run_new_data_scraper(headless=True):
    """
    Run new data scraper (external interface)
    """
    scraper = NewDataScraper(headless=headless)
    return scraper.run_new_data_scraper()
```

### Step 2: Add to Workflow
Create corresponding workflow in `../report_workflows/new_data.py`:

```python
from web_automation.new_scraper import run_new_data_scraper

def process_new_data_report(headless=True):
    """
    Complete workflow for new data report
    """
    print("🚀 Starting new data report processing...")
    
    results = run_new_data_scraper(headless=headless)
    
    if results['success']:
        print("✅ New data report completed successfully")
        # Process the data further if needed
    else:
        print("❌ New data report failed")
    
    return results
```

## Browser Configuration

### Default Settings
- **Browser**: Microsoft Edge (headless mode available)
- **Timeouts**: 30 seconds page load, 10 seconds implicit wait
- **Downloads**: Automatic download to temp directory
- **Logging**: Suppressed for headless mode

### Environment Requirements
```bash
# Required in .env file
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```

### Driver Management
The system uses automatic Edge WebDriver detection. Ensure Microsoft Edge browser is installed.

## SEED Website Interaction Patterns

### Login Process
1. Navigate to `https://mycantaloupe.com`
2. Detect login form by `testPasswordInput` class
3. Fill credentials using `testEmailInput` and `testPasswordInput`
4. Click login with `testSignInButton`
5. Wait for login completion (8 seconds)

### Common SEED URLs
- **Login**: `https://mycantaloupe.com`
- **Routes Summary**: `https://mycantaloupe.com/cs4/Reports/RoutesSummary?date={date}`
- **Item Export**: `https://mycantaloupe.com/cs4/ItemImportExport/ExcelExport`

### Element Selection Strategies
```python
# By class name (preferred for SEED)
element = driver.find_element(By.CLASS_NAME, "testEmailInput")

# By XPath for complex selections
route_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'RouteDetails')]")

# Wait for elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "target-class"))
)
```

## Error Handling Patterns

### Stale Element Handling
```python
from selenium.common.exceptions import StaleElementReferenceException

try:
    element.click()
except StaleElementReferenceException:
    # Re-find element and retry
    element = driver.find_element(By.ID, "element-id")
    element.click()
```

### Download Monitoring
```python
def wait_for_download(download_dir, timeout=60):
    """Wait for file download to complete"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        files = glob.glob(os.path.join(download_dir, "*"))
        for file_path in files:
            if file_path.endswith('.xlsx') and not file_path.endswith('.tmp'):
                return file_path
        time.sleep(1)
    
    return None
```

## File Management

### Download Handling
- Downloads go to temporary directories
- Files are validated after download
- Automatic cleanup of temp files
- Copy to standardized locations

### Excel File Validation
```python
def validate_excel_file(file_path):
    """Validate downloaded Excel file"""
    try:
        df = pd.read_excel(file_path)
        return {
            'valid': True,
            'rows': len(df),
            'columns': len(df.columns)
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }
```

## Dependencies

- `selenium` - Browser automation
- `pandas` - Data validation and processing
- `python-dotenv` - Environment variable loading
- `tempfile` - Temporary file management
- `glob` - File pattern matching

## Testing

### Test Browser Setup
```bash
cd /path/to/Monumator
python -c "from web_automation.base_scraper import BaseScraper; scraper = BaseScraper(); scraper.setup_browser(); print('Browser setup successful'); scraper.cleanup_browser()"
```

### Test SEED Login
```bash
python -c "from web_automation.seed_browser import SeedBrowser; from web_automation.base_scraper import BaseScraper; scraper = BaseScraper(); scraper.setup_browser(); seed = SeedBrowser(scraper.driver); print('Login successful:', seed.login()); scraper.cleanup_browser()"
```

## Performance Tips

1. **Use Headless Mode**: Faster execution in production
2. **Reuse Browser Instance**: Don't recreate browser for multiple operations
3. **Explicit Waits**: Use WebDriverWait instead of time.sleep()
4. **Element Caching**: Store frequently used elements
5. **Parallel Processing**: Run multiple scrapers concurrently when possible