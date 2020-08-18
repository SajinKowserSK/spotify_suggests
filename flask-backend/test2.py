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

        # result will be in form {"randomSongs": randomSongID, "dataframe":db_df}
        result = getRandomSongs(db_df)
        result["ratings"] = []
        result["finalSong"] = []

        # now json structure should be
        # {
        # "randomSongs": [int, int, int],
        #  "dataframe": dataFrameObject in form of dict
        #  "ratings": []
        #  "finalSong": []
        #  }
        return jsonify(result)

    # receiving ratings from front-end
    if request.method == "POST":
        data = request.json()
        ratings = data["ratings"]
        data["finalSong"] = ratings[0]

        # now json structure should be
        # {
        # "randomSongs": [int, int, int],
        #  "dataframe": dataFrameObject in form of dict
        #  "ratings": [int, int, int]
        #  "finalSong": [int]
        #  }

        return jsonify(data)