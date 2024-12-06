import json
import pandas as pd


def load_tmbd_movies(path):
    df = pd.read_csv(path)
    df['release_date'] = pd.to_datetime(df['release_date']).apply(lambda x: x.date())
    json_columns = ['genres', 'keywords', 'production_countries', 'production_companies', 'spoken_languages']
    for column in json_columns:
        df[column] = df[column].apply(json.loads)
    return df


def load_tmdb_credits(path):
    df = pd.read_csv(path)
    json_columns = ['cast', 'crew']
    for column in json_columns:
        df[column] = df[column].apply(json.loads)
    return df


movies_df = load_tmbd_movies("../data/raw/tmdb_5000_movies.csv")
credits_df = load_tmdb_credits("../data/raw/tmdb_5000_credits.csv")

credits_df = credits_df.drop(columns=['title'])

movies_credits_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='left')

columns_to_drop = ['homepage', 'id', 'tagline', 'status', 'movie_id', 'original_language', 'original_title', 'spoken_languages']
movies_credits_df = movies_credits_df.drop(columns=columns_to_drop)

# drop all movies where budget information is not available
movies_credits_df.drop(movies_credits_df[movies_credits_df['budget'] == 0].index, inplace=True)

movies_credits_df.to_csv("../data/cleaned/cleaned_movies_credits.csv", index=False)
