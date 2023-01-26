#Import libraries
import pandas as pd
import numpy as np
from tqdm import tqdm

# Data Visualization
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import re
from wordcloud import WordCloud
from math import pi
from collections import Counter
#%%
songs = pd.read_csv('../data/my_top_songs.csv')
songs.summary()
columns_to_drop=['track_id', 'track_uri', 'type', 'id', 'uri','track_href','analysis_url']
songs=songs.drop(columns_to_drop,axis=1)
songs=songs.dropna()
# Convert duration from ms to sec
songs['duration_ms']=songs['duration_ms']*10**-3


# initializing bad_chars_list

songs['artist_genres'] =songs['artist_genres'].apply( lambda x: re.sub(r"[]]", "", x, flags=re.MULTILINE))
songs['artist_name'] =songs['artist_name'].apply(str)
songs['artist_name'] =songs['artist_name'].apply( lambda x: re.sub(r'[^\w\s]', "", x, flags=re.MULTILINE))

songs = songs.rename(columns={'Unnamed: 0': 'rank', 'oldName2': 'newName2'})
#%%
top_gernes = ' '.join([word for word in songs['artist_genres']])
wordcloud_gernes = WordCloud(width=600,
                           height=400,
                           random_state=2,
                           max_font_size=100,
                           colormap='magma',
                           background_color="white").generate(top_gernes)


# Create a figure object and set its size and title
fig = plt.figure(figsize=(12, 6))
# showing image
plt.imshow(wordcloud_gernes)
plt.axis('off')
plt.title("Favorite gernes")

#%%
# ------- PART 1: Create background
features= ['danceability','liveness','energy','valence','speechiness','acousticness','year']
song_feat=songs.loc[:,features]

summary_stats = song_feat.groupby(["year"]).mean().reset_index()

#%%
# Shades of gray
GREY10 = "#1a1a1a"
GREY30 = "#4d4d4d"
GREY40 = "#666666"
GREY50 = "#7f7f7f"
GREY60 = "#999999"
GREY75 = "#bfbfbf"
GREY91 = "#e8e8e8"
GREY98 = "#fafafa"

# Colors used to shade countries
COLOR_SCALE = ["#7F3C8D", # ARG
    "#11A579", # BRA
    "#3969AC", # CHE
    "#F2B701", # DNK
    "#E73F74", # EUZ
    "#80BA5A", # GBR
    "#E68310", # SWE
]

# Vertical lines every 5 years
VLINES = np.arange(2016, 2023)
#%%
# Customize axes labels and ticks --------------------------------
# Initialize layout ----------------------------------------------
fig, ax = plt.subplots(figsize = (14, 8.5))
# Background color
fig.patch.set_facecolor(GREY98)
ax.set_facecolor(GREY98)

# Vertical lines used as scale reference
for h in VLINES:
    ax.axvline(h, color=GREY91, lw=0.6, zorder=0)

# Horizontal lines
ax.hlines(y=np.arange(0, 1.1 ,0.1), xmin=2016, xmax=2022, color=GREY91, lw=0.6)

# Darker horizontal line at y=0
ax.hlines(y=0, xmin=2016, xmax=2022, color=GREY60, lw=0.8)

# Vertical like at x = 2020
ax.axvline(2019, color=GREY40, ls="dotted")
# Annotations indicating the meaning of the vertical line
ax.text(2019.15, 0.85, "Moved to \n London",
        fontsize=14, fontweight=500, color=GREY40, ha="left")

# Vertical like at x = 2020
ax.axvline(2020, color=GREY40, ls="dotted")
# Annotations indicating the meaning of the vertical line
ax.text(2020.15, 0.85, "COVID-19 \n Lockdown",
        fontsize=14, fontweight=500, color=GREY40, ha="left")

# Vertical like at x = 2020
ax.axvline(2021, color=GREY40, ls="dotted")
# Annotations indicating the meaning of the vertical line
ax.text(2021.15, 0.85, "Live gigs \n allowed",
        fontsize=14, fontweight=500, color=GREY40, ha="left")

# Annotations indicating the meaning of the vertical line
#ax.text(2019.15, -0.35, "2019",fontsize=14, fontweight=500, color=GREY40, ha="left")

# First, adjust axes limits so annotations fit in the plot
ax.set_xlim(2016, 2023.5)
ax.set_ylim(0, 1)

# Customize axes labels and ticks --------------------------------
ax.set_yticks([y for y in np.around(np.arange(0, 1.1 , 0.1))])


ax.set_xticks([x for x in np.arange(2016, 2023)])
ax.set_xticklabels(
    [x for x in np.arange(2016, 2023)],
    fontsize=13,
    weight=500,
    color=GREY40
)

# Increase size and change color of axes ticks
ax.tick_params(axis="x", length=12, color=GREY91)
ax.tick_params(axis="y", length=8, color=GREY91)

# Customize spines
ax.spines["left"].set_color(GREY91)
ax.spines["bottom"].set_color(GREY91)
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")

# Positions
LABEL_Y = [
    0,
    0.57,  # ARG
    0.168,  # BRA
    0.736,    # CHE
    0.312,   # DNK
    0.07,  # EUZ
    0.146,   # GBR
]

#0.575220,0.168678,0.736020,0.312120,0.070012,0.146594


x_start = 2022
x_end = 2022.5
PAD = 0.1

for idx, feature in enumerate(summary_stats):
    if idx!=0:
        print(idx,feature)
        color = COLOR_SCALE[idx]
        ax.plot("year", feature, color=color, lw=1.8, data=summary_stats)
        # Country name
        text = feature

        # Vertical start of line
        y_start = summary_stats[feature].values[-1]
        # Vertical end of line
        y_end = LABEL_Y[idx]

        # Add line based on three points
        ax.plot(
            [x_start, (x_start + x_end - PAD) / 2 , x_end - PAD],
            [y_start, y_start, y_start],
            color=color,
            alpha=0.5,
            ls="dashed"
        )

        # Add country text
        ax.text(
            x_end,
            y_end,
            text,
            color=color,
            fontsize=14,
            weight="bold",
            va="center"
        )

fig.text(
    0.4,
    0.9,
    "Audio Features",
    color=GREY10,
    fontsize=16,
    weight="bold"
)

#%%
# Theme
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth':2})
palette = sns.color_palette("flare", 7)

# create a grid with a row for each 'Language'
g = sns.FacetGrid(songs, palette=palette, row="year", hue="year", height=0.8, aspect=10)

# map df - Kernel Density Plot of IMDB Score for each Language
g.map_dataframe(sns.kdeplot, x="tempo", fill=True, alpha=0.6)
g.map_dataframe(sns.kdeplot, x="tempo", color='black')

# function to draw labels
def label(x, color, label):
    ax = plt.gca() #get current axis
    ax.text(0, .2, label, color='black', fontsize=13,
            ha="left", va="center", transform=ax.transAxes)
# iterate grid to plot labels
g.map(label, "year")

# adjust subplots to create overlap
g.fig.subplots_adjust(hspace=-.5)

# remove subplot titles
g.set_titles("")

# remove yticks and set xlabel
g.set(yticks=[], xlabel="Tempo")
# remove left spine
g.despine(left=True)
# set title
plt.suptitle('Netflix Originals - IMDB Scores by Language', y=0.98)
#%%
# Flatten the list of tokens into a single list
artists =songs.loc[:,'artist_name']
# Use the Counter class to count the frequency of each word
word_counts = Counter(artists)
# Use the most_common() method to get the most common words
most_common_words = word_counts.most_common(20)
# Create dataframe
common_df = pd.DataFrame(most_common_words, columns=['Artist', 'Count'])

songs['artist_genres'] =songs['artist_genres'].apply( lambda x: re.sub(r"'", "", x, flags=re.MULTILINE))

genres =songs.loc[:,['artist_genres','year']]

df=songs.groupby("year")["artist_genres"].apply(lambda x: Counter(" ".join(x).split(',')).most_common(5)).to_frame()

#%%
# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
popularity=songs.loc[:,['year','artist_pop','popularity']]
popularity_sum = popularity.groupby(["year"]).mean().reset_index()
popularity_sum

sns.set(style="darkgrid")
df = sns.load_dataset('tips')

# Grouped violinplot
sns.violinplot(x="year", y="artist_pop", data=popularity)
plt.show()
#%%
from sklearn.manifold import TSNE

features= ['danceability','liveness','energy','valence','speechiness','acousticness','year']
song_feat=songs.loc[:,features]

tsne = TSNE(n_components=2, verbose=1, random_state=123, perplexity=20, n_iter=300)
songs_tsne = tsne.fit_transform(song_feat)

# Plot the result of our TSNE with the label color coded
# A lot of the stuff here is about making the plot look pretty and not TSNE
tsne_result_df = pd.DataFrame({'tsne_1': songs_tsne[:,0], 'tsne_2': songs_tsne[:,1], 'label': songs.loc[:,'year']})
fig, ax = plt.subplots(1)
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth':2})
sns.scatterplot(x='tsne_1', y='tsne_2', hue='label', data=tsne_result_df, ax=ax,s=12, palette=COLOR_SCALE)
lim = (songs_tsne.min()-5, songs_tsne.max()+5)
ax.set_xlim(lim)
ax.set_ylim(lim)
ax.set_aspect('equal')
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)



#%%
