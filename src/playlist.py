import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_likes(client_id, client_secret, redirect_uri):
    #Credentials to log in to spoti
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="user-library-read"))
    all_songs = []
    # Maximum songs by API call
    limit = 50
    # Api call to get the songs you have like
    results = sp.current_user_saved_tracks(limit=limit, offset=0)
    total_tracks = results['total']
    # all apis call until you have all your songs
    offset = 0
    while offset < total_tracks:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        all_songs.extend(results['items'])
        offset += limit
    # DataFrame with info
    song_info = []
    for song in all_songs:
        song_id = song['track']['id']
        song = sp.track(song_id)
        features = sp.audio_features(song_id)[0]
        song_info.append({
            'id': song['id'],
            'name': song['name'],
            'artist': song['artists'][0]['name'],
            'album': song['album']['name'],
            'release_date': song['album']['release_date'],
            'popularity': song['popularity'],
            'song_decade': song['album']['release_date'][:3] + '0s',
            'danceability': features['danceability'],
            'energy': features['energy'],
            'loudness': features['loudness'],
            'speechiness': features['speechiness'],
            'acousticness': features['acousticness'],
            'liveness': features['liveness'],
            'tempo': features['tempo'],
            'duration_ms': features['duration_ms'],
            'valence': features['valence'],
            'artist_followers': sp.artist(song['artists'][0]['id'])['followers']['total']
        })
    df_songs = pd.DataFrame(song_info)
    return df_songs

#'genre': song['album']['genres'][0] if song['album']['genres'] else '',

def spotify_uri(song_id):
    return "spotify:track:" + song_id

def replace_clusters(column_clusters):
    if column_clusters == 0:
        return "Sunshine State of Mind"
    elif column_clusters == 1:
        return "Echoes of Solitude"
    else:
        return column_clusters

def create_cluster_playlists(df, user_id, client_id, client_secret, redirect_uri):
    # Initialize Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

    # Iterate over clusters
    for cluster in df["Cluster_features"].value_counts().index.tolist():
        # Get list of track URIs for the cluster
        uris = df[df["Cluster_features"] == cluster]["Id"].tolist()

        # Create playlist
        playlist_name = f"{cluster}"
        sp.user_playlist_create(user=user_id, name=playlist_name)

        # Add songs to playlist
        playlist_id = sp.user_playlists(user=user_id, limit=1, offset=0)["items"][0]["id"]

        # Add songs to playlist in groups of 100
        uris_groups = [uris[i:i+100] for i in range(0, len(uris), 100)]
        for group in uris_groups:
            sp.playlist_add_items(playlist_id=playlist_id, items=group)