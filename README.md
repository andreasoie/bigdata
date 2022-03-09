# BigData - TMA4851

## Ideas for End-to-End pipline
- [ ] create suggestion to mini-thesis 
- [ ] setup query parameters and how to store data (sqlite? csv? json?)
- [ ] gather, process, and save relevant data
- [ ] vizualize and preprocess data (pandas)
- [ ] create cluster classifier (knn .. etc)
- [ ] setup final vizualization (plotly, geopandas .. etc)

### Installation

#### Prerequisite
Make sure you have support for python, pip and and your favorite virtual environment (see [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for more details)   


#### Changes
- Moving from pip to conda, as most mapping vizualization libraries are badly supported with windows / pip-
- BaseMap: https://rabernat.github.io/research_computing/intro-to-basemap.html
- Conda: ....

```bash
# Create and activate your environment
virtualenv venv
.\venv\Scripts\activate
```

```bash
# Install modules from the req file
pip install -r requirements.txt
```

### Demonstration
Please checkout *development.ipynb* for more information.

### Data Logic

1. Opprett keyword(s?), timeframe, threshold
2. Send til trending_all_countries => liste med aktuelle land (per keyword?)
3. Bruk landnavn med countries.txt for å få landkoder
5. Opprett aktuelle timeframes (på 6 måneder)
4. Send timeframe, landkoder og keyword(s?) til get_trending_data => få ut en liste med data som representerer hvor populært keywordet har vært for de ulike landene over perioden.
5. Legg dataen inn i en database

Ting å tenke over:
1. Trender fra to perioder har ikke nødvendigvis samme populæritet.
Altså: Periode 1 kan ha 100x mer søk enn periode 2, men siden dataen kun viser 
populæritetsgrad i forhold til perioden så vil ikke det nødvendigvis bety at grafen 
ser mye annerledes ut enn periode 2.
Mulig fix? Må tenke over, holde styr på perioder. I førsteomgang kan vi bare være
obs på at der periodene går over i hverandre kan det finnes "skaleringsfeil".
Dette kan være en grei måte fordi vi likevel sammenligner med andre land, og siden
de har feil på ca. samme sted så vil ikke det påvirke sammenligningen.
For å faktisk fikse det kan vi hente ut perioden fra siste dag av periode 1 til
første dag av periode 2, og dermed få en skalering fra periode 2 til 1.
Deretter kan vi gange periode 2 med denne skaleringen for å få kontinuitet.
Til slutt vil vi da eventuelt dele totale perioden på max(total periode)/100 for
å skalere slik at 100 er maks.
