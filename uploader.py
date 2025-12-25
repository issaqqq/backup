import sys
import os
import asyncio
from telethon import TelegramClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Get these from my.telegram.org
API_ID = 123123123          
# Your real API ID (Integer)

API_HASH = '123123ABCABC' 
# Your real API Hash (String)

# Use your Channel ID (starts with -100)
CHANNEL_ID = -100123123

# Folder to watch
WATCH_FOLDER = r'C:\Users\mylap\Documents\A\Blip\Backup'

# A queue to hold files so the detector never gets stuck waiting
file_queue = asyncio.Queue()

class Watcher(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        if event.is_directory:
            return
        
        # This runs instantly when a file appears
        print(f"Detected: {os.path.basename(event.src_path)}")
        
        # Safely put the file into the async queue from this thread
        self.loop.call_soon_threadsafe(file_queue.put_nowait, event.src_path)

async def upload_worker(client):
    print("Worker started. Waiting for files...")
    while True:
        # Wait here until a file appears in the queue
        file_path = await file_queue.get()
        
        file_name = os.path.basename(file_path)
        print(f"Starting upload: {file_name}")

        try:
            # Check if file is still being copied (size changing)
            initial_size = -1
            while initial_size != os.path.getsize(file_path):
                initial_size = os.path.getsize(file_path)
                await asyncio.sleep(1) # Wait 1s and check size again
            
            # Upload up to 2GB/4GB
            await client.send_file(CHANNEL_ID, file_path, caption=file_name)
            print(f"✅ Finished: {file_name}")
            
        except Exception as e:
            print(f"❌ Error uploading {file_name}: {e}")
        finally:
            file_queue.task_done()

async def main():
    # 1. Start Telegram Client
    client = TelegramClient('backup_session', API_ID, API_HASH)
    await client.start()
    print("Telegram Client Connected!")

    # 2. Start the Watchdog (The Eyes)
    loop = asyncio.get_running_loop()
    event_handler = Watcher(loop)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"Monitoring: {WATCH_FOLDER}")

    # 3. Start the Worker (The Hands)
    # You can start multiple workers if you want parallel uploads!
    worker_task = asyncio.create_task(upload_worker(client))

    try:
        # Keep running forever
        await client.run_until_disconnected()
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    asyncio.run(main())