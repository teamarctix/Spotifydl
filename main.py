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
               stats = f'<b>├  Playlist Name: </b>{df}\n'\
                           f'<b>├  Total No Of Songs: </b>{total}\n'\
                           f'<b>╰ Updated Time: </b>{crtda}\n\n'
               await app.send_photo(channel_id,photo=img,caption=stats)
               os.system("python -m spotdl "+id[0])
               for filename in os.listdir():
                for urls in read():
                  if urls[0]==filename:
                    #print(urls[0])
                    #print(filename)
                    break
                else:
                    if filename.endswith(".mp3"):
                       #print(filename)
                       await app.send_audio(channel_id, audio=filename,caption=filename)
                       os.system(f'''rclone --config './rclone.conf' move  """{filename}"""  'Drive:/Music'  ''')
                       os.system(f"""rclone --config './rclone.conf' move "Drive:/Music" "TD:/Music" -vP --delete-empty-src-dirs --drive-server-side-across-configs=true """)
                       write(filename)
                       try:
                         os.remove(filename)
                       except:
                          print("File Moved I Guess")









app.run(main())  # Automatically start() and idle()
