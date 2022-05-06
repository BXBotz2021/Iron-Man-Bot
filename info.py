import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
AUTO_DELETE = environ.get("AUTO_DELETE")

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]

# MongoDB information
DATABASE_URI = environ['DATABASE_URI']
DATABASE_NAME = environ['DATABASE_NAME']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Messages
default_start_msg = """**👋 Hey {}

ɪᴀᴍ ᴀ sɪᴍᴘʟᴇ ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ + ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜ. ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴍᴏᴠɪᴇs ɪɴ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs. ʏᴏᴜ ᴄᴀɴ sᴇᴀʀᴄʜ ᴍᴏᴠɪᴇs ᴠɪᴀ ɪɴʟɪɴᴇ. ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴇɴᴊᴏʏ

⚡ 𐌑ᥲiᥒᴛᥲiᥒᥱɗ BY : [Mᴜꜰᴀᴢ 🇮🇳 『Offline』](https://t.me/MufazTg)**
"""
START_MSG = environ.get('START_MSG', default_start_msg)

BUTTON = environ.get("BUTTON", False)
FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
