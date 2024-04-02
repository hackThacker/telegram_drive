from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from telethon.sync import TelegramClient
import asyncio
import os

# Google Drive API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
refresh_token = 'YOUR_REFRESH_TOKEN'

# Telegram API credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Connect to Google Drive
gauth = GoogleAuth()
gauth.settings['client_config_file'] = False
gauth.settings['client_config'] = {
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token
}
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

# Connect to Telegram
client = TelegramClient('session_name', api_id, api_hash)
client.start()

# Function to send files to Telegram
async def send_file_to_telegram(file_path, channel_name):
    channel = await client.get_entity(channel_name)
    await client.send_file(channel, file_path)

# Function to download files from Telegram
async def download_files_from_telegram(channel_name):
    channel = await client.get_entity(channel_name)
    messages = await client.get_messages(channel)
    for message in messages:
        if message.media:
            file_path = await client.download_media(message.media, file='temp')
            await asyncio.sleep(2)  # Avoid getting rate-limited by Telegram
            await send_file_to_drive(file_path)

# Function to send files to Google Drive
def send_file_to_drive(file_path):
    file = drive.CreateFile({'title': os.path.basename(file_path)})
    file.SetContentFile(file_path)
    file.Upload()

# Function to retrieve files from Google Drive and send to Telegram
def retrieve_files_from_drive_and_send(channel_name):
    folder_id = 'YOUR_FOLDER_ID'
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        file_path = os.path.join('temp', file['title'])
        file.GetContentFile(file_path)
        asyncio.run(send_file_to_telegram(file_path, channel_name))
        os.remove(file_path)

async def main():
    # Set the Telegram channel name
    telegram_channel_name = 'rupershor prabhuji lectures'

    # Download files from Telegram and upload to Google Drive
    await download_files_from_telegram(telegram_channel_name)

    # Retrieve files from Google Drive and send to Telegram
    retrieve_files_from_drive_and_send(telegram_channel_name)

# Run the main function
asyncio.run(main())
