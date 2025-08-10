"""
SEED API Report Downloader
==========================

Downloads reports from SEED API using HTTP requests.
"""

import requests
from base64 import b64encode
import os
from dotenv import load_dotenv
from config.report_config import SEED_API_HOST, SEED_API_ENDPOINT

load_dotenv()

def get_seed_credentials():
    """Get SEED credentials from environment"""
    username = os.getenv("SEED_USERNAME")
    password = os.getenv("SEED_PASSWORD")
    if not username or not password:
        raise ValueError("SEED_USERNAME and SEED_PASSWORD must be set in .env file")
    return username, password

def download_seed_report(report_id, filename, download_path=""):
    """Download report from SEED API"""
    full_path = os.path.join(download_path, filename) if download_path else filename
    username, password = get_seed_credentials()
    
    # Basic auth header
    credentials = f"{username}:{password}"
    auth_header = "Basic " + b64encode(credentials.encode()).decode()
    
    try:
        response = requests.get(
            f"{SEED_API_HOST}{SEED_API_ENDPOINT}?ReportId={report_id}",
            headers={'Authorization': auth_header}
        )
        
        if response.status_code == 200:
            if download_path:
                os.makedirs(download_path, exist_ok=True)
            
            with open(full_path, 'wb') as file:
                file.write(response.content)
            return {"success": True, "filename": filename, "path": full_path}
        else:
            return {"success": False, "error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

