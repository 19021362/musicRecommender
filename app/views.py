from re import S, T
import re
from smtpd import MailmanProxy
from this import s
from tkinter import E, Frame
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


search_cols = ['name', 'artists', 'id', 'popularity']
search_list = data[search_cols].sort_values(by=['popularity'], ascending=0)

def home(request):
    #sample_list = request.session.get('sample_list')
    sample_list_model = Sample.objects.all()
    sample_list = []
    for s in sample_list_model:
        sample_list.append(model_to_dict(s))

    request.session['sample_list'] = sample_list

    context = {
        'sample_list': sample_list
    }

    return render(request, 'index.html', context)


def recommendation_detail(request, sample_id):
    recommender = pickle.load(open('app/mlmodel.sav','rb'))
    play_list = Song_Sample.objects.filter(sample_id = sample_id)
    
    sample = Sample.objects.get(id=sample_id)
    sample = model_to_dict(sample)
    request.session['sample'] = sample        
    sample_list =  request.session.get('sample_list')

    if list(play_list) == []:
        
        context = {
            'sample_list': sample_list,
            'sample' : sample,
        }
    else:
        rec_song_list = request.session.get('rec_song_list')

        song_play_id = find_song_id(id=play_list[0])
        url = "https://open.spotify.com/embed/track/" + song_play_id + "?utm_source=generator"

        song_list = find_list_song(song_list=play_list)
        play_list_df = pd.DataFrame(song_list)
        n_songs = 20
        
        metadata_cols = ['name', 'id', 'artists']
        
        song_center = get_mean_vector(play_list, data)
        scaler = model.steps[0][1]
        scaled_data = scaler.transform(data[number_cols])
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))
        distances = cdist(scaled_song_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_songs][0])
        rec_songs = data.iloc[index]
        rec_songs = rec_songs[~rec_songs['id'].isin(play_list_df['id'])]

        rec_song_list = find_list_song(song_list=rec_songs['id'])
        
        request.session['rec_song_list'] = rec_song_list

        context = {
            'sample_list': sample_list,
            'song_list' : song_list,
            'recommend_list' : rec_song_list,
            'sample' : sample,
            'url' : url
        }

    return render(request, 'index.html', context)
    

def choose_song(request, id):
    recommender = pickle.load(open('app/mlmodel.sav','rb'))
    sample = request.session.get('sample')
    song_list = Song_Sample.objects.filter(sample_id = sample['id'])
    year_list = []
    
    
    url = "https://open.spotify.com/embed/track/" + id + "?utm_source=generator"

    song_list = find_list_song(song_list=song_list)
    sample_list =  request.session.get('sample_list')
    rec_song_list = request.session.get('rec_song_list')

    context = {
        'sample_list': sample_list,
        'song_list' : song_list,
        'recommend_list' : rec_song_list,
        'sample' : sample,
        'url' : url
    }

    return render(request, 'index.html', context)


def add_song_playlist(request, id):
    sample = request.session.get('sample')
    song = Song.objects.get(id=id)
    sample_model = Sample.objects.get(id=sample['id'])
    sample_song = Song_Sample(song=song, sample=sample_model)
    sample_song.save()

    return recommendation_detail(request=request, sample_id=sample['id'])


def remove_song_playlist(request, id):
    sample = request.session.get('sample')
    song = Song.objects.get(id=id)
    sample_model = Sample.objects.get(id=sample['id'])
    Song_Sample.objects.filter(song=song, sample=sample_model).first().delete()
    
    return recommendation_detail(request=request, sample_id=sample['id'])

def search(request, subname):
    res = search_list[search_list['name'].str.startswith(subname)]
    
    # re = find_list_song(res['id'])
    # re = sorted(re, key=lambda d: d['popularity'], reverse=True) 
    re = res.to_dict('records');
    request.session['search_results'] = re
    sample_list = request.session.get('sample_list')
    sample = request.session.get('sample')

    context = {
        'sample' : sample,
        'sample_list': sample_list,
        'result' : re
    }

    return render(request, 'search.html', context)


def search_choose_song(request, id):

    url = "https://open.spotify.com/embed/track/" + id + "?utm_source=generator"
    
    re = request.session.get('search_results')
    sample_list = request.session.get('sample_list')
    sample = request.session.get('sample')

    context = {
        'sample' : sample,
        'sample_list': sample_list,
        'result' : re,
        'url' : url
    }

    return render(request, 'search.html', context)
