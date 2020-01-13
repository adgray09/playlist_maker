from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
db = client.playlist_maker
playlists = db.playlists
songs = db.songs

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    playlist_items = playlists.find()
    return render_template ('index.html', playlist_items=playlist_items)

@app.route('/playlist')
def playlist_page():
    song_items = songs.find()
    return render_template ('playlist_show.html', song_items=song_items)

@app.route('/song/new')
#new song submission page
def new_song():
    return render_template('new_song.html')

@app.route('/playlist', methods=['POST'])
def submit_song():
    added_song = {
        'title': request.form.get('title'),
        'artist': request.form.get('artist'),
    }

    song_id = songs.insert_one(added_song).inserted_id
    return redirect(url_for('playlist_show', song_id=song_id))

@app.route('/playlist/new')
#playlist making page
def new_playlist():
    return render_template('new_playlist.html')

@app.route('/playlist', methods=['POST'])
def submit_playlist():
    added_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'songs': request.form.get('songs'),
    }
    playlist_id = playlists.insert_one(added_playlist).inserted_id 
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlist/<playlist_id>')
#look at one playlist
def playlist_show(playlist_id, song_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    song = songs.find_one({'_id': ObjectId(song_id)})
    return render_template('playlist_show.html', playlist=playlist, song=song)

@app.route('/playlist/<playlist_id>/delete', methods=['POST'])
#Delete post method
def playlists_delete(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
