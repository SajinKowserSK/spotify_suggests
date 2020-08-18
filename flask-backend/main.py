import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from auth_class import *

app = Flask(__name__)
app.secret_key = "shafibullah"
app.run(debug=True)

@app.route("/")
def my_index():
    return render_template("index.html", token="Hello Flask + React")

@app.route("/testEP", methods = ["GET", "POST"])
def testEP():
    if request.method == "GET":
        return "HELLO WORLD new 3"

    else:
        return "else case"


@app.route('/ep_simple',methods=['GET', 'POST'])
def ep_simple():

    # sending random songs to front end
    if request.method == "GET":
        db_df = pd.read_csv("1. Songs Analyzed.csv")

        result = getRandomSongs(db_df)

        # now json structure should be
        # {
        # "randomSongs": [int, int, int],
        #      "deleteTracks": [
        #         71,
        #         232,
        #         202
        #     ],
        #  "ratings": []
        #  "finalSong": []
        #  }
        return jsonify(result)

    # receiving ratings from front-end
    elif request.method == "POST":
        data = request.json
        ratings = data["ratings"]
        data["finalSong"] = ratings[0]

        # delete the tracks
        randomSongs = data["deleteTracks"]

        db_df = pd.read_csv("1. Songs Analyzed.csv")
        db_df = pd.DataFrame(db_df)

        db_df = db_df.drop([db_df.index[randomSongs[0]], db_df.index[randomSongs[1]], db_df.index[randomSongs[2]]])
        db_df = db_df.reset_index(drop=True)

        # now json structure should be
        # {
        # "randomSongs": [int, int, int],
        #      "deleteTracks": [
        #         71,
        #         232,
        #         202
        #     ],
        #  "ratings": [int, int, int]
        #  "finalSong": [int]
        #  }
        return jsonify(data)
# endpoint where axios will make the get and post requests
@app.route("/ep", methods=['POST', 'GET'])
def ep():
    # sending random songs to front end
    if request.method == "GET":
        db_df = pd.read_csv("1. Songs Analyzed.csv")
        result = getRandomSongs(db_df)
        return jsonify(result)

    elif request.method == "POST":
        json_data = request.json
        ratings = json_data["ratings"]
        # delete the tracks
        randomSongs = json_data["deleteTracks"]
        db_df = pd.read_csv("1. Songs Analyzed.csv")
        db_df = pd.DataFrame(db_df)
        db_df = db_df.drop([db_df.index[randomSongs[0]], db_df.index[randomSongs[1]], db_df.index[randomSongs[2]]])
        db_df = db_df.reset_index(drop=True)


        endpoint = 'https://api.spotify.com/v1/audio-features/'
        track_id = json_data["randomSongs"]
        i = 0
        songNum = 0
        stars = ratings

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
                # creating the data frame for the first time


                df = pd.DataFrame([[data[0] * rate, data[1] * rate, data[2] * rate, data[3] * rate, data[4] * rate,
                                    data[5] * rate, data[6] * rate, data[7] * rate, data[8] * rate, data[9] * rate]],
                                  columns=names)
                i = i + 1

            else:

                df2 = pd.DataFrame([[data[0] * rate, data[1] * rate, data[2] * rate, data[3] * rate, data[4] * rate,
                                     data[5] * rate, data[6] * rate, data[7] * rate, data[8] * rate, data[9] * rate]],
                                   columns=names)

                df = df.append(df2, ignore_index=True)

            songNum += 1

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

        # user's preferred vals
        preferred_vals = user_profile['Weighted_Values'].to_list()
        result = analyze(preferred_vals, db_df)
        result_song_id = result['id']

        json_data['finalSong'] = result_song_id

        return jsonify(json_data)

@app.route("/time")
def get_current_time():
    return {'time':10}


