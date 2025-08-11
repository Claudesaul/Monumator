# 📈 Excel Processing Module

Handles Excel report generation using templates with openpyxl and xlwings.

## 📄 Files

- **`base_excel.py`** - Common template management functions
- **`stockout_excel.py`** - Daily stockout reports (openpyxl)
- **`inventory_adjustment_excel.py`** - Inventory adjustment reports (xlwings)
- **`inventory_confirmation_excel.py`** - Inventory confirmation reports (xlwings)

## ⚙️ How It Works

Creates Excel reports by copying templates and filling with data:
- **openpyxl** - Simple data insertion, template preservation
- **xlwings** - Complex formulas, Excel automation

## 🚀 Usage

### Stockout Report (openpyxl)
```python
from excel_processing.stockout_excel import StockoutExcelProcessor

processor = StockoutExcelProcessor()
data_dict = {
    'highlights': highlights_df,
    'markets': markets_df,
    'null_orders': null_orders_df,
    'ocs': ocs_df
}
output_path = processor.generate_stockout_report(data_dict)
```

### Inventory Adjustment Report (xlwings)
```python
from excel_processing.inventory_adjustment_excel import InventoryExcelProcessor

processor = InventoryExcelProcessor()
output_path = processor.generate_inventory_adjustment_report(iad_data_df, product_list_df)
```

### Inventory Confirmation Report (xlwings)
```python
from excel_processing.inventory_confirmation_excel import InventoryConfirmationProcessor

processor = InventoryConfirmationProcessor()
route_data = [{'incomplete_assets': [{'asset_id': '123', 'location': 'Market A', ...}]}]
output_path = processor.generate_report(route_data)
```

## ➕ Adding New Report Processors

### Step 1: Create New Processor
Create `new_report_excel.py`:
```python
from .base_excel import ExcelProcessorBase
from openpyxl import load_workbook

class NewReportExcelProcessor(ExcelProcessorBase):
    def __init__(self, template_path="templates/New Report Template.xlsx"):
        super().__init__(template_path)
        
    def generate_new_report(self, data_df, output_directory="downloads/daily"):
        # Create working copy
        self.create_working_copy(output_directory, "New Report")
        
        # Load and populate
        workbook = load_workbook(self.output_path)
        # Add data insertion logic here
        workbook.save(self.output_path)
        
        return self.output_path
```

### Step 2: Use in Workflow
```python
from excel_processing.new_report_excel import NewReportExcelProcessor

processor = NewReportExcelProcessor()
output_path = processor.generate_new_report(data_df)
```

## 📋 Templates

Place Excel templates in `templates/` folder:
- `Daily Stockout Report.xlsx` - 4 sheets for stockout data
- `Inventory Adjustment Summary.xlsx` - 2 sheets for inventory
- `Daily Inventory Confirmation.xlsx` - Route asset tracking with UNIQUE formulas
- Headers in row 1, data starts row 2

## 📚 Library Choice

- **openpyxl** - Template preservation, simple data filling
- **xlwings** - Complex formulas (XLOOKUP), requires Excel installed

## File Naming

Generated files: `{Report Name} {MM.DD.YY}.xlsx`