from smtpd import MailmanProxy
from tkinter import Frame
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from matplotlib.style import context
from .models import *
from .mlmodel import *

import os

from scipy.spatial.distance import cdist


import pickle
import numpy as np 
import pandas as pd 
from django.shortcuts import render
from django.contrib import messages

from app import mlmodel 


data = pd.read_csv("app/tracks_features.csv")


def recommendation_detail(request, sample_id):
    recommender = pickle.load(open('app/mlmodel.sav','rb'))
    play_list = Song_Sample.objects.filter(sample_id = sample_id)
    year_list = []
    
    song_play_id = find_song_id(name=play_list[0])
    url = "https://open.spotify.com/embed/track/" + song_play_id + "?utm_source=generator"

    play_list_id = find_song_list_id(song_list=play_list)
    n_songs = 10
    
    metadata_cols = ['name', 'year', 'artists']
    
    song_center = get_mean_vector(play_list, data)
    scaler = model.steps[0][1]
    scaled_data = scaler.transform(data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    rec_songs = data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(play_list)]

    rec_songs_id = find_song_list_id(song_list=rec_songs['name'])

    context = {
        'song_list' : play_list_id,
        'year_list' : year_list,
        'recommend_list' : rec_songs_id,
        'url' : url
    }

    # return render(request, 'index.html', {'recommend_list':rec_songs[metadata_cols].to_dict(orient='records')})
    return render(request, 'index.html', context)
    

def choose_song(request, sample_id, id):
    recommender = pickle.load(open('app/mlmodel.sav','rb'))
    song_list = Song_Sample.objects.filter(sample_id = sample_id)
    year_list = []
    
    url = "https://open.spotify.com/embed/track/" + id + "?utm_source=generator"

    song_list_id = find_song_list_id(song_list=song_list)
    n_songs = 10
    
    metadata_cols = ['name', 'year', 'artists']
    # song_dict = flatten_dict_list(song_list)
    
    song_center = get_mean_vector(song_list, data)
    scaler = model.steps[0][1]
    scaled_data = scaler.transform(data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    rec_songs = data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_list)]

    rec_songs_id = find_song_list_id(song_list=rec_songs['name'])

    context = {
        'song_list' : song_list_id,
        'year_list' : year_list,
        'recommend_list' : rec_songs_id,
        'url' : url
    }

    return render(request, 'index.html', context)