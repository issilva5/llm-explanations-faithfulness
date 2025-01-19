import json
import os

from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

from src.recommendation import LLMClient
from src.util import powerset
from src.prompts import get_playlist_prompt
from src.input import get_playlist_data
from src.recommendation.rec_types import SongRecommendations

# Load the environment variables
load_dotenv()

# Get the playlist data
df = get_playlist_data()

# Recommendation features
colnames = ['playlist_name', 'song_1', 'song_2', 'song_3', 'song_4', 'song_5']
coalitions = powerset(colnames)

# Initialize the client
client = LLMClient()
client.add_openai_client(os.environ['OPENAI_KEY'])
client.add_groq_client(os.environ['GROQ_KEY'])

# Output configuration
path = 'data/spotify_mpd/recommendations'
os.makedirs(path, exist_ok=True)

for cid, coalition in tqdm(enumerate(coalitions), desc='Coalitions'):

    df_filtered = df[['pid'] + coalition]

    for row in tqdm(df_filtered.itertuples(index=False, name=None), desc='Playlists', total=df_filtered.shape[0]):

        pid = row[0]
        playlist_name = ""
        songs = []

        if 'playlist_name' in coalition:
            playlist_name = row[1]
            songs = row[2:]
        else:
            songs = row[1:]
        
        prompt = get_playlist_prompt(playlist_name, *songs)
        for model in ['gemma2-9b-it', 'mixtral-8x7b-32768', 'llama3-70b-8192', 'gpt-4o-2024-08-06']:

            if os.path.exists(f'{path}/{cid}_{pid}_{model}.json'):
                continue

            try:

                completion = client.get_chat_completion(prompt, model)
                recommendations = SongRecommendations.model_validate_json(completion)
                recommendations = recommendations.model_dump()
            
            except Exception as e:
                recommendations = {}
                recommendations['error'] = str(e)

            recommendations['coalition'] = coalition
            recommendations['model'] = model
            recommendations['pid'] = pid
            recommendations['created_at'] = datetime.now().isoformat()

            json.dump(recommendations, open(f'{path}/{cid}_{pid}_{model}.json', 'w', encoding='utf8'), indent=4)
