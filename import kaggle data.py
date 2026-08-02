# ==============================================================================================
# The purpose of this .py file is to import the data from the ZIP file downloaded from Kaggle
# and to view info, heads, and lists to preview the structure of the data.
# ==============================================================================================

import zipfile, pandas as pd

with zipfile.ZipFile('steam-games-dataset-2025.zip', 'r') as z:
    print('\nSHOW FILES IN ZIP')
    print(z.namelist())  # shows all files in the zip
    z.extractall('.')

# open applications as df
df_applications = pd.read_csv('steam_dataset_2025_csv/applications.csv', low_memory=False)

print('\nPRINT APPLICATIONS INFO')
print(df_applications.info())

print('\nPRINT APPLICATIONS HEAD')
print(df_applications.head())

# open genres as df
df_genre = pd.read_csv('steam_dataset_2025_csv/genres.csv')

print('\nPRINT GENRE INFO')
print(df_genre.info())

print('\nPRINT GENRE HEAD')
print(df_genre.head())

print('\nLIST ALL GENRES')
print(sorted(df_genre['name'].unique())) ## list each genre in the df
print(df_genre['name'].nunique())

# open reviews as df
df_reviews = pd.read_csv('steam_dataset_2025_csv/reviews.csv')

print('\nPRINT REVIEWS INFO')
print(df_reviews.info()) ## note: we will use "voted_up" as the basis for a positive review

print('\nPRINT REVIEWS HEAD')
print(df_reviews.head())

