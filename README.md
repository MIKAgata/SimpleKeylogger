# Educational Python Keylogger (Telegram Enabled)

Simple educational keylogger written in Python.  
This project demonstrates how keyboard events can be captured, processed, stored, and optionally sent to a remote service (Telegram).

The goal of this project is **learning about input monitoring, logging systems, and basic data exfiltration techniques** often studied in cybersecurity.

This project is for **educational and research purposes only**.

---

## Features

- Capture keyboard input using `pynput`
- Detect and display typed words
- Log keystrokes with timestamps
- Save logs to a local file
- Send captured logs to **Telegram**
- Buffered logging system (reduces file writes)
- Periodic log flushing using threading
- Colored terminal interface
- Graceful shutdown using `ESC`

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
