import os
import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWaitimport os
import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

async def delete_duplicates(client: Client, chat_id: int, wait_time: int = 5) -> int:
    files = []
    deleted_count = 0
    async for message in client.iter_history(chat_id, wait_time=wait_time):
        file_name = message.file_name.split(".")[0] if not hasattr(message.media, "document") else message.file_name
        deleted_count += await message.delete() if (file_name in files) else (files.append(file_name), 0)[1]
    return deleted_count

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
