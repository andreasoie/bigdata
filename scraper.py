from pytrends.request import TrendReq
# from matplotlib import pyplot as plt
import pandas as pd

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Vizu settings
# %matplotlib inline
# plt.rcParams['font.size'] = 16
# plt.rcParams['figure.figsize'] = (10, 6)

# Local imports
from utils import load_countries, plot_history, histories_to_pandas
from search_engine import SearchEngine

# reproducibility
import random
random.seed(1337)

COUNTRY_DIR = "docs/countries.txt"
COUNTRY_IGNORE_DIR = "docs/ignore.txt"
LANGUAGE = 'en-US'
TIME_ZONE = 360

search_engine = SearchEngine(
    pytrends = TrendReq(hl=LANGUAGE, tz=TIME_ZONE),
    supported_countries = load_countries(filename=COUNTRY_DIR, ignore=COUNTRY_IGNORE_DIR),
    fetch_interval = 2
)

YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

SEARCH_TERMS = ["Donald Trump", "Putin", "MeToo", "Bitcoin", "ISIS"]

SEARCH_COUNTRIES = ["United States", "Norway", "United Kingdom", "Canada", "Germany"]

historic_trends = []

for year in YEARS:

    history_trends = search_engine.get_daily_trends_by_year(
        search_terms=SEARCH_TERMS,
        year=year,
        countries=SEARCH_COUNTRIES
    )

    trends_df = histories_to_pandas(history_trends)

    historic_trends.append(trends_df)

historic_trends = pd.concat(historic_trends)

print("Head:", historic_trends.head())

print("Info: ", historic_trends.info())

print("Tail: ", historic_trends.tail())


historic_trends.to_csv("historic_trends_2010_2020.csv")