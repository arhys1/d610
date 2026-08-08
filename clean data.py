# ==============================================================================================
# The purpose of this .py file is to clean and wrangle the data imported from Kaggle
# ==============================================================================================

import pandas as pd

#### map non-English genre names to English genres ####

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


def add_english_genre_column(df: pd.DataFrame,
                              source_col: str = SOURCE_COL,
                              target_col: str = TARGET_COL) -> pd.DataFrame:
    """
    Adds an English-language genre column to df based on GENRE_TO_ENGLISH.
    Unmapped values become NaN so they're easy to spot and investigate.
    """
    df[target_col] = df[source_col].map(GENRE_TO_ENGLISH)

    unmapped = df.loc[df[target_col].isna(), source_col].dropna().unique()
    if len(unmapped) > 0:
        print(f"Warning: {len(unmapped)} unmapped genre value(s) found:")
        for val in unmapped:
            print(f"  - {val!r}")

    return df
