import glob
import json

import pandas as pd

from src.util import shapley_values, nested_dict_to_df
from src.input import get_book_data

# Get the playlist data
df = get_book_data()

# Recommendation features
colnames = ['liked_book_1', 'liked_book_2', 'liked_book_3', 'disliked_book_1', 'disliked_book_2', 'disliked_book_3']

# Output configuration
path = 'data/bookrec/recommendations'
characteristic_function = {}

uids = df['user_id'].unique()
for model in ['gemma2-9b-it', 'mixtral-8x7b-32768', 'llama3-70b-8192', 'gpt-4o-2024-08-06']:
    characteristic_function[model] = {}
    for uid in uids:
        characteristic_function[model][uid] = {}

        data = json.load(open(f"{path}/62_{uid}_{model}.json"))

        if 'error' in data:
            continue

        true_recs = data['recommendations']
        true_recs = [r['title'] + ' - by ' + r['author'] for r in true_recs]

        files = glob.glob(f"{path}/*_{uid}_{model}.json")

        for recommendation in true_recs:
            characteristic_function[model][uid][recommendation] = {}

        for file in files:
            data = json.load(open(file, 'r'))
            coalition = tuple(sorted(data['coalition']))

            if 'recommendations' in data:
                coalition_recs = data['recommendations']
                coalition_recs = [r['title'] + ' - by ' + r['author'] for r in coalition_recs]
            else:
                coalition_recs = []

            for recommendation in true_recs:
                characteristic_function[model][uid][recommendation][coalition] = 1 if recommendation in coalition_recs else 0

shapley_values_ = {}
for model in ['gemma2-9b-it', 'mixtral-8x7b-32768', 'llama3-70b-8192', 'gpt-4o-2024-08-06']:
    shapley_values_[model] = {}
    for uid in uids:
        shapley_values_[model][uid] = {}
        for recommendation in characteristic_function[model][uid]:
            shapley_values_[model][uid][recommendation] = shapley_values(colnames, characteristic_function[model][uid][recommendation])

df = nested_dict_to_df(shapley_values_).reset_index()
df.columns = ['model', 'uid', 'recommendation'] + colnames
df = pd.melt(df, id_vars=['model', 'uid', 'recommendation'], value_vars=colnames)
df.to_csv('shapley_values_books.csv', index=False)
