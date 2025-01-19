import json
import os

from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

from src.recommendation import LLMClient
from src.util import powerset
from src.prompts import get_book_prompt
from src.input import get_book_data
from src.recommendation.rec_types import BookRecommendations

# Load the environment variables
load_dotenv()

# Get the playlist data
df = get_book_data()

# Recommendation features
colnames = ['liked_book_1', 'liked_book_2', 'liked_book_3', 'disliked_book_1', 'disliked_book_2', 'disliked_book_3']
coalitions = powerset(colnames)

# Initialize the client
client = LLMClient()
client.add_openai_client(os.environ['OPENAI_KEY'])
client.add_groq_client(os.environ['GROQ_KEY'])

# Output configuration
path = 'data/bookrec/recommendations'
os.makedirs(path, exist_ok=True)

for cid, coalition in tqdm(enumerate(coalitions), desc='Coalitions'):

    df_filtered = df[['user_id'] + coalition]

    for row in tqdm(df_filtered.itertuples(index=False), desc='Users', total=df_filtered.shape[0]):
        row = row._asdict()
        uid = row['user_id']

        liked_books = []
        for f in ['liked_book_1', 'liked_book_2', 'liked_book_3']:
            if f in coalition:
                liked_books.append(row[f])
        
        disliked_books = []
        for f in ['disliked_book_1', 'disliked_book_2', 'disliked_book_3']:
            if f in coalition:
                disliked_books.append(row[f])
        
        prompt = get_book_prompt(liked_books, disliked_books)
        for model in ['gemma2-9b-it', 'mixtral-8x7b-32768', 'llama3-70b-8192', 'gpt-4o-2024-08-06']:

            if os.path.exists(f'{path}/{cid}_{uid}_{model}.json'):
                continue

            try:

                completion = client.get_chat_completion(prompt, model)
                recommendations = BookRecommendations.model_validate_json(completion)
                recommendations = recommendations.model_dump()
            
            except Exception as e:
                recommendations = {}
                recommendations['error'] = str(e)

            recommendations['coalition'] = coalition
            recommendations['model'] = model
            recommendations['uid'] = uid
            recommendations['created_at'] = datetime.now().isoformat()

            json.dump(recommendations, open(f'{path}/{cid}_{uid}_{model}.json', 'w', encoding='utf8'), indent=4)
