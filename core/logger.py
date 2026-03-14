class LogManager:

    def __init__(self, filename, telegram_sender=None):

        self.filename = filename
        self.buffer = ""
        self.telegram = telegram_sender

    def add(self, text):

        self.buffer += text

        if len(self.buffer) >= 200:
            self.flush()

    def flush(self):

        if not self.buffer:
            return

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(self.buffer)

        if self.telegram:
            self.telegram.send(self.buffer)

        self.buffer = ""