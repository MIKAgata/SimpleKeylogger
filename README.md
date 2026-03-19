# Educational Python Keylogger (Telegram Enabled)

Keylogger edukatif sederhana yang ditulis dalam Python.

Proyek ini mendemonstrasikan bagaimana peristiwa keyboard dapat ditangkap, diproses, disimpan, dan secara opsional dikirim ke layanan jarak jauh (Telegram).

Tujuan proyek ini adalah **mempelajari tentang pemantauan input, sistem pencatatan, dan teknik eksfiltrasi data dasar** yang sering dipelajari dalam keamanan siber.

Proyek ini hanya untuk **tujuan pendidikan dan penelitian**.

---

## Fitur

- Menangkap input keyboard menggunakan `pynput`
- Mendeteksi dan menampilkan kata-kata yang diketik
- Mencatat penekanan tombol dengan stempel waktu
- Menyimpan log ke file lokal
- Mengirim log yang ditangkap ke **Telegram**
- Sistem pencatatan buffer (mengurangi penulisan file)
- Pembersihan log berkala menggunakan threading
- Antarmuka terminal berwarna
- Penutupan yang aman menggunakan `ESC`
---

## Demo Output

Example terminal output:
```bash
[20:00:02] h
[20:00:02] e
[20:00:03] l
[20:00:03] l
[20:00:03] o
[WORD] hello
```

---

## Project Structure
project/
│
├── main.py
├── keylog.txt
├── .env
│
└── core/
├── config.py
├── banner.py
├── telegram_sender.py
├── logger.py
├── key_handler.py
└── keylogger.py


Description:

| File | Purpose |
|-----|------|
| `main.py` | Entry point of the program |
| `config.py` | Loads environment variables |
| `banner.py` | Terminal banner and UI |
| `telegram_sender.py` | Sends logs to Telegram |
| `logger.py` | Handles log buffer and file writing |
| `key_handler.py` | Processes keyboard events |
| `keylogger.py` | Main controller of the application |

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt

```

## Configuration

Create a .env file in the project root.

Example:
```bash
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

How to obtain them:

Telegram Bot Token

Open @BotFather

Run /newbot

Copy the bot token

Telegram Chat ID

Send a message to your bot, then use:

https://api.telegram.org/bot<TOKEN>/getUpdates

Find your chat_id in the response.


## Running the Program

Run:

```bash
python main.py
```

Program flow:

1. Initialize keylogger

2. Display banner

3. Start keyboard listener

4. Capture keystrokes

5. Save logs to file

6. Optionally send logs to Telegram

7. Press ESC to stop the keylogger.


## Log Format

Example log file (keylog.txt):

```bash 
[20:11:02] h
[20:11:02] e
[20:11:02] l
[20:11:03] l
[20:11:03] o
[20:11:03] [SPACE]
[20:11:03] [WORD] hello
```

## How It Works
1. pynput listens for keyboard events
2. Each key press is processed in on_press()
3. Characters are appended to a buffer
4. When the buffer reaches a limit:
    - It is written to keylog.txt
    - It can be sent to Telegram
5. Words are detected when:
    - Space
    - Enter
    - Tab
