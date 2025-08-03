"""
Report Configuration
===================

This module contains all configuration settings for the SEED report automation system.
Centralizes report IDs, download paths, and report type definitions for easy maintenance.
"""

# SEED API Report IDs mapped to descriptive names
SEED_REPORTS = {
    "daily_fill_oos": "33105",
    # Weekly Reports
    "Weekly Sales Reporting Market": "33106", 
    "Weekly Sales Reporting Delivery": "33107",
    "MKT Fills Per Visit By Section": "33108",
    "Product Activity Weekly": "33109",
    # Inventory Adjustment Detail reports
    "inventory_adjustment_previous_day": "33110",    # Tuesday-Friday: previous business day
    "inventory_adjustment_3_days_ago": "33111",      # Monday: 3 days ago (Friday data)
}

# Download directory paths
DOWNLOAD_PATHS = {
    "weekly": "downloads/weekly/",
    "daily": "downloads/daily/", 
    "temp": "downloads/temp/"
}

# Report type groupings
WEEKLY_REPORTS = ["Weekly Sales Reporting Market", "Weekly Sales Reporting Delivery", "MKT Fills Per Visit By Section", "Product Activity Weekly"]
DAILY_REPORTS = ["daily_fill_oos"]
INVENTORY_ADJUSTMENT_REPORTS = ["inventory_adjustment_previous_day", "inventory_adjustment_3_days_ago"]

# SEED API Configuration
SEED_API_HOST = "https://api.mycantaloupe.com"
SEED_API_ENDPOINT = "/Reports/Run"

# Download settings
MAX_CONCURRENT_DOWNLOADS = 25

# Product List API Configuration
PRODUCT_LIST_API_ENDPOINT = "https://mycantaloupe.com/cs4/ItemImportExport/ExcelExport" 