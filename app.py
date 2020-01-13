from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/playlistmaker')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
playlists = db.playlists

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    playlist_items = playlists.find()
    return render_template ('index.html', playlist_items=playlist_items)

@app.route('/playlist')
def playlist_page():
    song_items = songs.find()
    return render_template ('playlist_show.html', song_items=song_items)

@app.route('/playlist/<playlist_id>/add_song')
#new song submission page
def add_song(playlist_id):
    return render_template('new_song.html', playlist_id=playlist_id)

@app.route('/playlist/<playlist_id>/add_song', methods=['POST'])
# add new song to playlist
def submit_add_song(playlist_id):
    # grab playlist
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})

    # create new song
    updatedSongs = playlist['songs'] + [{
        'title': request.form.get('title'),
        'artist': request.form.get('artist'),
        'link': request.form.get('link'),
    }]

    # update on backend
    playlists.update_one(
        {'_id': ObjectId(playlist_id)}, # query for playlist
        {
            '$set' : {
                'songs': updatedSongs
            }
        }
    )

    # render playlist
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

# @app.route('/playlist', methods=['POST'])
# def new_song():
    
@app.route('/playlist/new')
#playlist making page
def new_playlist():
    return render_template('new_playlist.html')

@app.route('/playlist', methods=['POST'])
def submit_playlist():
    added_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'songs': [] # eventually will be an array of songs with title, artist, and link
    }
    playlist_id = playlists.insert_one(added_playlist).inserted_id 
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlist/<playlist_id>')
#look at one playlist
def playlist_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlist_show.html', playlist=playlist)

@app.route('/playlist/<playlist_id>/delete', methods=['POST'])
#Delete post method
def playlists_delete(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('index'))

@app.route('/playlist/<playlist_id>/delete_song/<song_index>', methods=['POST'])
def song_delete(playlist_id, song_index):
     # grab playlist
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})

    updatedSongs = []

    # use black magic to remove an element from a list in python
    songs = playlist['songs']
    for i in range(len(songs)):
        if i != int(song_index) - 1:
            updatedSongs.append(songs[i])

    # update on backend
    playlists.update_one(
        {'_id': ObjectId(playlist_id)}, # query for playlist
        {
            '$set' : {
                'songs': updatedSongs
            }
        }
    )

    # render playlist
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlist/<playlist_id>', methods=['POST'])
#edit playlist
def playlist_update(playlist_id):
    new_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'creator': request.form.get('creator'),
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': new_playlist})
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlist/<playlist_id>/edit')
#edit form
def chips_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('edit_playlist.html', playlist=playlist)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
