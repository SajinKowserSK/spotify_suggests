from auth_class import *
import requests
import pandas as pd



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


# This will be a dynamic list of songs that we find, for now we have two, this just dynamically adds the songs data, to the matrix in a formatted way
track_id = [
'06AKEBrKUckW0KREUWRnvT',
'6rqhFgbbKwnb9MLmUQDhG6'
]

i = 0

for song in track_id:
    r = requests.get(endpoint + song, headers=auth_header)
    names =  []

    #we would get this answer from the front end.
    rate = int(input("What do you rate this song, out of 5: "))

    data = []
    for keys in r.json():
        if(keys=="type"):
            break
        names.append(keys)
        data.append(float(r.json()[keys]))


    if i == 0:
        #creating the data frame for the first time
        df = pd.DataFrame([[   data[0]*rate, data[1]*rate,data[2]*rate,data[3]*rate,data[4]*rate,data[5]*rate,data[6]*rate,data[7]*rate,data[8]*rate,data[9]*rate,data[10]*rate]  ], columns=names)
        i = i +1
    else:
        df2 = pd.DataFrame([[data[0]*rate, data[1]*rate, data[2]*rate, data[3]*rate, data[4]*rate, data[5]*rate, data[6]*rate, data[7]*rate, data[8]*rate, data[9]*rate, data[10]*rate]],columns=names)
        df = df.append(df2, ignore_index=True)

print(df)
print(df.sum(axis=0))



