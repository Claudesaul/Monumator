# 🌐 Web Automation Setup Guide

## 🏢 Architecture Overview

Clean inheritance architecture with async Playwright and Firefox:

```
BaseScraper (browser setup/cleanup)
    ↓
SeedBrowser (SEED login/navigation) 
    ↓
InventoryScraper (route-specific scraping)
ProductScraper (product download logic)
    ↓
report_workflows/ (complete orchestration + Excel)
    ↓
Menu System (daily_reports.py with headless/visible options)
```

## 🔧 Core Components

### Firefox Profile (`./web_automation/firefox_profile/`)
**Purpose**: Persistent Firefox profile that maintains settings, cookies, and preferences across sessions.

**Contents**:
- **User preferences**: Custom settings for automation
- **Cookies/Sessions**: Maintains SEED login state when possible
- **Extensions**: Dark Reader and other productivity extensions
- **Cache**: Browser cache for faster page loading

**Benefits**:
- **Faster startup**: No need to reconfigure browser each time
- **Persistent settings**: Extensions and preferences carry over
- **Login persistence**: May maintain SEED sessions between runs
- **Debugging consistency**: Same browser state for testing

**Note**: Profile is automatically created on first run if it doesn't exist.

### 1. BaseScraper (`base_scraper.py`)
**Purpose**: Foundation class that handles browser lifecycle and common operations.

**Key Features**:
- **Browser Setup**: Firefox with optimized settings (1920x1080, custom user-agent)
- **Persistent Profile**: Uses `./web_automation/firefox_profile/` for settings persistence
- **Async Context Manager**: Use with `async with BaseScraper()` for automatic cleanup
- **Headless Control**: `BaseScraper(headless=False)` for visible browser
- **Error Handling**: Automatic cleanup on failures

**Key Methods**:
```python
async def setup_browser() -> Page        # Creates Firefox browser + page
async def cleanup_browser()              # Closes all browser resources
async def wait_for_page_load()           # Smart waiting for network idle
async def safe_click()                   # Retry logic for clicking elements
```

### 2. SeedBrowser (`seed_browser.py`)
**Purpose**: SEED-specific browser operations and navigation. **Inherits from BaseScraper.**

**Key Features**:
- **Inherits Browser Capabilities**: Gets all BaseScraper functionality
- **SEED Authentication**: Handles login with environment credentials
- **Smart Login Detection**: Checks if already logged in
- **SEED Navigation**: Pre-built navigation to common SEED pages
- **Environment Variables**: Requires `SEED_USERNAME` and `SEED_PASSWORD`
- **One-Call Setup**: `setup_and_login()` does everything

**Key Methods**:
```python
async def setup_and_login() -> bool             # Setup browser + login in one call
async def login() -> bool                       # Handle SEED login process
async def navigate_to_route_summary()           # Go to routes page with date
async def navigate_to_item_import_export()      # Go to product export page
async def check_logged_in() -> bool            # Verify login status
async def wait_for_element()                   # Wait for page elements
```

**Usage Pattern**:
```python
scraper = SeedBrowser(headless=False)
await scraper.setup_and_login()         # One call does everything
# Use scraper.page for operations
await scraper.cleanup_browser()         # Inherited from BaseScraper
```

## 📁 Specialized Scrapers (Inherit from SeedBrowser)

### InventoryScraper (`inventory_scraper.py`)
**Purpose**: Extract route inventory confirmation data
**Inherits**: All SEED login/navigation from SeedBrowser
**Size**: ~200 lines (was 341 - cleaned up!)

**Key Methods**:
```python
async def scrape_route_data(date)                # Main scraping method
async def find_routes_with_missing_inventory()   # Identify incomplete routes
async def extract_asset_data()                  # Get asset details from route
def get_previous_business_day()                # Calculate target date
```

**Usage Pattern**:
```python
scraper = InventoryScraper(headless=True)
await scraper.setup_and_login()               # Inherited - handles everything
route_data = await scraper.scrape_route_data(date)
await scraper.cleanup_browser()               # Inherited
```

### ProductScraper (`product_scraper.py`)  
**Purpose**: Download product lists from SEED ItemImportExport page
**Inherits**: All SEED login/navigation from SeedBrowser
**Size**: ~250 lines (was 307 - cleaned up!)

**Key Methods**:
```python
async def download_product_list()              # Complete download workflow
async def find_and_click_export_button()      # Locate and trigger export
async def handle_download()                   # Manage file download
def validate_excel_file()                    # Verify downloaded file
```

**Usage Pattern**:
```python
scraper = ProductScraper(headless=True)
await scraper.setup_and_login()               # Inherited - handles everything
result = await scraper.download_product_list()
await scraper.cleanup_browser()               # Inherited
```

## 📋 Workflow Orchestration (`report_workflows/`)

### What Workflows Do (vs Scrapers):
- **Scrapers**: Extract data only
- **Workflows**: Complete processes (scraping + Excel + cleanup)

### inventory_confirmation.py
**Purpose**: Complete inventory confirmation report workflow

**Process Flow**:
1. Initialize InventoryScraper
2. Setup browser and login (inherited)
3. Scrape route data
4. Generate Excel report (pandas)
5. Cleanup and return results

**Key Functions**:
```python
def process_inventory_confirmation_report(headless=True)  # Menu integration (sync)
async def run_inventory_confirmation_async(headless=True) # Actual async workflow
def generate_excel_report(route_data)                    # Excel generation
```

### inventory_adjustment.py
**Purpose**: Complete inventory adjustment report workflow

**Process Flow**:
1. Download IAD report (via API)
2. Download product list (via ProductScraper)
3. Process and merge data
4. Generate Excel report (with XLOOKUP formulas)
5. Cleanup temp files

**Key Functions**:
```python
def process_inventory_adjustment_summary()     # Complete workflow (sync)
async def download_product_list_async()       # Uses ProductScraper
def download_iad_report()                     # API download
def generate_inventory_excel()                # Excel with formulas
```

## 🎯 Menu Integration

### Daily Reports Menu Flow
From `main.py` → `daily_reports.py` → Workflow functions → Scrapers

**Menu Structure**:
```python
"📊 Daily Reports System"
├─ "📈 Daily Stockout Report"           → database workflow
├─ "📋 Inventory Adjustment Summary"    → API + scraper workflow  
├─ "🌐 Inventory Confirmation Report"   → pure scraper workflow
│   ├─ "🌐 Run Web Scraper (Headless)" → headless=True
│   └─ "👁️ Run Web Scraper (Visible)"  → headless=False
└─ "🔗 Test Database Connection"        → database test
```

### How It Works:
1. **Menu Selection**: User picks headless/visible option
2. **Workflow Call**: Menu calls `process_inventory_confirmation_report(headless=True/False)`
3. **Scraper Creation**: Workflow creates `InventoryScraper(headless=headless)`
4. **Inheritance Chain**: InventoryScraper → SeedBrowser → BaseScraper
5. **Browser Behavior**: 
   - `headless=True`: No browser window (faster, production)
   - `headless=False`: Visible browser (debugging, testing)

## 🔄 Sync/Async Pattern

**Problem**: Menu system is synchronous, scrapers are async.

**Solution**: Workflows provide sync wrappers:
```python
# Async function (internal workflow)
async def run_inventory_confirmation_async(headless=True):
    scraper = InventoryScraper(headless)
    await scraper.setup_and_login()
    # ... scraping logic ...

# Sync wrapper (for menu system)  
def process_inventory_confirmation_report(headless=True):
    return asyncio.run(run_inventory_confirmation_async(headless))
```

**Menu calls the sync wrapper**, which handles the async execution internally.

## 🛠️ Making Changes

### Adding New SEED Scraper
1. **Inherit from SeedBrowser**:
   ```python
   from web_automation.seed_browser import SeedBrowser
   
   class NewScraper(SeedBrowser):
       def __init__(self, headless=True):
           super().__init__(headless)
       
       async def scrape_new_data(self):
           # Your scraping logic - login already handled
           pass
   ```

2. **Create Workflow**:
   ```python
   # report_workflows/new_report.py
   async def run_new_report_async(headless=True):
       scraper = NewScraper(headless)
       try:
           await scraper.setup_and_login()  # Inherited
           data = await scraper.scrape_new_data()
           # Generate Excel, etc.
           return {'success': True, 'data': data}
       finally:
           await scraper.cleanup_browser()  # Inherited
   
   def process_new_report(headless=True):  # For menu
       return asyncio.run(run_new_report_async(headless))
   ```

3. **Add to Menu**: Update `daily_reports.py` with new options

### Benefits of New Architecture:
- **No Redundancy**: Login/navigation code exists once in SeedBrowser
- **Clean Separation**: Scrapers scrape, workflows orchestrate
- **Easy Extension**: Inherit from SeedBrowser, get everything
- **Smaller Files**: inventory_scraper.py went from 341 to ~200 lines

### Debugging Tips
- **Start visible**: Use `headless=False` when developing
- **Test inheritance**: Verify scrapers inherit properly from SeedBrowser
- **Check workflows**: Test complete process, not just scraping
- **Environment variables**: Ensure `.env` has `SEED_USERNAME` and `SEED_PASSWORD`

### Common Patterns

#### New Scraper Pattern:
```python
from web_automation.seed_browser import SeedBrowser

class MyScraper(SeedBrowser):           # Inherit SEED capabilities
    def __init__(self, headless=True):
        super().__init__(headless)      # Initialize parent
    
    async def my_specific_scraping(self):
        # Your logic here - login is handled by parent
        pass
```

#### Workflow Pattern:
```python
async def my_workflow_async(headless=True):
    scraper = MyScraper(headless)
    try:
        await scraper.setup_and_login()    # One call does everything
        data = await scraper.my_specific_scraping()
        # Process data, generate Excel, etc.
        return {'success': True, 'data': data}
    finally:
        await scraper.cleanup_browser()    # Always cleanup

def my_workflow(headless=True):            # Sync wrapper for menus
    return asyncio.run(my_workflow_async(headless))
```

## 🚀 Future Enhancement: Concurrent Daily Reports

### "Process All Daily Reports" Button Implementation

**Current State**: Reports run sequentially (one after another)
**Future State**: Reports run concurrently (all at the same time)

### Architecture Changes Required

**Concurrent Execution**:
```python
# Sequential (current):
result1 = process_stockout_report()
result2 = process_inventory_adjustment_summary()  
result3 = process_inventory_confirmation_report()

# Concurrent (future):
results = await asyncio.gather(
    run_stockout_async(),
    run_inventory_adjustment_async(), 
    run_inventory_confirmation_async()
)
```

**Browser Strategy**: Multiple browser instances (recommended):
```python
async def run_all_daily_reports_concurrent():
    # Each report gets its own browser
    tasks = [
        run_stockout_async(headless=True),
        run_inventory_adjustment_async(headless=True), 
        run_inventory_confirmation_async(headless=True)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

### Implementation Complexity

**🟢 What Stays the Same**:
- All scraper classes (work as-is with inheritance)
- Individual workflow functions
- Menu system integration  
- Environment variables and configuration

**🟡 What Needs Updates**:
- New `process_all_daily_reports_concurrent()` function
- Error handling for multiple processes
- Progress tracking in menu
- Resource management

**🔴 New Complexity**:
- Multiple SEED logins simultaneously
- SEED may throttle concurrent sessions
- 3x memory usage (3 browsers)
- Error isolation between reports

### Menu Integration Example
```python
# In daily_reports.py
"🎯 Process All Daily Reports"
├─ "🚀 Run All Sequentially (Current)"    → existing workflow
└─ "⚡ Run All Concurrently (Faster)"     → new concurrent workflow
```

The inheritance architecture supports this well - each concurrent process gets its own scraper instance with full capabilities.

## ✅ Best Practices

1. **Inherit from SeedBrowser** for new SEED scrapers (not BaseScraper)
2. **Use workflows** for complete processes (not direct scraper calls)
3. **Let workflows handle** Excel generation and file management
4. **Start visible**: Debug with `headless=False`, deploy with `headless=True`
5. **One call setup**: Use `setup_and_login()` for simplicity
6. **Always cleanup**: Automatic with inheritance, but verify in workflows
7. **Avoid redundancy**: Don't reimplement login/navigation logic

This clean architecture eliminates redundancy while maintaining flexibility for future SEED automation needs.