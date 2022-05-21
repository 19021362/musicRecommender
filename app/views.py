from smtpd import MailmanProxy
from this import s
from tkinter import Frame
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from matplotlib.style import context
from .models import *
from .mlmodel import *
from django.forms.models import model_to_dict

import os

from scipy.spatial.distance import cdist


import pickle
import numpy as np 
import pandas as pd 
from django.shortcuts import render
from django.contrib import messages

from app import mlmodel 


data = pd.read_csv("app/tracks_features.csv")
data['unique'] = data['name'] + data['artists']
data = data.drop_duplicates(subset='unique', keep='first')

def home(request):
    #sample_list = request.session.get('sample_list')
    sample_list_model = Sample.objects.all()
    sample_list = []
    for s in sample_list_model:
        sample_list.append(model_to_dict(s))

    request.session['sample_list'] = sample_list

    context = {
        'sample_list': sample_list,
    }

    return render(request, 'index.html', context)


def recommendation_detail(request, sample_id):
    recommender = pickle.load(open('app/mlmodel.sav','rb'))
    play_list = Song_Sample.objects.filter(sample_id = sample_id)
    # sample_list_model = Sample.objects.all()
    # sample_list = []
    # for s in sample_list_model:
    #     sample_list.append(model_to_dict(s))
    #print(sample_list)

    year_list = []
    rec_songs_id = request.session.get('rec_songs_id')
    #print(play_list)
    song_play_id = find_song_id(name=play_list[0])
    url = "https://open.spotify.com/embed/track/" + song_play_id + "?utm_source=generator"

    play_list_id = find_song_list_id(song_list=play_list)
    n_songs = 10
    
    metadata_cols = ['name', 'id', 'artists']
    
    song_center = get_mean_vector(play_list, data)
    scaler = model.steps[0][1]
    scaled_data = scaler.transform(data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    rec_songs = data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(play_list)]
    rec_songs_id = find_rec_list_id(song_list=rec_songs['id'])
    
    #print(rec_songs_id)
    sample_list =  request.session.get('sample_list')
    request.session['rec_songs_id'] = rec_songs_id
    request.session['sample_id'] = sample_id

    context = {
        'sample_list': sample_list,
        'song_list' : play_list_id,
        'year_list' : year_list,
        'recommend_list' : rec_songs_id,
        'url' : url
    }

    return render(request, 'index.html', context)
    

def choose_song(request, id):
    recommender = pickle.load(open('app/mlmodel.sav','rb'))
    sample_id = request.session.get('sample_id')
    song_list = Song_Sample.objects.filter(sample_id = sample_id)
    year_list = []
    # sample_list_model = Sample.objects.all()
    # sample_list = []
    # for s in sample_list_model:
    #     sample_list.append(model_to_dict(s))
    
    url = "https://open.spotify.com/embed/track/" + id + "?utm_source=generator"

    song_list_id = find_song_list_id(song_list=song_list)
    sample_list =  request.session.get('sample_list')
    rec_songs_id = request.session.get('rec_songs_id')

    context = {
        'sample_list': sample_list,
        'song_list' : song_list_id,
        'year_list' : year_list,
        'recommend_list' : rec_songs_id,
        'url' : url
    }

    return render(request, 'index.html', context)


def add_song_playlist(request, id):
    sample_id = request.session.get('sample_id')
    song = Song.objects.get(id=id)
    sample = Sample.objects.get(id=sample_id)
    sample_song = Song_Sample(song=song, sample=sample)
    sample_song.save()

    return recommendation_detail(request=request, sample_id=sample_id)


def remove_song_playlist(request, id):
    sample_id = request.session.get('sample_id')
    song = Song.objects.get(id=id)
    sample = Sample.objects.get(id=sample_id)
    Song_Sample.objects.filter(song=song, sample=sample).first().delete()
    
    return recommendation_detail(request=request, sample_id=sample_id)
