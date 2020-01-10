from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
db = client.playlist_maker
playlists = db.playlists

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    playlist_items = playlists.find()
    return render_template ('index.html', playlist_items=playlist_items)

@app.route('/playlist/new')
#playlist making page
def new_playlist():
    return render_template('new_playlist.html')

@app.route('/playlist', methods=['POST'])
def submit_playlist():
    added_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
    }
    playlist_id = playlists.insert_one(added_playlist).inserted_id 
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlist/<playlist_id>')
#look at one art piece
def playlist_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlist_show.html', playlist=playlist)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
