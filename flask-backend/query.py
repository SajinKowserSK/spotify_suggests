from auth_class import *
import sys
import requests

tracksList = []
test = [('RapCaviar', '37i9dQZF1DX0XUsuxWHRQd'),
('Most Necessary', '37i9dQZF1DX2RxBh64BHjQ'),
('Gold School', '37i9dQZF1DWVA1Gq4XHa6U'),
('Signed XOXO', '37i9dQZF1DX2A29LI7xHn1'),
("Feelin' Myself", '37i9dQZF1DX6GwdWRQMQpq'),
('I Love My Down South Classics', '37i9dQZF1DWYok9l1JL7GM'),
("Hip Hop Controller", "37i9dQZF1DWT5MrZnPU1zD"),
("Internet People: The Internet Money Takeover", "37i9dQZF1DX6OgmB2fwLGd"),
("Tear Drop", "37i9dQZF1DX6xZZEgC9Ubl"),
("Signed XOXO", "37i9dQZF1DX2A29LI7xHn1")
        ]

for elem in test:
    track = elem[0]
    track_id = elem[1]
    response = spotify.search(track, search_type="playlist")['playlists']['items']

    for key in response:
        if key['name'] == track and key['id'] == track_id:
            tracksList.append(key['tracks']['href'])


trackDict = {}

for tracks in tracksList:
    r = requests.get(tracks, headers=spotify.get_resource_header())
    r = r.json()['items']
    for key in r:
        track = key['track']
        if track is not None:
            if track['id'] not in trackDict:
                trackDict[track['id']] = track['name']

track_id_final = list(trackDict.keys())

