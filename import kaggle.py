import zipfile, pandas as pd

with zipfile.ZipFile('steam-games-dataset-2025.zip', 'r') as z:
    print('\nShow files in ZIP')
    print(z.namelist())  # shows all files in the zip
    z.extractall('.')

# open applications as df
df_applications = pd.read_csv('steam_dataset_2025_csv/applications.csv', low_memory=False)

print('\nprint applications head')
print(df_applications.head())

# open genres as df
df_genre = pd.read_csv('steam_dataset_2025_csv/genres.csv')

print('\nprint genre head')
print(df_genre.head())

# open reviews as df
df_reviews = pd.read_csv('steam_dataset_2025_csv/reviews.csv')

print('\nprint reviews head')
print(df_reviews.head())