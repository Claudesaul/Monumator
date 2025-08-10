# 🌐 Web Automation Setup Guide

## 🏢 Architecture Overview

Two-layer architecture with async Playwright and Firefox:

```
BaseScraper (Foundation)
    ↓
SeedBrowser (SEED-specific)
    ↓
Specialized Scrapers (inventory_scraper.py, product_scraper.py)
    ↓
Menu System (Daily Reports with headless/visible options)
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

**Usage Pattern**:
```python
scraper = BaseScraper(headless=False)    # Visible for debugging
await scraper.setup_browser()            # Sets up browser
# Use scraper.page for operations
await scraper.cleanup_browser()          # Always cleanup
```

### 2. SeedBrowser (`seed_browser.py`)
**Purpose**: SEED-specific browser operations and navigation.

**Key Features**:
- **SEED Authentication**: Handles login with environment credentials
- **Smart Login Detection**: Checks if already logged in
- **SEED Navigation**: Pre-built navigation to common SEED pages
- **Environment Variables**: Requires `SEED_USERNAME` and `SEED_PASSWORD`

**Key Methods**:
```python
async def login() -> bool                        # Handle SEED login process
async def navigate_to_route_summary()            # Go to routes page with date
async def navigate_to_item_import_export()       # Go to product export page
async def check_logged_in() -> bool             # Verify login status
async def wait_for_element()                    # Wait for page elements
```

**Usage Pattern**:
```python
scraper = BaseScraper(headless=False)
await scraper.setup_browser()
seed = SeedBrowser(scraper.page)         # Pass page instance
success = await seed.login()             # Login to SEED
```

## 📁 Specialized Scrapers

### inventory_scraper.py
- **Purpose**: Scrape route inventory confirmations
- **Uses**: BaseScraper + SeedBrowser
- **Output**: Route inventory data for reports

### product_scraper.py  
- **Purpose**: Download product lists from SEED
- **Uses**: BaseScraper + SeedBrowser
- **Output**: Excel files with product data

## 🎯 Menu Integration

### Daily Reports Menu Flow
From `main.py` → `daily_reports.py` → Web scrapers

**Inventory Confirmation Options**:
```python
"🌐 Inventory Confirmation Report"
├─ "🌐 Run Web Scraper (Headless)"     → headless=True
└─ "👁️ Run Web Scraper (Visible)"      → headless=False
```

**How Headless/Visible Works**:
1. **Menu Selection**: User chooses headless or visible option
2. **Parameter Passing**: `headless=True/False` passed to scraper functions
3. **BaseScraper Creation**: `BaseScraper(headless=headless)` 
4. **Browser Behavior**:
   - `headless=True`: No browser window (faster, production)
   - `headless=False`: Visible browser (debugging, testing)

## 🔄 Sync/Async Pattern

**Problem**: Menu system is synchronous, scrapers are async.

**Solution**: Sync wrapper functions in each scraper:
```python
# Async function (internal)
async def run_inventory_confirmation_scraper_async(headless=True):
    # Actual async scraping logic

# Sync wrapper (for menu system)  
def run_inventory_confirmation_scraper(headless=True):
    return asyncio.run(run_inventory_confirmation_scraper_async(headless))
```

**Menu calls the sync wrapper**, which internally runs the async function.

## 🛠️ Making Changes

### Adding New SEED Operations
1. **Add method to SeedBrowser**: New navigation or interaction methods
2. **Test with visible browser**: Use `headless=False` during development
3. **Add to specialized scraper**: Create new scraper or extend existing

### Adding New Scraper
1. **Create new file**: `web_automation/new_scraper.py`
2. **Use pattern**:
   ```python
   from .base_scraper import BaseScraper
   from .seed_browser import SeedBrowser
   
   async def new_scraper_async(headless=True):
       scraper = BaseScraper(headless=headless)
       try:
           await scraper.setup_browser()
           seed = SeedBrowser(scraper.page)
           await seed.login()
           # Your scraping logic here
       finally:
           await scraper.cleanup_browser()
   
   # Sync wrapper for menu system
   def new_scraper(headless=True):
       return asyncio.run(new_scraper_async(headless))
   ```
3. **Add to menu**: Update `daily_reports.py` with new options

### Debugging Tips
- **Always start with visible**: Use `headless=False` when developing
- **Check login first**: Test with system status check before complex scraping
- **Use async context manager**: `async with BaseScraper() as scraper:` for auto-cleanup
- **Environment variables**: Ensure `.env` has `SEED_USERNAME` and `SEED_PASSWORD`
- **Firefox profile**: Check `./web_automation/firefox_profile/` exists and isn't corrupted

### Common Patterns
```python
# Basic scraping pattern
scraper = BaseScraper(headless=False)
try:
    await scraper.setup_browser()
    seed = SeedBrowser(scraper.page)
    await seed.login()
    # Your operations here
finally:
    await scraper.cleanup_browser()

# Context manager pattern (recommended)
async with BaseScraper(headless=False) as scraper:
    seed = SeedBrowser(scraper.page)
    await seed.login()
    # Operations here - cleanup automatic
```

## 🚀 Future Enhancement: Concurrent Daily Reports

### "Process All Daily Reports" Button Implementation

**Current State**: Reports run sequentially (one after another)
**Future State**: Reports run concurrently (all at the same time)

### Architecture Changes Required

**🔄 What Changes**:
```python
# Instead of sequential:
result1 = await run_stockout_report()
result2 = await run_inventory_adjustment()  
result3 = await run_inventory_confirmation()

# Concurrent execution:
results = await asyncio.gather(
    run_stockout_report_async(),
    run_inventory_adjustment_async(), 
    run_inventory_confirmation_async()
)
```

**🌐 Browser Strategy Options**:

1. **Multiple Browsers** (Recommended):
   ```python
   # Each report gets its own browser instance
   async def run_all_daily_reports_concurrent():
       scrapers = [BaseScraper(headless=True) for _ in range(3)]
       
       tasks = [
           run_stockout_with_scraper(scrapers[0]),
           run_inventory_with_scraper(scrapers[1]), 
           run_confirmation_with_scraper(scrapers[2])
       ]
       
       results = await asyncio.gather(*tasks)
   ```

2. **Single Browser, Multiple Tabs**:
   ```python
   # Share browser, separate contexts/pages
   async def run_all_daily_reports_tabs():
       scraper = BaseScraper(headless=True)
       await scraper.setup_browser()
       
       # Create multiple browser contexts (isolated sessions)
       contexts = [await scraper.browser.new_context() for _ in range(3)]
       pages = [await ctx.new_page() for ctx in contexts]
       
       tasks = [
           run_stockout_with_page(pages[0]),
           run_inventory_with_page(pages[1]),
           run_confirmation_with_page(pages[2])
       ]
   ```

### Implementation Complexity

**🟢 What Stays the Same**:
- `BaseScraper` class (no changes needed)
- `SeedBrowser` class (no changes needed)  
- Individual scraper logic (works as-is)
- Menu system integration
- Environment variables and configuration

**🟡 What Needs Updates**:
- **New async function**: `process_all_daily_reports_concurrent()`
- **Error handling**: Handle individual report failures gracefully
- **Progress tracking**: Show which reports are running/completed
- **Resource management**: Proper cleanup of multiple browsers

**🔴 New Complexity**:
- **Login coordination**: Each browser needs separate SEED login
- **Rate limiting**: SEED might throttle multiple concurrent sessions
- **Memory usage**: 3x browser instances = 3x memory consumption
- **Error isolation**: One report failure shouldn't crash others

### Menu Integration Example
```python
# In daily_reports.py
"🎯 Process All Daily Reports"
├─ "🚀 Run All Sequentially (Current)"    → existing workflow
└─ "⚡ Run All Concurrently (Faster)"     → new concurrent workflow
```

### Performance Impact

Speed: Reports run simultaneously instead of sequentially
Resource cost: 3x browser memory usage
Network: 3x simultaneous connections

### Risk Considerations

SEED behavior:
- May limit concurrent logins
- Rate limiting possible
- Data consistency concerns

Mitigation:
- Stagger browser startups
- Monitor failures
- Fallback to sequential
- Thorough testing required

### Implementation Priority

**Phase 1**: Test concurrent capability with 2 reports
**Phase 2**: Add "Run All Concurrently" menu option  
**Phase 3**: Advanced features (progress bars, selective concurrency)

The async architecture supports concurrency. Main challenges are SEED behavior and resource management.

## ✅ Best Practices

1. **Always cleanup**: Use try/finally or context managers
2. **Start visible**: Debug with `headless=False`, deploy with `headless=True`
3. **Smart waits**: Use `await seed.wait_for_element()` instead of sleep
4. **Error handling**: Check return values from login and navigation
5. **Environment setup**: Keep credentials in `.env` file
6. **Sync wrappers**: Always provide sync wrappers for menu integration

This architecture provides a clean separation of concerns while maintaining flexibility for future SEED automation needs.