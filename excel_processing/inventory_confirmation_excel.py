"""
Inventory Confirmation Excel Processing
========================================

Generates Excel reports for inventory confirmation data using template.
"""

import os
import shutil
import pandas as pd
from datetime import datetime
import xlwings as xw
from excel_processing.base_excel import ExcelProcessorBase

class InventoryConfirmationProcessor(ExcelProcessorBase):
    """Excel processor for inventory confirmation reports"""
    
    def __init__(self):
        """Initialize with the Daily Inventory Confirmation template"""
        template_path = os.path.join("templates", "Daily Inventory Confirmation.xlsx")
        super().__init__(template_path)
    
    def generate_report(self, route_data: list) -> str:
        """
        Generate inventory confirmation report using template
        
        Args:
            route_data: List of route data with incomplete assets
            output_directory: Directory to save the report
            
        Returns:
            Path to generated Excel file
        """
        # Create working copy of template
        output_path = self.create_working_copy("downloads/daily", "Daily Inventory Confirmation")
        
        # Prepare data for Excel - matching template columns exactly
        all_assets = []
        
        for route in route_data:
            for asset in route.get('incomplete_assets', []):
                all_assets.append({
                    'Asset ID': asset.get('asset_id', ''),
                    'Location / Place': asset.get('location', ''),
                    'Type': asset.get('type', ''),
                    'Restock Time': asset.get('restock_time', ''),
                    "Inventory Req'd/Taken": asset.get('inventory_taken', 'YES/NO')
                })
        
        if all_assets:
            # Open with xlwings
            app = xw.App(visible=False)
            wb = app.books.open(output_path)
            ws = wb.sheets.active
            
            # Start writing data from row 2 (after headers)
            start_row = 2
            
            for idx, asset in enumerate(all_assets, start=start_row):
                ws.range(f'A{idx}').value = asset['Asset ID']
                ws.range(f'B{idx}').value = asset['Location / Place'] 
                ws.range(f'C{idx}').value = asset['Type']
                ws.range(f'D{idx}').value = asset['Restock Time']
                ws.range(f'E{idx}').value = asset["Inventory Req'd/Taken"]
            
            # Force recalculation
            app.calculate()
            
            wb.save()
            wb.close()
            app.quit()
        
        print(f"📁 Generated Excel report: {output_path}")
        
        return output_path

def generate_inventory_confirmation_report(route_data: list) -> str:
    """
    Convenience function for generating inventory confirmation report
    
    Args:
        route_data: List of route data with incomplete assets
        output_directory: Directory to save the report
        
    Returns:
        Path to generated Excel file
    """
    processor = InventoryConfirmationProcessor()
    return processor.generate_report(route_data)