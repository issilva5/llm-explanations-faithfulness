import glob
import json

import pandas as pd

from src.util import shapley_values, nested_dict_to_df
from src.input import get_playlist_data

# Get the playlist data
df = get_playlist_data()

# Recommendation features
colnames = ['playlist_name', 'song_1', 'song_2', 'song_3', 'song_4', 'song_5']

# Output configuration
path = 'data/spotify_mpd/recommendations'
characteristic_function = {}

pids = df['pid'].unique()
for model in ['gemma2-9b-it', 'mixtral-8x7b-32768', 'llama3-70b-8192', 'gpt-4o-2024-08-06']:
    characteristic_function[model] = {}
    for pid in pids:
        characteristic_function[model][pid] = {}

        data = json.load(open(f"{path}/62_{pid}_{model}.json"))

        if 'error' in data:
            continue

        true_recs = data['recommendations']
        true_recs = [r['title'] + ' - by ' + r['artist'] for r in true_recs]

        files = glob.glob(f"{path}/*_{pid}_{model}.json")

        for recommendation in true_recs:
            characteristic_function[model][pid][recommendation] = {}

        for file in files:
            data = json.load(open(file, 'r'))
            coalition = tuple(sorted(data['coalition']))

            if 'recommendations' in data:
                coalition_recs = data['recommendations']
                coalition_recs = [r['title'] + ' - by ' + r['artist'] for r in coalition_recs]
            else:
                coalition_recs = []

            for recommendation in true_recs:
                characteristic_function[model][pid][recommendation][coalition] = 1 if recommendation in coalition_recs else 0

shapley_values_ = {}
for model in ['gemma2-9b-it', 'mixtral-8x7b-32768', 'llama3-70b-8192', 'gpt-4o-2024-08-06']:
    shapley_values_[model] = {}
    for pid in pids:
        shapley_values_[model][pid] = {}
        for recommendation in characteristic_function[model][pid]:
            shapley_values_[model][pid][recommendation] = shapley_values(colnames, characteristic_function[model][pid][recommendation])

df = nested_dict_to_df(shapley_values_).reset_index()
df.columns = ['model', 'pid', 'recommendation'] + colnames
df = pd.melt(df, id_vars=['model', 'pid', 'recommendation'], value_vars=colnames)
df.to_csv('shapley_values_playlist.csv', index=False)
