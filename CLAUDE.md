# Monumator - Claude Documentation

## System Overview

Automation system for Monumental Markets that generates business reports from SEED (Cantaloupe) and SQL Server databases.

### Core Capabilities
- Arrow-key navigation menus
- SQL Server database integration (LightSpeed + Level)
- Excel report generation (openpyxl + xlwings)
- Web automation (Playwright + Firefox)
- API downloads
- System health checks
- Modular architecture

### Business Context
- Target System: SEED (Cantaloupe) vending management
- Data Sources: SEED API, SQL Server databases, web scraping
- Output: Excel reports
- Reports: Daily stockout, inventory adjustments, weekly analytics

## Architecture Overview

### Design Philosophy
- Direct imports (no complex packages)
- Modular separation
- Minimal boilerplate
- Expandable structure

### Project Structure
```
Monumator/
├── config/                    # Configuration (direct imports)
│   ├── database_config.py     # Database connections & settings
│   └── report_config.py       # SEED API IDs & download paths
├── database/                  # Database operations (direct imports)
│   ├── connection.py          # Clean connection management
│   └── queries.py             # All SQL queries & pandas processing
├── excel_processing/          # Excel generation (direct imports)
│   ├── base_excel.py          # Common Excel utilities
│   ├── stockout_excel.py      # Daily stockout (openpyxl)
│   └── inventory_excel.py     # Inventory adjustment (xlwings)
├── web_automation/            # Async Playwright automation (direct imports)
│   ├── base_scraper.py        # Async Firefox browser setup
│   ├── seed_browser.py        # Async SEED login & navigation
│   ├── inventory_confirmation_scraper.py   # Async route inventory confirmation
│   ├── items_scraper.py       # Async item export downloads
│   └── firefox_profile/       # Persistent Firefox profile
├── report_workflows/          # Complete workflows (direct imports)
│   ├── daily_stockout.py      # Daily stockout workflow (implemented)
│   ├── inventory_adjustment.py # Inventory adjustment (implemented)
│   ├── inventory_confirmation.py # Web scraping workflow (implemented)
│   ├── weekly_reports.py      # Legacy weekly downloads (implemented)
│   ├── weekly_sales.py        # Weekly sales (skeleton)
│   ├── oos_tracker.py         # OOS tracker (skeleton)
│   ├── ocs_in_full.py         # OCS analysis (skeleton)
│   ├── fresh_food_tracker.py  # Fresh food tracking (skeleton)
│   ├── market_inventory.py    # Market inventory (skeleton)
│   ├── spoilage_shrink.py     # Spoilage tracking (skeleton)
│   └── warehouse_inventory.py # Warehouse inventory (skeleton)
├── utils/                     # Utilities (direct imports)
│   ├── downloader.py          # SEED API downloads with concurrency
│   └── menu_navigator.py      # Arrow-key menu navigation
├── templates/                 # Excel template files
├── main.py                    # Main menu with arrow navigation
├── daily_reports.py           # Daily reports sub-menu system
└── weekly_reports.py          # Weekly reports sub-menu system
```

## Core Components

### 1. Navigation System

**Arrow-Key Menus (`utils/menu_navigator.py`)**
```python
class MenuNavigator:
    def __init__(self, options, title)
    def display()    # Shows menu with highlighting
    def navigate()   # Handles ↑↓ arrow keys, Enter, Q
```

**Entry Points:**
- `main.py` - Main menu (5 options)
- `daily_reports.py` - Daily reports with sub-menus (6 main options)
- `weekly_reports.py` - Weekly reports with sub-menus (7 reports + process all)

### 2. Database Integration (`database/`)

**Dual SQL Server Architecture:**
- **LightSpeed Database**: `dbo.ItemView` (order data) at 10.216.207.32
- **Level Database**: `dbo.AreaItemParView` (inventory data) at 10.216.207.32

**Key Functions:**
```python
# connection.py
get_lightspeed_connection()  # LightSpeed database
get_level_connection()       # Level database  
test_database_connection()   # Silent connectivity test
execute_query()              # Pandas DataFrame results

# queries.py
execute_all_queries()        # Complete stockout analysis
get_highlights_data()        # Stockout summary with counts
get_markets_data()           # Market-specific stockouts
get_null_orders_data()       # Missing quantity orders
get_ocs_data()              # Office coffee service analysis
get_sample_data()           # Testing fallback data
```

**Cross-Database Processing:**
1. Query each database separately
2. Merge using pandas DataFrames
3. Apply Access-like aggregations

### 3. Excel Processing (`excel_processing/`)

**Dual Library Strategy:**
- **openpyxl**: Template preservation, simple data insertion
- **xlwings**: Complex formulas, Excel automation

**Key Components:**
```python
# base_excel.py
class ExcelProcessorBase:
    create_working_copy()     # Copy template with date
    get_template_info()       # Template validation

# stockout_excel.py  
class StockoutExcelProcessor(ExcelProcessorBase):
    generate_stockout_report()  # 4-sheet report generation

# inventory_excel.py
class InventoryExcelProcessor(ExcelProcessorBase):
    generate_inventory_adjustment_report()  # XLOOKUP formulas
```

### 4. Web Automation (`web_automation/`)

**Async Browser Automation with Playwright & Firefox:**
```python
# base_scraper.py
class BaseScraper:
    async setup_browser()    # Firefox with Playwright (async)
    async cleanup_browser()  # Automatic resource cleanup

# seed_browser.py
class SeedBrowser:
    async login()            # Async SEED authentication
    async navigate_to()      # Async navigation methods

# Specialized scrapers (all async with sync wrappers)
inventory_confirmation_scraper.py  # Find routes with missing inventory, exclude FF/STATIC
items_scraper.py                   # Download item export files from SEED
```

**Key Features:**
- Firefox browser with persistent profile
- Async architecture 
- Native download handling
- Minimal wait conditions (Playwright auto-waits)

### 5. Report Workflows (`report_workflows/`)

**Implemented Workflows:**
```python
# daily_stockout.py
process_stockout_report(use_sample_data=False)
get_stockout_processing_status()

# inventory_adjustment.py  
process_inventory_adjustment_summary()
get_inventory_adjustment_status()

# inventory_confirmation.py
process_inventory_confirmation_report(headless=True)
get_inventory_confirmation_status()

# weekly_reports.py
process_weekly_reports()  # Legacy 4-report download
```

**Future Weekly Reports (Skeletons Ready):**
- Weekly Sales, OOS Tracker, OCS in Full
- Fresh Food Tracker, Market Inventory
- Spoilage/Shrink, Warehouse Inventory

### 6. Configuration (`config/`)

**Report Configuration (`report_config.py`):**
```python
SEED_REPORTS = {
    "daily_fill_oos": "33105",
    "Weekly Sales Reporting Market": "33106",
    # Add new report IDs here
}

DOWNLOAD_PATHS = {
    "weekly": "downloads/weekly/",
    "daily": "downloads/daily/",
    "temp": "downloads/temp/"
}
```

**Database Configuration (`database_config.py`):**
```python
LIGHTSPEED_CONNECTION = {
    "connection_string": f"DRIVER={{SQL Server}};SERVER=10.216.207.32;DATABASE=LightSpeed;UID={DB_USERNAME};PWD={DB_PASSWORD}"
}

LEVEL_CONNECTION = {
    "connection_string": f"DRIVER={{SQL Server}};SERVER=10.216.207.32;DATABASE=Level;UID={DB_USERNAME};PWD={DB_PASSWORD}"
}
```

## User Workflows

### Main Menu Navigation
```
python main.py
┌─ Use ↑↓ arrows to navigate
├─ 📅 Weekly Reports → weekly_reports.py sub-menu
├─ 📊 Daily Reports → daily_reports.py sub-menu  
├─ 📁 Download Directories → Show file organization
├─ 🔍 System Status → Quick health check
└─ 🚪 Exit
```

### Daily Reports Sub-Menu
```
📊 Daily Reports System
├─ 📈 Daily Stockout Report
│  ├─ 🔄 Process Report (live database)
│  └─ 📊 Use Sample Data (testing)
├─ 📋 Inventory Adjustment Summary
│  ├─ 🔄 Process Report (auto-download)
│  └─ 📅 Check Date Logic (Monday=Friday, else previous)
├─ 🌐 Inventory Confirmation Report  
│  ├─ 🌐 Run Web Scraper (Headless)
│  └─ 👁️ Run Web Scraper (Visible)
├─ 🎯 Process All Daily Reports
└─ 🔗 Test Database Connection
```

### Weekly Reports Sub-Menu
```
📅 Weekly Reports System
├─ 📈 Weekly Sales (ready for implementation)
├─ 📊 OOS Tracker (ready for implementation)
├─ ☕ OCS in Full (ready for implementation)
├─ 🥗 Fresh Food Tracker (ready for implementation)
├─ 📦 Market Inventory (ready for implementation)
├─ 🗑️ Spoilage/Shrink (ready for implementation)
├─ 🏢 Warehouse Inventory (ready for implementation)
└─ 🎯 Process All Weekly Reports (legacy + future)
```

## Data Flow Examples

### Daily Stockout Report Flow
```
User selects Daily Stockout → Process Report
├─ validate_stockout_prerequisites()
├─ execute_all_queries()
│  ├─ get_lightspeed_connection()
│  ├─ get_level_connection()  
│  ├─ Execute 4 separate SQL queries
│  └─ Merge data with pandas
├─ StockoutExcelProcessor.generate_stockout_report()
│  ├─ Create working copy from template
│  ├─ Populate 4 sheets (Highlights, Markets, NullOrders, OCS)
│  └─ Save as "Daily Stockout Report MM.DD.YY.xlsx"
└─ Return success/failure results
```

### Weekly Report Implementation Flow  
```
User selects Weekly Sales → Process Report
├─ Currently shows "Ready for implementation"
├─ When implemented:
│  ├─ Download sales data from SEED API
│  ├─ Process data with pandas
│  ├─ Generate Excel using excel_processing module
│  └─ Save as "Weekly Sales MM.DD.YY.xlsx"
└─ Return results
```

## How to Extend the System

### Adding a New Daily Report
1. **Create workflow file**: `report_workflows/new_daily_report.py`
2. **Add menu option**: Update `daily_reports.py` 
3. **Add configuration**: Update `config/report_config.py` if needed
4. **Create Excel processor**: Add to `excel_processing/` if needed

### Adding a New Weekly Report  
1. **Use existing skeleton**: Modify `report_workflows/[report_name].py`
2. **Menu already exists**: Weekly reports menu handles all 7 types
3. **Implement workflow**: Replace TODO comments with actual logic

### Adding a New SEED API Report
1. **Add report ID**: `config/report_config.py` → `SEED_REPORTS`
2. **Use downloader**: `utils/downloader.py` functions
3. **Process data**: Create workflow in `report_workflows/`

### Adding New Database Queries
1. **Add function**: `database/queries.py`
2. **Use connections**: `get_lightspeed_connection()` or `get_level_connection()`
3. **Return DataFrame**: Use `execute_query()` helper

## System Status & Health Checks

### Built-in Validation
- Database connectivity testing
- SEED login testing
- Template validation
- Environment variable checking
- **Prerequisites**: Per-report validation functions

### Testing Commands
```bash
# Test database connection
python -c "from database.connection import test_database_connection; print(test_database_connection())"

# Test Excel templates
python -c "from excel_processing.stockout_excel import get_stockout_template_info; print(get_stockout_template_info())"

# Test menu system
python main.py
```

## Performance & Scalability

### Features
- Concurrent downloads (up to 25 API calls)
- Direct SQL Server connections
- Excel template reuse
- Async web automation
- Persistent Firefox profile
- **Clean Resource Management**: Automatic cleanup with async context managers
- **Native Download Handling**: Built-in Playwright download monitoring

### Expandability
- Modular design
- Direct imports
- Consistent patterns
- Skeleton files for weekly reports

## Security & Environment

### Environment Variables
```bash
# Required in .env file
SEED_USERNAME=your_username
SEED_PASSWORD=your_password
```

### Database Security
- **Read-only access**: LSReadOnly user with limited permissions
- **Timeout controls**: Connection and query timeouts configured
- **Clean connections**: Automatic connection cleanup

### Best Practices
- **No hardcoded credentials**: Environment-based authentication
- **Input validation**: SQL injection prevention
- **Resource cleanup**: Proper browser and database session management

---

**Monumator v1.0** - Streamlined, Modular, Arrow-Navigated Report Automation  
Built for Monumental Markets - Optimized for Growth and Maintainability