# backup

# 📂 Auto Telegram Uploader

A high-performance Python automation script that monitors a local folder and instantly uploads any new files to a specific Telegram Channel.

Built with **Telethon** and **Watchdog**, this tool acts as a "Userbot," bypassing standard bot limits to allow **high-speed uploads** and **files up to 2GB (or 4GB with Premium)**.

## 🚀 Features

* **Instant Detection:** Uses filesystem events to detect files the millisecond they are dropped.
* **Queue System:** Asynchronous queue handles multiple files at once without crashing or freezing.
* **Large File Support:** Supports files >50MB (up to Telegram's 2GB/4GB limit).
* **Smart Upload:** waits for file copying to finish before attempting upload (prevents "File in use" errors).
* **Auto-Resume:** Logs in automatically after the first setup using a session file.

## 🛠️ Prerequisites

* **Python 3.7+**
* A Telegram Account
* API Credentials from Telegram

## 📦 Installation

1. **Clone the repository** (or create your project folder):
   ```bash
   git clone [https://github.com/yourusername/auto-telegram-uploader.git](https://github.com/yourusername/auto-telegram-uploader.git)
   cd auto-telegram-uploader