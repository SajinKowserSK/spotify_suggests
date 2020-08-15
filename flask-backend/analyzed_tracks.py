from auth_class import *
import requests
import pandas as pd
from query import *
from urllib.parse import urlencode

## endpoint (will always remain same for us), track_id should be changed dynamically
endpoint = 'https://api.spotify.com/v1/audio-features/'

# This will be a dynamic list of songs that we find, for now we have two, this just dynamically adds the songs data, to the matrix in a formatted way
track_id = track_id_final
songNum = 0

i = 0
for song in track_id:
    r = requests.get(endpoint + song, headers=auth_header)

    names =  ['id']

    #we would get this answer from the front end.
    # rate = int(input("What do you rate this song, out of 5: "))

    rate = 1
    data = [song]

    for keys in r.json():
        if keys == "type":
            break

        elif keys == "type" or keys == "duration_ms" or keys == "tempo":
            continue

        if keys == "key":
            names.append(keys)
            val = abs(float(r.json()[keys])) / 12
            data.append(val)


        elif keys == "loudness":
            names.append(keys)
            val = abs(float(r.json()[keys])) / 60
            data.append(val)

        else:
            names.append(keys)
            data.append(float(r.json()[keys]))

    if i == 0:
        #creating the data frame for the first time

        track1 = pd.DataFrame([[data[0], data[1], data[2], data[3], data[4],
                            data[5], data[6], data[7], data[8], data[9], data[10]]], columns=names)

        df = pd.DataFrame([[data[0], data[1] , data[2] , data[3] , data[4],
                            data[5] , data[6] , data[7], data[8], data[9], data[10]]], columns=names)
        i = i +1
        colNames = names
    else:

        track2 = pd.DataFrame([[data[0], data[1] , data[2] , data[3] , data[4],
                            data[5] , data[6] , data[7], data[8], data[9], data[10]]], columns=names)

        df2 = pd.DataFrame([[data[0], data[1] , data[2] , data[3] , data[4],
                            data[5] , data[6] , data[7], data[8], data[9], data[10]]], columns=names)

        df = df.append(df2, ignore_index=True)

    print(songNum)
    songNum += 1

## now we have a user profile (unweighted)
print(df)
df.to_csv("1. Songs Analyzed.csv", header=True, index=False)

