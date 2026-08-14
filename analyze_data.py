# ==============================================================================================
# The purpose of this .py file is to analyze the cleaned Steam data using multiple regression
# ==============================================================================================

import pandas as pd
from clean_data import run_cleaning_pipeline

def build_genre_multihot(df_application_genres, df_english_genres):
    """
    Builds a one-row-per-appid table with one binary column per English genre,
    True if the app belongs to that genre. Allows a game to belong to
    multiple genres without duplicating rows.
    """
    merged = df_application_genres.merge(
        df_english_genres.rename(columns={'id': 'english_genre_id', 'name': 'genre_name'}),
        on='english_genre_id',
        how='left'
    )

    genre_multihot = pd.crosstab(merged['appid'], merged['genre_name']) > 0
    genre_multihot = genre_multihot.add_prefix('genre_').reset_index()

    return genre_multihot

def add_genre_dummies(df, df_application_genres, df_english_genres):
    """
    Merges the multi-hot genre table onto df, keeping one row per game.
    """
    genre_multihot = build_genre_multihot(df_application_genres, df_english_genres)

    df = df.merge(genre_multihot, on='appid', how='left')

    genre_cols = [c for c in df.columns if c.startswith('genre_')]
    df[genre_cols] = df[genre_cols].fillna(False)

    return df

## test build_genre_multihot() and add_genre_dummies()
if __name__ == "__main__":
    df, df_application_genres, df_english_genres = run_cleaning_pipeline()

    print('\n###TEST ADD_GENRE_DUMMIES###')
    before_rows = len(df)
    df = add_genre_dummies(df, df_application_genres, df_english_genres)
    after_rows = len(df)

    print(f'\nROW COUNT BEFORE: {before_rows}, AFTER: {after_rows} (should match — one row per game)')

    print('\nCOLUMNS AFTER ADDING DUMMIES')
    print(df.columns.tolist())

    print('\nHEAD OF df')
    print(df.head())

    print('\nSAMPLE ROW WHERE A GAME HAS MULTIPLE GENRES TRUE')
    genre_cols = [c for c in df.columns if c.startswith('genre_')]
    multi_genre_sample = df[df[genre_cols].sum(axis=1) > 1]
    print(multi_genre_sample[['appid', 'name'] + genre_cols].head())