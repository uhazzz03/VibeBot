import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st

SPOTIFY_CLIENT_ID = st.secrets.get("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = st.secrets.get("SPOTIPY_CLIENT_SECRET")

def get_spotify_client():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None
    auth_manager = SpotifyClientCredentials(
        client_id = SPOTIFY_CLIENT_ID,
        client_secret = SPOTIFY_CLIENT_SECRET
    )

    return spotipy.Spotify(auth_manager=auth_manager)

def search_tracks(query, limit=5):
    sp = get_spotify_client()
    if sp is None:
        return []

    results = sp.search(q=query, type="track", limit=limit)
    tracks = results.get("tracks", {}).get("items", [])

    formatted_tracks = []
    for track in tracks:
        formatted_tracks.append({
            "name": track["name"],
            "artist": ", ".join(artist["name"] for artist in track["artists"]),
            "url": track["external_urls"]["spotify"]
        })

    return formatted_tracks

def search_playlists(query, limit=5):
    sp = get_spotify_client()
    if sp is None:
        return []

    try:
        results = sp.search(q=query, type="playlist", limit=limit)
        playlists = results.get("playlists", {}).get("items", [])

        formatted_playlists = []

        for playlist in playlists:
            if not playlist:
                continue  # skip None entries

            owner = playlist.get("owner") or {}
            owner_name = owner.get("display_name", "Unknown")

            formatted_playlists.append({
                "name": playlist.get("name", "Unknown Playlist"),
                "owner": owner_name,
                "url": playlist.get("external_urls", {}).get("spotify", "#")
            })

        return formatted_playlists

    except Exception:
        return []