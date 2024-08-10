# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=Config.SPOTIFY_CLIENT_ID,
                                                           client_secret=Config.SPOTIFY_CLIENT_SECRET))

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_audio_features(track_id):
    return sp.audio_features(track_id)[0]