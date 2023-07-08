from youtubesearchpython import *
import yt_dlp
import json,csv,os
import requests
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
     track = data['name']
     sample= data['preview_url']
     img = data['album']['images'][0]['url']
     return track, sample, img 



def rclone(name,name2):
    rcl = "rclone --config './rclone.conf' copy '" +name+ "' 'Mirror:/Bot/"+ name2 +"'"
    print(rcl)
    os.system(rcl)




def write(name,id):
  with open("songs.txt","a+") as filec:
           cwrite = csv.writer(filec)
           cwrite.writerow([name,id])



def read():
   global cread
   filec = open("songs.txt","r")
   cread=csv.reader(filec)
   return cread
 
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




def getplay(playlistlink):
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
      items = r.json()['items']
      for i in range(len(items)):
         count +=1
         #print(count,r.json()['items'][i]["track"]["external_urls"]["spotify"])
         os.systen("yt_dlp -f 'bestaudio*[ext=mp3]' --downloader aria2c --download-archive songs.txt "+ytsq(r.json()['items'][i]["track"]["external_urls"]["spotify"])[1])
         for name in os.listdir():
           if ytsq(r.json()['items'][i]["track"]["external_urls"]["spotify"])[0] in name:
              #rclone(name,pyname)
              pass
      else:
         if count == total:
            y = True
            break
         URL = r.json()['next'] +'&'+ "access_token=" + token
         r = requests.get(url = URL)
     return items




