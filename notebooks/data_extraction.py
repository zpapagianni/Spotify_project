# Import libraries
import re

import pandas as pd
import spotipy
import spotipy.util as util
from tqdm import tqdm

import config
import playlists

# %%
token = util.prompt_for_user_token(username='11182181486',
                                   scope='user-library-read',
                                   client_id=config.cid,
                                   client_secret=config.secret,
                                   redirect_uri=config.redirect_url)
sp = spotipy.Spotify(auth=token)


# %%

## Retrieve Data from Spotify Web API
def playlist_df(uri):
    ## Extracting Tracks From a Playlist
    track_uris = sp.playlist_items(uri)["items"]
    ## Create lists to save songs details
    artist_name = []
    artist_pop = []
    artist_genres = []
    track_name = []
    track_id = []
    track_uri = []
    popularity = []
    # for track in sp.playlist_tracks(uri)["items"]:
    for track in track_uris:
        # URI
        track_uri.append(track["track"]["uri"])
        # ID
        track_id.append(track["track"]['id'])
        # Track name
        track_name.append(track["track"]["name"])

        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        # Name, popularity, genre
        artist_name.append(track["track"]["artists"][0]["name"])
        artist_pop.append(artist_info["popularity"])
        artist_genres.append(artist_info["genres"])

        # Popularity of the track
        popularity.append(track["track"]["popularity"])

    # Create dataframe
    tracks_df = pd.DataFrame(
        {'artist_name': artist_name, 'artist_pop': artist_pop, 'artist_genres': artist_genres,
         'track_name': track_name, 'track_id': track_id, 'track_uri': track_uri, 'popularity': popularity})

    # Format URI
    tracks_df["track_uri"] = tracks_df["track_uri"].apply(lambda x: re.findall(r'\w+$', x)[0])
    # Get songs features
    feature_list = []
    for track in tracks_df["track_uri"]:
        feature_list.append(sp.audio_features(track)[0])
    # Create DataFrame
    feature_df = pd.DataFrame(feature_list)
    # Merge dataframes
    df = pd.merge(tracks_df, feature_df, left_on="track_uri", right_on="id")
    return df


# %%
# Load Data into DataFrame for Exploratory Data Analysis
# Create empty dataframe that will contain all the details
data = pd.DataFrame()
print("Extract songs features from each playlist:")
for key, value in tqdm(playlists.links.items()):
    # Get playlists URI
    playlist_URI = value.split("/")[-1].split("?")[0]
    # Get dataframe with the features of each song
    df = playlist_df(value)
    # Add column to store year
    df['year'] = int(key)
    # Add dataframe to data
    data = pd.concat([data, df])

print("Done")
print(data.shape)

# %%
## Save file to data folder
data.to_csv('./data/my_top_songs.csv')
