from pyrogram import Client, filters
import requests
from sub import *
import os
from time import time
import time
from datetime import datetime, timedelta
from pytz import *
import pytz
import threading

from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)





uploads ={"up":0}

api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
bot_token = "6593397412:AAFmJ8Hj9jnZuvLs_rLcu63bQwCp0EV829w"

app = Client(
    "Music_Bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)



def progress(current, total):
    print(f"{current * 100 / total:.1f}%")


def pread():
   global cread
   filec = open("playlist.txt","r")
   cread=csv.reader(filec)
   return cread




def pldl(app,playlist,channel_id):
    command = f"python -m spotdl --headless --threads 10 --format mp3 --archive songs.txt {playlist}"
    os.system(command)
    time.sleep(10)
    filenames = [file for file in os.listdir() if file.endswith(".mp3")]
    print(filenames)
    for filename in filenames:
                try:
                    app.send_audio(channel_id, audio=filename,progress=progress)
                    os.remove(filename)
                    uploads["up"]+=1
                except Exception as e:
                      print(e)

def main():
   with app:
                crtda = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%m/%d %H:%M:%S%p")
                channel_id = -1002034630043
                txt = f'Status : </b>Uploading\n'\
                      f'Updated Time: </b>{crtda}\n\n'
                start = app.send_message(channel_id,txt)
                playlists = pread()
                for playlist in playlists:
                        pldl(app,playlist[0],channel_id)
                

                t = f'Status : </b>Upload Completed\n'\
                    f'Total Songs : </b>{uploads["up"]}\n\n'
                app.edit_message_text(channel_id,start.id,t)
                exit()
                

app.run(main())  # Automatically start() and idle()
