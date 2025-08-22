"""
Inventory Adjustment Excel Processing
====================================

Handles Excel generation for Inventory Adjustment Reports using xlwings.
Supports complex formula application and Excel automation.
"""

import pandas as pd
import xlwings as xw
from .base_excel import ExcelProcessorBase

class InventoryExcelProcessor(ExcelProcessorBase):
    """
    Processes Inventory Adjustment Excel files using xlwings
    """
    
    def __init__(self, template_path="templates/Inventory Adjustment Summary.xlsx"):
        """Initialize with Inventory Adjustment template"""
        super().__init__(template_path)
        self.workbook = None
        self.app = None
        
    def load_workbook(self):
        """
        Load the working copy workbook with xlwings
        
        Returns:
            xlwings.Book: Loaded workbook object
        """
        if not self.output_path:
            raise FileNotFoundError("Working copy not found. Call create_working_copy() first.")
        
        try:
            # Start Excel application (hidden)
            self.app = xw.App(visible=False)
            
            # Open workbook
            self.workbook = self.app.books.open(self.output_path)
            return self.workbook
        except Exception as e:
            print(f"❌ Failed to load workbook: {str(e)}")
            if self.app:
                self.app.quit()
            raise
    
    def clear_sheet_data(self, sheet_name, start_row=2):
        """
        Clear data from a sheet while preserving formatting
        
        Args:
            sheet_name (str): Name of the sheet to clear
            start_row (int): Row to start clearing from (preserves headers)
        """
        if not self.workbook:
            raise RuntimeError("Workbook not loaded. Call load_workbook() first.")
        
        try:
            sheet = self.workbook.sheets[sheet_name]
            
            # Find used range and clear data
            used_range = sheet.used_range
            if used_range and used_range.last_cell.row >= start_row:
                clear_range = sheet.range(f"{start_row}:{used_range.last_cell.row}")
                clear_range.clear_contents()
                
        except Exception as e:
            print(f"⚠️ Could not clear sheet '{sheet_name}': {str(e)}")
    
    def insert_dataframe_to_sheet(self, dataframe, sheet_name, start_row=2, start_col=1, show_message=True):
        """
        Insert a pandas DataFrame into a worksheet
        
        Args:
            dataframe (pandas.DataFrame): Data to insert
            sheet_name (str): Name of the target sheet
            start_row (int): Starting row for data insertion
            start_col (int): Starting column for data insertion
            show_message (bool): Whether to show insertion message
        """
        if not self.workbook:
            raise RuntimeError("Workbook not loaded. Call load_workbook() first.")
        
        if dataframe.empty:
            print(f"⚠️ No data to insert into sheet '{sheet_name}'")
            return
        
        try:
            sheet = self.workbook.sheets[sheet_name]
            
            # Insert data using xlwings (more efficient than cell-by-cell)
            target_range = sheet.range((start_row, start_col)).resize(dataframe.shape[0], dataframe.shape[1])
            target_range.value = dataframe.values
            
            if show_message:
                print(f"📊 Inserted {len(dataframe)} rows into sheet '{sheet_name}'")
        except Exception as e:
            print(f"❌ Failed to insert data into sheet '{sheet_name}': {str(e)}")
    
    def copy_formulas_down(self, sheet_name, num_rows):
        """
        Copy formulas down for the specified number of rows using batch operations
        
        Args:
            sheet_name (str): Name of the sheet
            num_rows (int): Number of data rows to copy formulas for
        """
        if not self.workbook:
            raise RuntimeError("Workbook not loaded. Call load_workbook() first.")
        
        if num_rows == 0:
            print(f"⚠️ No rows to copy formulas for in sheet '{sheet_name}'")
            return
        
        try:
            sheet = self.workbook.sheets[sheet_name]
            
            # Define formula columns and their base formulas
            formula_definitions = {
                'N': "=-H2",  # Negative of incoming adjustment
                'O': "=-I2",  # Negative of outgoing adjustment  
                'P': "=-J2",  # Net adjustment (negative of total adjustment)
                'Q': '=XLOOKUP(B2,\'Seed Product List\'!A:A,\'Seed Product List\'!L:L,"")',  # Price lookup
                'R': '=IF(Q2<>"",P2*Q2,"")'  # Total value calculation
            }
            
            # Apply formulas using batch operations (one per column)
            for col_letter, base_formula in formula_definitions.items():
                end_row = num_rows + 1  # +1 because data starts at row 2
                range_address = f'{col_letter}2:{col_letter}{end_row}'
                
                # Set formula for entire column range at once
                column_range = sheet.range(range_address)
                column_range.formula = base_formula
            
            
        except Exception as e:
            print(f"❌ Failed to copy formulas in sheet '{sheet_name}': {str(e)}")
    
    def populate_iad_sheet(self, iad_data):
        """
        Populate the IAD data sheet
        
        Args:
            iad_data (pandas.DataFrame): IAD data to insert
        """
        self.clear_sheet_data("Seed IAD")
        self.insert_dataframe_to_sheet(iad_data, "Seed IAD", show_message=False)
        
        # Apply formulas if data exists
        if not iad_data.empty:
            self.copy_formulas_down("Seed IAD", len(iad_data))
            print(f"📊 Processed {len(iad_data)} rows in sheet 'Seed IAD' (data + formulas)")
    
    def populate_items_sheet(self, items_data):
        """
        Populate the Product List sheet
        
        Args:
            items_data (pandas.DataFrame): Product list data to insert
        """
        self.clear_sheet_data("Seed Product List")
        self.insert_dataframe_to_sheet(items_data, "Seed Product List")
    
    def save_and_close_workbook(self):
        """
        Save the workbook and close Excel application
        
        Returns:
            str: Path to the saved file
        """
        if not self.workbook:
            raise RuntimeError("Workbook not loaded")
        
        try:
            # Save workbook
            self.workbook.save()
            output_path = self.output_path
            
            # Close workbook and quit Excel
            self.workbook.close()
            if self.app:
                self.app.quit()
                
            print(f"💾 Saved Excel file: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Failed to save workbook: {str(e)}")
            # Ensure Excel is closed even if save fails
            try:
                if self.workbook:
                    self.workbook.close()
                if self.app:
                    self.app.quit()
            except:
                pass
            raise
    
    def generate_inventory_adjustment_report(self, iad_data, items_data, output_directory="downloads/daily"):
        """
        Complete workflow to generate Inventory Adjustment Report
        
        Args:
            iad_data (pandas.DataFrame): IAD data
            items_data (pandas.DataFrame): Product list data
            output_directory (str): Directory to save the report
            
        Returns:
            str: Path to the generated Excel file
        """
        try:
            # Create working copy
            self.create_working_copy(output_directory, "Inventory Adjustment Summary")
            
            # Load workbook
            self.load_workbook()
            
            # Populate sheets
            self.populate_iad_sheet(iad_data)
            self.populate_items_sheet(items_data)
            
            # Save and return path
            return self.save_and_close_workbook()
            
        except Exception as e:
            print(f"❌ Failed to generate inventory adjustment report: {str(e)}")
            # Ensure cleanup on error
            try:
                if self.workbook:
                    self.workbook.close()
                if self.app:
                    self.app.quit()
            except:
                pass
            raise

def get_inventory_template_info():
    """
    Get Inventory Adjustment template information
    
    Returns:
        dict: Template file information
    """
    processor = InventoryExcelProcessor()
    return processor.get_template_info()