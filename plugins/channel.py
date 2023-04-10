from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video | filters.audio
hash_dict = {}

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media_handler(bot, message):
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    file_hash, file_size = hash(media.file_id), media.file_size
    if (file_hash, file_size) in hash_dict:
        if (media.file_name or media.title) == hash_dict[(file_hash, file_size)]:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
        else:
            hash_dict[(file_hash, file_size)] = media.file_name or media.title
            media.file_type, media.caption = file_type, message.caption
            await save_file(media)
    else:
        hash_dict[(file_hash, file_size)] = media.file_name or media.title
        media.file_type, media.caption = file_type, message.caption
        await save_file(media)

    async for channel_message in bot.iter_history(chat_id=message.chat.id):
        if channel_message.message_id == message.message_id:
            break
        for file_type in ("document", "video", "audio"):
            channel_media = getattr(channel_message, file_type, None)
            if channel_media is not None:
                channel_file_hash, channel_file_size = hash(channel_media.file_id), channel_media.file_size
                if (channel_file_hash, channel_file_size) in hash_dict:
                    if (channel_media.file_name or channel_media.title) == hash_dict[(channel_file_hash, channel_file_size)]:
                        await bot.delete_messages(chat_id=message.chat.id, message_ids=channel_message.message_id)
                    else:
                        hash_dict[(channel_file_hash, channel_file_size)] = channel_media.file_name or channel_media.title
                else:
                    hash_dict[(channel_file_hash, channel_file_size)] = channel_media.file_name or channel_media.title


    try:
        welcome = await message.reply_photo(
            photo="https://i.imgur.com/Kz5fn5j.jpg",
            caption="Welcome to the group! Please read the rules in the pinned message and enjoy your stay."
        )
        temp.MELCOW['welcome'] = welcome.message_id
    except Exception as e:
        print(f"An error occurred while sending the welcome message: {e}")
