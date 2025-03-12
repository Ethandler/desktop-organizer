import sys
import argparse
from pathlib import Path
from gui.main_window import DesktopOrganizerGUI
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="Desktop Organization Suite")
    parser.add_argument('--gui', action='store_true', help='Launch graphical interface')
    parser.add_argument('--workspace', type=str, help='Set active workspace')
    args = parser.parse_args()
    
    if args.gui:
        root = tk.Tk()
        app = DesktopOrganizerGUI(root)
        root.mainloop()
    else:
        from modules.core_organizer import DesktopOrganizer
        organizer = DesktopOrganizer()
        desktop_path = Path.home() / "Desktop"
        organizer.organize(desktop_path)

if __name__ == "__main__":
    main()