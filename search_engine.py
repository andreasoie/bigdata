import time

import pandas as pd
from pytrends.request import TrendReq
from tqdm import tqdm

from testchecks import is_valid_country_query
from typerhints import (
    Countries,
    CountryList,
    HistoryFrame,
    HistoryFrameBlocks,
    SearchTerm,
)

# Local imports
from utils import get_sampled_countries, is_leap_year


class SearchEngine:
    def __init__(
        self,
        pytrends: TrendReq,
        supported_countries: CountryList,
        fetch_interval: int = 1,
    ):
        self.pytrends = pytrends
        self.supported_countries = supported_countries
        self.fetch_interval = fetch_interval

    def get_daily_trends_by_year(
        self, search_terms: SearchTerm, year: int, countries: Countries
    ) -> HistoryFrameBlocks:
        # check if illegal query
        if not is_valid_country_query(
            countries=countries, country_names=self.supported_countries
        ):
            raise ValueError("Illegal query")
        if len(search_terms) > 5:
            raise ValueError("Too many search terms: MAX 5")

        # Find countries either by specific countries or random sampling by indicies
        search_countries = get_sampled_countries(
            countries=countries, country_names=self.supported_countries
        )

        trends = []
        for geocode, country in tqdm(
            search_countries, desc=f"Fetching trends for {year}", colour="green"
        ):
            try:
                history = self._get_yearly_interest_by_country(
                    search_terms=search_terms, year=year, geocode=geocode
                )
                trends.append((country, history))
            except ValueError as ve:
                print(ve)
        return trends

    def _get_interest_over_time(
        self, search_terms: SearchTerm, tf: str, geocode: str
    ) -> HistoryFrame:
        current_year = int(tf.split(" ")[0][:4])
        # don't fetch too often I guess?
        time.sleep(self.fetch_interval)
        # create the payload for related queries
        self.pytrends.build_payload(search_terms, timeframe=tf, geo=geocode)
        # request data from dataframe
        payload = self.pytrends.interest_over_time()
        if payload.empty:
            raise ValueError(
                f"[ERROR] Geocode: {geocode} Year {current_year}: \
                empty payload for terms {search_terms}"
            )
        return payload.drop(columns=["isPartial"])

    def _get_yearly_interest_by_country(
        self,
        search_terms: SearchTerm,
        year: int,
        geocode: str,
    ) -> HistoryFrame:
        tmp_history = []

        expected_days = 365
        if is_leap_year(year):
            expected_days = 366

        # Build timeline
        first_six_months = f"{year}-1-1 {year}-6-30"
        last_six_months = f"{year}-7-1 {year}-12-31"
        time_periods = [first_six_months, last_six_months]

        for i, time_period in enumerate(time_periods):
            history_frame = self._get_interest_over_time(
                search_terms, time_period, geocode
            )
            tmp_history.append(history_frame)

        # without rescaling
        combined_history = pd.concat(tmp_history)

        assert (
            combined_history.shape[0] == expected_days
        ), f"Expected {expected_days}, not {combined_history.shape[0]} days in a year!"
        return combined_history

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

        assert len(hist.columns) == len(
            heads
        ), "length of heads doesnt match number of column names"
        assert len(hist.columns) == len(
            tails
        ), "length of tails doesnt match number of column names"

        return heads, tails


if __name__ == "__main__":

    from utils import histories_to_pandas, load_countries, plot_history

    COUNTRY_DIR = "docs/countries.txt"
    COUNTRY_IGNORE_DIR = "docs/ignore.txt"
    LANGUAGE = "en-US"
    TIME_ZONE = 360

    search_engine = SearchEngine(
        pytrends=TrendReq(hl=LANGUAGE, tz=TIME_ZONE),
        supported_countries=load_countries(
            filename=COUNTRY_DIR, ignore=COUNTRY_IGNORE_DIR
        ),
        fetch_interval=1,
    )

    YEAR = 2010
    SEARCH_TERMS = ["MeToo", "ski"]
    SEARCH_COUNTRIES = ["Norway"]

    history_trends = search_engine.get_daily_trends_by_year(
        search_terms=SEARCH_TERMS, year=YEAR, countries=SEARCH_COUNTRIES
    )

    jj = histories_to_pandas(history_trends)
    jj.to_csv("baselayer.csv", index=False)
    print(jj)
    print(jj.info())
    print(jj["date"].dtype)
