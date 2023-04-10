import os

from pyrogram import Client

from pyrogram.errors import FloodWait

from pyrogram.types import Message

from typing import List

# function to delete all duplicate files

async def delete_duplicates(client: Client, chat_id: int, wait_time: int = 5) -> int:

    files = []

    deleted_count = 0

    async for message in client.iter_history(chat_id, wait_time=wait_time):

        file_name = message.file_name.split(".")[0] if not hasattr(message.media, "document") else message.file_name

        deleted_count += await message.delete() if (file_name in files) else (files.append(file_name), 0)[1]

    return deleted_count

# command to delete duplicate files in a channel

@Client.on_message()

async def delete_duplicates_command(client: Client, message: Message):

    if message.text and message.text.startswith("/deletedupes"):

        chat_id = message.chat.id

        try:

            deleted_count = await delete_duplicates(client, chat_id)

            await message.reply_text(f"Deleted {deleted_count} duplicate files")

        except FloodWait as e:

            await message.reply_text(f"Encountered flood wait. Sleeping for {e.x}s.")

            await asyncio.sleep(e.x)

            await delete_duplicates(client, chat_id)

# start the bot

if __name__ == "__main__":

    api_id = os.environ.get("API_ID")

    api_hash = os.environ.get("API_HASH")

    bot_token = os.environ.get("BOT_TOKEN")

    if not all([api_id, api_hash, bot_token]):

        print("Please set API_ID, API_HASH, and BOT_TOKEN in environment variables")

    else:

        app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

        app.run()
