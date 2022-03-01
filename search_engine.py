import time
import pandas as pd

from pytrends.request import TrendReq
from tqdm import tqdm

# Local imports
from utils import get_sampled_countries
from testchecks import is_valid_country_query
from typerhints import CountryList, Countries, SearchTerm, HistoryFrame, HistoryFrameBlocks


class SearchEngine:
    def __init__(self, pytrends: TrendReq, supported_countries: CountryList, fetch_interval: int = 1):
        self.pytrends = pytrends
        self.supported_countries = supported_countries
        self.fetch_interval = fetch_interval

    def get_daily_trends_by_year(self, search_terms: SearchTerm, year: int, countries: Countries) -> HistoryFrameBlocks:
        # check if illegal query
        if not is_valid_country_query(countries=countries, country_names=self.supported_countries):
            raise ValueError("Illegal query")

        # Find countries either by specific countries or random sampling by indicies
        search_countries = get_sampled_countries(countries=countries, country_names=self.supported_countries)

        trends = []
        for geocode, country in tqdm(search_countries, desc="Fetching trends", colour="green"):
            try:
                history = self._get_yearly_interest_by_country(search_terms, year, geocode)
                trends.append((country, history))
            except ValueError as ve:
                print(ve)
        return trends
    
    def _get_interest_over_time(self, search_terms: SearchTerm, tf: str, geocode: str) -> HistoryFrame:
        # don't fetch too often I guess?
        time.sleep(self.fetch_interval)
        # create the payload for related queries
        self.pytrends.build_payload(search_terms, timeframe=tf, geo=geocode)
        # request data from dataframe
        payload = self.pytrends.interest_over_time()
        if payload.empty:
            raise ValueError(f"Dropping request: {search_terms} for geocode ({geocode})")
        return payload.drop(columns=['isPartial'])

    def _get_yearly_interest_by_country(self, search_terms: SearchTerm, year: int, geocode: str, ) -> HistoryFrame:
        tmp_history = []
        
        # Build timeline
        first_six_months = f"{year}-1-1 {year}-6-30"
        last_six_months = f"{year}-7-1 {year}-12-31"
        time_periods = [first_six_months, last_six_months]
        
        for time_period in time_periods:
            history_frame = self._get_interest_over_time(search_terms, time_period, geocode)
            tmp_history.append(history_frame)
        
        # Combine the two time period from the timeline
        combined_history = pd.concat(tmp_history)
        assert combined_history.shape[0] == 365, "Expected 365 days in a year!"
        return combined_history

    