import pandas as pd

def get_playlist_data(path = 'data/spotify_mpd/data.csv') -> pd.DataFrame:
    df = pd.read_csv(path)

    # Combine 'track_name' and 'artist_name' with ' - '
    df['track_artist'] = df['track_name'] + ' - by ' + df['artist_name']

    # Pivot wider
    df_pivot = df.pivot(index=['pid', 'playlist_name'], columns='tid', values='track_artist')

    # Rename the columns to track_1, track_2, etc.
    df_pivot.columns = [f'song_{col+1}' for col in df_pivot.columns]

    # Reset index to flatten the dataframe
    df = df_pivot.reset_index()

    return df

def get_book_data(path = "data/bookrec/data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df['book_author'] = df['book_title'] + ' - by ' + df['book_author']
    df = df[["user_id", "book_author", "liked"]]
    df['rank'] = df.groupby(['user_id', 'liked']).cumcount() + 1
    
    pivot_df = df.pivot(index='user_id', columns=['liked', 'rank'], values='book_author')
    pivot_df.columns = [f'{"liked_book" if liked else "disliked_book"}_{rank}' for liked, rank in pivot_df.columns]

    df = pivot_df.reset_index()
    return df

def get_movie_data(path = "data/movies/data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[["prolificPID", "movieTitle", "liked"]]
    df['rank'] = df.groupby(['prolificPID', 'liked']).cumcount() + 1
    
    pivot_df = df.pivot(index='prolificPID', columns=['liked', 'rank'], values='movieTitle')
    pivot_df.columns = [f'{"liked_movie" if liked else "disliked_movie"}_{rank}' for liked, rank in pivot_df.columns]

    df = pivot_df.reset_index()
    return df

def get_book_preferences(path = "data/bookrec/data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df['book_author'] = df['book_title'] + ' - by ' + df['book_author']
    df = df[["user_id", "book_author", "liked"]]
    df = df.groupby(by = ['user_id', 'liked'])['book_author'].apply(list).reset_index()
    df = df.pivot(index='user_id', columns=['liked'], values='book_author')
    df = df.to_dict(orient='index')
    return df

def get_movie_preferences(path = "data/movies/data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[["prolificPID", "movieTitle", "liked"]]
    df = df.groupby(by = ['prolificPID', 'liked'])['movieTitle'].apply(list).reset_index()
    df = df.pivot(index='prolificPID', columns=['liked'], values='movieTitle')
    df = df.to_dict(orient='index')
    return df

def get_playlists_content(path = 'data/spotify_mpd/data.csv') -> pd.DataFrame:
    df = pd.read_csv(path)
    df['track_artist'] = df['track_name'] + ' - by ' + df['artist_name']
    df = df[['pid', 'playlist_name', 'track_artist']]
    df = df.groupby(by = ['pid', 'playlist_name'])['track_artist'].apply(list).reset_index()
    df = df.set_index(['pid'])
    df = df.to_dict(orient='index')
    return df