# Music recommender
## To run this project

If cannot directly `manage.py runserver` this project then delete the folder /venv.

Then again recreate a new virtual environment
`python3 -m venv venv`
and activate it by `source venv/bin/activate`.

Install bunch of packages:

`pip3 install django djangorestframework numpy scipy matplotlib scikit-learn pandas`

Remember this:
```pip3 install spotipy```
___

## What can be extended
- Playable music
- Edit (add, remove) playlist by searching song name -> return list of song with details about artist, year
- Use restAPI to be faster and to look smarter
- Improve this ugly design??
___
## What fun haha
`sudo apt install sqlite3`

`sqlite3 db.sqlite3` to do sql
