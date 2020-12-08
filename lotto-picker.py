import requests
from bs4 import BeautifulSoup

import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler

print(pd.__version__)
URL = "https://www.e-lotto.be/FR/drawGames/lotto/results/statistics/palmares"
# URL = "https://www.skysports.com/premier-league-table"
# headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# page = requests.get(URL, headers=headers)

# soup = BeautifulSoup(page.text, 'html.parser')

# df = soup.find('table', class_ ='draw-games-statistics-table Lotto6')
# df = soup.find('table', class_ ='draw-games-statistics-table Lotto6')
df = pd.read_html(URL)

print(df)

df.Pourcentage = df.Pourcentage.apply(lambda x: x.replace('%', ''))
df.Pourcentage = df.Pourcentage.apply(lambda x: x.replace(',', '.'))
df.Pourcentage = df.Pourcentage.astype('float')

# Prendre les plus haut pourcentages sortis il y a le plus longtemps
def normalize_df(df):
    scaler = MinMaxScaler() 
    scaled_values = scaler.fit_transform(df)
    df_norm = df.copy()
    df_norm.loc[:,:] = scaled_values
    df_norm.columns = [x+'_norm' for x in df_norm.columns]
    return(df_norm)

df_scaled = pd.concat([df, normalize_df(df[['Pourcentage','Last']])], axis=1)
df_scaled['proba'] = df_scaled.Pourcentage_norm * df_scaled.Last_norm
df_scaled = df_scaled.sort_values('proba', ascending=False)
top10 = df_scaled.head(10)['Numéro'].values.tolist()
top6 = df_scaled.head(6)['Numéro'].values.tolist()
top6.sort()

print('Top Combinaison : ' + str(top6))

for i in range(2,7):
    comb = random.sample(top10, 6)
    comb.sort()
    print('Combinaison n° ' + str(i) + ' : ' + str(comb))

print('Top 10 : ' + str(top10))