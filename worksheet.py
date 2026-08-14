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

    print(df_genre_english.head())
    print(df.head())
    print(df.info())
    print(df_application_genres.head())
    print(df_application_genres.info())
    print(df_english_genres.describe())
    print(df_english_genres.head())
    print(df_english_genres.info())