import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# API keys
import config

from tqdm import tqdm
import re
#%%

client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#%%
playlist_link = "https://open.spotify.com/playlist/4R7d3nxcH5L8lFrnpz5kwg?si=ff9678e085b048d3"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
#%% Extracting Tracks From a Playlist
artist_name = []
artist_pop= []
track_name = []
popularity = []
track_id = []
track_uri=[]
for track in sp.playlist_tracks(playlist_URI)["items"]:
    #URI
    track_uri.append(track["track"]["uri"])

    track_id.append(track["track"]['id'])
    #Track name
    track_name.append(track["track"]["name"])

    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    #Name, popularity, genre
    artist_name.append(track["track"]["artists"][0]["name"])
    artist_pop.append(artist_info["popularity"])

    #Popularity of the track
    popularity.append(track["track"]["popularity"])

#%%
import pandas as pd
track_dataframe = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_uri, 'track_uri' : track_id, 'popularity' : popularity})
print(track_dataframe.shape)
track_dataframe.head()
df=track_dataframe
#%%
df["track_uri"] = df["track_uri"].apply(lambda x: re.findall(r'\w+$', x)[0])
df["track_uri"]
featureLIST = []
for track in df["track_uri"]:
    featureLIST.append(sp.audio_features(track)[0])
#%%
featureLIST = []
for track in tqdm(df["track_uri"]):
    featureLIST.append(sp.audio_features(track)[0])

#Preview the DataFrame
featureDF = pd.DataFrame(featureLIST)
featureDF
#%%
new_df = pd.merge(df,featureDF, left_on = "track_uri", right_on= "id")

new_df.to_csv('../data/processed_data.csv')