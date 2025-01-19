import glob
import json
import os

from dotenv import load_dotenv
from tqdm import tqdm

from src.recommendation import LLMClient
from src.prompts import get_playlist_prompt_exp
from src.input import get_playlists_content

# Load the environment variables
load_dotenv()

# Get the playlist data
preferences = get_playlists_content()

# Initialize the client
client = LLMClient()
client.add_openai_client(os.environ['OPENAI_KEY'])
client.add_groq_client(os.environ['GROQ_KEY'])

# Output configuration
path = 'data/spotify_mpd/recommendations'
files = glob.glob(f"{path}/62_*.json")
explanation_attr = 'explanation'

with open('error.log', 'a') as error_log:

    for file in tqdm(files, desc='Files'):
        data = json.load(open(file, 'r'))

        if 'error' in data:
            continue

        pid = data['pid']
        model = data['model']
        playlist_name = preferences[pid]['playlist_name']
        tracks = preferences[pid]['track_artist']

        for recommendation in data['recommendations']:

            if explanation_attr in recommendation:
                continue

            prompt = get_playlist_prompt_exp(
                recommendation['title'],
                recommendation['artist'],
                recommendation['positive'],
                playlist_name, 
                tracks
            )

            try:

                completion = client.get_chat_completion(prompt, model)
                explanation = json.loads(completion)['explanation']
                recommendation[explanation_attr] = explanation
            
            except Exception as e:
                print(pid, model, file, e)
                error_log.write(" ".join([str(pid), model, file, str(e), '\n']))

        json.dump(data, open(file, 'w', encoding='utf8'), indent=4)
