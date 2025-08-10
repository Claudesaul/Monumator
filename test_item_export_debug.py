"""
Debug Item Export Page Structure
===============================

Investigate the actual structure of the Item Import/Export page to find the download mechanism.
"""

import asyncio
from web_automation.items_scraper import ItemsScraper

async def debug_item_export_page():
    """Debug the item export page structure"""
    print("DEBUGGING ITEM EXPORT PAGE STRUCTURE")
    print("=" * 50)
    print("Running in VISIBLE mode to inspect page")
    print()
    
    scraper = None
    
    try:
        # Initialize scraper in visible mode
        scraper = ItemsScraper(headless=False)
        
        # Setup browser and login
        print("Setting up browser and logging into SEED...")
        if not await scraper.setup_and_login():
            raise Exception("Failed to setup browser and login to SEED")
        print("Login successful!")
        print()
        
        # Navigate to item import/export page
        print("Navigating to Item Import/Export page...")
        if not await scraper.navigate_to_item_import_export():
            raise Exception("Failed to navigate to Item Import/Export page")
        print("Navigation successful!")
        print()
        
        print("DETAILED PAGE ANALYSIS:")
        print("=" * 40)
        print(f"Current URL: {scraper.page.url}")
        print()
        
        # Check page title
        title = await scraper.page.title()
        print(f"Page Title: {title}")
        print()
        
        # Analyze the form
        forms = await scraper.page.locator("form").all()
        print(f"Found {len(forms)} form(s):")
        
        for i, form in enumerate(forms):
            action = await form.get_attribute("action") or "No action"
            method = await form.get_attribute("method") or "No method"
            print(f"  Form {i+1}: Action='{action}', Method='{method}'")
            
            # Get form inputs
            form_inputs = await form.locator("input").all()
            print(f"    Inputs in form: {len(form_inputs)}")
            
            for j, input_elem in enumerate(form_inputs[:10]):  # First 10 inputs
                input_type = await input_elem.get_attribute("type") or "text"
                input_name = await input_elem.get_attribute("name") or "No name"
                input_value = await input_elem.get_attribute("value") or ""
                input_id = await input_elem.get_attribute("id") or "No id"
                
                print(f"      Input {j+1}: Type='{input_type}', Name='{input_name}', Value='{input_value}', ID='{input_id}'")
                
                # Look for submit buttons or export-related inputs
                if input_type.lower() in ['submit', 'button'] or 'export' in input_name.lower() or 'download' in input_name.lower():
                    print(f"        *** POTENTIAL EXPORT BUTTON! ***")
        
        print()
        
        # Look for all buttons on the page
        print("BUTTON ANALYSIS:")
        all_buttons = await scraper.page.locator("button, input[type='button'], input[type='submit']").all()
        print(f"Found {len(all_buttons)} button elements:")
        
        for i, button in enumerate(all_buttons):
            text = (await button.text_content() or "").strip()
            button_type = await button.get_attribute("type") or "button"
            onclick = await button.get_attribute("onclick") or ""
            value = await button.get_attribute("value") or ""
            
            print(f"  Button {i+1}: Text='{text}', Type='{button_type}', Value='{value}'")
            if onclick:
                print(f"    OnClick: {onclick[:100]}...")
            
            # Highlight potential export buttons
            if any(keyword in text.lower() for keyword in ['export', 'download', 'generate', 'submit']):
                print(f"    *** POTENTIAL EXPORT BUTTON! ***")
        
        print()
        
        # Look for links that might trigger downloads
        print("LINK ANALYSIS:")
        links = await scraper.page.locator("a").all()
        print(f"Found {len(links)} links:")
        
        for i, link in enumerate(links[:20]):  # First 20 links
            href = await link.get_attribute("href") or ""
            text = (await link.text_content() or "").strip()
            
            if href and any(keyword in href.lower() for keyword in ['export', 'download', 'excel', 'csv']):
                print(f"  Link {i+1}: '{text}' -> {href}")
                print(f"    *** POTENTIAL EXPORT LINK! ***")
            elif any(keyword in text.lower() for keyword in ['export', 'download', 'excel', 'csv']):
                print(f"  Link {i+1}: '{text}' -> {href}")
                print(f"    *** POTENTIAL EXPORT LINK! ***")
        
        print()
        
        # Check for JavaScript functions that might handle downloads
        print("JAVASCRIPT ANALYSIS:")
        print("Looking for export-related JavaScript functions...")
        
        # Execute JavaScript to find export functions
        try:
            js_functions = await scraper.page.evaluate("""
                () => {
                    const functions = [];
                    for (let prop in window) {
                        if (typeof window[prop] === 'function') {
                            const name = prop.toString();
                            if (name.toLowerCase().includes('export') || 
                                name.toLowerCase().includes('download') ||
                                name.toLowerCase().includes('excel')) {
                                functions.push(name);
                            }
                        }
                    }
                    return functions;
                }
            """)
            
            if js_functions:
                print(f"Found {len(js_functions)} export-related JS functions:")
                for func in js_functions:
                    print(f"  - {func}()")
            else:
                print("No export-related JavaScript functions found")
                
        except Exception as e:
            print(f"JavaScript analysis failed: {str(e)}")
        
        print()
        print("MANUAL INSPECTION:")
        print("The browser window is open for manual inspection.")
        print("Look for:")
        print("1. Export or Download buttons")
        print("2. Form submit buttons")
        print("3. Links that might trigger downloads")
        print("4. Right-click context menus")
        print()
        print("Press Enter when you've finished inspecting the page...")
        
        # Wait for user input to keep browser open
        input()
        
    except Exception as e:
        print(f"Debug failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper:
            print("\nCleaning up browser...")
            await scraper.cleanup_browser()
    
    print("\nDebug completed!")

def main():
    """Run the debug"""
    print("Starting item export page debug...")
    asyncio.run(debug_item_export_page())

if __name__ == "__main__":
    main()