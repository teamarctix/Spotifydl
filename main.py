from pyrogram import Client, filters
import requests
from sub import *
import os
from time import time
import time
from datetime import datetime, timedelta
from pytz import *
import pytz

from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)


api_id = 3702208
api_hash = "3ee1acb7c7622166cf06bb38a19698a9"
bot_token = "6751694050:AAEPfuYWXDq5OL_jQiqzacooOtcsC9AxA8U"

app = Client(
    "Music_Bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)




def main():
   with app:
                crtda = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%m/%d %H:%M %p")
                channel_id = -1002143076171
                txt = f'Status : </b>Uploading\n'\
                    f'Updated Time: </b>{crtda}\n\n'
                app.edit_message_text(channel_id,2,txt)
                playlists = pread()
                for id in playlists:

                      playlist_id = id[0][34:].split('?')[0]
                      URL2 = "https://api.spotify.com/v1/playlists/"+ playlist_id +"?access_token=" + token 
                      r2 = requests.get(URL2)

                      img = r2.json()['images'][0]['url']
                      df = r2.json()['name']
                      total = r2.json()['tracks']['total']

                      items,up= getplay(id[0],app,channel_id)
                txt = f'Status : </b>Upload Completed\n'\
                      f'Total Songs : </b>{up}\n\n'
                app.edit_message_text(channel_id,2,txt)
                exit()
                  






app.run(main())  # Automatically start() and idle()
