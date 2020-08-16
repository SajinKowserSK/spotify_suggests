from auth_class import *
from query import *
import requests
from urllib.parse import urlencode
import random
import pandas as pd
import sys
db_df = pd.read_csv("1. Songs Analyzed.csv")
db_df = pd.DataFrame(db_df)
randomSongs = []

print(db_df.iloc[0]['id'])
######################### generating 3 random song id indices
for x in range(0, 3):
    i = random.randint(0, 430)

    while i in randomSongs:
        i = random.randint(0, 430)

    randomSongs.append(i)

######################### getting the random songs by ID
for x in range(0, 3):
    i = random.randint(0, 430)

    while i in randomSongs:
        i = random.randint(0, 430)

    randomSongs.append(i)

randomSongID = []
for x in range (0, len(randomSongs)):
    randomSongID.append(db_df.iloc[randomSongs[x]]['id'])


######################### deleting them from db
db_df = db_df.drop([db_df.index[randomSongs[0]], db_df.index[randomSongs[1]], db_df.index[randomSongs[2]]])
db_df = db_df.reset_index(drop=True)


######################### getting user ratings or "stars"
stars = []
for x in range (0, len(randomSongID)):
    getTrack(randomSongID[x])
    response = int(input("Please rate this song out of 5"))
    stars.append(response)


######################### creating user profile with audio analysis on songs THEY RATED
endpoint = 'https://api.spotify.com/v1/audio-features/'
track_id = randomSongID

i = 0
songNum = 0
colNames = []

for song in track_id:
    r = requests.get(endpoint + song, headers=auth_header)

    names = []
    rate = stars[songNum]
    data = []

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
                            data[5], data[6], data[7], data[8], data[9]]], columns=names)

        df = pd.DataFrame([[data[0] * rate, data[1] * rate, data[2] * rate, data[3] * rate, data[4] * rate,
                            data[5] * rate, data[6] * rate, data[7] * rate, data[8] * rate, data[9] * rate]], columns=names)
        i = i +1
        colNames = names
    else:

        track2 = pd.DataFrame([[data[0], data[1], data[2], data[3], data[4],
                                data[5], data[6], data[7], data[8], data[9]]], columns=names)

        df2 = pd.DataFrame([[data[0] * rate, data[1] * rate, data[2] * rate, data[3] * rate, data[4] * rate,
                            data[5] * rate, data[6] * rate, data[7] * rate, data[8] * rate, data[9] * rate]], columns=names)

        df = df.append(df2, ignore_index=True)

    songNum += 1

# print(df)

######################### creating user profile with audio analysis on songs THEY RATED
user_profile = df.sum(axis=0)
user_profile = pd.DataFrame(user_profile, columns=['Value Totals'])
user_profile['Weighted_Values'] = 0

user_profile_totals = user_profile['Value Totals'].sum()

rowNum = 0
NEW_COL = 1
OLD_COL = 0

# creating a new column with the weighted values for each feature based on user profile
for index, row in user_profile.iterrows():
    user_profile.iloc[rowNum, NEW_COL] = user_profile.iloc[rowNum, OLD_COL] / user_profile_totals
    rowNum += 1

# creating the matrix / row with user's preferred values for each feature
weighted_mtx = user_profile['Weighted_Values'].to_list()
track1_mtx = track1.values.tolist()[0]
track2_mtx = track2.values.tolist()[0]

print(weighted_mtx)
print(track1_mtx, '\n')

prediction_vals = []

for x in range(0, len(weighted_mtx)):
    prediction_vals.append(weighted_mtx[x] * track1_mtx[x])


print('chance as decimal user will like song')
print(sum(prediction_vals))

for x in range(0, len(prediction_vals)):
    print(colNames[x] + " val is " + str(prediction_vals[x]))

print("\n", "\n")

prediction_vals = []
for x in range(0, len(weighted_mtx)):
    prediction_vals.append(weighted_mtx[x] * track2_mtx[x])

print('chance as decimal user will like song')
print(sum(prediction_vals))

for x in range(0, len(prediction_vals)):
    print(colNames[x] + " val is " + str(prediction_vals[x]))

for x in range(0, len(track1_mtx)):
    print("Track 1 Feature Val is " + str(track1_mtx[x]))

# code to convert to dataframe
# weighted_matrix = [weighted_matrix]
# weighted_matrix = pd.DataFrame(weighted_matrix, columns=colNames)
