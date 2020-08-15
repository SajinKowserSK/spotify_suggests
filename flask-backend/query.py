from auth_class import *
import sys
import requests

tracksList = []
test = [("RapCaviar", "37i9dQZF1DX0XUsuxWHRQd"),
        ("Most Necessary", "37i9dQZF1DX2RxBh64BHjQ"),
        ("Gold School", "37i9dQZF1DWVA1Gq4XHa6U"),
        ("Signed XOXO", "37i9dQZF1DX2A29LI7xHn1"),
        ("Feelin' Myself", "37i9dQZF1DX6GwdWRQMQpq"),
        ("I Love My '80s Hip-Hop", "37i9dQZF1DX2XmsXL2WBQd"),
        ("I Love My Down South Classics", "37i9dQZF1DWYok9l1JL7GM")
        ]

for elem in test:
    track = elem[0]
    track_id = elem[1]
    response = spotify.search(track, search_type="playlist")['playlists']['items']

    for key in response:
        if key['name'] == track and key['id'] == track_id:
            tracksList.append(key['tracks']['href'])

print(tracksList)
trackDict = {}
for tracks in tracksList:
    tracks = "https://api.spotify.com/v1/playlists/37i9dQZF1DX0XUsuxWHRQd/tracks"
    r = requests.get(tracks, headers=spotify.get_resource_header())
    r = r.json()['items']
    for key in r:
        track = key['track']
        if track is not None:
            print(track['name'])
            trackDict[track['name']] = track['id']

print(trackDict)