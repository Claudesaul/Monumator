# Excel Processing Module

This module handles all Excel report generation with template preservation and complex formula application.

## What This Module Contains

- **`base_excel.py`** - Common Excel functionality and template management
- **`stockout_excel.py`** - Daily Stockout Report processing (openpyxl)
- **`inventory_excel.py`** - Inventory Adjustment Report processing (xlwings)

## Purpose

Provides unified Excel processing capabilities while supporting different libraries for different needs:
- **openpyxl**: Template preservation, simple data insertion
- **xlwings**: Complex formulas, Excel automation, pivot tables

## Quick Reference

**Main Excel Files:**
- `base_excel.py` - Common template and file management functions
- `stockout_excel.py` - Daily stockout reports (uses openpyxl)
- `inventory_excel.py` - Inventory adjustment reports (uses xlwings)

**Direct imports** - No package structure:
```python
from excel_processing.stockout_excel import StockoutExcelProcessor
from excel_processing.inventory_excel import InventoryExcelProcessor
from excel_processing.base_excel import ExcelProcessorBase
```

## Key Features

- **Template Management**: Automatic template copying and date formatting
- **Dual Library Support**: openpyxl and xlwings for different use cases
- **Formula Application**: Complex XLOOKUP formulas for inventory reports
- **Error Handling**: Comprehensive error handling with cleanup
- **Unified Interface**: Consistent API across different Excel operations

## How It Works

1. **Base Class**: `ExcelProcessorBase` provides common functionality
2. **Specialized Processors**: Specific implementations for different report types
3. **Template Copying**: Creates dated working copies of templates
4. **Data Insertion**: Efficient DataFrame to Excel conversion
5. **Formula Processing**: Applies complex formulas where needed

## Usage Examples

### Daily Stockout Report (openpyxl)
```python
from excel_processing.stockout_excel import StockoutExcelProcessor

# Create processor
processor = StockoutExcelProcessor()

# Generate report
data_dict = {
    'highlights': highlights_df,
    'markets': markets_df,
    'null_orders': null_orders_df,
    'ocs': ocs_df
}

output_path = processor.generate_stockout_report(data_dict)
print(f"Report generated: {output_path}")
```

### Inventory Adjustment Report (xlwings)
```python
from excel_processing.inventory_excel import InventoryExcelProcessor

# Create processor
processor = InventoryExcelProcessor()

# Generate report with formulas
output_path = processor.generate_inventory_adjustment_report(
    iad_data_df, 
    product_list_df
)
print(f"Report generated: {output_path}")
```

### Check Template Status
```python
from excel_processing.stockout_excel import get_stockout_template_info
from excel_processing.inventory_excel import get_inventory_template_info

# Check if templates exist
stockout_info = get_stockout_template_info()
inventory_info = get_inventory_template_info()

print(f"Stockout template exists: {stockout_info['exists']}")
print(f"Inventory template exists: {inventory_info['exists']}")
```

## Adding New Excel Reports

### Step 1: Create New Processor
Create `new_report_excel.py`:

```python
from .base_excel import ExcelProcessorBase
import pandas as pd
from openpyxl import load_workbook  # or xlwings as xw

class NewReportExcelProcessor(ExcelProcessorBase):
    """
    Processes New Report Excel files
    """
    
    def __init__(self, template_path="templates/New Report Template.xlsx"):
        super().__init__(template_path)
        self.workbook = None
        
    def load_workbook(self):
        """Load workbook with appropriate library"""
        if not self.output_path:
            raise FileNotFoundError("Working copy not found. Call create_working_copy() first.")
        
        # Use openpyxl for simple reports
        self.workbook = load_workbook(self.output_path)
        return self.workbook
        
        # OR use xlwings for complex reports
        # self.app = xw.App(visible=False)
        # self.workbook = self.app.books.open(self.output_path)
        # return self.workbook
    
    def populate_data(self, data_df):
        """Insert data into Excel"""
        # Your data insertion logic here
        pass
    
    def generate_new_report(self, data_df, output_directory="downloads/daily"):
        """
        Complete workflow for new report generation
        """
        try:
            # Create working copy
            self.create_working_copy(output_directory, "New Report")
            
            # Load workbook
            self.load_workbook()
            
            # Populate data
            self.populate_data(data_df)
            
            # Save (method depends on library used)
            return self.save_workbook()  # or self.save_and_close_workbook()
            
        except Exception as e:
            print(f"❌ Failed to generate new report: {str(e)}")
            raise

def get_new_report_template_info():
    """Get template information"""
    processor = NewReportExcelProcessor()
    return processor.get_template_info()
```

### Step 2: Update Workflow
Add to `../report_workflows/new_report.py`:

```python
from excel_processing.new_report_excel import NewReportExcelProcessor

def generate_new_report_excel(data_df, output_directory="downloads/daily"):
    processor = NewReportExcelProcessor()
    return processor.generate_new_report(data_df, output_directory)
```

## Template Requirements

### Template File Structure
Templates should be placed in `../templates/` directory:
- `Daily Stockout Report.xlsx` - 4 sheets (Highlights, Markets, NullOrders, OCS)
- `Inventory Adjustment Summary.xlsx` - 2 sheets (Seed IAD, Seed Product List)
- `Daily Inventory SEED.xlsx` - Inventory confirmation template

### Template Guidelines
1. **Headers**: First row should contain column headers
2. **Data Area**: Data starts from row 2
3. **Formatting**: Use Excel formatting for appearance
4. **Formulas**: Place template formulas in row 2 for xlwings processors

## Library Comparison

### When to Use openpyxl
- ✅ Template preservation important
- ✅ Simple data insertion
- ✅ No complex formulas needed
- ✅ File-based operations
- ✅ Better performance for large datasets

### When to Use xlwings
- ✅ Complex formulas required (XLOOKUP, etc.)
- ✅ Excel automation needed
- ✅ Pivot tables, charts
- ✅ Macro execution
- ⚠️ Requires Excel application installed

## File Naming Convention

Generated files follow this pattern:
- `{Report Name} {MM.DD.YY}.xlsx`
- Example: `Daily Stockout Report 08.02.25.xlsx`

## Error Handling Patterns

```python
try:
    # Excel operations
    result = processor.generate_report(data)
    return result
except Exception as e:
    print(f"❌ Excel processing failed: {str(e)}")
    # Cleanup resources
    if hasattr(processor, 'workbook') and processor.workbook:
        processor.workbook.close()
    if hasattr(processor, 'app') and processor.app:
        processor.app.quit()
    raise
```

## Dependencies

- `openpyxl` - Excel file operations without Excel application
- `xlwings` - Excel automation (requires Excel installed)
- `pandas` - Data manipulation
- `datetime` - Date formatting for filenames
- `os`, `shutil` - File operations

## Testing

Test Excel processing:
```bash
cd /path/to/Monumator
python -c "from excel_processing.stockout_excel import get_stockout_template_info; print(get_stockout_template_info())"
```