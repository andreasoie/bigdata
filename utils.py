import random
from typerhints import CountryList, StringList, Countries

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

def get_sampled_countries(countries: Countries, country_names: CountryList) -> CountryList:
    if isinstance(countries, int):
        if countries == 0:
            # return all available countries
            return country_names
        else:
            # return random sample of countries
            return random.sample(country_names, countries)
    elif isinstance(countries, list):
        return _selected_countries(countries, country_names)

def _selected_countries(selected_countries: StringList, country_options: CountryList) -> CountryList:
    # @TODO: refactor
    
    # just lower all characters to simplicity
    selected_countries = [search_country.lower() for search_country in selected_countries]
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


