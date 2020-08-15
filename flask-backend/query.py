from auth_class import *

response = spotify.search("Go Crazy", search_type="track")['tracks']['items']
print(response)
print(len(response))

for key in response:
    print(key)