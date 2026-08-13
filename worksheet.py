import pandas as pd
from import_data import load_steam_data
from clean_data import (add_english_genre_column, build_english_genre_lookup, map_app_genres_to_english, filter_paid_games,
                        filter_usd_currency, add_release_year_column, filter_release_year,
                        build_analysis_df, drop_null_key_columns)

if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)
    df_applications = add_release_year_column(df_applications)
    df_applications = filter_release_year(df_applications)

    df_genre_english = add_english_genre_column(df_genre)
    df_genre_english, df_english_genres = build_english_genre_lookup(df_genre_english)
    df_application_genres = map_app_genres_to_english(df_application_genres, df_genre_english)

    df = build_analysis_df(df_applications, df_application_genres)

    print('\n###CHECK NULL COUNTS BEFORE DROPPING###')
    print(df.isna().sum())

    df = drop_null_key_columns(df)

    print('\n###TEST BUILD_ANALYSIS_DF AND DROP_NULL_KEY_COLUMNS###')
    print('\nHEAD OF df')
    print(df.head())

    print('\nSHAPE OF df')
    print(df.shape)

    print('\nNULL COUNTS REMAINING (metacritic_score, recommendations_total, genre expected to have some)')
    print(df[['metacritic_score', 'recommendations_total', 'english_genre_id']].isna().sum())