"""
Base Excel Processing
====================

Common functionality for all Excel report generation.
Provides template management and common utilities.
"""

import os
import shutil
from datetime import datetime

class ExcelProcessorBase:
    """
    Base class for Excel processing with common functionality
    """
    
    def __init__(self, template_path):
        """
        Initialize the Excel processor
        
        Args:
            template_path (str): Path to the template file
        """
        self.template_path = template_path
        self.output_path = None
        
    def validate_template_exists(self):
        """
        Check if the template file exists
        
        Returns:
            bool: True if template exists, False otherwise
        """
        if not os.path.exists(self.template_path):
            print(f"❌ Template file not found: {self.template_path}")
            print("📁 Please ensure the template file is placed in the templates/ directory")
            return False
        print(f"✅ Template file found: {self.template_path}")
        return True
    
    def create_working_copy(self, output_directory, filename_prefix):
        """
        Create a working copy of the template file
        
        Args:
            output_directory (str): Directory to save the working copy
            filename_prefix (str): Prefix for the output filename
            
        Returns:
            str: Path to the working copy file
        """
        if not self.validate_template_exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        # Generate output filename with date
        today = datetime.now()
        date_str = today.strftime("%m.%d.%y")
        filename = f"{filename_prefix} {date_str}.xlsx"
        self.output_path = os.path.join(output_directory, filename)
        
        # Copy template to working location
        shutil.copy2(self.template_path, self.output_path)
        print(f"📄 Created working copy: {self.output_path}")
        
        return self.output_path
    
    def get_template_info(self):
        """
        Get template file information
        
        Returns:
            dict: Template file information
        """
        template_info = {
            'exists': False,
            'path': self.template_path,
            'size': 0,
            'modified': 'Unknown'
        }
        
        if os.path.exists(self.template_path):
            template_info['exists'] = True
            template_info['size'] = os.path.getsize(self.template_path)
            
            # Get modification time
            mod_time = os.path.getmtime(self.template_path)
            template_info['modified'] = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        return template_info
    
    def cleanup_temp_files(self, *file_paths):
        """
        Clean up temporary files
        
        Args:
            *file_paths: Variable number of file paths to clean up
        """
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"🗑️ Removed temp file: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"⚠️ Could not remove temp file {file_path}: {str(e)}")

def ensure_directory_exists(directory_path):
    """
    Ensure directory exists (replaces utils.file_manager functionality)
    
    Args:
        directory_path (str): Path to directory
    """
    os.makedirs(directory_path, exist_ok=True)