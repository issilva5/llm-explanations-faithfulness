import glob
import json
import os

from dotenv import load_dotenv
from tqdm import tqdm

from src.recommendation import LLMClient
from src.prompts import get_book_prompt_exp
from src.input import get_book_preferences

# Load the environment variables
load_dotenv()

# Get the playlist data
preferences = get_book_preferences()

# Initialize the client
client = LLMClient()
client.add_openai_client(os.environ['OPENAI_KEY'])
client.add_groq_client(os.environ['GROQ_KEY'])

# Output configuration
path = 'data/bookrec/recommendations'
files = glob.glob(f"{path}/62_*.json")
explanation_attr = 'explanation'

with open('error.log', 'a') as error_log:

    for file in tqdm(files, desc='Files'):
        data = json.load(open(file, 'r'))

        if 'error' in data:
            continue

        uid = data['uid']
        model = data['model']
        liked_books = preferences[uid][True]
        disliked_books = preferences[uid][False]

        for recommendation in data['recommendations']:

            if explanation_attr in recommendation:
                continue

            prompt = get_book_prompt_exp(
                recommendation['title'],
                recommendation['author'],
                recommendation['positive'],
                liked_books, 
                disliked_books
            )

            try:

                completion = client.get_chat_completion(prompt, model)
                explanation = json.loads(completion)['explanation']
                recommendation[explanation_attr] = explanation
            
            except Exception as e:
                print(uid, model, file, e)
                error_log.write(" ".join([str(uid), model, file, str(e), '\n']))

        json.dump(data, open(file, 'w', encoding='utf8'), indent=4)
