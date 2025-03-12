import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

class LaunchpadView:
    def __init__(self, parent):
        self.parent = parent
        self.icon_size = 64
        self.padding = 10
        self._setup_view()
        
    def _setup_view(self):
        self.canvas = tk.Canvas(self.parent, bg='white')
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.icon_frame = ttk.Frame(self.canvas)
        
        self.icon_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.icon_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def load_icons(self, directory: Path):
        """Load application icons from directory"""
        for widget in self.icon_frame.winfo_children():
            widget.destroy()
            
        for idx, item in enumerate(directory.iterdir()):
            if item.is_file() and item.suffix.lower() in ['.exe', '.lnk']:
                self._create_icon(item, idx)
                
    def _create_icon(self, path: Path, position: int):
        frame = ttk.Frame(self.icon_frame)
        row = position // 4
        col = position % 4
        
        try:
            img = Image.open(self._get_icon_path(path))
            img = img.resize((self.icon_size, self.icon_size), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(img)
            
            label = ttk.Label(frame, image=icon)
            label.image = icon
            label.pack()
            
            text = ttk.Label(frame, text=path.stem)
            text.pack()
            
            frame.grid(row=row, column=col, padx=self.padding, pady=self.padding)
        except Exception as e:
            print(f"Error loading icon for {path.name}: {e}")
            
    def _get_icon_path(self, path: Path) -> Path:
        # Implement icon extraction logic
        return Path("default_icon.png")