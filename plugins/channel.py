from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video | filters.audio

# Create a dictionary to store the hash values of files
hash_dict = {}

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    print("Received media message:", message)
    """Media Handler"""
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            print("Found media of type", file_type)
            break
    else:
        print("No supported media types found")
        return
    
    # Calculate the hash value of the file
    file_hash = hash(media.file_id)
    print("Generated hash value:", file_hash)
    
    # Check if the hash value already exists in the dictionary
    if file_hash in hash_dict:
        # If the hash value exists, delete the duplicate file
        print("Found duplicate file, deleting message...")
        await bot.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
    else:
        # If the hash value does not exist, save the file and add the hash value to the dictionary
        hash_dict[file_hash] = True
        media.file_type = file_type
        media.caption = message.caption
        
        # Check all messages in the channel for duplicates
        async for channel_message in bot.iter_history(chat_id=message.chat.id):
            for channel_file_type in ("document", "video", "audio"):
                channel_media = getattr(channel_message, channel_file_type, None)
                if channel_media is not None and hash(channel_media.file_id) == file_hash:
                    print("Found duplicate file in channel, deleting message...")
                    await bot.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
                    return
        await save_file(media)
        print("Saved media file:", media)
