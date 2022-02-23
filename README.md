# BigData - TMA4851


### Prerequisite
Make sure you have support for python, pip and and your favorite virtual environment (see [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for more details)   


### Installation
```bash
# Create and activate your environment
virtualenv venv
.\venv\Scripts\activate
```

```bash
# Install modules from the req file
pip install -r requirements.txt
```

### Data Logic

1. Opprett keyword(s?), timeframe, (threshold?)
2. Send til trending_all_countries => liste med aktuelle land (per keyword?)
3. Bruk landnavn med countries.txt for å få landkoder
5. Opprett aktuelle timeframes (på 6 måneder)
4. Send landkoder og keyword(s) til get_trending_data
