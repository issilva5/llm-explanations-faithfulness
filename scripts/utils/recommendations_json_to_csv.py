import glob
import json

import pandas as pd

from tqdm import tqdm

path = 'data/bookrec/recommendations'
files = glob.glob(f"{path}/62_*.json")

def json_to_df(file):
    data = json.load(open(file, 'r'))
    df = pd.json_normalize(data)

    if 'error' in data:
        return df

    df = df.explode('recommendations')
    df: pd.DataFrame = pd.concat(
        [
            df.drop(columns=['recommendations']).reset_index(drop=True), 
            pd.json_normalize(df['recommendations'])
        ], axis=1
    )
    return df.drop(columns = ['explanation', 'explanationt'], errors='ignore')

list_of_dfs = []
for file in tqdm(files):
    list_of_dfs.append(json_to_df(file))

df = pd.concat(list_of_dfs)
df.reset_index(drop=True).to_csv('recommendations_books.csv', index=False)