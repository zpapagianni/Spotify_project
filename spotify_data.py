import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# API keys
import config
#%%

client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)