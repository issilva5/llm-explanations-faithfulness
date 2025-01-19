import os
import pandas as pd

from src.recommendation import LLMClient
from dotenv import load_dotenv
from src.recommendation.rec_types import FeatureRanking
from src.prompts import get_prompt_ranking_movies as get_prompt

from tqdm import tqdm

load_dotenv()

client = LLMClient()
client.add_openai_client(os.environ['OPENAI_KEY'])

df = pd.read_csv('proc_shapley_values_movies.csv')

df1 = df[['model', 'uid', 'variable', 'variable_value']].drop_duplicates()
df1 = df1.pivot(index=['model', 'uid'], columns='variable', values='variable_value')
preferences = df1.to_dict(orient='index')

explanations = df[['model', 'uid', 'recommendation', 'positive', 'explanation']].drop_duplicates()

all_rankings = []
for row in tqdm(explanations.iterrows(), total=explanations.shape[0]):

    row = row[1]
    
    try:
        upreferences = preferences[(row['model'], row['uid'])]
        liked_movies = [upreferences['liked_movie_1'], upreferences['liked_movie_2'], upreferences['liked_movie_3']]
        disliked_movies = [upreferences['disliked_movie_1'], upreferences['disliked_movie_2'], upreferences['disliked_movie_3']]
        prompt = get_prompt(row['recommendation'], row['explanation'], row['positive'], liked_movies, disliked_movies)

        model = 'gpt-4o-2024-08-06'
        
        completion = client.get_chat_completion(prompt, model)
        rankings = FeatureRanking.model_validate_json(completion)
        rankings = rankings.model_dump()
    except Exception as e:
        rankings = {"ranking": []}
        print(e)

    rankings['model'] = row['model']
    rankings['uid'] = row['uid']
    rankings['recommendation'] = row['recommendation']

    all_rankings.append(rankings)

df_rankings = pd.DataFrame(all_rankings)
df_rankings.to_csv('ranking_from_explanations_movies.csv', index=False)