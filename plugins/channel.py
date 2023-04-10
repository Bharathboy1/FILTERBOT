from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video | filters.audio


# Create a dictionary to store the hash values of files
hash_dict = {}

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return
    
    # Calculate the hash value of the file
    file_hash = hash(media.file_id)
    
    # Check if the hash value already exists in the dictionary
    if file_hash in hash_dict:
        # If the hash value exists, delete the duplicate file
        await bot.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
    else:
        # If the hash value does not exist, save the file and add the hash value to the dictionary
        hash_dict[file_hash] = True
        media.file_type = file_type
        media.caption = message.caption
        await save_file(media)
