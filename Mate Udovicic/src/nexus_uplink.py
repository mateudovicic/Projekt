import json      # Biblioteka za rad s JSON formatom (standard za podatke)
import requests  # Biblioteka za slanje HTTP zahtjeva (potrebno instalirati)
import datetime  # Za bilježenje točnog vremena
import pandas as pd
import time

# --- MODUL 1: PAKIRANJE PODATAKA ---
def kreiraj_tovarni_list(id_palete, tezina, hitno=False):
    """
    Funkcija prima sirove varijable i slaže ih u RJEČNIK (Dictionary).
    """

    df_lokacije = pd.read_csv('mars_sample_locations.csv', sep=';')
    df_kandidati = pd.read_csv('mars_kandidati.csv', sep=';')

    lok_row = df_lokacije[df_lokacije['ID_Uzorka'] == id_palete]
    sen_row = df_kandidati[df_kandidati['ID_Uzorka'] == id_palete]

    lat = float(lok_row['GPS_LAT'].values[0])
    lon = float(lok_row['GPS_LONG'].values[0])

    dubina = float(sen_row['Dubina_Busenja_cm'].values[0])
    temp = float(sen_row['Temp_Tla_C'].values[0])
    ph = float(sen_row['pH_Vrijednost'].values[0])
    vlaga = float(sen_row['H2O_Postotak'].values[0])
    metan = str(sen_row['Metan_Senzor'].values[0])
    organske = str(sen_row['Organske_Molekule'].values[0])

    paket = {
        "projekt": "Nexus",
        "posiljatelj": "Mate Udovicic",
        "vrijeme": str(datetime.datetime.now()),
        "meta": {
            "uzorak_id": int(id_palete),
            "lokacija": {
                "lat": lat,
                "lon": lon
            }
        }
        },
    senzori: {
            "dubina_busenja": dubina,
            "temperatura": temp,
            "ph_vrijednost": ph,
            "vlaga": vlaga,
            "metan_senzor": metan,
            "organske_molekule": organske,
            "status": "PRIORITET" if hitno else "NORMALNO"
    }

    return paket

def spremi_lokalno(podaci, zadnja_paleta):
    """
    Sprema rječnik u .json datoteku na disku.
    """
    print(f"--- Arhiviram paletu {podaci['id_artikla']} ---")

    try:
        # 'w' mode otvara datoteku za pisanje
        with open (zadnja_paleta, 'w') as f:
            # indent=4 čini da JSON izgleda lijepo i čitljivo
            json.dump(podaci, f, indent=4)
        print(f"Podaci uspješno zapisani u '{zadnja_paleta}'.")
    except Exception as e:
        print(f"Greška pri spremanju: {e}")

def posalji_na_server(url, podaci_json):
    """
    Šalje podatke na centralni server koristeći POST metodu.
    """
    print(f"--- Šaljem podatke na: {url} ---")

    try:
        # timeout=5 znači: ako server šuti 5 sekundi, odustani.
        odgovor = requests.post(url, json=podaci_json, timeout=5)

        if odgovor.status_code == 200:
            print("SERVER POTVRDIO: Paket primljen.")
        else:
            print(f"SERVER ODBIO: Greška kod {odgovor.status_code}")

    except Exception as greska:
        print(f"KOMUNIKACIJSKA GREŠKA: {greska}")

skenirani_barkod = 900255
tezina_senzora = 12.5
je_hitno = True

moj_paket = kreiraj_tovarni_list(skenirani_barkod, tezina_senzora, je_hitno)

print("Generirani paket u memoriji:")
print(moj_paket)

spremi_lokalno(moj_paket, "zadnja_paleta.json")

server_url = "https://webhook.site/f79bf0fc-e5b4-4f0e-a5d2-023d21e0403d"
posalji_na_server(server_url, moj_paket)