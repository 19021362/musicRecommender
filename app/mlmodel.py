#Run this in terminal: 
# pip3 install spotipy --upgrade

from asyncio.windows_events import NULL
from calendar import c
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numpy as np
import pandas as pd
import pickle

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist
from collections import defaultdict

import warnings
warnings.filterwarnings("ignore")


# data = pd.read_csv("/content/drive/MyDrive/Spotify-data/data.csv")

data = pd.read_csv("app\data.csv")
data['unique'] = data['name'] + data['artists']
data = data.drop_duplicates(subset='unique', keep='first')

client_id = "a8ef1499b1f3468d9ce3186629adae0c"
client_secret = "30423bf1520b4e00a5bc4e076fe870aa"

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def find_song_id(id):

    #results = sp.track(track_id=id)
    results = sp.track(track_id= '{}'.format(id))
    if results is None or results == {}:
        return None

    track_id = results['id']
    return track_id


def find_list_song(song_list):
    ls = []
    #print(song_list)
    for s in song_list:
        #results = sp.track(track_id=s)
        results = sp.track(track_id= '{}'.format(s))

        if results is None or results == {}:
            continue

        track_name = results['name']
        track_id = results['id']
        track_artist = results["artists"][0]["name"]
        track_pop = results["popularity"]
        ls.append({"name" : track_name, "id" : track_id, "artist" : track_artist, "popularity" : track_pop})

    return ls


def find_song(id):
    song_data = defaultdict()
    #results = sp.track(track_id=id)
    results = sp.track(track_id= '{}'.format(id))
    if results is None or results == {}:
        return None

    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [results['name']]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)

#cluster songs with kmean

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=20, 
                                   verbose=False))
                                 ], verbose=False)
model = song_cluster_pipeline

number_cols = ['valence', 'year', 'acousticness', 'danceability', 
    'duration_ms', 'energy', 'explicit',
    'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 
    'popularity', 'speechiness', 'tempo']

X = data[number_cols]
number_cols = list(X.columns)
model.fit(X)
song_cluster_labels = model.predict(X)
data['cluster_label'] = song_cluster_labels




def get_song_data(song, spotify_data):
    
    try:
        song_data = spotify_data[(spotify_data['id'] == str(song)) 
                                ].iloc[0]
        return song_data
    
    except IndexError:
        return find_song(str(song))
        
# Trong cai song_list nay chi co ten thoi
def get_mean_vector(song_list, spotify_data):
    
    song_vectors = []
    
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)  
    
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)


def flatten_dict_list(dict_list):

    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

pickle.dump(model, open('mlmodel.sav','wb'))
