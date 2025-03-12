import tkinter as tk
from tkinter import messagebox
from plyer import notification
import winsound

class NotificationManager:
    def __init__(self):
        self.enabled = True
        self.sound_enabled = True
        
    def show_notification(self, title: str, message: str, duration: int = 5):
        if self.enabled:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=duration
                )
                if self.sound_enabled:
                    winsound.MessageBeep()
            except Exception as e:
                self._fallback_notification(title, message)
                
    def _fallback_notification(self, title: str, message: str):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()
        
    def configure(self, enabled: bool = True, sound: bool = True):
        self.enabled = enabled
        self.sound_enabled = sound