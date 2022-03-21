from typerhints import Countries, CountryList, StringList
from utils import load_countries


def is_valid_country_query(countries: Countries, country_names: CountryList) -> bool:
    if isinstance(countries, int):
        if countries < 0:
            raise ValueError("Number of countries can't be negative")
        elif countries > 250:
            raise ValueError("Doesn't exist so many countries?")
        else:
            return True
    elif isinstance(countries, list):
        if countries == []:
            return False
        elif not len(countries) > 0:
            return False
        elif _is_countries_supported(countries, country_names):
            return True
        else:
            raise ValueError("No valid countries provided")


def _is_countries_supported(countries: StringList, country_names: CountryList) -> bool:
    available_countries = [country[1].lower() for country in country_names]
    for country in countries:
        if not country.lower() in available_countries:
            print(f"{country} is not a supported country!")
            return False
    return True


if __name__ == "__main__":
    # TESTING
    random_countries = [
        "Spain",
        "Bermuda",
        "France",
        "Germany",
        "Italy",
        "Japan",
        "Mexico",
        "United Kingdomly",
        "United States",
    ]
    true_countries = load_countries("countries.txt", "ignore.txt")
    print(_is_countries_supported(random_countries, true_countries))
