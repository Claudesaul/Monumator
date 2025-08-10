"""
Menu Navigation Utility
======================

Provides arrow-key navigation for console menus.
"""

import os
import msvcrt

class MenuNavigator:
    """Simple arrow-key menu navigation"""
    
    def __init__(self, options, title="MENU"):
        self.options = options
        self.title = title
        self.selected = 0
    
    def display(self):
        """Display menu with highlighted selection"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{'=' * 60}")
        print(f"🎯 {self.title}")
        print(f"{'=' * 60}\n")
        
        for i, option in enumerate(self.options):
            if i == self.selected:
                print(f"→ {option}")
            else:
                print(f"  {option}")
        
        print(f"\n{'=' * 60}")
        print("Use ↑↓ arrows to navigate, Enter to select, Q to quit")
    
    def navigate(self):
        """Handle arrow key navigation"""
        while True:
            self.display()
            
            key = msvcrt.getch()
            
            # Check for arrow keys (two-byte sequence)
            if key in [b'\xe0', b'\x00']:  # Arrow key prefixes
                key2 = msvcrt.getch()
                if key2 == b'H':  # Up arrow
                    self.selected = (self.selected - 1) % len(self.options)
                elif key2 == b'P':  # Down arrow
                    self.selected = (self.selected + 1) % len(self.options)
            
            # Enter key
            elif key in [b'\r', b'\n']:
                return self.selected
            
            # Quit options
            elif key.lower() == b'q':
                return -1