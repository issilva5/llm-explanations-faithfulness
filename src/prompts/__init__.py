from typing import List

def get_playlist_prompt(playlist_name: str = "", *songs):

    instructions = f"""You are a music playlist recommendation assistant. 
Your task is to recommend songs to be added to a user's playlist based on the provided information about the playlist. 
The user wants two songs that fit the playlist (aka. positive) and two songs that do not (aka. negative).
"""
    
    input = "Input:"

    if playlist_name != "":
        input += f"\n- Playlist's title: {playlist_name}"
    
    if len(songs) > 0:
        input += "\n- Playlist's current songs:"
        for i, song in enumerate(songs):
            input += f"\n  {i+1}. {song}"
    
    output = """Output:
- The output must be a JSON object.
- Include no additional text besides the JSON
- The JSON object must have the following format:
    {
        "recommendations": [
            {
                "title": "Song title",
                "artist": "Artist",
                "positive": true
            },
            {
                "title": "Song title",
                "artist": "Artist",
                "positive": true
            },
            {
                "title": "Song title",
                "artist": "Artist",
                "positive": false
            },
            {
                "title": "Song title",
                "artist": "Artist",
                "positive": false
            }
        ]
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output


def get_book_prompt(liked_books = [], disliked_books = []):

    instructions = f"""You are a book recommendation assistant. 
Your task is to recommend books to a user based based on the provided information about the user reading preferences.
The user wants two book recommendations that their will like (aka. positive) and two book recommendations that they will not (aka. negative).
"""
    
    input = "Input:"

    if len(liked_books) > 0:
        input += "\n- Liked books: "
        input += "; ".join(liked_books)
    
    if len(disliked_books) > 0:
        input += "\n- Disliked books: "
        input += "; ".join(disliked_books)
    
    output = """Output:
- The output must be a JSON object.
- Include no additional text besides the JSON
- The JSON object must have the following format:
    {
        "recommendations": [
            {
                "title": "Book title",
                "author": "Author",
                "positive": true
            },
            {
                "title": "Book title",
                "author": "Author",
                "positive": true
            },
            {
                "title": "Book title",
                "author": "Author",
                "positive": false
            },
            {
                "title": "Book title",
                "author": "Author",
                "positive": false
            }
        ]
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output

def get_movie_prompt(liked_movies = [], disliked_movies = []):

    instructions = f"""You are a movie recommendation assistant. 
Your task is to recommend movies to a user based based on the provided information about the user preferences.
The user wants two movie recommendations that their will like (aka. positive) and two movie recommendations that they will not (aka. negative).
"""
    
    input = "Input:"

    if len(liked_movies) > 0:
        input += "\n- Liked movies: "
        input += "; ".join(liked_movies)
    
    if len(disliked_movies) > 0:
        input += "\n- Disliked movies: "
        input += "; ".join(disliked_movies)
    
    output = """Output:
- The output must be a JSON object.
- Include no additional text besides the JSON
- The JSON object must have the following format:
    {
        "recommendations": [
            {
                "title": "movie title",
                "positive": true
            },
            {
                "title": "movie title",
                "positive": true
            },
            {
                "title": "movie title",
                "positive": false
            },
            {
                "title": "movie title",
                "positive": false
            }
        ]
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output


def get_book_prompt_exp(title: str, author: str, liked: bool, liked_books: List[str], disliked_books: List[str]):
    instructions = f"""You are a book recommendation assistant. 
Your task is to, based on the provided information about the user reading preferences, explain why they received a certain recommendation.
The recommendation can either be positive (a book they should read) or negative (a book they should avoid).
"""
    
    input = "Input:"
    input += "\n- Liked books: "
    input += "; ".join(liked_books)
    input += "\n- Disliked books: "
    input += "; ".join(disliked_books)
    input += f"\n\nRecommendation: {title} - by {author}"
    input += f"\nRecommendation type: {'positive' if liked else 'negative'}"

    output = """Output:
- The output must be a JSON object.
- Include no additional text besides the JSON
- The JSON object must have the following format:
    {
        "explanation": "explanation"
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output

def get_playlist_prompt_exp(title: str, artist: str, liked: bool, playlist_name: str, songs: List[str]):
    instructions = f"""You are a music playlist recommendation assistant. 
Your task is to, based on the provided information about the playlist, explain why they received a certain recommendation.
The recommendation can either be positive (a song they may add to the playslit) or negative (a song they should avoid).
"""
    
    input = "Input:"

    if playlist_name != "":
        input += f"\n- Playlist's title: {playlist_name}"
    
    if len(songs) > 0:
        input += "\n- Playlist's current songs:"
        for i, song in enumerate(songs):
            input += f"\n  {i+1}. {song}"

    input += f"\n\nRecommended Song: {title} - by {artist}"
    input += f"\nRecommendation type: {'positive' if liked else 'negative'}"

    output = """Output:
- The output must be a JSON object.
- Include no additional text besides the JSON
- The JSON object must have the following format:
    {
        "explanation": "explanation"
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output

    
def get_movie_prompt_exp(title: str, liked: bool, liked_movies: List[str], disliked_movies: List[str]):
    instructions = f"""You are a movie recommendation assistant.  
Your task is to, based on the information provided about the user's preferences, explain why they received a certain recommendation.
The recommendation can either be positive (a movie they should watch) or negative (a movie they should avoid).
"""
    
    input = "Input:"
    input += "\n- Liked movies: "
    input += "; ".join(liked_movies)
    input += "\n- Disliked movies: "
    input += "; ".join(disliked_movies)
    input += f"\n\nRecommendation: {title}"
    input += f"\nRecommendation type: {'positive' if liked else 'negative'}"

    output = """Output:
- The output must be a JSON object.
- Include no additional text besides the JSON
- The JSON object must have the following format:
    {
        "explanation": "explanation"
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output

def get_prompt_ranking_books(recommendation: str = "", explanation: str = "", positive: bool = True, liked_books: List[str] = [], disliked_books: List[str] = []):

    instructions = f"""The book {recommendation} was recommended to {'not ' if not positive else ''}be read by a certain user.

The recommended system provided the following explanation: {explanation}. 

Your task is to given the recommendation and its explanation, provide a ranking of the input features based on their importance to the recommendation.
"""
    
    input = "Input features:"
    input += "\n- Liked books: "
    input += "; ".join(liked_books)
    input += "\n- Disliked books: "
    input += "; ".join(disliked_books)
    
    output = """Output:
- The output must be a JSON object.
- The JSON must have one key, "ranking", which is a list of the input features in order of importance.
- Each book is an input feature. All features must be included in the ranking.
- Consider the following feature names: ["liked_book_1", "liked_book_2", "liked_book_3", "disliked_book_1", "disliked_book_2", "disliked_book_3"]
- Include no additional text besides the JSON.
- The JSON object must have the following format:
    {
        "ranking": [
            {"name": "feature_name_1", "value": "feature_1}", 
            {"name": "feature_name_2", "value": "feature_2}", 
            {"name": "feature_name_3", "value": "feature_3}",
            ...
        ]
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output


def get_prompt_ranking_movies(recommendation: str = "", explanation: str = "", positive: bool = True, liked_movies: List[str] = [], disliked_movies: List[str] = []):

    instructions = f"""The movie {recommendation} was recommended to {'not ' if not positive else ''}be watched by a certain user.

The recommended system provided the following explanation: {explanation}. 

Your task is to given the recommendation and its explanation, provide a ranking of the input features based on their importance to the recommendation.
"""
    
    input = "Input features:"
    input += "\n- Liked movies: "
    input += "; ".join(liked_movies)
    input += "\n- Disliked movies: "
    input += "; ".join(disliked_movies)
    
    output = """Output:
- The output must be a JSON object.
- The JSON must have one key, "ranking", which is a list of the input features in order of importance.
- Each movie is an input feature. All features must be included in the ranking.
- Consider the following feature names: ["liked_movie_1", "liked_movie_2", "liked_movie_3", "disliked_movie_1", "disliked_movie_2", "disliked_movie_3"]
- Include no additional text besides the JSON.
- The JSON object must have the following format:
    {
        "ranking": [
            {"name": "feature_name_1", "value": "feature_1}", 
            {"name": "feature_name_2", "value": "feature_2}", 
            {"name": "feature_name_3", "value": "feature_3}",
            ...
        ]
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output


def get_prompt_ranking_playlist(recommendation: str = "", explanation: str = "", positive: bool = True, playlist_name: str = "", *songs):

    instructions = f"""The song {recommendation} was recommended to {'not ' if not positive else ''}be added to a user playlist.

The recommended system provided the following explanation: {explanation}. 

Your task is to given the recommendation and its explanation, provide a ranking of the input features based on their importance to the recommendation.
"""
    
    input = "Input features:"
    input += f"\n- Playlist's title: {playlist_name}"
    input += "\n- Playlist's current songs:"
    for i, song in enumerate(songs):
        input += f"\n  {i+1}. {song}"
    
    output = """Output:
- The output must be a JSON object.
- The JSON must have one key, "ranking", which is a list of the input features in order of importance.
- The playlist's title and each song are input features. All features must be included in the ranking.
- Consider the following feature names: ["playlist_name", "song_1", "song_2", "song_3", "song_4", "song_5"]
- Include no additional text besides the JSON.
- The JSON object must have the following format:
    {
        "ranking": [
            {"name": "feature_name_1", "value": "feature_1}", 
            {"name": "feature_name_2", "value": "feature_2}", 
            {"name": "feature_name_3", "value": "feature_3}",
            ...
        ]
    }
"""

    return instructions + "\n----------\n" + input + "\n----------\n" + output
