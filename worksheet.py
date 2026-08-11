import pandas as pd
from import_data import load_steam_data
from clean_data import (add_english_genre_column, build_english_genre_lookup, map_app_genres_to_english, filter_paid_games,
                        filter_usd_currency)

#### remove games where currency is not USD ####

## check unique values before filtering out non-USD currency
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)

    print('\n###CHECK UNIQUE CURRENCIES BEFORE FILTERING###')

    print('\nUNIQUE VALUES IN "mat_currency"')
    print(df_applications['mat_currency'].unique())

## define function filter_usd_currency
def filter_usd_currency(df_applications):
    """
    Keeps only rows in df_applications where mat_currency == 'USD'.
    Rows with a non-USD currency or a missing (NaN) currency are removed.
    """
    before_count = len(df_applications)

    df_applications = df_applications[df_applications['mat_currency'] == 'USD']

    after_count = len(df_applications)
    print(f"Removed {before_count - after_count} rows ({before_count} -> {after_count})")

    return df_applications

## test filter_usd_currency()
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)

    print('\n###TEST FILTER_USD_CURRENCY###')

    print('\nUNIQUE VALUES IN "mat_currency" AFTER FILTER')
    print(df_applications['mat_currency'].unique())