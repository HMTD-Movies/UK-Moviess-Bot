import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

class script(object):
    HOME_BUTTONURL_UPDATES = environ.get("HOME_BUTTONURL_UPDATES", 'https://tnlink.in/ref/KarthikUK')
    START_TXT = environ.get("START_TXT", '''<b>Hello 👋🏻 {} ♥️,\nI'm an UK Studios Official Auto Filter Bot (Movie Search Bot) Maintained by <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>. We are Providing Tamil and Tamil Dubbed Movies. More Languages Coming Soon. Keep me Join to Our Official Channel to Receive Bot & Movies Updates in <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>. Check "😁 About" Button.</b>''')
    HELP_TXT = """<b>Hello 👋🏻 {} ♥️,
I have that Features.
Create One Link This :-
» I will Create For One Bot You. But Paid
» Contact Me <a href=https://t.me/HMTD_Karthik><b>Karthik</b></a></b>"""
    ABOUT_TXT = """<b><i>🤖 My Name :- <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a>\n
🧑🏻‍💻 Developer :- <a href=https://t.me/HMTD_Karthik><b>Karthik</b></a>\n
📝 Language :- Pyrogram\n
📚 Framework :- Python3\n
📡 Hosted on :- VPS\n
📢 Updates Channel :- <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>\n
🌐 Website :- <a href=https://www.HMTDMovies.tk><b></b>www.HMTDMovies.tk</a>\n
🌟 Version :- 4.2</b></i>"""
    SOURCE_TXT = """<b>Create One Like This :-</b>
» I will Create One Bot For You. But Paid<b>
» Contact Me</b> <a href=https://t.me/HMTD_Karthik><b>Karthik</b></a>"""
    MANUELFILTER_TXT = """<b>Help :-</b> <b>Filters</b>

<b>- Filter is the Feature Were Users Can set Automated Replies for a Particular Keyword and <a href=https://t.me/UK_Movies_Bot><b>Our Bot</b></a> will Respond Whenever a Keyword is Found the Message</b>

<b>NOTE :-</b>
<b>1. <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> Should have Admin Privillage.
2. Only Admins can Add Filters in a Chat.
3. Alert Buttons have a Limit of 64 Characters.</b>

<b>Commands and Usage :</b>
<b>• /filter - Add a Filter in Chat
• /filters - list all the Filters of a Chat
• /del - Delete a Specific Filter in Chat 
• /delall - Delete the Whole Filters in a Chat (Chat Owner Only)</b>"""
    BUTTON_TXT = """<b>Help :-</b> <b>Buttons</b>

<b>- <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> Supports Both URL and Alert Inline Buttons.</b>

<b>NOTE :</b>
<b>1. Telegram will Not Allows you to Send Buttons Without Any Content, so Content is Mandatory.
2. <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> supports Buttons With Any Telegram Media/File type.
3. Buttons Should be Properly Parsed as Markdown Format</b>

<b>URL Buttons :-</b>
<code>[Button Text](buttonurl:https://t.me/UK_Movies_Zone_Updates)</code>

<b>Alert Buttons :</b>
<code>[Button Text](buttonalert:This is an Alert Message)</code>"""
    AUTOFILTER_TXT = """<b>Help :-</b> <b>Auto Filter</b>

<b>NOTE :</b>
<b>1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db.</b>"""
    CONNECTION_TXT = """<b>Help :</b> <b>Connections</b>

<b>- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.</b>

<b>NOTE :</b>
<b>1. Only admins can add a connection.
2. Send</b> <code>/connect</code> <b>for connecting me to ur PM</b>

<b>Commands and Usage :</b>
<b>• /connect  - connect a particular chat to your PM
• /disconnect  - disconnect from a chat
• /connections - list all your connections</b>"""
    EXTRAMOD_TXT = """<b>Help :</b> <b>Extra Modules</b>

<b>NOTE :</b>
<b>these are the extra features of Auto Filter Bot (Movie Search Bot)</b>

<b>Commands and Usage :</b>
<b>• /id - get id of a specified user.
• /info  - get information about a user.
• /imdb  - get the film information from IMDb source.
• /search  - get the film information from various sources.</b>"""
    ADMIN_TXT = """<b>Help :</b> <b>Admin mods</b>

<b>NOTE :</b>
<b>This module only works for my admins</b>

<b>Commands and Usage :</b>
<b>• /logs - to get the rescent errors
• /stats - to get status of files in db.
• /delete - to delete a specific file from db.
• /users - to get list of my users and ids.
• /chats - to get list of the my chats and ids 
• /leave  - to leave from a chat.
• /disable  -  do disable a chat.
• /ban  - to ban a user.
• /unban  - to unban a user.
• /channel - to get list of total connected channels
• /broadcast - to broadcast a message to all users</b>"""
    STATUS_TXT = """<b>🗃️ Total Files :</b> <code>{}</code> <b>Files</b>\n
<b>👩🏻‍💻 Total Users :</b> <code>{}</code> <b>Users</b>\n
<b>👥 Total Groups :</b> <code>{}</code> <b>Groups</b>\n
<b>💾 Used Storage :</b> <code>{}</code>\n
<b>🆓 Free Storage :</b> <code>{}</code>"""
    LOG_TEXT_G = """<b>#New_Group</b>
    
<b>᚛› Group ⪼ {}(<code>{}</code>)</b>
<b>᚛› Total Members ⪼ <code>{}</code></b>
<b>᚛› Added By ⪼ {}</b>
"""
    LOG_TEXT_P = """<b>#New_User</b>
    
<b>᚛› ID - <code>{}</code></b>
<b>᚛› Name - {}</b>
"""

REQ_TO_ADMIN = """<b>This Movie Not Found my Database or Not Released This Movie \n\nRequest to Admin</b>"""
