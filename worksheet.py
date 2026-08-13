import pandas as pd
from import_data import load_steam_data
from clean_data import (add_english_genre_column, build_english_genre_lookup, map_app_genres_to_english, filter_paid_games,
                        filter_usd_currency)

## check sample values and format of release_date before conversion
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)

    print('\n###CHECK RELEASE_DATE BEFORE CONVERSION###')

    print('\nSAMPLE VALUES IN "release_date"')
    print(df_applications['release_date'].head(10))

    print('\nCOUNT OF NULL/MISSING VALUES')
    print(df_applications['release_date'].isna().sum())

## update release_date dtype to datetime and add release_year column
def add_release_year_column(df_applications):
    """
    Converts release_date to datetime and adds a release_year column.
    Rows where release_date fails to parse become NaT/NaN in release_year.
    """
    df_applications['release_date'] = pd.to_datetime(
        df_applications['release_date'], format='%Y-%m-%d', errors='coerce'
    )
    df_applications['release_year'] = df_applications['release_date'].dt.year

    unparsed = df_applications['release_year'].isna().sum()
    if unparsed > 0:
        print(f"Warning: {unparsed} rows had a release_date that failed to parse")

    return df_applications

def filter_release_year(df_applications, min_year=2003, max_year=2026):
    """
    Keeps only rows in df_applications where release_year is between
    min_year and max_year, inclusive.
    """
    before_count = len(df_applications)

    df_applications = df_applications[
        (df_applications['release_year'] >= min_year) & (df_applications['release_year'] <= max_year)
    ].copy()

    df_applications['release_year'] = df_applications['release_year'].astype(int)

    after_count = len(df_applications)
    print(f"Removed {before_count - after_count} rows ({before_count} -> {after_count})")

    return df_applications

## test add_release_year_column() and filter_release_year()
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)
    df_applications = add_release_year_column(df_applications)
    df_applications = filter_release_year(df_applications)

    print('\n###TEST ADD_RELEASE_YEAR_COLUMN AND FILTER_RELEASE_YEAR###')

    print('\nSAMPLE OF release_date AND release_year')
    print(df_applications[['release_date', 'release_year']].head(10))

    print('\nMIN AND MAX release_year AFTER FILTER')
    print(df_applications['release_year'].min(), '-', df_applications['release_year'].max())