import os
import pandas as pd

from src.recommendation import LLMClient
from dotenv import load_dotenv
from src.recommendation.rec_types import FeatureRanking
from src.prompts import get_prompt_ranking_playlist as get_playlist_prompt

from tqdm import tqdm

load_dotenv()

client = LLMClient()
client.add_openai_client(os.environ['OPENAI_KEY'])

df = pd.read_csv('proc_shapley_values_playlist.csv')

df1 = df[['model', 'pid', 'variable', 'variable_value']].drop_duplicates()
df1 = df1.pivot(index=['model', 'pid'], columns='variable', values='variable_value')
preferences = df1.to_dict(orient='index')

explanations = df[['model', 'pid', 'recommendation', 'positive', 'explanation']].drop_duplicates()

all_rankings = []
with open('error.log', 'a') as error_log:
    for row in tqdm(explanations.iterrows(), total=explanations.shape[0]):

        row = row[1]
        
        try:
            upreferences = preferences[(row['model'], row['pid'])]
            playlist_title = upreferences['playlist_name']
            songs = [upreferences['song_1'], upreferences['song_2'], upreferences['song_3'], upreferences['song_4'], upreferences['song_5']]
            prompt = get_playlist_prompt(row['recommendation'], row['explanation'], row['positive'], playlist_title, *songs)
            model = 'gpt-4o-2024-08-06'
            completion = client.get_chat_completion(prompt, model)
            rankings = FeatureRanking.model_validate_json(completion)
            rankings = rankings.model_dump()
        except Exception as e:
            rankings = {"ranking": []}
            print(e)
            error_log.write(" ".join([row['model'], row['uid'], row['recommendation'], str(e)]))

        rankings['model'] = row['model']
        rankings['pid'] = row['pid']
        rankings['recommendation'] = row['recommendation']

        all_rankings.append(rankings)

df_rankings = pd.DataFrame(all_rankings)
df_rankings.to_csv('ranking_from_explanations_playlist.csv', index=False)
