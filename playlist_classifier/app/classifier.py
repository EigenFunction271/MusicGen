# -*- coding: utf-8 -*-
import joblib
from sklearn.ensemble import RandomForestClassifier
from .spotify_utils import get_audio_features

# Assume we've trained and saved our models
mood_classifier = joblib.load('mood_classifier.joblib')
genre_classifier = joblib.load('genre_classifier.joblib')

def classify_song(track_id):
    features = get_audio_features(track_id)
    feature_vector = [features['danceability'], features['energy'], features['key'],
                      features['loudness'], features['mode'], features['speechiness'],
                      features['acousticness'], features['instrumentalness'],
                      features['liveness'], features['valence'], features['tempo']]
    
    mood = mood_classifier.predict([feature_vector])[0]
    genre = genre_classifier.predict([feature_vector])[0]
    return mood, genre

def classify_playlist(playlist_id):
    from .spotify_utils import get_playlist_tracks
    
    tracks = get_playlist_tracks(playlist_id)
    classified_songs = []
    for track in tracks:
        track_id = track['track']['id']
        song_name = track['track']['name']
        mood, genre = classify_song(track_id)
        classified_songs.append({
            'name': song_name,
            'mood': mood,
            'genre': genre
        })
    return classified_songs