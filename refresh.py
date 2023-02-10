import requests 
from urllib.parse import urlencode
import base64,csv
client_id = "157ea601d4e04eb487df842f1fbb3fa3"
client_secret = "7ea9beec487d46d98295a21c96a29dad"
f = open ('token.csv','r')
cread=csv.reader(f)
for i in cread:
 code=i[2]
encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")


token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}



token_data = {
    "grant_type": "refresh_token",
    "refresh_token": code,
    "redirect_uri": "http://localhost:7777/callback"
}


def retk():
     r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
     token = r.json()["access_token"]
     return token

