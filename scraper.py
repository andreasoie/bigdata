import os
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


import pandas as pd
from seach_countries import mylist as selected_countries
from pytrends.request import TrendReq

from search_engine import SearchEngine
from search_terms import CONFIGS
from utils import histories_to_pandas, load_countries, load_merge_save_csv

COUNTRY_DIR = "docs/countries.txt"
COUNTRY_IGNORE_DIR = "docs/ignore.txt"

search_engine = SearchEngine(
    pytrends=TrendReq(hl="en-US", tz=360, timeout=60, retries=10, backoff_factor=0.1),
    supported_countries=load_countries(filename=COUNTRY_DIR, ignore=COUNTRY_IGNORE_DIR),
    fetch_interval=0,
)

CONFIG_ID = None  # CHANGE
csv_filename = None  # CHANGE

SEARCH_TERMS = CONFIGS[CONFIG_ID]
SEARCH_COUNTRIES = selected_countries
YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

if not os.path.exists(csv_filename):
    print(f"Creating {csv_filename}")
    initframe = pd.read_csv("initDB.csv")
    initframe["date"] = pd.to_datetime(initframe["date"])
    initframe.to_csv(csv_filename, index=False, date_format="%Y-%m-%d")

for year in YEARS:
    search_config = [SEARCH_TERMS, year, SEARCH_COUNTRIES]
    yearly_trends = search_engine.get_daily_trends_by_year(*search_config)
    yearly_trends = histories_to_pandas(yearly_trends)
    load_merge_save_csv(filename=csv_filename, data=yearly_trends)
