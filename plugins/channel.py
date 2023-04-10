@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media_handler(bot, message, message_ids=None):
    """Media Handler"""
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return
    
    # Calculate the hash value and size of the file
    file_hash = hash(media.file_id)
    file_size = media.file_size
    
    # Check if the hash value and size already exist in the dictionary
    if (file_hash, file_size) in hash_dict:
        # If the hash value and size exist, compare the file names
        existing_file_name = hash_dict[(file_hash, file_size)]
        current_file_name = media.file_name or media.title
        if current_file_name == existing_file_name:
            # If the file names match, delete the duplicate file
            await bot.delete_messages(chat_id=message.chat.id, message_ids=message_ids or message.message_id)
        else:
            # If the file names do not match, add the file name to the dictionary
            hash_dict[(file_hash, file_size)] = current_file_name
            media.file_type = file_type
            media.caption = message.caption
            await save_file(media)
    else:
        # If the hash value and size do not exist, save the file and add the hash value and size to the dictionary
        hash_dict[(file_hash, file_size)] = media.file_name or media.title
        media.file_type = file_type
        media.caption = message.caption
        await save_file(media)

    # Get all the messages in the channel to check for duplicates
    channel_messages = await bot.get_history(chat_id=message.chat.id)
    for channel_message in channel_messages:
        if channel_message.message_id == message.message_id:
            # Stop iterating once the current message is reached
            break
        
        for file_type in ("document", "video", "audio"):
            channel_media = getattr(channel_message, file_type, None)
            if channel_media is not None:
                # Calculate the hash value and size of the file in the channel
                channel_file_hash = hash(channel_media.file_id)
                channel_file_size = channel_media.file_size
                
                if (channel_file_hash, channel_file_size) in hash_dict:
                    # If the hash value and size exist, compare the file names
                    existing_file_name = hash_dict[(channel_file_hash, channel_file_size)]
                    current_file_name = channel_media.file_name or channel_media.title
                    if current_file_name == existing_file_name:
                        # If the file names match, delete the duplicate file in the channel
                        await bot.delete_messages(chat_id=channel_message.chat.id, message_ids=message_ids or channel_message.message_id)
                    else:
                        # If the file names do not match, add the file name to the dictionary
                        hash_dict[(channel_file_hash, channel_file_size)] = current_file_name
