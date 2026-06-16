import zipfile, pandas as pd

   with zipfile.ZipFile('steam-games-dataset-2025.zip', 'r') as z:
       z.extractall('data/')

