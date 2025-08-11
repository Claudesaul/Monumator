# Monumator

Automation system for Monumental Markets that generates business reports from SEED (Cantaloupe) and SQL Server databases.


## 📁 Project Structure

```
Monumator/
├── config/                    # Configuration settings (direct imports)
│   ├── database_config.py     # Database connections
│   └── report_config.py       # API settings and report IDs
├── database/                  # Database operations (direct imports)
│   ├── connection.py          # Database connection management
│   └── queries.py             # SQL queries and data processing
├── excel_processing/          # Excel report generation (direct imports)
│   ├── base_excel.py          # Common Excel utilities
│   ├── stockout_excel.py      # Daily stockout reports (openpyxl)
│   └── inventory_excel.py     # Inventory reports (xlwings)
├── web_automation/            # Async Playwright Firefox automation (direct imports)
│   ├── base_scraper.py        # Async Firefox browser setup
│   ├── seed_browser.py        # Async SEED login/navigation
│   ├── inventory_confirmation_scraper.py   # Async route inventory confirmation
│   ├── items_scraper.py       # Async item export downloads
│   └── firefox_profile/       # Persistent Firefox profile
├── report_workflows/          # Complete report workflows (direct imports)
│   ├── daily_stockout.py      # Daily stockout workflow
│   ├── inventory_adjustment.py # Inventory adjustment workflow
│   ├── inventory_confirmation.py # Confirmation report workflow
│   ├── weekly_sales.py        # Weekly sales workflow
│   ├── oos_tracker.py         # OOS tracker workflow
│   ├── ocs_in_full.py         # OCS in full workflow
│   ├── fresh_food_tracker.py  # Fresh food tracker workflow
│   ├── market_inventory.py    # Market inventory workflow
│   ├── spoilage_shrink.py     # Spoilage/shrink workflow
│   └── warehouse_inventory.py # Warehouse inventory workflow
├── utils/                     # Utilities (direct imports)
│   ├── downloader.py          # SEED API downloads
│   └── menu_navigator.py      # Arrow-key menu navigation
├── reports/                   # Report menu systems (direct imports)
│   ├── daily_reports.py       # Daily reports menu
│   └── weekly_reports.py      # Weekly reports menu
├── templates/                 # Excel templates
└── main.py                    # Main menu
```

## 🛠️ Installation

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Claudesaul/Monumator
   cd Monumator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install firefox
   ```

3. **Configure environment variables**
   Create `.env` file:
   ```
   SEED_USERNAME=your_username
   SEED_PASSWORD=your_password
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   ```

4. **Configure database**
   System uses direct SQL Server connections to LightSpeed and Level databases

## 🚀 Usage

### Quick Start
```bash
# Main menu with arrow navigation
python main.py
```

### Navigation
- **Use ↑↓ arrow keys** to navigate menus
- **Enter** to select an option
- **Q** to quit/exit

### Main Menu Options
- **📅 Weekly Reports** - Access 7 specialized weekly reports with sub-menus
- **📊 Daily Reports** - Access daily processing with sub-menus
- **📁 Download Directories** - View file organization  
- **🔍 System Status** - Quick system health check
- **🚪 Exit**

### Daily Reports Sub-Menus

**📈 Daily Stockout Report**
- Process Report (live database data)
- Use Sample Data (for testing)

**📋 Inventory Adjustment Summary**  
- Process Report (auto-downloads IAD + product list)
- Check Date Logic (Monday = Friday data, else previous day)

**🌐 Inventory Confirmation Report**
- Run Web Scraper (Headless) - production mode
- Run Web Scraper (Visible) - debugging mode

**Plus:**
- **🔗 Test Database Connection** - Quick database connectivity test

### Weekly Reports Sub-Menus

**📈 Weekly Sales**
- Process Report (revenue & sales analysis)
- Check Configuration

**📊 OOS Tracker**  
- Process Report (out-of-stock tracking)
- Check Configuration

**☕ OCS in Full**
- Process Report (office coffee service analysis)
- Check Configuration

**🥗 Fresh Food Tracker**
- Process Report (fresh food inventory & sales)
- Check Configuration

**📦 Market Inventory**
- Process Report (market-level inventory analysis)
- Check Configuration

**🗑️ Spoilage/Shrink**
- Process Report (product shrink & spoilage tracking)
- Check Configuration

**🏢 Warehouse Inventory**
- Process Report (warehouse inventory management)
- Check Configuration




## 🎯 Adding New Features

### Adding New Reports
Each module has a detailed README with examples:
- [Database Module](database/README.md) - Adding new queries
- [Excel Processing](excel_processing/README.md) - Adding new Excel reports
- [Web Automation](web_automation/README.md) - Adding new scrapers
- [Report Workflows](report_workflows/README.md) - Creating complete workflows

### Quick Examples

**New Database Query:**
```python
# In database/queries.py
def get_new_analysis_data():
    query = "SELECT product, quantity FROM dbo.ItemView WHERE..."
    # Implementation here
```

**New Excel Report:**
```python
# In excel_processing/new_report_excel.py
from .base_excel import ExcelProcessorBase

class NewReportProcessor(ExcelProcessorBase):
    def generate_new_report(self, data):
        # Implementation here
```

**New Web Scraper:**
```python
# In web_automation/new_scraper.py
from .base_scraper import BaseScraper
from .seed_browser import SeedBrowser

class NewScraper(BaseScraper):
    def scrape_new_data(self):
        # SEED login handled automatically
        # Implementation here
```

## 🗃️ File Organization

### Download Directories
- **`downloads/weekly/`** - Weekly report files
- **`downloads/daily/`** - Daily reports and processed outputs
- **`downloads/temp/`** - Temporary files (auto-cleanup)

### File Naming
- Weekly: `weekly_sales_market.xlsx`
- Daily: `daily_fill_oos.xlsx`  
- Processed: `Daily Stockout Report 08.02.25.xlsx`

## ⚙️ Configuration

### Report IDs
Edit `config/report_config.py` to add new reports:
```python
SEED_REPORTS = {
    "existing_report": "33105",
    "new_report": "NEW_ID"  # Add here
}
```

### Database Settings
Database credentials are securely stored in `.env` file:
```python
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
```

### Download Settings
```python
MAX_CONCURRENT_DOWNLOADS = 25  # Adjust as needed
```

## 🔍 System Status

### Health Checks
System status checking:
- Template files
- Database connections
- SEED login
- Environment variables

### Testing
```bash
# Test database connection
python -c "from database.connection import test_database_connection; print(test_database_connection())"

# Test Excel templates
python -c "from excel_processing.stockout_excel import get_stockout_template_info; print(get_stockout_template_info())"

# Test SEED credentials
python -c "from utils.downloader import get_seed_credentials; print(bool(get_seed_credentials()[0]))"
```

## 🛡️ Error Handling

- Sample data fallback
- Automatic retries
- Error logging
- Resource cleanup
- Prerequisites validation

## ✨ Features

- Concurrent API downloads
- Database query operations
- Excel template processing
- Headless web automation
- Resource cleanup

## 🔒 Security

- Environment variables for credentials
- Read-only database access
- Input validation
- API authentication

## 📦 Dependencies

```
requests
pandas
python-dotenv
pyodbc
openpyxl
xlwings
playwright
```

### System Requirements
- SQL Server access
- Firefox browser
- Excel application


## 🤝 Contributing

1. **Read Module READMEs**: Each module has detailed documentation
2. **Follow Patterns**: Use existing error handling and result formats
3. **Add Tests**: Include validation for new features
4. **Update Documentation**: Keep READMEs current

## 📞 Support

### Troubleshooting
- Check module-specific READMEs for detailed guidance
- Verify `.env` file has correct credentials
- Ensure all dependencies are installed
- Run system status check for comprehensive diagnostics

### Common Issues
- **Database Connection**: Ensure VPN connection to access SQL Server at 10.216.207.32
- **Web Scraping**: Check Firefox browser and internet connectivity
- **Permissions**: Verify file write permissions in download directories

---

**Monumator v1.0** - Streamlined, Modular, Expandable Report Automation  
Built for Monumental Markets - Optimized for Growth  
**Designed by Claude Belizaire**
