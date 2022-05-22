from tkinter import CASCADE
from django.db import models

# Create your models here.

class Song(models.Model):
    valence = models.FloatField()
    year = models.IntegerField()
    acousticness = models.FloatField()
    #Cai nay la danh sach cac ten, comma separated
    artist = models.CharField(max_length=300)
    danceability = models.FloatField()
    duration = models.IntegerField()
    energy = models.FloatField()
    explicit = models.IntegerField()
    id = models.CharField(max_length=30, primary_key=True)
    instrumentalness = models.FloatField()
    key = models.IntegerField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    name = models.CharField(max_length=300)
    popularity = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()

    def __str__(self):
        return self.id
    
    def get_year(self):
        return self.year

class Sample(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Song_Sample(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.song)