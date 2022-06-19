#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from pyrogram import Client, filters
import re
import os
import asyncio
import imdb
from utils import get_filter_results, get_file_details
import pytz, datetime
import requests

API_KEY = os.environ.get("API_KEY")

BUTTONS = {}
BOT = {}
SEND_CHANNEL = int(os.environ.get("SEND_CHANNEL"))
SEND_USERNAME = os.environ.get("SEND_USERNAME")
FILE_CAP = """<b>Hey 👋 {} ⚡🔥</b>

<code>{} [{}]</code>

🔰 ʙᴇᴄᴀᴜsᴇ ᴏꜰ ᴄᴏᴘʏʀɪɢʜᴛ ᴛʜɪs ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ꜰʀᴏᴍ ʜᴇʀᴇ ᴡɪᴛʜɪɴ 20 ᴍɪɴᴜᴛᴇs
sᴏ ꜰᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ᴀɴʏᴡʜᴇʀᴇ ʙᴇꜰᴏʀᴇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ!

<i>കോപ്പിറൈറ്റ് ഉള്ളതുകൊണ്ട് ഈ ഫയൽ 20 മിനിറ്റിനുള്ളിൽ ഇവിടെനിന്നും ഡിലീറ്റ് ആകുന്നതാണ്
അതുകൊണ്ട് ഇവിടെ നിന്നും മറ്റെവിടെക്കെങ്കിലും മാറ്റിയതിന് ശേഷം ഡൗൺലോഡ് ചെയ്യുക!</i>

<b>✅ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : {}</b>
"""
autofiltercaption = """<b>🎬 Title : {}
                            
📆 Release : {}
🌟 Rating : {}/10
⏱ Duration : {} minutes
🎭 Genres : {}
👤 Requested BY : {}</b>
"""

MAX_LIST_ELM = int(5)
def list_to_str(k):
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    elif MAX_LIST_ELM:
        k = k[:int(MAX_LIST_ELM)]
        return ' '.join(f'{elem}, ' for elem in k)
    else:
        return ' '.join(f'{elem}, ' for elem in k)
    
@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{file.file_name}"
                filesize = f"[{get_size(file.file_size)}] "
                btn.append(
                    [InlineKeyboardButton(text=f"■ {filesize} - {filename}", callback_data=f"subinps#{file_id}")]
                )
        else:
            google_keyword = search.replace(" ", "+")
            msg = await message.reply_text(text="""
                <b>Hello {} I could not find the movie you asked for 🥲

Click on buttons below to search on google or IMDb</b>
                  """.format(message.from_user.mention),
                 reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('🌟 IMDB 🌟', url='https://imdb.com'),
                        InlineKeyboardButton('⚡ GOOGLE ⚡️', url=f'https://www.google.com/search?q={google_keyword}')
                    ],
                    [
                        InlineKeyboardButton("😐 Nonsense 😐", callback_data="no_results")
                    ]
                ]
            )
        )
            await asyncio.sleep(20)
            await message.delete()
            await msg.delete()
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ 🔒",callback_data="close")])

            search = message.text
            ia = imdb.IMDb()
            movies = ia.search_movie(search)
            if movies:
                id = movies[0].getID()
                movie = ia.get_movie(id)
                title = movie['title']
                runtime = list_to_str(movie['runtime'])
                rating = movie['rating']
                year = movie['year']
                genre = list_to_str(movie['genres'])
                plo = movie['plot']
                plot = plo[0]
                language = movie['languages']
                director = movie['director']
                stars = list_to_str(movie['cast'])
                fileid = movies[0].get_fullsizeURL()
                mention = message.from_user.mention
                chat = message.chat.title
                dell = await message.reply_photo(photo=fileid, caption=autofiltercaption.format(title, year, rating, runtime, genre, mention), reply_markup=InlineKeyboardMarkup(buttons))  
                await asyncio.sleep(3000)
                await dell.delete()
   
            else:
                del1 = await message.reply_text(f"""<b>Hey 👋 {message.from_user.mention} 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(3000)
                await del1.delete()
               
        btns = list(split_list(btn, 10)) 
        keyword = f"{message.chat.id}-{message.id}"
        BUTTONS[keyword] = {
            "total" : len(btns),
            "buttons" : btns
        }
        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="ɴᴇxᴛ ☞",callback_data=f"next_0_{keyword}")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ 🔒",callback_data="close")])
         
        search = message.text
        ia = imdb.IMDb()
        movies = ia.search_movie(search)
        if movies:
            id = movies[0].getID()
            movie = ia.get_movie(id)
            title = movie['title']
            year = movie['year']
            rating = movie['rating']
            runtime = list_to_str(movie['runtime'])
            genre = list_to_str(movie['genres'])
            language = movie['languages']
            director = movie['director']
            stars = list_to_str(movie['cast'])
            fileid = movies[0].get_fullsizeURL()
            mention = message.from_user.mention
            chat = message.chat.title
            del2 = await message.reply_photo(photo=fileid, caption=autofiltercaption.format(title, year, rating, runtime, genre, mention), reply_markup=InlineKeyboardMarkup(buttons))  
            await asyncio.sleep(3000)
            await del2.delete()
   
        else:
            del3 = await message.reply_text(f"""<b>Hey 👋 {message.from_user.mention} 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
            reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(3000)
            await del3.delete()
     

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("☜ ʙᴀᴄᴋ", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ 🔒",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("☜ ʙᴀᴄᴋ", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ 🔒",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("ɴᴇxᴛ ☞", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ 🔒",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("☜ ʙᴀᴄᴋ", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ 🔒",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                mention = query.from_user.mention
                chat = query.message.chat.title
                m = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                time = m.hour

                if time < 12:
                    get="Good Morning"
                elif time < 15:
                    get="Good Afternoon"
                elif time < 20:
                    get="Good Evening"
                else:
                    get="Good Night"

                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption, time=get)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"""<b>Hey 👋 {query.from_user.mention} ⚡🔥</b>

<code>{title} [{size}]</code>

🔰 ʙᴇᴄᴀᴜsᴇ ᴏꜰ ᴄᴏᴘʏʀɪɢʜᴛ ᴛʜɪs ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ꜰʀᴏᴍ ʜᴇʀᴇ ᴡɪᴛʜɪɴ 20 ᴍɪɴᴜᴛᴇs
sᴏ ꜰᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ᴀɴʏᴡʜᴇʀᴇ ʙᴇꜰᴏʀᴇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ!

<i>കോപ്പിറൈറ്റ് ഉള്ളതുകൊണ്ട് ഈ ഫയൽ 20 മിനിറ്റിനുള്ളിൽ ഇവിടെനിന്നും ഡിലീറ്റ് ആകുന്നതാണ്
അതുകൊണ്ട് ഇവിടെ നിന്നും മറ്റെവിടെക്കെങ്കിലും മാറ്റിയതിന് ശേഷം ഡൗൺലോഡ് ചെയ്യുക!</i>

<b>✅ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : {query.chat.title}</b>"""
                buttons = [
                    [
                        InlineKeyboardButton('🔗 Join Here 😍🔥', url='https://t.me/MH_MAIN')
                    ]
                    ]
                
                await query.answer()
                filess = await client.send_cached_media(
                    chat_id=SEND_CHANNEL,
                    file_id=file_id,
                    caption=FILE_CAP.format(mention, title, size, chat),
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                
                
                humm = [[
                        InlineKeyboardButton("📥 Download Link 📥", url=f"{filess.link}")
                        ],[
                        InlineKeyboardButton("⚠️ Can't Access❓ Click Here ⚠️", url=f"https://t.me/{SEND_USERNAME}")
                        ]]
                reply_markup=InlineKeyboardMarkup(humm)
                msg1 = await query.message.reply(text=f"""<b>Hey 👋 {query.from_user.mention} 

📫 Yᴏʀ Fɪʟᴇ ɪꜱ Rᴇᴀᴅʏ 👇

📂 Mᴏᴠɪᴇ Nᴀᴍᴇ :</b> <code>{title}</code>

<b>⚙️ Mᴏᴠɪᴇ Sɪᴢᴇ : {size}</b>
""", reply_markup=reply_markup)
                await asyncio.sleep(1200)
                await filess.delete()
                await msg1.delete()
                
                return  
        


        elif query.data == "pages":
            await query.answer("No Use", show_alert=False)
        elif query.data == "close":
            try:
                await query.message.reply_to_message.delete()
                await query.message.delete()
            except:
                await query.message.delete()
        elif query.data == "no_results":
            await query.answer("സിനിമ ലഭിക്കണം എങ്കിൽ താങ്കൾ ഗൂഗിൾ നോക്കി സിനിമയുടെ correct spelling ഇവിടെ send ചെയ്യുക എങ്കിലേ താങ്കൾ ഉദ്ദേശിക്കുന്ന സിനിമ എനിക്ക് അയച്ചു തരാൻ കഴിയുകയുള്ളു 😊", show_alert=True)
                
    else:
        await query.answer("Not For You !",show_alert=True)
