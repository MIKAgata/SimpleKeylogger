import os
import datetime
from PIL import ImageGrab

class ScreenshotTaker:
    def __init__(self, save_dir="screenshots"):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def take(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.save_dir, f"screenshot_{timestamp}.png")
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(filename)
            return filename
        except Exception:
            return None