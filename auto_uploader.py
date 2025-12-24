import sys
import time
import asyncio
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram import Bot

# --- CONFIGURATION ---
TOKEN = '8236308872:AAE92UfV2MXLQoq6IcAcQ7esKsb2VCUKQNY'  
# Your Telegram Bot Token

CHANNEL_ID = '@TestBackup' 
# e.g., "@my_channel" or "-100123456789"

WATCH_FOLDER = r'C:\Users\YourName\Desktop\BackupFolder'  
# Path to watch

class UploaderHandler(FileSystemEventHandler):
    def __init__(self, bot, loop):
        self.bot = bot
        self.loop = loop

    def on_created(self, event):
        if event.is_directory:
            return

        # Log detection
        print(f"New file detected: {event.src_path}")
        
        # files often trigger 'created' before they are fully copied. 
        # We wait a moment to ensure the file is free to use.
        time.sleep(2) 
        
        # Run the async upload function from this synchronous callback
        self.loop.run_until_complete(self.upload_file(event.src_path))

    async def upload_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                print(f"Uploading {os.path.basename(file_path)}...")
                
                # 'send_document' is generic and works for files, photos, and videos
                await self.bot.send_document(chat_id=CHANNEL_ID, document=f)
                
                print("Upload Successful!")
        except Exception as e:
            print(f"Failed to upload: {e}")

def main():
    # Initialize Bot
    bot = Bot(token=TOKEN)
    
    # Create an event loop for async telegram calls
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Setup Watchdog
    event_handler = UploaderHandler(bot, loop)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    
    print(f"Monitoring folder: {WATCH_FOLDER}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()