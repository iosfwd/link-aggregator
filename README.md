# 23.4

Haku-ominaisuus lisätty. Lähdekoodeja refaktoroitu. Ulkoasu kaipaisi
vielä työstöä.

# 2.4

Tällä hetkellä sovelluksen aiemmin mainitut ominaisuudet on toteutettu
pl. haku. Lisäksi sovelluksessa voi merkitä itseä kiinnostavia
linkkejä. Sovellus on tällä hetkellä käyttökokemukseltaan ja
visuaalisesti todella kämäinen, koska se puoli ei ole tuttua.

# Käynnistysohjeet

Pääkäyttäjälle pääsee kirjautumaan tunnuksin root:root.

Luo virtuaaliympäristö ja asenna riippuvuudet:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r ./requirements.txt

Luo kansioon src/ .env tiedosto ja täydennä siihen tietokannan
paikallinen osoite ja salainen avain:

    DATABASE_URL=<tietokannan_osoite>
    SECRET_KEY=<salainen_avain>

Alusta tietokanta:

    $ cd src/
    $ psql -d tietokannan_nimi < schema.sql

Vaihtoehtoisesti käynnistä Postgres-tulkki src/ kansiossa ja aja:

    $ cd src/
    $ psql -d tietokannan_nimi
    # \i schema.sql

Käynnistys:

    $ cd src/
    $ flask run

# Linkkiaggregaattori

Sovellus listaa linkkejä. Sovelluksessa voi jakaa linkkejä
mielenkiintoisiin uutisiin ja artikkeleihin ja keskustella niistä.
Jokainen käyttäjä on on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä voi jakaa linkkejä ja antaa niille otsikoita. Käyttäjä voi
* kommentoida linkkejä. Käyttäjä voi antaa linkeille ylä- ja alaääniä.
* Käyttäjä voi listata näytettäviä linkkejä eri perusteilla, kuten
  tuoreus, äänien lukumäärä, tai kommenttien lukumäärä.
* Käyttäjä voi hakea linkkejä hakusanan perusteella.
* Käyttäjä voi muokata ja poistaa omia linkkejänsä ja kommentteja.
* Ylläpitäjä voi muokata ja poistaa kaikkien linkkejä ja kommentteja.
