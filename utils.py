import random

import pandas as pd
from matplotlib import pyplot as plt

from typerhints import (
    Countries,
    CountryList,
    HistoryFrame,
    HistoryFrameBlocks,
    SearchTerm,
    StringList,
)


def load_merge_save_csv(filename: str, data: pd.DataFrame) -> None:
    # loaded_data = pd.read_csv(filename)
    # loaded_data
    # loaded_data["date"] = pd.to_datetime(loaded_data["date"])
    # loaded_data.sort_values(by="date", inplace=True)
    # loaded_data.to_csv(filename, index=False, date_format="%Y-%m-%d")
    loaded_data = pd.read_csv(filename)
    filedata = pd.concat([loaded_data, data])
    filedata["date"] = pd.to_datetime(filedata["date"])
    filedata.sort_values(by="date", inplace=True)
    filedata.to_csv(filename, index=False, date_format="%Y-%m-%d")


def load_countries(filename: str, ignore: str) -> CountryList:
    unavailable_countries = _load_unavailable_countries(ignore)
    valid_countries = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line_list = line.split(",")
            code = line_list[0]
            country = line_list[1]
            if country not in unavailable_countries:
                valid_countries.append((code, country))
    return valid_countries


def _load_unavailable_countries(filename: str) -> StringList:
    unavailable_countries = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            unavailable_countries.append(line)
    return unavailable_countries


def plot_history(history: list, search_terms: SearchTerm) -> None:
    for search_term in search_terms:
        plt.figure()
        for hist in history:
            plt.plot(hist[1][search_term], label=hist[0])
        plt.legend(loc="upper right")
        plt.xlabel("Date")
        plt.ylabel("Interest")
        plt.title(f"{search_term.capitalize()}: Interest Over Time")
    plt.show()


def get_sampled_countries(
    countries: Countries, country_names: CountryList
) -> CountryList:
    if isinstance(countries, int):
        if countries == 0:
            # return all available countries
            return country_names
        else:
            # return random sample of countries
            return random.sample(country_names, countries)
    elif isinstance(countries, list):
        return _selected_countries(countries, country_names)


def _selected_countries(
    selected_countries: StringList, country_options: CountryList
) -> CountryList:

    # just lower all characters to simplicity
    selected_countries = [
        search_country.lower() for search_country in selected_countries
    ]
    optional_countries = [countryblock[1].lower() for countryblock in country_options]

    # find and save all countries that are in the selected countries
    my_selected_countries = []
    for selected_country in selected_countries:
        if selected_country in optional_countries:
            # Find the index of the country in the country_options list
            country_index = optional_countries.index(selected_country)
            # Extract the correspding country by index
            new_country = country_options[country_index]
            # Add the country to the list of selected countries
            my_selected_countries.append(new_country)
    return my_selected_countries


def histories_to_pandas(histories: HistoryFrameBlocks) -> pd.DataFrame:
    if isinstance(histories, pd.DataFrame):
        return histories
    blocks = []
    for country_name, country_data in histories:
        country_data["country"] = country_name
        country_data.reset_index(inplace=True)
        blocks.append(country_data)
    return pd.concat(blocks)


def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
