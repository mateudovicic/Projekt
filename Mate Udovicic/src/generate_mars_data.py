import pandas as pd
import numpy as np
import random

def generate_mars_data(num_samples=20000):
    """
    Generira sintetičke podatke za misiju na Marsu (20k uzoraka).
    Uključuje 3 specifična klastera s visokom vjerojatnošću života.
    """
    print(f"Inicijalizacija generiranja {num_samples} podataka...")

    ids = np.arange(1, num_samples + 1)

    # Inicijalizacija polja s "background" podacima (nasumični šum, nepovoljni uvjeti)
    # Većina Marsa je hladna, suha i bez metana.
    depths = np.random.exponential(scale=5, size=num_samples) # Većinom plitko
    temps = np.random.normal(-60, 10, num_samples) # Hladno
    ph_values = np.random.normal(7.0, 2.0, num_samples) # Varijabilni pH
    h2o = np.random.exponential(scale=0.5, size=num_samples) # Jako suho

    # Koordinate (Centar Jezero kratera)
    jezero_center_lat = 18.4447
    jezero_center_lon = 77.4508

    # Generiramo nasumične lokacije oko kratera (široko područje)
    lats = np.random.normal(jezero_center_lat, 0.05, num_samples)
    longs = np.random.normal(jezero_center_lon, 0.05, num_samples)

    metan = ['Negativno'] * num_samples
    organske = ['Ne'] * num_samples

    # --- KREIRANJE 3 KLASTERA ŽIVOTA (GEOGRAFSKI SPECIFIČNI) ---
    # 1. Neretva Vallis Delta (Ušće rijeke): Bogato sedimentima. (NW od centra)
    # 2. Neretva Vallis (Kanal): Drevno riječno korito. (Zapadno, ulaz u krater)
    # 3. Rub Kratera (Rim): Stijene izbačene udarom, hidrotermalni izvori? (Jugoistok)

    clusters = [
        # Delta: Bliže centru, malo sjeverozapadno
        {'lat_offset': 0.04, 'lon_offset': -0.06, 'count': 250, 'desc': 'Delta'},

        # Vallis: Dalje na zapad, ulazni kanal
        {'lat_offset': 0.05, 'lon_offset': -0.12, 'count': 200, 'desc': 'Vallis'},

        # Rub Kratera: Daleko na jugoistok
        {'lat_offset': -0.12, 'lon_offset': 0.12, 'count': 300, 'desc': 'Crater Rim'}
    ]

    # Indeksi koje ćemo prepisati klasterima
    current_idx = 0

    for cluster in clusters:
        count = cluster['count']
        indices = range(current_idx, current_idx + count)
        current_idx += count

        # 1. Lokacija klastera (malo šire raspršenje za prirodniji izgled)
        lats[indices] = np.random.normal(jezero_center_lat + cluster['lat_offset'], 0.005, count)
        longs[indices] = np.random.normal(jezero_center_lon + cluster['lon_offset'], 0.005, count)

        # 2. Povoljni uvjeti (malo variraju po klasterima)
        if cluster['desc'] == 'Delta':
            depths[indices] = np.random.normal(10, 2, count) # Sediment, mekše
            h2o[indices] = np.random.normal(5.0, 0.5, count) # Jako vlažno
        elif cluster['desc'] == 'Vallis':
            depths[indices] = np.random.normal(12, 3, count)
            h2o[indices] = np.random.normal(4.0, 0.5, count)
        else: # Rim
            depths[indices] = np.random.normal(20, 5, count) # Duboko u stijeni
            h2o[indices] = np.random.normal(3.5, 0.5, count) # Manje vlage, ali stabilno

        temps[indices] = np.random.normal(-20, 5, count)
        ph_values[indices] = np.random.normal(7.0, 0.2, count)

        # 3. Metan i Organske tvari
        for i in indices:
            metan[i] = 'Pozitivno' if random.random() < 0.9 else 'Negativno'
            organske[i] = 'Da' if random.random() < 0.8 else 'Ne'

    # Malo "šuma" metana i u ostatku podataka (lažni pozitivi)
    for i in range(current_idx, num_samples):
        if random.random() < 0.01: # 1% šanse random metan
            metan[i] = 'Pozitivno'

    # Zaokruživanje
    depths = np.round(depths, 1)
    temps = np.round(temps, 1)
    ph_values = np.clip(np.round(ph_values, 2), 0, 14)
    h2o = np.round(h2o, 2)
    lats = np.round(lats, 6)
    longs = np.round(longs, 6)

    # Kreiranje DataFrame-ova
    df_samples = pd.DataFrame({
        'ID_Uzorka': ids,
        'Dubina_Busenja_cm': depths,
        'Temp_Tla_C': temps,
        'pH_Vrijednost': ph_values,
        'H2O_Postotak': h2o,
        'Metan_Senzor': metan,
        'Organske_Molekule': organske
    })

    df_locations = pd.DataFrame({
        'ID_Uzorka': ids,
        'GPS_LAT': lats,
        'GPS_LONG': longs
    })

    return df_samples, df_locations

if __name__ == "__main__":
    print("Generiram podatke...")
    samples, locations = generate_mars_data(20000) # 20000 uzoraka

    # Spremanje u CSV
    samples.to_csv('mars_soil_samples.csv', index=False, sep=';')
    locations.to_csv('mars_sample_locations.csv', index=False, sep=';')

    print(f"Generirano {len(samples)} uzoraka.")
    print("Datoteke kreirane: 'mars_soil_samples.csv', 'mars_sample_locations.csv'")

    # Brzi pregled "zanimljivih" uzoraka
    zanimljivi = samples[(samples['Metan_Senzor'] == 'Pozitivno') & (samples['H2O_Postotak'] > 3.0)]
    print(f"\nBroj potencijalno zanimljivih uzoraka (Metan+ i Voda>3%): {len(zanimljivi)}")
