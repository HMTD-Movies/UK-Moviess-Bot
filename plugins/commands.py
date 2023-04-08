import os
import logging
import random
import asyncio
from urllib.parse import quote
from googletrans import Translator
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from database.gtrans_mdb import find, insert, find_one
from utils import get_file_id
from Script import script
import os
import math
import time
import heroku3
import requests
from database.gtrans_mdb import set,unset ,insert
from pyrogram import Client, filters, enums
from database.users_chats_db import db
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db
from plugins.list import list
from info import *
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
import asyncio
import re, asyncio, time, shutil, psutil, os, sys
from pyrogram import Client, filters, enums
from pyrogram.types import *
import os
import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.handlers import MessageHandler
from pyshorteners import Shortener
from info import BOT_START_TIME, ADMINS
from utils import humanbytes
logger = logging.getLogger(__name__)

#=====================================================

HEROKU_API_KEY = (os.environ.get("HEROKU_API_KEY", "01b8b9ae-78d3-428e-88ef-f42af78b623c"))

#=====================================================

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton('📢 Update Channel', url='https://t.me/UK_Movies_Zone_Updates')
            ],
            [
                InlineKeyboardButton('💰 Earn Money', url=f"https://tnlink.in/ref/KarthikUK"),
            ],
            [
                InlineKeyboardButton(text=DOWNLOAD_TEXT_NAME,url=DOWNLOAD_TEXT_URL)
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), disable_web_page_preview=True, reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('©️ Add me to Your Group', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('💰 Earn Money' , url='https://tnlink.in/ref/KarthikUK'),
            InlineKeyboardButton('📢 Update Channel', url='https://t.me/UK_Movies_Zone_Updates')
            ],[
            InlineKeyboardButton('😎 Help', callback_data='help'),
            InlineKeyboardButton('😁 About', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("<b>Make sure Bot is Admin in Forcesub Channel</b>")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🔥 Join Update Channel 🔥", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton(" 🔄 Try Again", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="<b>Hello {u.mention}💗\nJoin Our Movie Updates Channel To Use Me ☺️\nYou Need to Join Our Channel to Use me\nKindly Please Join Our Channel</b>",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('©️ Add me to Your Group', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('💰 Earn Money', url='https://tnlink.in/ref/KarthikUK'),
            InlineKeyboardButton('📢 Update Channel', url='https://t.me/UK_Movies_Zone_Updates')
            ],[
            InlineKeyboardButton('😎 Help', callback_data='help'),
            InlineKeyboardButton('😁 About', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("<b>Accessing Files 📂.../</b>")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1) 
        await sts.delete()
        return
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("<b>Accessing Files 📂.../</b>")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()
        

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🔥 Join Our Channel 🔥', url='https://t.me/UK_Movies_Zone_Updates') ] ] ),
        protect_content=True if pre == 'filep' else False,
        )

@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(client, message):
        buttons = [[
            InlineKeyboardButton('Manuel Filter', callback_data='manuelfilter'),
            InlineKeyboardButton('Auto Filter', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Connections', callback_data='coct'),
            InlineKeyboardButton('Extra Mods', callback_data='extra')
        ], [
            InlineKeyboardButton('🏠 Home 🏠', callback_data='start'),
            InlineKeyboardButton('📊 Status', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.HELP_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(client, message):
        buttons = [[
            InlineKeyboardButton('🏠 Home 🏠', callback_data='start'),
            InlineKeyboardButton('😎 Help', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.ABOUT_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Client.on_message(filters.command("group_broadcast") & filters.user(ADMINS) & filters.reply)
async def grp_brodcst(bot, message):
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='<b>Broadcasting Your Messages to Connected Groups 😁...</b>'
    )
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for chat in chats:
        pti, sh = await broadcast_messages(int(chat['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"<b>Broadcast in Progress :-\n\nTotal Chats {total_chats}\nCompleted :- {done} / {total_chats}\nSuccess :- {success}\nFailed :- {failed}</b>")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"<b>Broadcast Completed :-\nCompleted in {time_taken} Seconds.\n\nTotal Chats {total_chats}\nCompleted :- {done} / {total_chats}\nSuccess :- {success}\nFailed :- {failed}</b>")


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send Basic Information of Channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '<b>📑 Indexed Channels/Groups</b>\n'
    for Channel in Channels :
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n<b>Total : {len(CHANNELS)}</b>'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send Log File 📂"""
    try:
        await message.reply_document('UKMoviesBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("<b>🗑️ Deleting...</b>", quote=True)
    else:
        await message.reply('<b>Reply to File 📂 with /delete which You Want to Delete</b>', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('<b>This is not Supported File Format</b>')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('<b>File 📂 Successfully Deleted</b>')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('<b>File 📂 Successfully Deleted</b>')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('<b>File 📂 Successfully Deleted</b>')
            else:
                await msg.edit('<b>File 📂 Not Found in Databas</b>')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        '<b>This Process Will Delete All The Files From Your Database.\nDo You Want to Continue This...??</b>',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚡ Yes ⚡", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⛔ Cancel ⛔", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Please Share & Support Us')
    await message.message.edit('<b>Succesfully Deleted All The Indexed Files.</b>')


@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are Anonymous Admin. Use /connect {message.chat.id} in PM</b>")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("<b>Make Sure I'm Present in Your Group!</b>", quote=True)
                return
        else:
            await message.reply_text("<b>I'm not Connected to any Groups!</b>", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'Filter Button',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Single' if settings["button"] else 'Double',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Bot PM',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["botpm"] else '❌ No',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'File Secure',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["file_secure"] else '❌ No',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'IMDB',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["imdb"] else '❌ No',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Spell Check',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["spell_check"] else '❌ No',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Welcome',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["welcome"] else '❌ No',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=f"<b>Change The Bot Settings For {title}..⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )



@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("<b>Checking New Template</b>")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are Anonymous Admin. Use /connect {message.chat.id} in PM</b>")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("<b>Make Sure I'm Present in Your Group!</b>", quote=True)
                return
        else:
            await message.reply_text("<b>I'm not Connected to any Groups!</b>", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("No Input!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"<b>Successfully Upgraded Your Template For {title} to\n\n{template}</b>")

@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your Message has Been Successfully Send to {user.mention}.</b>")
            else:
                await message.reply_text("<b>This User Didn't Started This Bot Yet !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error :- {e}</b>")
    else:
        await message.reply_text("<b>Use This Command as a Reply to any Message Using the Target Chat ID. For Example :- /send userid</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hello 👋🏻 {message.from_user.mention} ❤️, This command Won't Work in Groups. It Will only Works on My PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    k = await bot.send_message(chat_id=message.chat.id, text=f"<b>Fetching Files for Your Query {keyword} on DB... Please wait...</b>")
    files, next_offset, total = await get_bad_files(keyword)
    await k.edit_text(f"<b>Found {total} Files for Your Query {keyword} !\n\nFile Deletion Process will start in 5 Seconds !</b>")
    await asyncio.sleep(5)
    deleted = 0
    for file in files:
        await k.edit_text(f"<b>Process Started for Deleting Files From DB. Successfully Deleted {str(deleted)} Files From DB for Your Query {keyword} !\n\nPlease wait...</b>")
        file_ids = file.file_id
        file_name = file.file_name
        result = await Media.collection.delete_one({
            '_id': file_ids,
        })
        if result.deleted_count:
            logger.info(f'File Found for Your Query {keyword}! Successfully Deleted {file_name} from Database.')
        deleted += 1
    await k.edit_text(text=f"<b>Process Completed for File Deletion !\n\nSuccessfully Deleted {str(deleted)} Files from Database for your Query {keyword}.</b>")

@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your message has been successfully send to {user.mention}.</b>")
            else:
                await message.reply_text("<b>This user didn't started this bot yet !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error: {e}</b>")
    else:
        await message.reply_text("<b>Use this command as a reply to any message using the target chat id. For eg: /send userid</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command won't work in groups. It only works on my PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    btn = [[
       InlineKeyboardButton("Yes, Continue !", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("No, Abort operation !", callback_data="close_data")
    ]]
    await message.reply_text(
        text="<b>Are you sure? Do you want to continue?\n\nNote:- This could be a destructive action !</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("graph") & filters.private)
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        await update.reply_text("**Reply to a Photo or Video Under 5MB.**")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await update.reply_text("**Not Supported Media!**")
        return
    text = await update.reply_text(text="<b>Downloading to My Server ...</b>", disable_web_page_preview=True)   
    media = await update.reply_to_message.download()   
    await text.edit_text(text="<b>Downloading Completed. Now I am Uploading to graph.org Link...</b>", disable_web_page_preview=True)                                            
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"**Error :- {error}**", disable_web_page_preview=True)       
        return    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return    
    await text.edit_text(
        text=f"<b>Your Photo or Video Link :-</b>\n\n<b>https://graph.org{response[0]}</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Open Link", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ],[
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]])
        )

@Client.on_message(filters.command(["share_text", "share", "sharetext",]))
async def share_text(client, message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Notice :-\n\n1. Reply Any Messages.\n2. No Media Support\n\nAny Question Join Support Chat**",                
            reply_to_message_id=reply_id,
            quote=True,               
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 Support Chat", url=f"https://t.me/HMTD_Discussion_Group")]])
            )                                                   
        return
    await message.reply_text(
        text=f"**Here is Your Sharing Text 👇\n\nhttps://telegram.me/share/url?url={quote(input_text)}**",
        reply_to_message_id=reply_id,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("♂️ Share", url=f"https://telegram.me/share/url?url={quote(input_text)}")]])       
    )    

@Client.on_message(filters.command('status'))
async def bot_status(client,message):
    if HEROKU_API_KEY:
        try:
            server = heroku3.from_key(HEROKU_API_KEY)

            user_agent = (
                'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )
            accountid = server.account().id
            headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
            }

            path = "/accounts/" + accountid + "/actions/get-quota"

            request = requests.get("https://api.heroku.com" + path, headers=headers)

            if request.status_code == 200:
                result = request.json()

                total_quota = result['account_quota']
                quota_used = result['quota_used']

                quota_left = total_quota - quota_used
                
                total = math.floor(total_quota/3600)
                used = math.floor(quota_used/3600)
                hours = math.floor(quota_left/3600)
                minutes = math.floor(quota_left/60 % 60)
                days = math.floor(hours/24)

                usedperc = math.floor(quota_used / total_quota * 100)
                leftperc = math.floor(quota_left / total_quota * 100)

                quota_details = f"""
Heroku Account Status
➪ 𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 {total} 𝗁𝗈𝗎𝗋𝗌 𝗈𝖿 𝖿𝗋𝖾𝖾 𝖽𝗒𝗇𝗈 𝗊𝗎𝗈𝗍𝖺 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖾𝖺𝖼𝗁 𝗆𝗈𝗇𝗍𝗁.
➪ 𝖣𝗒𝗇𝗈 𝗁𝗈𝗎𝗋𝗌 𝗎𝗌𝖾𝖽 𝗍𝗁𝗂𝗌 𝗆𝗈𝗇𝗍𝗁:
        • {used} 𝖧𝗈𝗎𝗋𝗌 ( {usedperc}% )
➪ 𝖣𝗒𝗇𝗈 𝗁𝗈𝗎𝗋𝗌 𝗋𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝗆𝗈𝗇𝗍𝗁:
        • {hours} 𝖧𝗈𝗎𝗋𝗌 ( {leftperc}% )
        • Approximately {days} days!"""
            else:
                quota_details = ""
        except:
            print("Check your Heroku API key")
            quota_details = ""
    else:
        quota_details = ""

    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - BOT_START_TIME))

    try:
        t, u, f = shutil.disk_usage(".")
        total = humanbytes(t)
        used = humanbytes(u)
        free = humanbytes(f)

        disk = "\n**Disk Details**\n\n" \
            f"> USED  :  {used} / {total}\n" \
            f"> FREE  :  {free}\n\n"
    except:
        disk = ""

    await message.reply_text(
        "𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝘀𝘁𝗮𝘁𝘂𝘀 𝗼𝗳 𝘆𝗼𝘂𝗿 𝗕𝗼𝘁\n\n"
        "DB Status\n"
        f"➪ 𝖡𝗈𝗍 𝖴𝗉𝗍𝗂𝗆𝖾: {uptime}\n"
        f"{quota_details}"
        f"{disk}",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="**🔄 Bot 🤖 Process is Stopped. Bot is Restarting...**", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**✅️ Bot 🤖 is Restarted. Now You Can Use Me 😁**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**\n`{message.reply_to_message.sticker.file_id}`\n\n**Unique ID is **\n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("<b>Oops !! Not a sticker file</b>")

@Client.on_message(filters.command(["translater"]) & filters.text)
async def echo(client, message):
	keybord1= InlineKeyboardMarkup( [
        [   InlineKeyboardButton("Tamil",callback_data = "ta"),
        ],
        [    InlineKeyboardButton("Afrikaans", callback_data='af'),
             InlineKeyboardButton("Albanian", callback_data='sq'),
            InlineKeyboardButton("Amharic",callback_data ='am'),
        ],
        [   InlineKeyboardButton("Arabic", callback_data='ar'),
        InlineKeyboardButton("Armenian", callback_data='hy'),      
        InlineKeyboardButton("Azerbaijani",callback_data = 'az'),        
        ],
        [InlineKeyboardButton("Basque",callback_data ="eu"),
        	 InlineKeyboardButton("Belarusian",callback_data ="be"),       	
	InlineKeyboardButton("Bengali",callback_data="bn")],
	
	[InlineKeyboardButton("Bosnian",callback_data = "bs"),
	InlineKeyboardButton("Bulgarian",callback_data ="bg"),
	InlineKeyboardButton("Catalan",callback_data = "ca")
	],
	[ 
	InlineKeyboardButton("Corsican",callback_data ="co"),
	InlineKeyboardButton("Croatian",callback_data = "hr"),
	InlineKeyboardButton("Czech", callback_data = "cs"),
	],
	[ InlineKeyboardButton("Danish",callback_data = "da"),
	InlineKeyboardButton("Dutch",callback_data = "nl"),
	InlineKeyboardButton("Esperanto",callback_data = "eo"),	 
	],
	[InlineKeyboardButton(" Next --->",callback_data = "page2")
	]
	] )
	try:
		code =find(int(message.chat.id))
	except Exception as e:
		await message.reply_text(f" Error : {e}\nclick /start ........")
		return 	

	if code :
			try:
				lgcd = message.text.split("/translater")
				lg_cd = lgcd[1].lower().replace(" ", "")
				translater_text = message.reply_to_message.text
				translator = Translator()
				translation = translator.translate(message.text,dest = code)
			except Exception as e:
				await message.reply_text(f"Error : {e}")
				return
			try:
					for i in list:
						if list[i]==translation.src:
							fromt = i
						if list[i] == translation.dest:
							to = i
					await message.reply_text(f"Translated from **{fromt.capitalize()}** To **{to.capitalize()}**\n\n```{translation.text}```\n\n join @lntechnical")
			except Exception as e:
					await message.reply_text(f"Translated from **{translation.src}** To **{translation.dest}**\n\n```{translation.text}```\n\n join @lntechnical")
	else:
		await  message.reply_text("Select language 👇",reply_to_message_id = message.id, reply_markup =keybord1)

@Client.on_callback_query()
async def translate_text(bot,update):
      keybord1= InlineKeyboardMarkup( [
        [   InlineKeyboardButton("Tamil",callback_data = "ta"),
        ], 
        [    InlineKeyboardButton("Afrikaans", callback_data='af'),
             InlineKeyboardButton("Albanian", callback_data='sq'),
            InlineKeyboardButton("Amharic",callback_data ='am'),
        ],
        [   InlineKeyboardButton("Arabic", callback_data='ar'),
        InlineKeyboardButton("Armenian", callback_data='hy'),      
        InlineKeyboardButton("Azerbaijani",callback_data = 'az'),        
        ],
        [InlineKeyboardButton("Basque",callback_data ="eu"),
        	 InlineKeyboardButton("Belarusian",callback_data ="be"),       	
	InlineKeyboardButton("Bengali",callback_data="bn")],
	
	[InlineKeyboardButton("Bosnian",callback_data = "bs"),
	InlineKeyboardButton("Bulgarian",callback_data ="bg"),
	InlineKeyboardButton("Catalan",callback_data = "ca")
	],
	[ 
	InlineKeyboardButton("Corsican",callback_data ="co"),
	InlineKeyboardButton("Croatian",callback_data = "hr"),
	InlineKeyboardButton("Czech", callback_data = "cs"),
	],
	[ InlineKeyboardButton("Danish",callback_data = "da"),
	InlineKeyboardButton("Dutch",callback_data = "nl"),
	InlineKeyboardButton("Esperanto",callback_data = "eo"),	 
	],
	[InlineKeyboardButton(" Next --->",callback_data = "page2")
	]
	] )

      keybord2= InlineKeyboardMarkup([
           [InlineKeyboardButton("English",callback_data = "en"),
           InlineKeyboardButton("Estonian",callback_data = "et"),
           InlineKeyboardButton("Finnish",callback_data = "fi")
           ],
           [InlineKeyboardButton("French",callback_data = "fr"),
           InlineKeyboardButton("Frisian",callback_data = "fy"),
           InlineKeyboardButton("Galician",callback_data = "gl")
           ],
           [InlineKeyboardButton("Georgian",callback_data = "ka"),
           InlineKeyboardButton("German",callback_data = "de"),
           InlineKeyboardButton("Greek",callback_data = "el")
           ],
           [InlineKeyboardButton("Gujarati",callback_data = "gu"),
           InlineKeyboardButton("Haitian Creole",callback_data = "ht"),
           InlineKeyboardButton("Hausa",callback_data ="ha")
           ],
           [InlineKeyboardButton("Hindi",callback_data = "hi"),
           InlineKeyboardButton("Hungarian",callback_data = "hu"),
           InlineKeyboardButton("Icelandic",callback_data = "is")
           ],
           [InlineKeyboardButton("Igbo",callback_data = "ig"),
           InlineKeyboardButton("Indonesian",callback_data = "id"),
           InlineKeyboardButton("Irish",callback_data = "ga")
           ],
           [InlineKeyboardButton("<--- Back",callback_data = "page1"),
           InlineKeyboardButton(" Next --->",callback_data = "page3"),
           ]
            ])
		
      keybord3 = InlineKeyboardMarkup([
                [ InlineKeyboardButton("Italian",callback_data = "it"),
                InlineKeyboardButton("Japanese",callback_data = "ja"),
                InlineKeyboardButton("Javanese",callback_data = "jv")
                ],
                [InlineKeyboardButton("Kannada",callback_data = "kn"),
                InlineKeyboardButton("Kazakh",callback_data = "kk"),
                InlineKeyboardButton("Khmer",callback_data = "km")
                ],
                [InlineKeyboardButton("Kinyarwanda",callback_data = "rw"),
                InlineKeyboardButton("Korean",callback_data ="ko"),
                InlineKeyboardButton("Kurdish",callback_data = "ku")
                ],
                [ InlineKeyboardButton("Kyrgyz",callback_data ="ky"),
                InlineKeyboardButton("Lao",callback_data = "lo"),
                InlineKeyboardButton("Latin",callback_data = "la")
                ],
                [InlineKeyboardButton("Latvian",callback_data = "lv"),
                InlineKeyboardButton('Lithuanian',callback_data ="lt"),
                InlineKeyboardButton("Luxembourgish",callback_data = "lb")
                ],
                [InlineKeyboardButton("Macedonian",callback_data = "mk"),
                InlineKeyboardButton("Malagasy",callback_data ="mg"),
                InlineKeyboardButton("Malay",callback_data ="ms")
                ],
                [InlineKeyboardButton("<--- Back",callback_data = "page2"),
                InlineKeyboardButton(" Next --->",callback_data = "page4")
                ]
              
 
 ])

      keybord4 = InlineKeyboardMarkup([
          [InlineKeyboardButton("Malayalam",callback_data = "ml"),
          InlineKeyboardButton("Maltese",callback_data = "mt"),
          InlineKeyboardButton("Maori",callback_data = "mi")
          ],
          [InlineKeyboardButton("Marathi",callback_data = "mr"),
          InlineKeyboardButton("Mongolian",callback_data = "mn"),
          InlineKeyboardButton("Myanmar (Burmese)",callback_data = "my")
          ],
          [InlineKeyboardButton("Nepali",callback_data ="ne"),
          InlineKeyboardButton("Norwegian",callback_data = "no"),
          InlineKeyboardButton("Nyanja (Chichewa)",callback_data = "ny")
          ],
          [InlineKeyboardButton("Odia",callback_data = "or"),
          InlineKeyboardButton("Pashto",callback_data = "ps"),
          InlineKeyboardButton("Persian",callback_data = "fa"),
          ],
          [InlineKeyboardButton("Polish",callback_data = "pl"),
          InlineKeyboardButton("Portuguese",callback_data = "pt"),
          InlineKeyboardButton("Punjabi",callback_data = "pa"),
          ],
          [InlineKeyboardButton("Romanian",callback_data = "ro"),
          InlineKeyboardButton("Russian",callback_data = "ru"),
          InlineKeyboardButton("Samoan",callback_data= "sm"),
          ],
          [InlineKeyboardButton("<--- Back",callback_data = "page3"),
          InlineKeyboardButton("Next --->",callback_data = "page5")
          ]
          
 
 
 
 ])

      keybord5 = InlineKeyboardMarkup([
         [InlineKeyboardButton("Scots Gaelic",callback_data = "gd"),
         InlineKeyboardButton("Serbian",callback_data = "sr"),
         InlineKeyboardButton("Sesotho",callback_data = "st")
         ],
         [InlineKeyboardButton("Shona",callback_data ="sn"),
         InlineKeyboardButton("Sindhi",callback_data ="sd"),
         InlineKeyboardButton("Sinhala (Sinhalese)",callback_data = "si")
         ],
         [InlineKeyboardButton("Slovak",callback_data = "sk"),
         InlineKeyboardButton("Slovenian",callback_data = "sl"),
         InlineKeyboardButton("Somali",callback_data = "so")
         ],
         [InlineKeyboardButton("Spanish",callback_data = "es"),
         InlineKeyboardButton("Sundanese",callback_data ="su"),
         InlineKeyboardButton("Swahili",callback_data ="sw")
         ],
         [InlineKeyboardButton("Swedish",callback_data = "sv"),
         InlineKeyboardButton("Tagalog (Filipino)",callback_data ='tl'),
         InlineKeyboardButton("Tajik",callback_data = "tg")
         ],
         [InlineKeyboardButton("Tamil",callback_data = "ta"),
         InlineKeyboardButton("Tatar",callback_data = "tt"),
         InlineKeyboardButton("Telugu",callback_data = "te")
         ],
         [InlineKeyboardButton("<--- Back",callback_data = "page4"),
         InlineKeyboardButton("Next --->",callback_data = "page6")
         ]  ])




      keybord6 =  InlineKeyboardMarkup([
       [InlineKeyboardButton("Thai",callback_data = "th"),
       InlineKeyboardButton("Turkish",callback_data = "tr"),
       InlineKeyboardButton("!Not Valid",callback_data ="en")     
       ],
       [InlineKeyboardButton("Ukrainian",callback_data = "uk"),
       InlineKeyboardButton("Urdu",callback_data = "ur"),
       InlineKeyboardButton("Uyghur",callback_data ="ug")
       
       ],
       [InlineKeyboardButton("Uzbek",callback_data = "uz"),
       InlineKeyboardButton("Vietnamese",callback_data ="vi"),
       InlineKeyboardButton("Welsh",callback_data = "cy")
       
       ],
       [InlineKeyboardButton("Xhosa",callback_data = "xh"),
       InlineKeyboardButton("Yiddish",callback_data = "yi"),
       InlineKeyboardButton("Yoruba",callback_data = "yo")],
       [InlineKeyboardButton("<--- Back",callback_data = "page5")
       
       ] ])
      
      
      
      tr_text = update.message.reply_to_message.text
      cb_data = update.data
      if cb_data== "page2":
      	await update.message.edit("Select language 👇",reply_markup = keybord2)
      elif cb_data == "page1":
      	await update.message.edit("Select language 👇",reply_markup =keybord1)
      elif cb_data =="page3":
      	await update.message.edit("Select language 👇",reply_markup =keybord3)
      elif cb_data == "page4":
      	await update.message.edit("Select language 👇",reply_markup =keybord4)
      elif cb_data =="page5":
      	await update.message.edit("Select language 👇",reply_markup =keybord5)
      elif cb_data =="page6":
      	await update.message.edit("Select language 👇",reply_markup =keybord6)
      else :
      		try:
      			lgcd = message.text.split("/translater")
      			lg_cd = lgcd[1].lower().replace(" ", "")
      			translater_text = message.reply_to_message.text
      			translator = Translator()
      			translation = translator.translate(tr_text,dest = cb_data)
      		except Exception as e:
      			await update.message.edit(f"Error : {e}")
      			return
      		try:
      			for i in list:
      				if list[i]==translation.src:
      					fromt = i
      				if list[i] == translation.dest:
      					to = i 
      			await update.message.edit(f"Translated from **{fromt.capitalize()}** To **{to.capitalize()}**\n\n```{translation.text}```\n\n Join @HMTD_Links")
      		except Exception as e:
      			await update.message.edit(f"Translated from **{translation.src}** To **{translation.dest}**\n\n```{translation.text}```\n\n Join @HMTD_Links")

@Client.on_message(filters.private &filters.command(['unset']))
async def unsetlg(client,message):
	unset(int(message.chat.id))
	await message.reply_text("**Successfully removed custom default language**")

@Client.on_message(filters.private &filters.command(['set']))
async def setlg(client,message):
    	    user_id = int(message.chat.id)
    	    insert(user_id)
    	    text = message.text
    	    textspit = text.split('/set')
    	    lg_code = textspit[1]
    	    if lg_code:
    	    		cd = lg_code.lower().replace(" ", "")
    	    		try:
    	    			lgcd = list[cd]
    	    		except:
    	    			await message.reply_text("❗️ This language Not available in My List \n Or Check Your spelling 😉",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Check List 📑" ,url="https://raw.githubusercontent.com/lntechnical2/Google-Translater-/main/List/list.txt")]]))
    	    			return
    	    		set(user_id,lgcd)
    	    		await message.reply_text(f"Successfully set custom default language **{cd}**")
    	    else:
    	    		await message.reply_text(" Please use this command with an argument. \n **For Example:/set English**",reply_markup=InlineKeyboardMarkup([[	InlineKeyboardButton("How To Use",url = "https://youtu.be/dUYvenXiYKE")]]))

BITLY_API = os.environ.get("BITLY_API", "aa2132168583d283fb288625d9352f2c5835512a")
CUTTLY_API = os.environ.get("CUTTLY_API", "bd3a3ab946d7598ee459331dac9e9568e3d66")
EZ4SHORT_API = os.environ.get("EZ4SHORT_API", "e41618d805b3c4256dfa99abde6ef11fc7629c47")
TINYURL_API = os.environ.get("TINYURL_API", "iRkhyhlmfJ07cFVsFV0NpvX6dOWZIwPglbq8jQDuSBMqAEk5Y81BX04ejVQk")
DROPLINK_API = os.environ.get("DROPLINK_API", "1d85e33efc4969b36e0f6c0a017aaaefd8accccc")
TNLINK_API = os.environ.get("TNLINK_API", "d03a53149bf186ac74d58ff80d916f7a79ae5745")
SHAREUS_API = os.environ.get("SHAREUS_API", "IiXFmlsLukgMvDpc3t3FHbLal4u1")

reply_markup = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📢 Update Channel', url='https://t.me/UK_Movies_Zone_Updates')
        ],
        [
        InlineKeyboardButton('⚡ Request', url=f"https://t.me/TG_Karthik"),
        ],
        [
        InlineKeyboardButton('🚫 Close', callback_data='close_data')
        ]]
    )

@Client.on_message(filters.command(["short"]) & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="**Analysing Your Link...**",
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0),
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_to_message_id=message.id
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shortened URLs--**\n"
    
    # Bit.ly Shortener
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**1) Bit.ly :- {url}**\n"
        except Exception as error:
            print(f"Bit.ly Error :- {error}")
        
    # Clck.ru Shortener
    try:
        s = Shortener()
        url = s.clckru.short(link)
        shorten_urls += f"\n**2) Clck.ru :- {url}**\n"
    except Exception as error:
        print(f"Click.ru Error :- {error}")
    
    # Cutt.ly Shortener
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**3) Cutt.ly :- {url}**\n"
        except Exception as error:
            print(f"Cutt.ly Error :- {error}")
    
    # Da.gd Shortener
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**4) Da.gd :- {url}**\n"
    except Exception as error:
        print(f"Da.gd Error :- {error}")
    
    # Is.gd Shortener
    try:
        s = Shortener()
        url = s.isgd.short(link)
        shorten_urls += f"\n**5) Is.gd :- {url}**\n"
    except Exception as error:
        print(f"Is.gd Error :- {error}")
    
    # Osdb.link Shortener
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**6) Osdb.link :- {url}**\n"
    except Exception as error:
        print(f"Osdb.link Error :- {error}")
                
    # Droplink.co Shortener
    try:
        api_url = "https://droplink.co/api" 
        params = {'api': DROPLINK_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**7) Droplink.co :- {url}**\n"
    except Exception as error:
        print(f"Droplink.co Error :- {error}")

    # TNLink.in Shortener
    try:
        api_url = "https://tnlink.in/api" 
        params = {'api': TNLINK_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**8) TNLink.in :- {url}**\n"
    except Exception as error:
        print(f"TNLink.in Error :- {error}")

    # TinyURL.com Shortener
    try:
        s = Shortener(api_key=TINYURL_API)
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**9) TinyURL.com :- {url}**\n"
    except Exception as error:
        print(f"TinyURL.com Error :- {error}")
    
    # Ez4short.com Shortener
    try:
        api_url = "https://ez4short.com/api" 
        params = {'api': EZ4SHORT_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**10) Ez4short.com :- {url}**\n"
    except Exception as error:
        print(f"Ez4short.com Error :- {error}")

    # Shareus.io Shortener
    try:
        api_url = "https://shareus.io/api" 
        params = {'api': SHAREUS_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**11) Shareus.io :- {url}**\n"
    except Exception as error:
        print(f"Shareus.io Error :- {error}")
    
    # Send the text
    try:
        shorten_urls += ""
        return shorten_urls
    except Exception as error:
        return error
