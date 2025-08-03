# Report Workflows Module

This module contains complete end-to-end workflows for generating reports. Each workflow orchestrates the entire process from data acquisition to final report generation.

## What This Module Contains

**Daily Reports:**
- **`daily_stockout.py`** - Complete Daily Stockout Report workflow
- **`inventory_adjustment.py`** - Complete Inventory Adjustment Summary workflow  
- **`inventory_confirmation.py`** - Complete Inventory Confirmation Report workflow

**Weekly Reports:**
- **`weekly_reports.py`** - Legacy weekly reports download workflow
- **`weekly_sales.py`** - Weekly sales workflow (ready for implementation)
- **`oos_tracker.py`** - OOS tracker workflow (ready for implementation)
- **`ocs_in_full.py`** - OCS in full workflow (ready for implementation)
- **`fresh_food_tracker.py`** - Fresh food tracker workflow (ready for implementation)
- **`market_inventory.py`** - Market inventory workflow (ready for implementation)
- **`spoilage_shrink.py`** - Spoilage/shrink workflow (ready for implementation)
- **`warehouse_inventory.py`** - Warehouse inventory workflow (ready for implementation)

## Purpose

Provides high-level orchestration of complete report generation processes by coordinating:
- **Data acquisition** (database queries, API downloads, web scraping)
- **Data processing** (cleaning, validation, transformation)
- **Report generation** (Excel file creation)
- **Error handling and recovery**

## Quick Reference

**Main Workflow Files:**
- All workflows follow the same pattern: `validate_prerequisites() → process_report() → get_status()`
- Daily workflows are fully implemented and functional
- Weekly workflows are prepared for implementation with skeleton code

**Direct imports** - No package structure:
```python
from report_workflows.daily_stockout import process_stockout_report
from report_workflows.inventory_adjustment import process_inventory_adjustment_summary
from report_workflows.weekly_sales import process_weekly_sales_report
```

## Key Features

- **Complete Workflows**: End-to-end report generation
- **Error Recovery**: Graceful handling of failures at each step
- **Status Reporting**: Detailed progress and result information
- **Flexible Data Sources**: Database, API, and web scraping support
- **Validation**: Prerequisites checking before processing

## How It Works

Each workflow follows a consistent pattern:
1. **Prerequisites Validation** - Check templates, database, credentials
2. **Data Acquisition** - Fetch data from appropriate sources
3. **Data Processing** - Clean and validate the data
4. **Report Generation** - Create Excel files using templates
5. **Cleanup** - Remove temporary files and close connections

## Usage Examples

### Daily Stockout Report
```python
from report_workflows.daily_stockout import process_stockout_report

# Generate stockout report from database
results = process_stockout_report(use_sample_data=False)

if results['success']:
    print(f"Report generated: {results['output_path']}")
    print(f"Processing time: {results['processing_time']:.2f} seconds")
    print(f"Data summary: {results['data_summary']}")
else:
    print(f"Report failed: {results['error']}")

# Use sample data for testing
test_results = process_stockout_report(use_sample_data=True)
```

### Inventory Adjustment Summary
```python
from report_workflows.inventory_adjustment import process_inventory_adjustment_summary

# Generate inventory adjustment report
results = process_inventory_adjustment_summary()

if results['success']:
    print(f"Report generated: {results['output_path']}")
    print(f"Report ID used: {results['report_id']} - {results['description']}")
    print(f"Data summary: {results['data_summary']}")
else:
    print(f"Report failed: {results['error']}")
```

### Inventory Confirmation Report
```python
from report_workflows.inventory_confirmation import process_inventory_confirmation_report

# Generate inventory confirmation report via web scraping
results = process_inventory_confirmation_report(headless=True)

if results['success']:
    print(f"Report generated: {results['excel_file']}")
    print(f"Routes found: {results['routes_found']}")
    print(f"Assets processed: {results['assets_processed']}")
else:
    print(f"Report failed: {results['error']}")
```

### Weekly Reports
```python
from report_workflows.weekly_reports import process_weekly_reports

# Download all weekly reports
successful, failed = process_weekly_reports()
print(f"Downloaded {len(successful)} reports, {len(failed)} failed")
```

## Adding New Report Workflows

### Step 1: Create New Workflow File
Create `new_report.py`:

```python
"""
New Report Workflow
==================

Complete workflow for generating new reports.
"""

import time
from datetime import datetime

def validate_new_report_prerequisites():
    """
    Validate prerequisites for new report generation
    
    Returns:
        dict: Validation results
    """
    validation_results = {
        'template_exists': False,
        'data_source_available': False,
        'all_valid': False
    }
    
    # Check template file
    import os
    template_path = "templates/New Report Template.xlsx"
    validation_results['template_exists'] = os.path.exists(template_path)
    
    # Check data source (database, API, etc.)
    try:
        # Your data source validation logic here
        validation_results['data_source_available'] = True
    except:
        validation_results['data_source_available'] = False
    
    # Overall validation
    validation_results['all_valid'] = all(validation_results.values())
    
    if validation_results['all_valid']:
        print("✅ New report prerequisites validated")
    else:
        print("❌ New report prerequisites validation failed")
    
    return validation_results

def fetch_new_report_data():
    """
    Fetch data for new report
    
    Returns:
        pandas.DataFrame: Report data
    """
    print("📊 Fetching new report data...")
    
    # Your data acquisition logic here
    # Could be database queries, API calls, web scraping, etc.
    
    try:
        # Example: Database query
        from database.connection import get_lightspeed_connection, execute_query
        
        query = """
        SELECT product, quantity, location
        FROM dbo.ItemView 
        WHERE orderDate = '{today}'
        """
        
        conn = get_lightspeed_connection()
        today = datetime.now().date()
        query_formatted = query.format(today=today)
        data = execute_query(conn, query_formatted)
        conn.close()
        
        print(f"📋 Fetched {len(data)} records")
        return data
        
    except Exception as e:
        print(f"❌ Data fetch failed: {str(e)}")
        raise

def process_new_report_data(raw_data):
    """
    Process and validate new report data
    
    Args:
        raw_data (pandas.DataFrame): Raw data
        
    Returns:
        pandas.DataFrame: Processed data
    """
    print("🔄 Processing new report data...")
    
    # Data cleaning and processing
    processed_data = raw_data.fillna('')  # Replace NaN values
    
    # Additional processing logic here
    # Filtering, calculations, aggregations, etc.
    
    print(f"✅ Processed {len(processed_data)} records")
    return processed_data

def generate_new_report_excel(data, output_directory="downloads/daily"):
    """
    Generate Excel report from processed data
    
    Args:
        data (pandas.DataFrame): Processed data
        output_directory (str): Output directory
        
    Returns:
        str: Path to generated Excel file
    """
    print("📄 Generating new report Excel file...")
    
    # Use appropriate Excel processor
    from excel_processing.base_excel import ExcelProcessorBase
    # or create specific processor in excel_processing module
    
    # Excel generation logic here
    output_path = f"{output_directory}/New Report {datetime.now().strftime('%m.%d.%y')}.xlsx"
    
    # Save data to Excel (simplified example)
    data.to_excel(output_path, index=False)
    
    print(f"📊 Generated Excel file: {output_path}")
    return output_path

def process_new_report(output_directory="downloads/daily"):
    """
    Complete workflow for processing new report
    
    Args:
        output_directory (str): Directory to save the report
        
    Returns:
        dict: Results dictionary with success status and details
    """
    start_time = time.time()
    
    try:
        print("🚀 Starting new report processing...")
        
        # Step 1: Validate prerequisites
        validation = validate_new_report_prerequisites()
        
        if not validation['all_valid']:
            raise Exception("Prerequisites validation failed")
        
        # Step 2: Fetch data
        raw_data = fetch_new_report_data()
        
        if raw_data is None or raw_data.empty:
            raise Exception("No data retrieved")
        
        # Step 3: Process data
        processed_data = process_new_report_data(raw_data)
        
        # Step 4: Generate Excel report
        output_path = generate_new_report_excel(processed_data, output_directory)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare results
        results = {
            'success': True,
            'output_path': output_path,
            'processing_time': processing_time,
            'data_summary': {
                'rows': len(processed_data),
                'columns': len(processed_data.columns) if hasattr(processed_data, 'columns') else 0
            },
            'validation': validation
        }
        
        print(f"✅ New report completed successfully in {processing_time:.2f} seconds")
        print(f"📁 Output file: {output_path}")
        
        return results
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ New report failed: {str(e)}")
        
        return {
            'success': False,
            'error': str(e),
            'processing_time': processing_time
        }

def get_new_report_status():
    """
    Get current status of new report processing capabilities
    
    Returns:
        dict: Status information
    """
    validation = validate_new_report_prerequisites()
    
    status = {
        'ready_for_processing': validation['all_valid'],
        'template_exists': validation['template_exists'],
        'data_source_available': validation['data_source_available'],
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return status
```

### Step 2: Add to Menu System
Update `../daily_reports.py` to include new report option:

```python
# Add menu option
print("11. 🆕 Process New Report")

# Add handling in main loop
elif choice == 11:  # Process New Report
    print("\n🚀 Starting New Report Processing...")
    from report_workflows.new_report import process_new_report
    results = process_new_report()
    
    if results['success']:
        print(f"✅ New Report completed successfully!")
        print(f"📁 Output file: {results['output_path']}")
    else:
        print(f"❌ New Report failed: {results['error']}")
```

### Step 3: Add Status Checking
Update status function to include new report:

```python
# In show_daily_reports_status()
from report_workflows.new_report import get_new_report_status

new_report_status = get_new_report_status()
print(f"   • New Report: {'✅' if new_report_status['ready_for_processing'] else '❌'}")
```

## Workflow Design Patterns

### Standard Result Format
All workflows return results in this format:
```python
{
    'success': True/False,
    'output_path': 'path/to/generated/file.xlsx',  # if successful
    'processing_time': 45.2,  # seconds
    'error': 'Error message',  # if failed
    'data_summary': {  # additional info if relevant
        'rows': 100,
        'columns': 10
    }
}
```

### Error Handling Pattern
```python
try:
    # Main processing logic
    result = perform_operation()
    return {'success': True, 'data': result}
except Exception as e:
    print(f"❌ Operation failed: {str(e)}")
    return {'success': False, 'error': str(e)}
finally:
    # Cleanup resources
    cleanup_resources()
```

### Prerequisites Validation Pattern
```python
def validate_prerequisites():
    validation = {
        'template_exists': check_template(),
        'database_connected': check_database(),
        'credentials_available': check_credentials(),
        'all_valid': False
    }
    validation['all_valid'] = all(validation.values())
    return validation
```

## Integration Points

### Database Module
```python
from database.queries import execute_all_queries, get_sample_data
from database.connection import test_database_connection
```

### Excel Processing Module
```python
from excel_processing.stockout_excel import StockoutExcelProcessor
from excel_processing.inventory_excel import InventoryExcelProcessor
```

### Web Automation Module
```python
from web_automation.inventory_scraper import run_inventory_confirmation_scraper
from web_automation.product_scraper import download_product_list_with_browser
```

### Utils Module
```python
from utils.downloader import download_seed_report, download_multiple_reports_concurrent
```

## Testing Workflows

### Individual Workflow Testing
```bash
cd /path/to/Monumator
python -c "from report_workflows.daily_stockout import process_stockout_report; print(process_stockout_report(use_sample_data=True))"
```

### Status Checking
```bash
python -c "from report_workflows.daily_stockout import get_stockout_processing_status; print(get_stockout_processing_status())"
```

## Dependencies

- **Database modules** - For data queries
- **Excel processing modules** - For report generation
- **Web automation modules** - For web scraping
- **Utils modules** - For downloads and file management
- **Config modules** - For settings and configuration