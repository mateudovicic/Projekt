import pandas as pd

df = pd.read_csv('mars_sample_locations.csv', sep=';')
print(df.head())

df_kemija = pd.read_csv('mars_soil_samples.csv')

df_gps = pd.read_csv('mars_sample_locations.csv')

print(f"Broj kemijskih uzoraka: {df_kemija.shape[0]}")
print(f"Broj GPS zapisa: {df_gps.shape[0]}")

print(f"Najsjevernija tocka: {df['GPS_LAT'].max()}")
print(f"Najjužniju točku: {df['GPS_LAT'].min()}")
print(f"Najistočniju točku: {df['GPS_LONG'].max()}")
print(f"Najzapadniju točku: {df['GPS_LONG'].min()}")

Površina = (df['GPS_LAT'].max() - df['GPS_LAT'].min()) * (df['GPS_LONG'].max() - df['GPS_LONG'].min())
print("povrsina je", Površina)