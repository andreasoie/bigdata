import time
import pandas as pd

from pytrends.request import TrendReq
from tqdm import tqdm

# Local imports
from utils import get_sampled_countries, is_leap_year
from testchecks import is_valid_country_query
from typerhints import CountryList, Countries, SearchTerm, HistoryFrame, HistoryFrameBlocks
from sklearn.preprocessing import MinMaxScaler

class SearchEngine:
    def __init__(self, pytrends: TrendReq, supported_countries: CountryList, fetch_interval: int = 1):
        self.pytrends = pytrends
        self.supported_countries = supported_countries
        self.fetch_interval = fetch_interval
        self.scaler = MinMaxScaler(feature_range=(0, 100))

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
        
        expected_days = 365
        if is_leap_year(year):
            expected_days = 366

        # Build timeline
        first_six_months = f"{year}-1-1 {year}-6-30"
        last_six_months = f"{year}-7-1 {year}-12-31"
        time_periods = [first_six_months, last_six_months]
        
        for time_period in time_periods:
            history_frame = self._get_interest_over_time(search_terms, time_period, geocode)
            tmp_history.append(history_frame)

        # with rescaling
        # combined_history = self._get_rescaled_history(search_terms, tmp_history, time_periods, geocode)

        # without
        combined_history= pd.concat(tmp_history)

        assert combined_history.shape[0] == expected_days, f"Expected {expected_days}, not {combined_history.shape[0]} days in a year!"
        return combined_history

    def _get_rescaled_history(self, search_terms, full_history, time_periods, geocode):
    
        first_six_months = time_periods[0]
        last_six_months = time_periods[1]
        first_last_day = first_six_months.split(" ")[1]
        last_first_day = last_six_months.split(" ")[0]

        merge_period = f"{first_last_day} {last_first_day}"

        time.sleep(0.25)
        # create the payload for related queries
        self.pytrends.build_payload(search_terms, timeframe=merge_period, geo=geocode)
        # request data from dataframe
        payload = self.pytrends.interest_over_time()
        if payload.empty:
            raise ValueError(f"Dropping request: {search_terms} for geocode ({geocode})")
        merge_history = payload.drop(columns=['isPartial'])

        # Implementation below accounts for multiple search terms,
        # we're only using one (!!!)
        merge_lists = []
        scale_factors = []

        # Gather the values for each search term
        for col_name in merge_history.columns:
            tmp_list = merge_history[col_name].values.tolist()
            merge_lists.append(tmp_list)

        # Processing and creating the scale factors
        for mlist, mhist in zip(merge_lists, full_history):
            BP0, BP1 = mlist
            P1, P2 = SearchEngine._get_head_and_tail_values(mhist)
            # Scaler algorithm
            s = (BP1 * P1[-1]) / (BP0 * P2[0])
            scale_factors.append(s)

        # Scale second half of the year
        first_half_of_year = full_history[0]
        second_half_of_year = full_history[1]
        second_half_of_year = second_half_of_year.mul(scale_factors[0], axis=0)

        # merge both halfs 
        full_year_history = pd.concat([first_half_of_year, second_half_of_year])

        # scale full_year_history
        m = 100/full_year_history[search_terms[0]].max()
        full_year_history = full_year_history.mul(m, axis=0)

        return full_year_history

    @staticmethod
    def _get_head_and_tail_values(hist):
        head_hist = hist.head(1)
        tail_hist = hist.tail(1)

        heads = []
        tails = []

        for name in hist.columns:
            hval = head_hist[name].values[0]
            tval = tail_hist[name].values[0]
            
            heads.append(hval)
            tails.append(tval)

        assert len(hist.columns) == len(heads), "length of heads doesnt match number of column names"
        assert len(hist.columns) == len(tails), "length of tails doesnt match number of column names"

        return heads, tails


if __name__ == "__main__":
    
    from utils import load_countries, plot_history, histories_to_pandas

    COUNTRY_DIR = "docs/countries.txt"
    COUNTRY_IGNORE_DIR = "docs/ignore.txt"
    LANGUAGE = 'en-US'
    TIME_ZONE = 360

    search_engine = SearchEngine(
        pytrends = TrendReq(hl=LANGUAGE, tz=TIME_ZONE),
        supported_countries = load_countries(filename=COUNTRY_DIR, ignore=COUNTRY_IGNORE_DIR),
        fetch_interval = 1
    )

    YEAR = 2018
    SEARCH_TERMS = ["Donald Trump"]
    SEARCH_COUNTRIES = ["United States"]

    history_trends = search_engine.get_daily_trends_by_year(
        search_terms=SEARCH_TERMS,
        year=YEAR,
        countries=SEARCH_COUNTRIES
    )