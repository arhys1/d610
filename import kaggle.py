import zipfile, pandas as pd

with zipfile.ZipFile('steam-games-dataset-2025.zip', 'r') as z:
    print('\nShow files in ZIP')
    print(z.namelist())  # shows all files in the zip
    z.extractall('.')

# open genres as df
df = pd.read_csv('steam_dataset_2025_csv/genres.csv')

print('\nprint genre head')
print(df.head())
