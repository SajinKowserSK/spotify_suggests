## This class provides all the helper methods we need to set up the API Authorization

import base64
import datetime
import requests
from urllib.parse import urlencode
import pandas as pd
import random

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def search(self, query, search_type='artist'):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def getTracks(self):
        headers = self.get_resource_header()
        endpoint = "'https://api.spotify.com/v1/playlists/37i9dQZF1DX0XUsuxWHRQd/tracks"
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()


def getTrack(id):
    track = requests.get("https://api.spotify.com/v1/tracks/" + str(id), headers=spotify.get_resource_header()).json()
    artist = track['artists'][0]['name']
    songName = track['name']
    print("Now playing", songName, "by", artist)


def analyze(preferred_vals, db):
    bestSong = {}
    bestSong['id'] = "None"
    bestSong['chance'] = 0

    counter = 0
    for index, row in db.iterrows():
        currSong_vals = db.iloc[counter].to_list()
        song_id = currSong_vals.pop(0)

        prediction_vals = []
        for x in range(0, len(preferred_vals)):
            prediction_vals.append(preferred_vals[x] * currSong_vals[x])


        curr_chance = sum(prediction_vals)
        # print("This is the vlaue of the best song " + str(curr_chance))
        if curr_chance > bestSong['chance']:
            bestSong['id'] = song_id
            bestSong['chance'] = curr_chance

        counter += 1
    print(bestSong)
    return bestSong

def getRandomSongs(db_df):
    db_df = pd.DataFrame(db_df)
    randomSongs = []
    for x in range(0, 3):
        i = random.randint(0, 430)
        while i in randomSongs:
            i = random.randint(0, 430)
        randomSongs.append(i)
    randomSongID = []
    for x in range(0, len(randomSongs)):
        randomSongID.append(db_df.iloc[randomSongs[x]]['id'])

    returnDict = {"ratings": [], "finalSong": [], "randomSongs": randomSongID, "deleteTracks": randomSongs}
    return returnDict


## Stuff to put in git ignore file when making repo public
client_id = 'key'
client_secret = 'key'

token_url = "https://accounts.spotify.com/api/token"
method = "POST"

## performing authorization with auth class
spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token
auth_header = {
    "Authorization": f'Bearer {access_token}'
}
