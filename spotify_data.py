import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# API keys
import config
# Playlists links
import playlists
from tqdm import tqdm
import re
import pandas as pd

# %%
client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# %%
def playlist_df(uri):
    # track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(uri)["items"]]

    track_uris = sp.playlist_tracks(uri)["items"]
    ##Extracting Tracks From a Playlist
    artist_name = []
    artist_pop = []
    track_name = []
    popularity = []
    track_id = []
    track_uri = []
    # for track in sp.playlist_tracks(uri)["items"]:
    for track in track_uris:
        # URI
        track_uri.append(track["track"]["uri"])

        track_id.append(track["track"]['id'])
        # Track name
        track_name.append(track["track"]["name"])

        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # Name, popularity, genre
        artist_name.append(track["track"]["artists"][0]["name"])
        artist_pop.append(artist_info["popularity"])

        # Popularity of the track
        popularity.append(track["track"]["popularity"])
    tracks_df = pd.DataFrame(
        {'artist_name': artist_name, 'track_name': track_name, 'track_id': track_uri, 'track_uri': track_id,
         'popularity': popularity})
    # Format URI
    tracks_df["track_uri"] = tracks_df["track_uri"].apply(lambda x: re.findall(r'\w+$', x)[0])
    # Get songs features
    featureLIST = []
    for track in tracks_df["track_uri"]:
        featureLIST.append(sp.audio_features(track)[0])
    # Preview the DataFrame
    featureDF = pd.DataFrame(featureLIST)
    df = pd.merge(tracks_df, featureDF, left_on="track_uri", right_on="id")
    return df


# %%
playlist_link = "https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=86e1e8d8626a45a6"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
df = playlist_df(playlist_URI)

track_uris = sp.playlist_tracks(playlist_link)["items"]
# %%
data = pd.DataFrame()
print("Extract songs features:")
for key, value in tqdm(playlists.links.items()):
        playlist_URI = value.split("/")[-1].split("?")[0]
        df = playlist_df(value)
        df['year'] = int(key)
        data = pd.concat([data, df])
# %%
data.to_csv('data/my_top_songs.csv')
#data.to_csv('../data/my_top_songs_2021_2022.csv')

# %%
playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1F0sijgNaJdgit?si=b9c96d4fc2234cbd'
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = sp.playlist_tracks(playlist_link)["items"]