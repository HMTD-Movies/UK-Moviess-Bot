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
    START_TXT = environ.get("START_TXT", '''<b>Hello ๐๐ป {} โฅ๏ธ,\nI'm an UK Studios Official <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> Maintained by <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>. We are Providing Tamil and Tamil Dubbed Movies. More Languages Coming Soon. Keep me Join to Our Official Channel to Receive Bot & Movies Updates in <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>. Check "๐ About" Button.</b>''')
    HELP_TXT = """<b>Hello ๐๐ป {} โฅ๏ธ,
I have that Features.
Create One Link This :-
ยป I will Create For One Bot You. But Paid
ยป Contact Me <a href=https://t.me/HMTD_Karthik><b>Karthik</b></a></b>"""
    ABOUT_TXT = """<b><i>๐ค My Name :- <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a>\n
๐ง๐ปโ๐ป Developer :- <a href=https://t.me/HMTD_Karthik><b>Karthik</b></a>\n
๐ Language :- Pyrogram\n
๐ Framework :- Python3\n
๐ก Hosted on :- VPS\n
๐ข Updates Channel :- <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>\n
๐ Website :- <a href=https://www.HMTDMovies.tk><b></b>www.HMTDMovies.tk</a>\n
๐ Version :- 4.2</b></i>"""
    SOURCE_TXT = """<b>Create One Like This :-</b>
ยป I will Create One Bot For You. But Paid<b>
ยป Contact Me</b> <a href=https://t.me/HMTD_Karthik><b>Karthik</b></a>"""
    MANUELFILTER_TXT = """<b>Help :-</b> <b>Filters</b>

<b>- Filter is the Feature Were Users Can set Automated Replies for a Particular Keyword and <a href=https://t.me/UK_Movies_Bot><b>Our Bot</b></a> will Respond Whenever a Keyword is Found the Message</b>

<b>NOTE :-</b>
<b>1. <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> Should have ๐จโโ๏ธ Admin Privillage.
2. Only ๐จโโ๏ธ Admins can Add Filters in a Chat.
3. Alert Buttons have a Limit of 64 Characters.</b>

<b>Commands and Usage :-</b>
<b>โข /filter - Add a Filter in Chat
โข /filters - list all the Filters of a Chat
โข /del - Delete a Specific Filter in Chat 
โข /delall - Delete the Whole Filters in a Chat (Chat Owner Only)</b>"""
    BUTTON_TXT = """<b>Help :-</b> <b>Buttons</b>

<b>- <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> Supports Both URL and Alert Inline Buttons.</b>

<b>NOTE :-</b>
<b>1. Telegram will Not Allows you to Send Buttons Without Any Content, so Content is Mandatory.
2. <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a> supports Buttons With Any Telegram Media/File type.
3. Buttons Should be Properly Parsed as Markdown Format</b>

<b>URL Buttons :-</b>
<code>[Button Text](buttonurl:https://t.me/UK_Movies_Zone_Updates)</code>

<b>Alert Buttons :-</b>
<code>[Button Text](buttonalert:This is an Alert Message)</code>"""
    AUTOFILTER_TXT = """<b>Help :-</b> <b>Auto Filter</b>

<b>NOTE :-</b>
<b>1. Make Me The ๐จโโ๏ธ Admin of Your Channel if it's Private.
2. Make Sure that Your Channel Doesn't Contains Camrips, Porn and Fake Files ๐.
3. Forward the last Message to me with Quotes.
 I'll Add all the Files ๐ in that Channel to My Database.</b>"""
    CONNECTION_TXT = """<b>Help :-</b> <b>Connections</b>

<b>- Used to Connect Bot to PM for Managing Filters 
- it Helps To Avoid Spamming in Groups.</b>

<b>NOTE :-</b>
<b>1. Only ๐จโโ๏ธ Admins can Add a Connection.
2. Send</b> <code>/connect</code> <b>for Connecting Me To Your PM</b>

<b>Commands and Usage :</b>
<b>โข /connect  - Connect a Particular Chat to Your PM
โข /disconnect  - Disconnect From a Chat 
โข /connections - List All Your Connections</b>"""
    EXTRAMOD_TXT = """<b>Help :-</b> <b>Extra Modules</b>

<b>NOTE :-</b>
<b>These are the Extra Features of Our <a href=https://t.me/UK_Movies_Bot><b>UK Movies Bot</b></a></b>

<b>Commands and Usage :</b>
<b>โข /id - Get ID of a Specified User.
โข /info  - Get Information About a User.
โข /imdb  - Get the Movie ๐ฅ Information From IMDB Source.
โข /search  - Get the Movie ๐ฅ Information from Various Sources.</b>"""
    ADMIN_TXT = """<b>Help :-</b> <b>๐จโโ๏ธ Admin Mods</b>

<b>NOTE :-</b>
<b>This Module only Works for My ๐จโโ๏ธ Admins</b>

<b>Commands and Usage :-</b>
<b>โข /logs - to Get The Recent Errors
โข /stats - to Get Status Of Files ๐ in Database.
โข /delete - to Delete ๐๏ธ a Specific File ๐ From Database.
โข /users - to Get List of My Users and IDs.
โข /chats - to Get List of The My Chats and IDs
โข /leave  - to Leave From a Chat.
โข /disable  -  do Disable a Chat.
โข /ban  - to Ban a User.
โข /unban  - to Unban a User.
โข /channel - to Get List of Total Connected Channels 
โข /broadcast - to Broadcast a Message to All Users ๐</b>"""

    STATUS_TXT = """<b>๐๏ธ Total Files :</b> <code>{}</code> <b>Files</b>\n
<b>๐ฉ๐ปโ๐ป Total Users :</b> <code>{}</code> <b>Users</b>\n
<b>๐ฅ Total Groups :</b> <code>{}</code> <b>Groups</b>\n
<b>๐พ Used Storage :</b> <code>{}</code>\n
<b>๐ Free Storage :</b> <code>{}</code>"""

    LOG_TEXT_G = """<b>#New_Group</b>
    
<b>แโบ Group โชผ {}(<code>{}</code>)</b>
<b>แโบ Total Members โชผ <code>{}</code></b>
<b>แโบ Added By โชผ {}</b>
"""
    LOG_TEXT_P = """<b>#New_User</b>
    
<b>แโบ ID - <code>{}</code></b>
<b>แโบ Name - {}</b>
"""

REQ_TO_ADMIN = """<b>๐ Currently Unavailable to My Database or Not Released This Movie ๐ฅ ! We are Really Sorry for Inconvenience..!\n Have Patience..! Our Greatest ๐จโโ๏ธ Admins Will Upload This Movie ๐ฅ As Soon as Possible.!\n\nRequest to Our Greatest ๐จโโ๏ธ Admins</b>"""
