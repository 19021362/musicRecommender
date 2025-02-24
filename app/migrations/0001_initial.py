# Generated by Django 2.2.12 on 2022-05-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('valence', models.FloatField()),
                ('year', models.IntegerField()),
                ('acousticness', models.FloatField()),
                ('artist', models.CharField(max_length=300)),
                ('danceability', models.FloatField()),
                ('duration', models.IntegerField()),
                ('energy', models.FloatField()),
                ('explicit', models.IntegerField()),
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('instrumentalness', models.FloatField()),
                ('key', models.IntegerField()),
                ('liveness', models.FloatField()),
                ('loudness', models.FloatField()),
                ('mode', models.IntegerField()),
                ('name', models.CharField(max_length=300)),
                ('popularity', models.IntegerField()),
                ('speechiness', models.FloatField()),
                ('tempo', models.FloatField()),
            ],
        ),
    ]
