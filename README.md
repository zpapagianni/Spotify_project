# Spotify: Listening history 2016-2022

I am a HUGE fan of music and I wanted to see how my taste has changed from 2016 to 2022, going through different stages of life 
and transitions.I found out about [Spotify's Web API](https://developer.spotify.com/documentation/web-api/) and
I wanted to use it to get information about my favorite songs. I retrieved my listening history from Spotify's Web API 
to see how my top songs have changed over the last 7 years.
To accomplish this, I used Python to retrieve and analyze my listening history from Spotify API. I also used data visualization techniques to present my findings in an easily understandable format. Additionally, I will be incorporating 
information about the different stages of my life into the analysis. 
This will allow me to understand how my music taste may have been influenced by life events 
such as graduating, experiencing my first heartbreak, moving to a new city or starting a new job. 
By examining the correlation between these events and my listening history, I hope to gain a deeper understanding of how my 
music preferences have evolved over time. Overall, this project has been really fun to do and very insightful.

I divided this project into two parts:

**Part I**: Extracting song data from Spotify’s API in Python

**Part II**: EDA and Clustering

## Data Collection

### Spotify API Acquisition
If you haven’t used an API before, the use of various keys for authentication, 
and the sending of requests can prove to be a bit daunting. 
The first thing we’ll look at is getting keys to use. 
For this, we need a [Spotify for developers] (https://developer.spotify.com/) account. 
This is the same as a Spotify account, and doesn’t require Spotify Premium. 
From here, go to the dashboard and “create an app”. After creating the app, we can get a client ID and a client secret.
Both of these will be required to authenticate with the Spotify web API for our application, 
and can be thought of as a kind of username and password for the application. 
It is best practice not to share either of these, but especially don’t share the client secret key. 
To prevent this, I stored them in a separate file named `confing.py`, which should be Gitignored. The first line as the
**client ID** and the second line as the **client secret**:

We use the Authorization Code Flow method/ This flow is suitable for long-running applications in which the user grants permission 
only once. It provides an access token that can be refreshed. 
Since the token exchange involves sending your secret key, perform this on a secure location, 
like a backend service, and not from a client such as a browser or from a mobile app. I pass my app credentials directly into the method as arguments and
the desired scope (see [Using Scopes](https://developer.spotify.com/web-api/using-scopes/) for information about scopes) and credentials

The links for my playlists are stored in `playlists.py` 
as a dictionary where the key is equal to the year and the value in the link to the playlist.

### Data features
From [Spotify's API documentation](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track) :

* artist name: The name of the album. In case of an album takedown, the value may be an empty string.
* artist genres:A list of the genres the artist is associated with. If not yet classified, the array is empty.
* artist popularity: The popularity of the artist. The value will be between 0 and 100, with 100 being the most popular. The artist's popularity is calculated from the popularity of all the artist's tracks.
* Track popularity: The popularity of the track. The value will be between 0 and 100, with 100 being the most popular.
  The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.
  Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from track popularity. Note: the popularity value may lag actual popularity by a few days: the value is not updated in real time.
* acousticness : A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
* energy:Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
* danceability : Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
* energy : Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
* instrumentalness : Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
* key : The key the track is in. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
* liveness : Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
* loudness : The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.
* mode : Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
* speechiness : Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
* tempo : The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
* time_signature : An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).
* valence : A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
* duration_ms : The duration of the track in milliseconds.

### EDA and clustering

## Repo Structure

```
│
├── README.md              <- The top-level README with instructions.
├── data
│   ├── my_top_songs.csv   <- The original data set containing my top songs from 2016 to 2022.
│   ├── processed      <- The preprocessed data sets for training.
│   ├── test           <- The test data sets for testing.
│   └── final          <- The final data sets for modeling.
│
├── playlists.py            
│
├── notebooks               <- Jupyter notebooks created in the project.
│   ├── playlists.py        <- File containing dictionary with links to my top songs playlists.
│   ├── data_extraction.py  <- Script for data extraction and loading data
│   ├── Extraction.ipynb          <- Data extraction using Spotify API
│   └── EDA-clustering.ipynb               <- Exploratory data analysis process.

└── requirements.txt   <- The requirements file for reproducing the analysis environment.
```
