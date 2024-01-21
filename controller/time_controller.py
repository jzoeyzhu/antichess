"""
Used/Modified code from:
Chan Mk, python-chess-engine-extension, (2019), GitHub repository
https://github.com/Mk-Chan/python-chess-engine-extensions
"""

import datetime as dt
from abc import ABC

class TimeController(ABC):
    start_time = None
    end_time = None

    def start_signal(self, movetime):
        self.start_time = dt.datetime.now().timestamp()
        self.end_time = self.start_time + movetime / 1000.0
        return

    def stop_signal(self):
        return dt.datetime.now().timestamp() > self.end_time
