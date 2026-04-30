import pandas as pd
import numpy as np
import random
import time
import os

def generiraj_moje_podatke():
    """
    Kada se pokrene, ova funkcija stvara jedinstveni set od 2000 podataka
    za projekt Nexus. Anomalije i lokacije žarišta su nasumično raspoređene.
    """
    # Generiramo 'sjeme' na temelju trenutnog vremena kako bi svaki pokretaj bio jedinstven
    jedinstveno_sjeme = int(time.time() * 1000) % 100000
    np.random.seed(jedinstveno_sjeme)
    random.seed(jedinstveno_sjeme)

    n_rows = 2000

    # --- 1. TABLICA: GPS LOKACIJE ---
    # Osnovne koordinate oko kojih Rover istražuje (krater Jezero)
    lat_base, lon_base = 18.48, 77.39

    # Raspršivanje točaka oko baze
    lats = np.random.normal(lat_base, 0.01, n_rows)
    lons = np.random.normal(lon_base, 0.01, n_rows)

    df_gps = pd.DataFrame({
        'ID_Uzorka': range(1, n_rows + 1),
        'GPS_LAT': np.round(lats, 6),
        'GPS_LONG': np.round(lons, 6)
    })

    # --- 2. TABLICA: MJERENJA ---
    # Stvaramo osnovne 'normalne' uvjete
    df_mjerenja = pd.DataFrame({
        'ID_Uzorka': range(1, n_rows + 1),
        'Dubina_Busenja_cm': np.round(np.random.uniform(0.1, 15.0, n_rows), 1),
        'Temp_Tla_C': np.round(np.random.normal(-50, 15, n_rows), 1),
        'pH_Vrijednost': np.round(np.random.normal(7.0, 0.5, n_rows), 2),
        'H2O_Postotak': np.round(np.random.uniform(0.1, 6.0, n_rows), 2),
        # Metan i organika su rijetki u normalnim uvjetima
        'Metan_Senzor': np.random.choice(['Negativno', 'Pozitivno'], p=[0.92, 0.08], size=n_rows),
        'Organske_Molekule': np.random.choice(['Ne', 'Da'], p=[0.95, 0.05], size=n_rows)
    })

    # --- 3. DODAVANJE ANOMALIJA (KVAR SENZORA) ---
    # Ovi podaci služe kao "zamka" za inženjera. Treba ih filtrirati!
    for _ in range(8):
        idx = random.randint(0, n_rows - 1)
        df_mjerenja.at[idx, 'Temp_Tla_C'] = 150.0  # Fizički nemoguća temperatura na Marsu
        df_mjerenja.at[idx, 'pH_Vrijednost'] = -2.0 # Krivi pH
        df_mjerenja.at[idx, 'Metan_Senzor'] = 'Pozitivno'

    # --- 4. DODAVANJE ŽARIŠTA (POTENCIJALNI ŽIVOT) ---
    # Stvaramo grupirana područja (klastere) koja zaista obećavaju
    n_hotspots = random.randint(2, 4)

    for _ in range(n_hotspots):
        # Odabir nasumične točke koja postaje centar žarišta
        h_idx = random.randint(0, n_rows - 1)
        t_lat = df_gps.at[h_idx, 'GPS_LAT']
        t_lon = df_gps.at[h_idx, 'GPS_LONG']

        # Pronalazak svih uzoraka u vrlo malom radijusu od tog centra
        udaljenost = np.sqrt((df_gps['GPS_LAT'] - t_lat)**2 + (df_gps['GPS_LONG'] - t_lon)**2)
        mask = (udaljenost < 0.002)

        # Modifikacija vrijednosti na tim lokacijama (simulacija 'plodnog' tla)
        df_mjerenja.loc[mask, 'H2O_Postotak'] += np.random.uniform(3.0, 6.0)
        df_mjerenja.loc[mask, 'Metan_Senzor'] = 'Pozitivno'
        df_mjerenja.loc[mask, 'Organske_Molekule'] = 'Da'
        # Temperatura je malo viša, ali unutar granica normale
        df_mjerenja.loc[mask, 'Temp_Tla_C'] = np.round(np.random.uniform(-20, -5, size=mask.sum()), 1)

    # --- 5. SPREMANJE PODATAKA ---
    # Spremamo u istu mapu gdje se nalazi i ova skripta
    folder_name = "moji_mars_podaci"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    putanja_gps = os.path.join(folder_name, 'mars_lokacije.csv')
    putanja_mjerenja = os.path.join(folder_name, 'mars_uzorci.csv')

    df_gps.to_csv(putanja_gps, index=False, sep=';', decimal=',')
    df_mjerenja.to_csv(putanja_mjerenja, index=False, sep=';', decimal=',')

    print("\n" + "="*50)
    print("🚀 GENERIRANJE PODATAKA ZAVRŠENO 🚀")
    print("="*50)
    print(f"Uspješno su stvorene 2 datoteke u mapi: '{folder_name}'")
    print(f"1. {putanja_gps}")
    print(f"2. {putanja_mjerenja}")
    print("\nSada možeš započeti zadatak analize!")

if __name__ == "__main__":
    generiraj_moje_podatke()


df_lokacije = pd.read_csv('/home/mateudovicic/moji_mars_podaci/mars_lokacije.csv', sep=';')
df_uzorci = pd.read_csv('/home/mateudovicic/moji_mars_podaci/mars_uzorci.csv', sep=';')

merged = pd.merge(
    df_lokacije,
    df_uzorci,
    on="ID_Uzorka"
)

print(merged)

krivi_ID = df[(df['ID_Uzorka'] < 0) | (df['ID_Uzorka'] > 2000)]

