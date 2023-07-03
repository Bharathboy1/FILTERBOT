import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQuery
from database.ia_filterdb import get_search_results
from utils import is_subscribed, get_size, temp
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

async def inline_users(query: InlineQuery):
    if AUTH_USERS:
        if query.from_user and query.from_user.id in AUTH_USERS:
            return True
        else:
            return False
    if query.from_user and query.from_user.id not in temp.BANNED_USERS:
        return True
    return False

@Client.on_inline_query()
async def answer(bot, query):
    """Show search results for given inline query"""
    
   # if query.data.startswith("forward_"):
       # file_id = query.data.split("_")[1]
        # Perform the forward action using the file_id
        #await bot.forward_messages(chat_id, from_chat_id, file_id)
        # You can also delete the message or perform any other actions if needed
        #await query.answer('I hope your Message got forwarded!')

    # Existing code...

    
    if not await inline_users(query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='okDa',
                           switch_pm_parameter="hehe")
        return

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You have to subscribe my channel to use the bot',
                           switch_pm_parameter="subscribe")
        return
    if isinstance(query, InlineQuery):
        # Handle the inline query
        
        # Existing code...
        
        # Create and set the inline keyboard
        reply_markup = get_reply_markup(query.query, file_id=None)
        
        # Existing code...
        
    elif isinstance(query, CallbackQuery):
        # Handle the callback query
        
        if query.data.startswith("forward_"):
            file_id = query.data.split("_")[1]
            
            # Perform the forward action using the file_id
            await bot.forward_messages(chat_id, from_chat_id, file_id)
            
            # You can also delete the message or perform any other actions if needed
            await query.answer('I hope your message got forwarded!')
    
    # Existing cod

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    file_id = query.data.split("_")[1]
    reply_markup = get_reply_markup(query=string, file_id=file_id)
    files, next_offset, total = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        title=file.file_name
        size=get_size(file.file_size)
        f_caption=file.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{file.file_name}"
            f_caption += "\n\n•This file will be automatically deleted after 24 hours\n•Please save it to saved message or forward it anywhere."
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                document_file_id=file.file_id,
                caption=f_caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))
        await asyncio.sleep(86400)
        await d.delete()

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results - {total}"
        if string:
            switch_pm_text += f" for {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")
   # if query.data.startswith("forward_"):
       # file_id = query.data.split("_")[1]
    # Perform the forward action using the file_id
        #await client.forward_message(chat_id, from_chat_id, message_id)
    # You can also delete the message or perform any other actions if needed
       # await query.answer('I hope your Message got forwarded!')


def get_reply_markup(query, file_id):
    buttons = [
        [
            InlineKeyboardButton('Search again', switch_inline_query_current_chat=query)
        ],
        [
            InlineKeyboardButton('Forward', callback_data=f'forward_{file_id}')
        ]
    ]
    return InlineKeyboardMarkup(buttons)
