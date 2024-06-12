import os
import json
import logging
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerChannel
from utils import get_env_var

# Logging configuration
from logging_config import setup_logging

setup_logging()

# Load environment variables
print(get_env_var("API_ID"))
api_id = int(get_env_var("API_ID"))
api_hash = get_env_var("API_HASH")
phone_number = get_env_var("PHONE_NUMBER")

# Telegram client
client = TelegramClient('MedaData', api_id, api_hash)

# File to store scraped data
data_file_path = os.path.join('data', 'scraped_data.json')

# Ensure the data directory exists
os.makedirs(os.path.dirname(data_file_path), exist_ok=True)

async def fetch_channel_data(channel_username):
    channel_data = {
        "channel": channel_username,
        "messages": []
    }
    
    try:
        await client.start()
        # Ensure we are authorized
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            try:
                await client.sign_in(phone_number, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))
        
        entity = await client.get_entity(channel_username)
        my_channel = InputPeerChannel(entity.id, entity.access_hash)
        
        # Get the history of messages
        history = await client(GetHistoryRequest(
            peer=my_channel,
            limit=100,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        
        messages = history.messages
        
        # Process messages and media
        for message in messages:
            message_data = {
                "message_id": message.id,
                "date": message.date.isoformat(),
                "sender_id": message.from_id.user_id if message.from_id else None,
                "text": message.message,
                "media_type": None,
                "file_path": None,
                "file_name": None,
                "file_size": None,
                "forwarded_from": message.forward.from_id if message.forward else None,
                "reply_to_msg_id": message.reply_to_msg_id,
                "views": message.views,
                "forwards": message.forwards,
                "replies": message.replies.replies if message.replies else None,
                "edit_date": message.edit_date.isoformat() if message.edit_date else None,
                "post_author": message.post_author,
                "grouped_id": message.grouped_id
            }
            
            if message.media:
                file_path = await client.download_media(message, file=f"media/{channel_username}")
                message_data.update({
                    "media_type": message.media.document.mime_type if message.media.document else "image",
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_size": os.path.getsize(file_path)
                })
                logging.info(f"Media saved to {file_path}")
            
            channel_data["messages"].append(message_data)
        
        # Append channel data to the main data file
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append(channel_data)

        with open(data_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    except Exception as e:
        logging.error(f"Error fetching data from {channel_username}: {e}")
    finally:
        await client.disconnect()

def scrape_telegram_channels():
    channels = [
        "DoctorsET",
        "CheMed123",
        "lobelia4cosmetics",
        "yetenaweg",
        "EAHCI"
    ]
    
    for channel in channels:
        client.loop.run_until_complete(fetch_channel_data(channel))