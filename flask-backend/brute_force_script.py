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

# just using these as dummy values rn so I don't have to add in user input everytime (commented out user rate)
stars = [4,5]
songNum = 0
for song in track_id:
    r = requests.get(endpoint + song, headers=auth_header)

    names =  []

    #we would get this answer from the front end.
    # rate = int(input("What do you rate this song, out of 5: "))

    rate = stars[songNum]
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

    songNum += 1

## now we have a user profile (unweighted)
print(df)

user_profile = df.sum(axis=0)
user_profile = pd.DataFrame(user_profile, columns=['Values'])
user_profile['Weighted_Values'] = 0

# gets the total of values, we must now divide each feature val by this total
user_profile_totals = user_profile['Values'].sum()

rowNum = 0
NEW_COL = 1
OLD_COL = 0

# creating a new column with the weighted values for each feature based on user profile
for index, row in user_profile.iterrows():
    user_profile.iloc[rowNum, NEW_COL] = user_profile.iloc[rowNum, OLD_COL] / user_profile_totals
    rowNum += 1

print(user_profile)
print('\n', user_profile['Weighted_Values'].sum())


