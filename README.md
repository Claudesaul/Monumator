# Monumator

A streamlined automation system for Monumental Markets that integrates with SEED (Cantaloupe) and Lightspeed to generate comprehensive reports. Built with a modular, expandable architecture for easy maintenance and feature additions.


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
├── web_automation/            # Browser automation (direct imports)
│   ├── base_scraper.py        # Common browser setup
│   ├── seed_browser.py        # SEED login/navigation
│   ├── inventory_scraper.py   # Inventory confirmation scraping
│   └── product_scraper.py     # Product list downloads
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
├── templates/                 # Excel templates
├── main.py                    # Main menu
├── daily_reports.py           # Daily reports menu
└── weekly_reports.py          # Weekly reports menu
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Microsoft Edge browser (for web scraping)
- Excel (for inventory adjustment reports)
- Lightspeed ODBC DSN configured

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Monumator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
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
   Ensure Lightspeed ODBC DSN is set up on your system

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
The system includes comprehensive status checking:
- Template file availability
- Database connectivity
- Download directory structure
- Selenium dependencies
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

- **Graceful Degradation**: Sample data fallback when database unavailable
- **Retry Logic**: Automatic retries for failed operations
- **Comprehensive Logging**: Detailed error messages with context
- **Resource Cleanup**: Automatic cleanup of browser sessions and temp files
- **Validation**: Prerequisites checking before processing

## 📈 Performance

- **Concurrent Downloads**: Up to 25 simultaneous API downloads
- **Optimized Queries**: Efficient database operations
- **Template Caching**: Reused Excel templates
- **Headless Automation**: Faster web scraping in production
- **Memory Management**: Proper resource cleanup

## 🔒 Security

- **Environment Variables**: Credentials stored securely in `.env`
- **Read-only Database**: Limited database permissions
- **Input Validation**: SQL injection prevention
- **Secure Authentication**: Base64 encoded API authentication

## 📋 Dependencies

### Core Dependencies
```
requests>=2.25.1          # HTTP requests and API calls
pandas>=1.3.0             # Data manipulation
python-dotenv>=0.19.0     # Environment variables
pyodbc>=4.0.35            # Database connectivity
openpyxl>=3.1.0           # Excel operations
xlwings>=0.30.0           # Excel automation
selenium>=4.0.0           # Browser automation
```

### System Requirements
- **ODBC DSN**: Lightspeed database connection
- **Microsoft Edge**: Browser for automation
- **Excel**: Required for xlwings operations


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
- **Database Connection**: If accessing remotely, ensure Monumental Markets VPN is connected, verify ODBC DSN configuration
- **Web Scraping**: Check Edge browser and internet connectivity
- **Permissions**: Verify file write permissions in download directories

---

**Monumator v1.0** - Streamlined, Modular, Expandable Report Automation  
Built for Monumental Markets - Optimized for Growth  
**Designed by Claude Belizaire**