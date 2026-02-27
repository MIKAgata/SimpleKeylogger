# keylogger/utils.py
import os
import datetime

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_banner():
    banner = """
    __ __          __                          
   / //_/__  __  __/ /___  ____ _____ ____  _____
  / ,<  / _ \/ / / / / __ \/ __ `/ __ `/ _ \/ ___/
 / /| |/  __/ /_/ / / /_/ / /_/ / /_/ /  __/ /    
/_/ |_|\___/\__, /_/\____/\__, /\__, /\___/_/     
           /____/        /____//____/              
"""
    return banner

def print_banner(start_time, filename, telegram_enabled):
    print("\033[1;34m" + get_banner() + "\033[0m")
    print("\033[1;37m" + "=" * 70 + "\033[0m")
    print("\033[1;33m[*]\033[0m Educational Keylogger v1.0 (Telegram Enabled)")
    print("\033[1;33m[*]\033[0m Starting at: \033[1;32m{}\033[0m".format(
        start_time.strftime('%Y-%m-%d %H:%M:%S')))
    print("\033[1;33m[*]\033[0m Log file: \033[1;32m{}\033[0m".format(filename))
    if telegram_enabled:
        print("\033[1;33m[*]\033[0m Telegram: \033[1;32mEnabled\033[0m")
    else:
        print("\033[1;33m[*]\033[0m Telegram: \033[1;31mDisabled\033[0m")
    print("\033[1;37m" + "=" * 70 + "\033[0m")
    print()

def print_footer(start_time, key_count, filename):
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print()
    print("\033[1;37m" + "=" * 70 + "\033[0m")
    print("\033[1;33m[*]\033[0m Keylogger stopped")
    print("\033[1;33m[*]\033[0m End time: \033[1;32m{}\033[0m".format(
        end_time.strftime('%Y-%m-%d %H:%M:%S')))
    print("\033[1;33m[*]\033[0m Duration: \033[1;32m{}\033[0m".format(duration))
    print("\033[1;33m[*]\033[0m Total keys logged: \033[1;32m{}\033[0m".format(key_count))
    print("\033[1;33m[*]\033[0m Log saved to: \033[1;32m{}\033[0m".format(filename))
    print("\033[1;37m" + "=" * 70 + "\033[0m")