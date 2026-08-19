# ==============================================================================================
# The purpose of this .py file is to clean and wrangle the data imported from Kaggle
# ==============================================================================================

import pandas as pd
from import_data import load_steam_data

#### map non-English genre names to English genres; set up dictionary####

# --- Column names -----------------------------------
SOURCE_COL = "name"          # column in df_genre holding the raw genre text
TARGET_COL = "genre_english"  # new column that will be created

# --- Full genre -> English mapping --------------------------------------
GENRE_TO_ENGLISH = {
    "360 Video": "360 Video",
    "Accounting": "Accounting",

    # Action
    "Acción": "Action",
    "Actie": "Action",
    "Action": "Action",
    "Acțiune": "Action",
    "Akció": "Action",
    "Akcja": "Action",
    "Aksi": "Action",
    "Aksiyon": "Action",
    "Azione": "Action",
    "Ação": "Action",
    "Бойовики": "Action",
    "Экшены": "Action",
    "إثارة": "Action",  # note: literally "Thriller" in Arabic; generalized to Action
    "アクション": "Action",
    "动作": "Action",
    "動作": "Action",

    # Adventure
    "Abenteuer": "Adventure",
    "Adventure": "Adventure",
    "Aventura": "Adventure",
    "Aventure": "Adventure",
    "Aventură": "Adventure",
    "Avventura": "Adventure",
    "Dobrodružné": "Adventure",
    "Eventyr": "Adventure",
    "Macera": "Adventure",
    "Petualangan": "Adventure",
    "Przygodowe": "Adventure",
    "Äventyr": "Adventure",
    "Пригоди": "Adventure",
    "Приключенческие игры": "Adventure",
    "アドベンチャー": "Adventure",
    "冒险": "Adventure",
    "冒險": "Adventure",

    "Animation & Modeling": "Animation & Modeling",
    "Audio Production": "Audio Production",

    # Casual
    "Basit Eğlence": "Casual",
    "Casual": "Casual",
    "Gelegenheitsspiele": "Casual",
    "Kasual": "Casual",
    "Rekreacyjne": "Casual",
    "Неангажиращи": "Casual",
    "カジュアル": "Casual",
    "休閒": "Casual",

    "Design & Illustration": "Design & Illustration",
    "Documentary": "Documentary",

    # Early Access
    "Acesso Antecipado": "Early Access",
    "Early Access": "Early Access",

    # Education
    "Bildung": "Education",
    "Education": "Education",

    "Episodic": "Episodic",

    # Free to Play
    "Бесплатные": "Free to Play",
    "Free To Play": "Free to Play",
    "Free to Play": "Free to Play",
    "Gratis at spille": "Free to Play",
    "Gratis att spela": "Free to Play",
    "Gratuitos para Jogar": "Free to Play",
    "مجانية": "Free to Play",
    "免费开玩": "Free to Play",
    "Gratis te spelen": "Free to Play",

    # Game Development
    "Game Development": "Game Development",
    "Spieleentwicklung": "Game Development",

    "Gore": "Gore",

    # Indie
    "Nezávislé": "Indie",
    "Indie": "Indie",
    "Indépendant": "Indie",
    "Niezależne": "Indie",
    "Інді": "Indie",
    "Инди": "Indie",
    "Независими": "Indie",
    "インディー": "Indie",
    "独立": "Indie",
    "獨立製作": "Indie",
    "Bağımsız Yapımcı": "Indie",

    "Fritid": "Leisure",

    # Massively Multiplayer
    "Devasa Çok Oyunculu": "Massively Multiplayer",
    "Masivně multiplayerové": "Massively Multiplayer",
    "Massively Multiplayer": "Massively Multiplayer",
    "Multigiocatore di massa": "Massively Multiplayer",
    "Multijogador Massivo": "Massively Multiplayer",
    "Multijugador masivo": "Massively Multiplayer",
    "MMO": "Massively Multiplayer",
    "Многопользовательские игры": "Massively Multiplayer",

    "Movie": "Movie",
    "Nudity": "Nudity",
    "Passatempo": "Pastime",
    "Photo Editing": "Photo Editing",

    # Racing
    "Corrida": "Racing",
    "Corse": "Racing",
    "Racing": "Racing",
    "Rennspiele": "Racing",
    "Гонки": "Racing",
    "Перегони": "Racing",
    "竞速": "Racing",

    # RPG
    "Rol": "RPG",
    "RPG": "RPG",
    "RYO": "RPG",
    "Rollenspiel": "RPG",
    "Ролевые игры": "RPG",
    "Rollespill": "RPG",
    "Рольові ігри": "RPG",
    "角色扮演": "RPG",

    "Sexual Content": "Sexual Content",
    "Short": "Short",

    # Simulation
    "Simulaatio": "Simulation",
    "Simuladores": "Simulation",
    "Simulasi": "Simulation",
    "Simulatie": "Simulation",
    "Simulation": "Simulation",
    "Simulationen": "Simulation",
    "Simulatoare": "Simulation",
    "Simulazione": "Simulation",
    "Simulação": "Simulation",
    "Simulering": "Simulation",
    "Simuleringar": "Simulation",
    "Simülasyon": "Simulation",
    "Symulacje": "Simulation",
    "Szimuláció": "Simulation",
    "Симулатори": "Simulation",
    "Симулятори": "Simulation",
    "模拟": "Simulation",
    "Simulátory": "Simulation",
    "Симуляторы": "Simulation",

    "Software Training": "Software Training",

    # Sports
    "Sport": "Sports",
    "Deportes": "Sports",
    "Esportes": "Sports",
    "Spor": "Sports",
    "Sportovní": "Sports",
    "Sportowe": "Sports",
    "Sports": "Sports",
    "Спорт": "Sports",
    "体育": "Sports",

    # Strategy
    "Estrategia": "Strategy",
    "Estratégia": "Strategy",
    "Strategi": "Strategy",
    "Strategia": "Strategy",
    "Strategické": "Strategy",
    "Strategie": "Strategy",
    "Strategy": "Strategy",
    "Strateji": "Strategy",
    "Stratégia": "Strategy",
    "Stratégie": "Strategy",
    "Стратегии": "Strategy",
    "Стратегії": "Strategy",
    "ストラテジー": "Strategy",
    "策略": "Strategy",

    "Tutorial": "Tutorial",
    "Utilities": "Utilities",
    "Video Production": "Video Production",
    "Violent": "Violent",

    # Web Publishing
    "Web Publishing": "Web Publishing",
    "Web-Publishing": "Web Publishing",
}

def add_english_genre_column(df_genre: pd.DataFrame,
                              source_col: str = SOURCE_COL,
                              target_col: str = TARGET_COL) -> pd.DataFrame:
    """
    Adds an English-language genre column to df_genre based on GENRE_TO_ENGLISH.
    Unmapped values become NaN so they're easy to spot and investigate.
    """
    df_genre[target_col] = df_genre[source_col].map(GENRE_TO_ENGLISH)

    unmapped = df_genre.loc[df_genre[target_col].isna(), source_col].dropna().unique()
    if len(unmapped) > 0:
        print(f"Warning: {len(unmapped)} unmapped genre value(s) found:")
        for val in unmapped:
            print(f"  - {val!r}")

    return df_genre

## test add_english_genre_column() and print results
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_genre_english = add_english_genre_column(df_genre)

    print('\n###TEST FUNCTION ADD_ENGLISH_GENRE_COLUMN###')

    print('\nPRINT GENRE HEAD WITH ENGLISH COLUMN')
    print(df_genre_english.head())

    print('\nCHECK FOR UNMAPPED VALUES')
    print(df_genre_english['genre_english'].isna().sum(), "unmapped rows")

    print('\nLIST ALL ENGLISH GENRES')
    for genre in sorted(df_genre_english['genre_english'].unique()):
        print(genre)
    print(df_genre_english['genre_english'].nunique())

## build a new df to house the 35 unique English genres
def build_english_genre_lookup(df_genre_english):
    """
    Builds a lookup table of distinct English genre categories, each with its own id.
    Also returns df_genre_english with an english_genre_id column added,
    mapping each original genre id to its English category id.
    """
    distinct_english = sorted(df_genre_english['genre_english'].dropna().unique())
    df_english_genres = pd.DataFrame({
        'id': range(1, len(distinct_english) + 1),
        'name': distinct_english,
    })

    name_to_id = dict(zip(df_english_genres['name'], df_english_genres['id']))
    df_genre_english['english_genre_id'] = df_genre_english['genre_english'].map(name_to_id)

    return df_genre_english, df_english_genres

## update the df_application_genres CSV to include the English ID
def map_app_genres_to_english(df_application_genres, df_genre_english):
    """
    Adds an english_genre_id column to df_application_genres by joining on genre_id.
    """
    df_application_genres = df_application_genres.merge(
        df_genre_english[['id', 'english_genre_id']],
        left_on='genre_id',
        right_on='id',
        how='left'
    )
    df_application_genres = df_application_genres.drop(columns=['id'])

    unmapped = df_application_genres['english_genre_id'].isna().sum()
    if unmapped > 0:
        print(f"Warning: {unmapped} rows in application_genres had no matching genre_id")

    return df_application_genres

## test build_english_genre_lookup() and map_app_genres_to_english()
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()

    df_genre_english = add_english_genre_column(df_genre)
    df_genre_english, df_english_genres = build_english_genre_lookup(df_genre_english)
    df_application_genres = map_app_genres_to_english(df_application_genres, df_genre_english)

    print('\n###TEST FUNCTIONS BUILD_ENGLISH_GENRE_LOOKUP AND MAP_APP_GENRES_TO_ENGLISH###')

    print('\nPRINT ALL ENGLISH GENRES')
    print(df_english_genres.to_string())

    print('\nPRINT APPLICATION_GENRES HEAD')
    print(df_application_genres.head())

#### remove free-to-play games as well as demos and dlc ####

## check unique values before filtering out free-to-play games and DLC
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()

    print('\n###CHECK UNIQUE GAME TYPES BEFORE FILTERING###')

    print('\nUNIQUE VALUES IN "type"')
    print(df_applications['type'].unique())

    print('\nUNIQUE VALUES IN "is_free"')
    print(df_applications['is_free'].unique())

## define function filter_paid_games
def filter_paid_games(df_applications):
    """
    Keeps only rows in df_applications where type == 'game' and is_free == False.
    Removes free-to-play games and non-game entries (e.g. dlc, demo, video).
    """
    before_count = len(df_applications)

    df_applications = df_applications[
        (df_applications['type'] == 'game') & (df_applications['is_free'] == False)
    ]

    after_count = len(df_applications)
    print(f"Removed {before_count - after_count} rows ({before_count} -> {after_count}) with filter_paid_games")

    return df_applications

## test function filter_paid_games
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()

    print('\n###TEST FILTER_PAID_GAMES###')
    df_applications = filter_paid_games(df_applications)

    print('\nUNIQUE VALUES IN "type" AFTER FILTER')
    print(df_applications['type'].unique())

    print('\nUNIQUE VALUES IN "is_free" AFTER FILTER')
    print(df_applications['is_free'].unique())

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
    print(f"Removed {before_count - after_count} rows ({before_count} -> {after_count}) with filter_usd_currency")

    return df_applications

## test filter_usd_currency()
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)

    print('\n###TEST FILTER_USD_CURRENCY###')

    print('\nUNIQUE VALUES IN "mat_currency" AFTER FILTER')
    print(df_applications['mat_currency'].unique())

#### create new column in df_applications for release year ####

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

#### build final analysis-ready dataframe with only relevant columns ####

def build_analysis_df(df_applications):
    """
    Selects only the columns needed for analysis from df_applications.
    Genre is added separately via build_genre_multihot, since a game can
    belong to multiple genres.
    """
    relevant_cols = [
        'appid', 'name', 'release_date', 'release_year',
        'metacritic_score', 'recommendations_total',
        'mat_initial_price', 'mat_final_price', 'mat_discount_percent'
    ]
    df = df_applications[relevant_cols].copy()

    return df

def drop_null_key_columns(df):
    """
    Drops rows with null values in the most important columns
    (appid, name, mat_initial_price, mat_final_price, mat_discount_percent).
    Leaves metacritic_score and recommendations_total untouched, since a
    high proportion of rows are missing that data but the rest of the row
    still holds valuable information.
    """
    before_count = len(df)

    key_cols = ['appid', 'name', 'mat_initial_price', 'mat_final_price', 'mat_discount_percent']
    df = df.dropna(subset=key_cols).copy()

    after_count = len(df)
    print(f"Removed {before_count - after_count} rows ({before_count} -> {after_count}) with drop_null_key_columns")

    return df

## update price from cents to dollars
def convert_price_to_dollars(df):
    """
    Converts mat_initial_price and mat_final_price from cents to dollars.
    The raw values (e.g. 599, 999, 190000) match Steam's actual price points
    when divided by 100 (e.g. $5.99, $9.99, $1900.00), indicating the source
    data stores price in cents rather than dollars.
    """
    df = df.copy()
    df['mat_initial_price'] = df['mat_initial_price'] / 100
    df['mat_final_price'] = df['mat_final_price'] / 100
    return df

## test build_analysis_df() and drop_null_key_columns()
if __name__ == "__main__":
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()
    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)
    df_applications = add_release_year_column(df_applications)
    df_applications = filter_release_year(df_applications)

    df_genre_english = add_english_genre_column(df_genre)
    df_genre_english, df_english_genres = build_english_genre_lookup(df_genre_english)
    df_application_genres = map_app_genres_to_english(df_application_genres, df_genre_english)

    df = build_analysis_df(df_applications)

    print('\n###CHECK NULL COUNTS BEFORE DROPPING###')
    print(df.isna().sum())

    df = drop_null_key_columns(df)

    print('\n###TEST BUILD_ANALYSIS_DF AND DROP_NULL_KEY_COLUMNS###')
    print('\nHEAD OF df')
    print(df.head())

    print('\nSHAPE OF df')
    print(df.shape)

    print('\nNULL COUNTS REMAINING (metacritic_score, recommendations_total')
    print(df[['metacritic_score', 'recommendations_total']].isna().sum())

## define a cleaning pipeline to clean up the functions list
def run_cleaning_pipeline():
    """
    Runs the full import + cleaning pipeline end to end and returns the
    analysis-ready dataframe (one row per game), the application-genre
    junction table, and the English genre lookup table.
    """
    df_applications, df_genre, df_reviews, df_application_genres = load_steam_data()

    df_applications = filter_paid_games(df_applications)
    df_applications = filter_usd_currency(df_applications)
    df_applications = add_release_year_column(df_applications)
    df_applications = filter_release_year(df_applications)

    df_genre_english = add_english_genre_column(df_genre)
    df_genre_english, df_english_genres = build_english_genre_lookup(df_genre_english)
    df_application_genres = map_app_genres_to_english(df_application_genres, df_genre_english)

    df = build_analysis_df(df_applications)
    df = drop_null_key_columns(df)
    df = convert_price_to_dollars(df)

    return df, df_application_genres, df_english_genres

## check for price outliers
def investigate_price_outliers(df, price_col='mat_final_price'):
    """
    Prints summary statistics and the most extreme values for price,
    to check for outliers that could distort downstream analysis.
    """
    print(f'\nDESCRIBE {price_col}')
    print(df[price_col].describe())

    print(f'\nTOP 20 MOST EXPENSIVE GAMES')
    print(df.nlargest(20, price_col)[['appid', 'name', price_col]].to_string())

    print(f'\nPERCENTILES')
    for p in [0.90, 0.95, 0.99, 0.999]:
        print(f'{p * 100:.1f}th percentile: {df[price_col].quantile(p):.2f}')

## test run_cleaning_pipeline() (copy and run in a worksheet)
if __name__ == "__main__":
    df, df_application_genres, df_english_genres = run_cleaning_pipeline()

    print('\n###TEST RUN_CLEANING_PIPELINE###')

    print('\nHEAD OF df')
    print(df.head())

    print('\nSHAPE OF df')
    print(df.shape)

    print('\nHEAD OF df_english_genres')
    print(df_english_genres.head())

    print('\n###INVESTIGATE PRICE OUTLIERS###')
    investigate_price_outliers(df)