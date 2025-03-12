import schedule
import time
import threading
from datetime import datetime
from typing import Callable

class TaskScheduler:
    def __init__(self):
        self.jobs = []
        self.running = False
        self.thread = None
        
    def add_daily_task(self, task: Callable, time_str: str) -> None:
        schedule.every().day.at(time_str).do(task)
        
    def add_interval_task(self, task: Callable, minutes: int) -> None:
        schedule.every(minutes).minutes.do(task)
        
    def start(self) -> None:
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.start()
        
    def stop(self) -> None:
        self.running = False
        if self.thread:
            self.thread.join()
            
    def _run_scheduler(self) -> None:
        while self.running:
            schedule.run_pending()
            time.sleep(1)