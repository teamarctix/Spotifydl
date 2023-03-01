from pyrogram import Client, filters
import requests
from sub import *
import os
from time import time
import time
from datetime import datetime
from pytz import timezone

from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)


api_id = 3702208
api_hash = "3ee1acb7c7622166cf06bb38a19698a9"
bot_token = "5300188722:AAFlruACp00Hv2ZD1RPjE9P0FahI52swqpU"

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)



@app.on_message(filters.command("dl"))
async def start_command(client,message):
    chat_id = message.chat.id
    link = message.text
    if link[4:].startswith("https") or link.startswith("http"):
          if link.split( "/")[4] == "track" :
  
             ytlink = ytsq(link[4:])
             ytdl(ytlink[1])
      
             for name in os.listdir():
               if ytlink[0] in name: 
                await app.send_audio(chat_id, audio=name,caption=name)
                write(link[4:],name)
                os.system("rm '"+name+"'")

          else:
                 info =  dytdl(link[4:])
                 for name in os.listdir():
                     if info[0] in name:
                       if name.endswith("mp4"):
                         await app.send_video(chat_id, video=name,caption=name )
                       else:
                         await app.send_document(chat_id, document=name,caption=name )
                      write(link[4:],name)
                      if name.endswith("py") or name.endswith("csv"):
                       print("*****")
                      else:
                        os.system("rm '"+name+"'")
             
    else:
           await app.send_message(channel_id,"Link Not Vaild!!!!")








@app.on_message(filters.command("update"))
async def start_command(client,message):
         cdid= message.chat.id
         button_list =[]
         for each in pread():
             button_list.append([InlineKeyboardButton(each[1], callback_data =str(each[2]))]) 
             reply_markup=InlineKeyboardMarkup(button_list)
         await app.send_message(
            cdid,"Select The Required Playlist:",reply_markup=reply_markup)





@app.on_callback_query()
async def answer(client, call):
          msgid = call.message.id
          chat = call.message.chat.id
          print(chat,msgid)
          await app.edit_message_text(chat,msgid,"Update Started!!!")
          playlist_id = call.data
          URL2 = "https://api.spotify.com/v1/playlists/"+ playlist_id +"?access_token=" + token 
          r2 = requests.get(URL2)
          img = r2.json()['images'][0]['url']
          df = r2.json()['name']
          total = r2.json()['tracks']['total']
          now=datetime.now()
          crtda = now.strftime('%m/%d %I:%M:%S %p')
          if os.getcwd().endswith("Spotdl"):
             os.system("mkdir " + df)
          else:
             os.chdir("../")
             os.system("mkdir " + df)
          stats =  f'<b>├  Playlist Name: </b>{df}\n'\
                        f'<b>├  Total No Of Songs: </b>{total}\n'\
                        f'<b>╰ Updated Time: </b>{crtda}\n\n'
          os.chdir(df)
          await app.send_photo(chat,photo=img,caption=stats)
          os.system("spotdl https://open.spotify.com/playlist/"+playlist_id)
          for filename in os.listdir():
              if filename.endswith(".mp3"):
                await app.send_audio(chat, audio=filename,caption=filename)



async def main():
   async with app:
             channel_id = -1001861533379
             #await app.send_message(channel_id,"Playlist!")
             for id in pread():
               playlist_id = id[0][34:].split('?')[0]
               URL2 = "https://api.spotify.com/v1/playlists/"+ playlist_id +"?access_token=" + token 
               r2 = requests.get(URL2)
               img = r2.json()['images'][0]['url']
               df = r2.json()['name']
               total = r2.json()['tracks']['total']
               now=datetime.now()
               crtda = now.strftime('%m/%d %I:%M:%S %p')
               # print(os.getcwd())
               if os.getcwd().endswith("SpidySpotdl"):
                    os.system("mkdir " + df)
               else:
                    os.chdir("../")
                    os.system("mkdir " + df)
               stats = f'<b>├  Playlist Name: </b>{df}\n'\
                           f'<b>├  Total No Of Songs: </b>{total}\n'\
                           f'<b>╰ Updated Time: </b>{crtda}\n\n'
               os.chdir(df)
               await app.send_photo(channel_id,photo=img,caption=stats)
               os.system("spotdl "+id[0])
               for filename in os.listdir():
                  if filename.endswith(".mp3"):
                   #print(filename)
                   await app.send_audio(channel_id, audio=filename,caption=filename)










@app.on_message(filters.command("add"))
async def start_command(client,message):
    link = message.text[5:]
    pwrite(link)
    await message.reply("Added Playlist!")
    



@app.on_message(filters.command("list"))
async def start_command(client,message):
        cdid= message.chat.id
        if "playlist.csv" in os.litdir():
         pylnames =[]
         for  pyname in pread():
             pylnames.append([InlineKeyboardButton(pyname[1], callback_data =str(pyname[2]))]) 
             reply_markup=InlineKeyboardMarkup(pylnames)
         list = await app.send_message(
            cdid,"Playlists:",reply_markup=reply_markup)
         time.sleep(5)
         msgid =list.id
         chat = list.chat.id
         await app.delete_messages(chat,msgid)
       else:
          await app.send_message(
            cdid,"Playlist Can't be Found!!\n\
                  Try Adding A Playlist\",)





app.run(main())  # Automatically start() and idle()
