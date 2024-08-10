# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Set up Spotify client credentials
client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Mock user database (replace with a real database in production)
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}

# Mock classification function (replace with your real classifier)
def classify_song(song_title):
    moods = ['happy', 'playful', 'dark', 'melancholic', 'energetic']
    genres = ['techno', 'metal', 'JPop', 'rock', 'classical']
    return random.choice(moods), random.choice(genres)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/classify', methods=['POST'])
def classify_playlist():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    playlist_id = request.form['playlist_id']
    try:
        tracks = sp.playlist_tracks(playlist_id)['items']
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    classified_songs = []
    for track in tracks:
        song_title = track['track']['name']
        mood, genre = classify_song(song_title)
        classified_songs.append({
            'title': song_title,
            'mood': mood,
            'genre': genre
        })
    
    return jsonify(classified_songs)

@app.route('/generate', methods=['POST'])
def generate_playlist():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    selected_mood = request.form['mood']
    selected_genre = request.form['genre']
    
    # In a real app, you'd search for songs matching these criteria
    # Here, we're just returning a mock result
    new_playlist = [
        {'title': f'New {selected_mood} {selected_genre} Song 1'},
        {'title': f'New {selected_mood} {selected_genre} Song 2'},
        {'title': f'New {selected_mood} {selected_genre} Song 3'},
    ]
    
    return jsonify(new_playlist)

if __name__ == '__main__':
    app.run(debug=True)