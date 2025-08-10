# 🔄 Report Workflows Module

Contains complete end-to-end workflows for generating reports from data acquisition to Excel output.

## 📄 Files

**Daily Reports (Implemented):**
- **`daily_stockout.py`** - Daily stockout report from database
- **`inventory_adjustment.py`** - Inventory adjustment summary with smart date logic
- **`inventory_confirmation.py`** - Inventory confirmation via web scraping

**Weekly Reports:**
- **`weekly_reports.py`** - Legacy weekly downloads (implemented)
- **`weekly_sales.py`** - Weekly sales (skeleton ready)
- **`oos_tracker.py`** - OOS tracker (skeleton ready)
- **`ocs_in_full.py`** - OCS analysis (skeleton ready)
- **`fresh_food_tracker.py`** - Fresh food tracking (skeleton ready)
- **`market_inventory.py`** - Market inventory (skeleton ready)
- **`spoilage_shrink.py`** - Spoilage tracking (skeleton ready)
- **`warehouse_inventory.py`** - Warehouse inventory (skeleton ready)

## ⚙️ How It Works

Each workflow follows the same pattern:
1. **Validate prerequisites** - Check templates, database, credentials
2. **Fetch data** - Database queries, API downloads, or web scraping
3. **Process data** - Clean and transform data
4. **Generate Excel** - Create reports using templates
5. **Return results** - Status and file paths

## 🚀 Usage

### Daily Stockout Report
```python
from report_workflows.daily_stockout import process_stockout_report

# From database
results = process_stockout_report(use_sample_data=False)

# With sample data for testing
results = process_stockout_report(use_sample_data=True)

if results['success']:
    print(f"Report: {results['output_path']}")
```

### Inventory Adjustment Summary
```python
from report_workflows.inventory_adjustment import process_inventory_adjustment_summary

results = process_inventory_adjustment_summary()
if results['success']:
    print(f"Report: {results['output_path']}")
```

### Inventory Confirmation (Web Scraping)
```python
from report_workflows.inventory_confirmation import process_inventory_confirmation_report

results = process_inventory_confirmation_report(headless=True)
if results['success']:
    print(f"Routes found: {results['routes_found']}")
```

## ➕ Adding New Workflows

### Step 1: Create Workflow File
Create `new_report.py`:
```python
import time
from datetime import datetime

def validate_new_report_prerequisites():
    """Check template and data source availability"""
    import os
    validation = {
        'template_exists': os.path.exists("templates/New Report Template.xlsx"),
        'data_source_available': True,  # Your validation logic
        'all_valid': False
    }
    validation['all_valid'] = all([validation['template_exists'], validation['data_source_available']])
    return validation

def process_new_report(output_directory="downloads/daily"):
    """Complete workflow for new report"""
    start_time = time.time()
    
    try:
        # Validate prerequisites
        validation = validate_new_report_prerequisites()
        if not validation['all_valid']:
            raise Exception("Prerequisites validation failed")
        
        # Fetch data (database, API, web scraping)
        from database.queries import execute_query
        # Your data acquisition logic here
        
        # Process data
        # Your data processing logic here
        
        # Generate Excel
        from excel_processing.base_excel import ExcelProcessorBase
        # Your Excel generation logic here
        
        return {
            'success': True,
            'output_path': f"{output_directory}/New Report {datetime.now().strftime('%m.%d.%y')}.xlsx",
            'processing_time': time.time() - start_time
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'processing_time': time.time() - start_time
        }

def get_new_report_status():
    """Get status of new report capabilities"""
    validation = validate_new_report_prerequisites()
    return {
        'ready_for_processing': validation['all_valid'],
        'template_exists': validation['template_exists'],
        'data_source_available': validation['data_source_available']
    }
```

### Step 2: Add to Menu System
Update appropriate menu file (e.g., `daily_reports.py`):
```python
# Add menu option
print("11. 🆕 Process New Report")

# Add handling
elif choice == 11:
    from report_workflows.new_report import process_new_report
    results = process_new_report()
    if results['success']:
        print(f"✅ Report completed: {results['output_path']}")
    else:
        print(f"❌ Report failed: {results['error']}")
```

## 📋 Standard Result Format

All workflows return this format:
```python
{
    'success': True/False,
    'output_path': 'path/to/file.xlsx',  # if successful
    'processing_time': 45.2,  # seconds
    'error': 'Error message',  # if failed
    'data_summary': {  # optional additional info
        'rows': 100,
        'columns': 10
    }
}
```

## 🔗 Integration Points

Uses all other modules:
- **database** - For SQL queries and data retrieval
- **excel_processing** - For report generation
- **web_automation** - For SEED website scraping
- **utils** - For downloads and file management
- **config** - For settings and report IDs