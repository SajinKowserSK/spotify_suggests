from auth_class import *
import sys
import requests

response = spotify.search("Rap Caviar", search_type="playlist")['playlists']['items']

## UNCOMENT TO GET THE ALBUM NAME, WITH ID AND TRACKS

# print(response)
# print(len(response))

# for key in response:
#     print(key['name'])
#     print(key)

tracks = "https://api.spotify.com/v1/playlists/37i9dQZF1DX0XUsuxWHRQd/tracks"
r = requests.get(tracks, headers=spotify.get_resource_header())
r = r.json()['items']
for key in r:
    track = key['track']
    if track is not None:
        print(track['name'])