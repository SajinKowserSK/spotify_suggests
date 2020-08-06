from auth_class import *
import requests
from urllib.parse import urlencode

## Stuff to put in git ignore file when making repo public
client_id = 'aaf30baaa7ca45878db0454df408e8a3'
client_secret = 'c1fd3a9cdc544005be49aef9e2ab3434'

token_url = "https://accounts.spotify.com/api/token"
method = "POST"

## performing authorization with auth class
spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token
auth_header = {
    "Authorization": f'Bearer {access_token}'
}

## endpoint (will always remain same for us), track_id should be changed dynamically
endpoint = 'https://api.spotify.com/v1/audio-features/'
track_id = '06AKEBrKUckW0KREUWRnvT'

## sample call
r = requests.get(endpoint+track_id, headers=auth_header)
print(r.json())