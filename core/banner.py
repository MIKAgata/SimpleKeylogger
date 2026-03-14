import datetime

def print_banner(start_time, filename, telegram_enabled):
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

    print(f"\033[1;33m[*]\033[0m Starting at: {start_time}")
    print(f"\033[1;33m[*]\033[0m Log file: {filename}")

    if telegram_enabled:
        print("\033[1;33m[*]\033[0m Telegram: Enabled")
    else:
        print("\033[1;33m[*]\033[0m Telegram: Disabled")

    print("\033[1;37m" + "=" * 70 + "\033[0m")