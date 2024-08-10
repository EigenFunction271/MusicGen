# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputClassifier

# Set up Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_audio_features(track_id):
    features = sp.audio_features(track_id)[0]
    return [features['danceability'], features['energy'], features['valence'],
            features['tempo'], features['loudness'], features['acousticness']]

def create_dataset(playlist_ids):
    data = []
    for playlist_id in playlist_ids:
        tracks = sp.playlist_tracks(playlist_id)['items']
        for track in tracks:
            track_id = track['track']['id']
            features = get_audio_features(track_id)
            # You would need to manually label these or use another method to get labels
            mood = "happy"  # placeholder
            genre = "pop"   # placeholder
            data.append(features + [mood, genre])
    return pd.DataFrame(data, columns=['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness', 'mood', 'genre'])

# Create dataset (you'd need to provide playlist IDs and labels)
df = create_dataset(['playlist_id1', 'playlist_id2', 'playlist_id3'])

# Prepare the data
X = df.drop(['mood', 'genre'], axis=1)
y_mood = df['mood']
y_genre = df['genre']

# Encode labels
le_mood = LabelEncoder()
le_genre = LabelEncoder()
y_mood_encoded = le_mood.fit_transform(y_mood)
y_genre_encoded = le_genre.fit_transform(y_genre)

# Combine mood and genre into a single target variable
y = np.column_stack((y_mood_encoded, y_genre_encoded))

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
model = MultiOutputClassifier(rf, n_jobs=-1)
model.fit(X_train, y_train)

def classify_song(track_id):
    features = get_audio_features(track_id)
    prediction = model.predict([features])[0]
    mood = le_mood.inverse_transform([prediction[0]])[0]
    genre = le_genre.inverse_transform([prediction[1]])[0]
    return mood, genre

# Example usage
track_id = '5ChkMS8OtdzJeqyybCc9R5'  # Example track ID
mood, genre = classify_song(track_id)
print(f"Predicted mood: {mood}, Predicted genre: {genre}")