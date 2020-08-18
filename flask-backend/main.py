import flask
from flask import Flask, render_template, request, jsonify
import requests
from requests import request
import pandas as pd
import random
from random import randint
from brute_force_script import *

app = Flask(__name__)

@app.route("/")
def my_index():
    return render_template("index.html", token="Hello Flask + React")

@app.route("/ep" ,methods=['POST', 'GET'])
def ep():

    # sending random songs to front end
    if request.method == "GET":
        db_df = pd.read_csv("1. Songs Analyzed.csv")
        result = getRandomSongs(db_df)
        result["ratings"] = []
        result["finalSong"] = []

        # now json structure should be
        # {
        # "randomSongs": [int, int, int],
        #  "dataframe": dataFrameObject probs in form of dict
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
        #  "dataframe": dataFrameObject probs in form of dict
        #  "ratings": [int, int, int]
        #  "finalSong": [int]
        #  }

        return jsonify(data)





@app.route("/time")
def get_current_time():
    return {'time':10}


app.run(debug=True)