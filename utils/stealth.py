import platform
import sys
import os

class Stealth:
    @staticmethod
    def hide_console():
        system = platform.system()
        if system == "Windows":
            Stealth._hide_windows()
        elif system == "Linux":
            Stealth._hide_linux()
        # Mac not implemented

    @staticmethod
    def _hide_windows():
        import ctypes
        wh = ctypes.windll.kernel32.GetConsoleWindow()
        if wh:
            ctypes.windll.user32.ShowWindow(wh, 0)  # 0 = SW_HIDE

    @staticmethod
    def _hide_linux():
        # On Linux, we can daemonize
        if os.fork() > 0:
            sys.exit(0)
        os.setsid()
        if os.fork() > 0:
            sys.exit(0)
        sys.stdout.flush()
        sys.stderr.flush()
        with open('/dev/null', 'r+') as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())