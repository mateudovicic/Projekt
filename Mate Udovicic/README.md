# A. Izvršni sažetak (Executive Summary)

Ovaj projekt, nazvan "Nexus", ima za cilj automatizaciju prikupljanja i prijenosa znanstvenih podataka s površine Marsa, konkretno iz područja kratera Jezero, poznatog po potencijalnim tragovima drevnog života. Ulazni podaci obuhvaćaju GPS koordinate lokacija uzorkovanja te senzorske mjerne vrijednosti poput dubine bušenja, temperature tla, pH vrijednosti, postotka vlage, prisutnosti metana i organskih molekula — sve pohranjeno u CSV datotekama (mars_sample_locations.csv i mars_kandidati.csv). Konačni cilj je izgradnja automatiziranog sustava koji, na temelju skeniranog barkoda palete i izmjerene težine senzora, pakira sve relevantne podatke u strukturirani JSON nalog (tovarni list), lokalno ga arhivira te ga šalje na centralni server putem HTTP POST zahtjeva, s mogućnošću označavanja prioritetnih (hitnih) uzoraka — čime se omogućuje brza, pouzdana i automatizirana navigacija i logistika misije.Sonnet 4.6

# B. Metodologija obrade podataka (Data Wrangling)


U ovom projektu, obrada podataka temelji se na preciznom filtriranju DataFrame objekata kako bi se za svaki skenirani uzorak dohvatili isključivo relevantni redovi iz dviju CSV datoteka. Logički uvjet df_lokacije[df_lokacije['ID_Uzorka'] == id_palete] primijenjen je kako bi se izbjeglo miješanje podataka različitih uzoraka — svaki uzorak ima jedinstveni ID, pa je uvjetno filtriranje jedina pouzdana metoda za točno mapiranje GPS koordinata i senzorskih vrijednosti. Vrijednosti su potom eksplicitno konvertirane u odgovarajuće tipove (float, int, str) kako bi se spriječile greške pri serijalizaciji u JSON format, budući da pandas po defaultu vraća numpy tipove koji nisu uvijek kompatibilni. Što se tiče senzorskog šuma, sustav se oslanja na pretpostavku da su ulazni CSV podaci već prošli primarnu validaciju — međutim, ekstremne temperature ili anomalne pH vrijednosti mogle bi biti detektirane naknadnom provjerom raspona (npr. temperatura izvan očekivanog marsovskog raspona ili pH izvan ljestvice 0–14 signalizira grešku senzora). Takav pristup filtriranja po ID-u, uz strogu tipizaciju podataka i prepoznavanje potencijalnih anomalija, osigurava integritet analitičkog modela i pouzdanost generiranih tovarnih naloga.



# C. Geoprostorna analiza i vizualizacija


## Geoprostorna analiza i vizualizacija podataka iz kratera Jezero


[![H2O%,Temp.tla i metan](assets/graf1_temperatura_voda.png)]
Na ovom grafu vidimo postotak vode, temperaturu tla i prisutnost metana.
Najviše točkica to jest dobrih rezultata izažslo je iz točkica koje se nalaze na
H2O postotku između 0% i 6%, te temperaturi tla između -80C i -20C.
U tom području metan je ponajviše negativan. Pozitivni metan je najzastupljeniji na temperaturi
od -20C i 0C te H2O postotku od 4% do 10%

[![Dubina bušenja](assets/graf2_karta_dubine.png)]
Na ovom grafu vidimo odakle su zadovoljavajući uzorci došli.
Najviše ih je došlo sa koordinatama između 18.47 i 18.49 LON te
77.38 i 77.40 LAT i na dubini između 6 i 10 metara

[![Metan](assets/graf3_metan.png)]
Na ovom grafu vidimo prisutnost metana na određenim koordinatama, najveća prisutnost metana
je na koordinatama između 18.47 I 18.49 LON te 77.38 i 77.40 LAT. Koordinate bez prisutnosti
metana su najčešce na koordinatama 18.48 LON,77.39 LAT i 18.48 LON,77.397 LAT.

### Interpretacija raspodjele vode, temperature, dubine i metana kroz grafičke prikaze i prostorne uzorke**

[![Temp,vlaznost i metan](assets/graf_4_.png)]
Na ovom grafu vidimo na kojim je koordinatama metan najviše zastupljen u ppm.
Koordinate sa preko 50 ppm metana se sve vrte oko 226.0 LON i 18.7 LAT

[![Temp,vlaznost i metan](assets/graf_5_.png)]
Ovaj graf je skoro isti kao i prošli, samo u ovom su rubovi točkica podebljani i 
to nam omogućava da lakše očitamo koordinate i da vidimo i točkica sa manjom prisutnosti metana.

# D. Komunikacijski protokol (JSON Uplink)


## Komunikacijski protokol i struktura JSON paketa
Mrežni paket generiran funkcijom kreiraj_tovarni_list() šalje se na centralni server putem HTTP POST zahtjeva, a njegova precizna JSON struktura izgleda ovako:

{
  "projekt": "Nexus",
  "posiljatelj": "Mate Udovicic",
  "vrijeme": "2025-05-14 10:23:45.123456",
  "meta": {
    "uzorak_id": 900255,
    "lokacija": {
      "lat": 18.4446,
      "lon": 77.4508
    }
  },
  "senzori": {
    "dubina_busenja": 32.5,
    "temperatura": -63.2,
    "ph_vrijednost": 7.1,
    "vlaga": 0.04,
    "metan_senzor": "DETEKTIRAN",
    "organske_molekule": "POZITIVNO",
    "status": "PRIORITET"
  }
}

Ovakva ugniježđena struktura omogućuje vanjskim sustavima jednoznačno parsiranje podataka — meta blok identificira uzorak i njegovu lokaciju, dok senzori blok sadrži sve mjerne vrijednosti. Polje status automatski se postavlja na "PRIORITET" ili "NORMALNO" ovisno o zastavici hitno, čime se eliminira ručno kodiranje prioriteta. Za automatizirano generiranje naredbi za više uzoraka koristi se petlja koja iterira kroz listu ID-ova uzoraka:
id_lista = [900255, 900256, 900257]

for id_uzorka in id_lista:
    paket = kreiraj_tovarni_list(id_uzorka, tezina_senzora, je_hitno)
    spremi_lokalno(paket, f"paleta_{id_uzorka}.json")
    posalji_na_server(server_url, paket)
    time.sleep(1)  # pauza između slanja kako bi se izbjeglo preopterećenje servera

  Na ovaj način sustav automatski prolazi kroz sve uzorke, pakira podatke, arhivira ih lokalno i šalje na server — bez ikakvog ručnog unosa, što je ključno za autonomni rad terenskog robota u uvjetima ograničene komunikacije s Marsa.

# E. Inženjerski dnevnik (Troubleshooting Log)

Problem 1: Greška pri relacijskom spajanju tablica zbog pogrešnog separatora
Pri prvom pokretanju skripte, pd.read_csv() vraćao je DataFrame s jednim stupcem umjesto očekivanih višestrukih stupaca — što je uzrokovalo KeyError pri pokušaju pristupa stupcima poput 'ID_Uzorka' ili 'GPS_LAT'. Dijagnozom je utvrđeno da CSV datoteke koriste točku-zarez (;) kao separator, a ne zadani zarez (,). Skripta je pokušavala parsirati cijeli redak kao jednu vrijednost.
Rješenje: Dodan je eksplicitni parametar sep=';' u pozive pd.read_csv():
pythondf_lokacije = pd.read_csv('mars_sample_locations.csv', sep=';')
Nakon ispravka, DataFrame je ispravno razdvajao stupce i filtriranje po ID_Uzorka radilo je očekivano.

Problem 2: Odbijanje mrežnog zahtjeva od strane poslužitelja (timeout/connection error)
Pri pozivu funkcije posalji_na_server(), skripta je povremeno pucala s iznimkom requests.exceptions.ConnectionError ili je server vraćao status kod različit od 200. U jednom slučaju, server nije odgovarao unutar zadanog vremena, što je bez timeout parametra uzrokovalo beskonačno čekanje i zamrzavanje skripte.
Rješenje: Dodan je timeout=5 parametar u requests.post() poziv, čime se osigurava da skripta odustaje od čekanja nakon 5 sekundi i ispisuje jasnu poruku greške umjesto da se zamrzne:
pythonodgovor = requests.post(url, json=podaci_json, timeout=5)
Dodatno, cijeli blok slanja omotan je try/except strukturom koja hvata sve komunikacijske greške i ispisuje ih u konzolu, omogućujući nastavak rada skripte za preostale uzorke bez rušenja cijelog procesa.




