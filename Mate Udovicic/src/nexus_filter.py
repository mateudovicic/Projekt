import pandas as pd


df = pd.read_csv('mars_soil_samples.csv', sep=';')

print("Podaci učitani.")
print(f"Ukupan broj uzoraka: {df.shape[0]}")


df_topli = df[ df['Temp_Tla_C'] > -60 ]

print("\n--- TEMPERATURNI FILTER ---")
print(f"Broj uzoraka nakon filtriranja temperature: {df_topli.shape[0]}")



print(f"Nova minimalna temperatura: {df_topli['Temp_Tla_C'].min()}")


df_voda = df[ df['H2O_Postotak'] > 1.5 ]

print("\n--- FILTER VODE ---")
print(f"Broj vlažnih uzoraka: {df_voda.shape[0]}")


kandidati = df[ (df['Temp_Tla_C'] > -60) &
                (df['H2O_Postotak'] > 1.0) &
                (df['Metan_Senzor'] == 'Pozitivno') ]

print("\n--- KONAČNI KANDIDATI ---")
print(f"Pronađeno savršenih lokacija: {kandidati.shape[0]}")
print(kandidati.head())

kandidati.to_csv('mars_kandidati.csv', sep=';', index=False)
print("\nDatoteka 'mars_kandidati.csv' je uspješno kreirana.")


kandidati = df[ (df['Temp_Tla_C'] > 0) |
                (df['pH_Vrijednost'] < 3) ]

print(f"Pronađeno ekstremnih lokacija: {kandidati.shape[0]}")
print(kandidati.head())