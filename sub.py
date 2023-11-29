from youtubesearchpython import *
import yt_dlp
import json,csv,os
import requests
import subprocess
from refresh import *


token=retk()


def plnm(playlistlink):
           playlist_id = playlistlink[34:].split('?')[0]
           URL = "https://api.spotify.com/v1/playlists/" + playlist_id  + "/tracks?access_token=" + token
           r = requests.get(url = URL) 
           items= r.json()['items']
           return items


def gettrack(track):
     global token
     URL = "https://api.spotify.com/v1/tracks/" + track + "?access_token=" + token
     r = requests.get(url = URL)
     data = r.json()
     title  = data['name']
     artist = [artists["name"] for artists in data["artists"]]
     img = data['album']['images'][0]['url']
     return title,artist,img 



def rclone(name,name2):
    rcl = "rclone --config './rclone.conf' copy '" +name+ "' 'Mirror:/Bot/"+ name2 +"'"
    print(rcl)
    os.system(rcl)




def write(name,id):
  with open("songs.txt","a+") as filec:
           cwrite = csv.writer(filec)
           cwrite.writerow([name,id])


def read():
   try:
      filec = open("songs.txt","r")
      cread=csv.reader(filec)
      links =[link[0] for link in cread]
   except:
      links = []
   return links




 
def ytsq(link):
   tkid=link.split("/")[4].split("?")[0]

   videosSearch = VideosSearch(gettrack(tkid)[0], limit = 1)
   #print(gettrack(tkid)[0])
   #print(videosSearch.result()['result'][0]['link'])
   id = videosSearch.result()['result'][0]['id']
   link = videosSearch.result()['result'][0]['link']
   return id , link

def ytsn(query):
   videosSearch = VideosSearch(query, limit = 1)
   #print(videosSearch.result()['result'])
   id = videosSearch.result()['result'][0]['id']
   link = videosSearch.result()['result'][0]['link']
   title = videosSearch.result()['result'][0]['title']
   img = videosSearch.result()['result'][0]['thumbnails'][0]['url']
   return id , link , title , img 

def dytdl(link):
      ytdl = yt_dlp.YoutubeDL()
      ytdl.download(link)
      info=ytdl.extract_info(link)
      id = info['id']
      return id 

def urlytdl(link):
      ydl_opts = {'format': 'mp4/240/best',
  }
      ytdl = yt_dlp.YoutubeDL(ydl_opts)
      info= ytdl.extract_info(link,download=False)
      return info




def ytdl(link):
   ytlink = [ link ] 
   ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }]
      }
   with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(ytlink)


def pwrite(playlistlink):
  playlist_id = playlistlink[34:].split('?')[0]
  URL2 = "https://api.spotify.com/v1/playlists/"+ playlist_id +"?access_token=" + token  
  r2 = requests.get(URL2)
  pyname = r2.json()['name']
  with open("playlist.csv","a+",newline='\n') as filec:
           cwrite = csv.writer(filec)
           cwrite.writerow([playlistlink,pyname, playlist_id])



def pread():
   global cread
   filec = open("playlist.txt","r")
   cread=csv.reader(filec)
   return cread


def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

def getplay(playlistlink,app,channel_id):
     totalup = 0
     playlist_id = playlistlink[34:].split('?')[0]
     URL = "https://api.spotify.com/v1/playlists/" + playlist_id  + "/tracks?access_token=" + token
     URL2 = "https://api.spotify.com/v1/playlists/"+ playlist_id +"?access_token=" + token  
     r2 = requests.get(URL2)
     pyname = 'Playlist/' + r2.json()['name'] + "'"
     r = requests.get(url = URL)
     total = r.json()['total']
     count=0
     y=False

     while not y:  
      try:
            items = r.json()['items']
            for i in range(len(items)):
               
                        details = gettrack(r.json()['items'][i]["track"]["external_urls"]["spotify"].split("/")[-1])
                        title  = details[0]
                        file = title +"-"+",".join(details[1])
                        count +=1


                        if not r.json()['items'][i]["track"]["external_urls"]["spotify"] in read():
                           spotify_url = r.json()['items'][i]["track"]["external_urls"]["spotify"]
                           command = f"python -m spotdl --headless --threads 10  --format mp3 --archive songs.txt {spotify_url}"
                           os.system(command)
                           filenames = [file for file in os.listdir() if file.endswith(".mp3") and title in file]
                           if len(filenames)>0:
                                 filename = filenames[0]
                                 img = str(hash(filename))+".jpg"
                                 os.system(f'wget -qq {details[2]} -O """{img}""" ')
                                 id = app.send_audio(channel_id, audio=filename,caption=filename[0:-4],thumb=img, progress=progress)
                                 print(f'''Downloaded & Uploaded {filename}''')
                                 totalup +=1
                                 os.remove(filename)
                                 os.remove(img)
                           else:
                              print(f'''{file} Not Avaliable''')
                              with open("Missing,txt","a+") as f:
                                 f.write(file+"\n")
                        else:
                           print(f'''{file} Already Exists''')
            else:
               if count == total and not r.json()['next']:
                  y = True
                  break
                  
            URL = r.json()['next'] +'&'+ "access_token=" + token
            r = requests.get(url = URL)
      except Exception as e:
             print("Oppps Something Happened\n",e)
             continue


     return items,totalup
