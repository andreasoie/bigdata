import os
from re import S
import re
import warnings
import requests


warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
from search_countries import mylist as selected_countries
from pytrends.request import TrendReq

from search_engine import SearchEngine
from utils import (
    histories_to_pandas,
    load_countries,
    load_merge_save_csv,
    merge_dataframes,
)


def get_config_settings(base_dir: str, configs: list):
    # csv_filename = f"newtrends/db_{CONFIG_ID}.csv"
    FILE_PREFIX = "db_"
    FILE_SUFFIX = ".csv"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    final_serch_terms = None
    final_csv_filename = None

    for idx, search_term in enumerate(configs):
        file_name = FILE_PREFIX + str(idx) + FILE_SUFFIX
        csv_filename = os.path.join(base_dir, file_name)
        print(f"Checking filename: {csv_filename} ")
        if not os.path.exists(csv_filename):
            print(f"Creating {csv_filename}")
            initframe = pd.read_csv("initDB.csv")
            initframe["date"] = pd.to_datetime(initframe["date"])
            initframe.to_csv(csv_filename, index=False, date_format="%Y-%m-%d")

        saved_file = pd.read_csv(csv_filename)

        # Check if its just the init file.
        if len(saved_file) <= 1:
            # Allocate search terms, and exit
            final_serch_terms = search_term
            final_csv_filename = csv_filename
            break
        else:
            # Found existing file, keep searching for available search terms
            continue
    return final_serch_terms, final_csv_filename


def scraper_trends(
    selected_countries: list,
    years: list,
    search_terms: list,
    csv_filename: str,
    engine: SearchEngine,
):
    for year in years:
        yearly_trends = []
        for search_term in search_terms:
            search_config = [[search_term], year, selected_countries]
            yearly_trend = engine.get_daily_trends_by_year(*search_config)
            pdframe = histories_to_pandas(yearly_trend)
            yearly_trends.append(pdframe)
        load_merge_save_csv(filename=csv_filename, data=merge_dataframes(yearly_trends))


def init_engine():
    countries = "docs/countries.txt"
    ignores = "docs/ignore.txt"
    pytrends = TrendReq(hl="en-US", tz=360, timeout=60, retries=10, backoff_factor=0.1)
    supported_countries = load_countries(filename=countries, ignore=ignores)
    fetch_interval = 0
    search_engine = SearchEngine(pytrends, supported_countries, fetch_interval)
    return search_engine


if __name__ == "__main__":

    from expressvpn import random_connect
    from new_terms import CONFIGS

    while True:
        try:
            engine = init_engine()
            terms, fname = get_config_settings(base_dir="newtrends", configs=CONFIGS)
            if terms is None or fname is None:
                break
            scraper_trends(
                contries=selected_countries,
                years=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
                search_terms=terms,
                csv_filename=fname,
                engine=engine,
            )
        except requests.exceptions.RetryError:
            random_connect()
        except requests.exceptions.ConnectionError:
            random_connect()
