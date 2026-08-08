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