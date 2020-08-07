import pandas as pd

lst = [0.007138845215558036, 0.002916036774490655, 0.030249344133720494, -0.2590674828988358, 0.0060498688267440984, 0.0004397044663277611, 0.004677758576838537, 0.005603146512577314, 0.0014229291480502121, 0.0032669291664418135, 1.197302920078087]
names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
mtx = [lst]

df = pd.DataFrame(mtx, columns=names)


for x in range (0, 10000):
    print(x)